"""Shared helpers: download official files into data/ and chart styling."""
from pathlib import Path
import urllib.request

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
OUTPUT = ROOT / "output"

PINK_SHEET_URL = ("https://thedocs.worldbank.org/en/doc/74e8be41ceb20fa0da750cda2f6b9e4e-0050012026/"
                  "related/CMO-Historical-Data-Monthly.xlsx")
FAO_FFPI_URL = ("https://www.fao.org/media/docs/worldfoodsituationlibraries/wfs-library/"
                "ffpi-data-2026-10.xlsx?sfvrsn=63809b16_131")


def download(url: str, name: str) -> Path:
    """Download url to data/name unless it is already there."""
    DATA.mkdir(exist_ok=True)
    path = DATA / name
    if not path.exists():
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=120) as r, open(path, "wb") as f:
            f.write(r.read())
    return path


def style():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams.update({
        "figure.facecolor": "white", "axes.facecolor": "white", "savefig.facecolor": "white",
        "font.size": 22, "axes.titlesize": 32, "axes.labelsize": 22,
        "xtick.labelsize": 20, "ytick.labelsize": 20,
        "axes.spines.top": False, "axes.spines.right": False,
    })
    return plt
