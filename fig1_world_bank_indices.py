"""Figure 1: World Bank energy, food and fertiliser price indices, Jan 2022-Sep 2026, 2025 average = 100."""
import pandas as pd
from common import OUTPUT, PINK_SHEET_URL, download, style

SERIES = {"Energy": "Energy", "Food": "Food **", "Fertilisers": "Fertilizers **"}
COLORS = {"Energy": "#c0392b", "Food": "#1f77b4", "Fertilisers": "#2ca02c"}


def load() -> pd.DataFrame:
    path = download(PINK_SHEET_URL, "CMO-Historical-Data-Monthly.xlsx")
    raw = pd.read_excel(path, sheet_name="Monthly Indices", header=None)
    assert "Updated on October 02, 2026" in raw.iloc[:5, 0].astype(str).tolist(), "unexpected Pink Sheet edition"
    header = raw.iloc[5:9].astype(str).apply(lambda c: c.str.strip())
    cols = {}
    for name, label in SERIES.items():
        hits = [j for j in raw.columns if label in header[j].tolist()]
        assert len(hits) == 1, (name, hits)
        cols[name] = hits[0]
    body = raw.iloc[9:]
    body = body[body[0].astype(str).str.match(r"^\d{4}M\d{2}$")]
    df = pd.DataFrame({n: pd.to_numeric(body[c]) for n, c in cols.items()})
    df.index = pd.to_datetime(body[0].str.replace("M", "-") + "-01")
    return df


def rebased(df: pd.DataFrame) -> pd.DataFrame:
    base = df.loc["2025"].mean()
    return (df / base * 100).loc["2022-01":"2026-09"]


def main():
    df = rebased(load())
    plt = style()
    fig, ax = plt.subplots(figsize=(16, 9), dpi=120)
    for name in df.columns:
        ax.plot(df.index, df[name], lw=4, color=COLORS[name])
        ax.annotate(f"{name} {df[name].iloc[-1]:.0f}", (df.index[-1], df[name].iloc[-1]),
                    xytext=(12, 0), textcoords="offset points", va="center",
                    color=COLORS[name], fontsize=24, fontweight="bold")
    ax.axhline(100, color="#888", lw=1.5, ls="--")
    ax.set_title("Energy, food and fertiliser prices, 2025 average = 100", loc="left", pad=20)
    ax.set_ylabel("Index, 2025 average = 100")
    ax.grid(axis="y", color="#ddd")
    import matplotlib.dates as mdates
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    ax.margins(x=0.01)
    fig.subplots_adjust(right=0.80)
    OUTPUT.mkdir(exist_ok=True)
    fig.savefig(OUTPUT / "fig1_energy_food_fertiliser.png")
    df.rename_axis("month").round(2).to_csv(OUTPUT / "fig1_energy_food_fertiliser.csv")
    print(df.tail(1).round(1).to_string())


if __name__ == "__main__":
    main()
