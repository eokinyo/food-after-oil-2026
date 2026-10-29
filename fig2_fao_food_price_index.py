"""Figure 2: FAO Food Price Index, September 2026 vs September 2025, % change."""
import pandas as pd
from common import FAO_FFPI_URL, OUTPUT, download, style

GROUPS = {"Food Price Index": "Overall", "Cereals": "Cereals", "Oils": "Vegetable oils",
          "Sugar": "Sugar", "Meat": "Meat", "Dairy": "Dairy"}


def load() -> pd.DataFrame:
    path = download(FAO_FFPI_URL, "ffpi-data-2026-10.xlsx")
    raw = pd.read_excel(path, sheet_name="Indices_Monthly", header=None)
    header = raw.iloc[2].astype(str).str.strip().tolist()
    body = raw.iloc[3:, : len(GROUPS) + 1]
    body.columns = header[: len(GROUPS) + 1]
    body = body.dropna(subset=["Date"])
    body.index = pd.to_datetime(body.pop("Date"))
    return body.apply(pd.to_numeric)


def changes() -> pd.Series:
    df = load()
    pct = (df.loc["2026-09-01"] / df.loc["2025-09-01"] - 1) * 100
    return pct.rename(index=GROUPS)[list(GROUPS.values())]


def main():
    pct = changes()
    plt = style()
    order = pct.iloc[::-1]
    fig, ax = plt.subplots(figsize=(16, 9), dpi=120)
    colors = ["#c0392b" if v > 0 else "#1f77b4" for v in order]
    ax.barh(order.index, order.values, color=colors, height=0.65)
    for y, v in enumerate(order.values):
        ax.text(v + (0.6 if v >= 0 else -0.6), y, (f"{v:+.1f}%" if round(v, 1) != 0 else "0.0%"), va="center",
                ha="left" if v >= 0 else "right", fontsize=24, fontweight="bold")
    ax.axvline(0, color="#333", lw=1.5)
    ax.set_xlim(min(order.min(), 0) - 7, max(order.max(), 0) + 7)
    ax.set_title("Food prices, September 2026 vs a year earlier (%)", loc="left", pad=20)
    ax.tick_params(axis="y", labelsize=24, length=0)
    ax.spines["left"].set_visible(False)
    ax.set_xticks([])
    ax.spines["bottom"].set_visible(False)
    fig.subplots_adjust(left=0.18)
    OUTPUT.mkdir(exist_ok=True)
    fig.savefig(OUTPUT / "fig2_fao_food_price_index.png")
    pct.round(2).to_csv(OUTPUT / "fig2_fao_food_price_index.csv", header=["pct_change"])
    print(pct.round(2).to_string())


if __name__ == "__main__":
    main()
