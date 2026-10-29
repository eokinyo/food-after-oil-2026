import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from fig2_fao_food_price_index import changes  # noqa: E402

EXPECTED = {"Overall": 5.8, "Cereals": 17.2, "Vegetable oils": 18.3, "Sugar": 14.7, "Dairy": -19.1}


def test_fao_sep2026_vs_sep2025():
    pct = changes()
    for k, v in EXPECTED.items():
        assert round(pct[k], 1) == v, (k, pct[k])
