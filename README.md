# After oil, the food bill: charts (2026)

Code for the charts in the article "After oil, the food bill". Each script downloads the official data file
into `data/` itself and writes a PNG (and the plotted values as CSV) to `output/`. No numbers are typed in by hand.

| Figure | Script | Output |
|---|---|---|
| 1. Energy, food and fertiliser price indices, Jan 2022 to Sep 2026, each rebased to its 2025 average = 100 | `fig1_world_bank_indices.py` | `output/fig1_energy_food_fertiliser.png` |
| 2. FAO Food Price Index, Sep 2026 vs Sep 2025, % change: overall, cereals, vegetable oils, sugar, meat, dairy | `fig2_fao_food_price_index.py` | `output/fig2_fao_food_price_index.png` |

Figure 3 (World Bank food price index, baseline vs adverse scenario) is not included: the October 2026 forecast
data file contains the baseline forecasts only, with no adverse-scenario series.

## Sources

| Source | File | Release date | Retrieved |
|---|---|---|---|
| World Bank, Commodity Price Data ("Pink Sheet"), monthly indices, nominal US dollars (sheet "Monthly Indices": Energy, Food, Fertilizers) | [CMO-Historical-Data-Monthly.xlsx](https://thedocs.worldbank.org/en/doc/74e8be41ceb20fa0da750cda2f6b9e4e-0050012026/related/CMO-Historical-Data-Monthly.xlsx), linked from https://www.worldbank.org/en/research/commodity-markets | 2 Oct 2026 ("Updated on October 02, 2026") | 29 Oct 2026 |
| FAO, Food Price Index, monthly nominal indices, 2014-2016 = 100 (sheet "Indices_Monthly") | [ffpi-data-2026-10.xlsx](https://www.fao.org/media/docs/worldfoodsituationlibraries/wfs-library/ffpi-data-2026-10.xlsx?sfvrsn=63809b16_131), linked from https://www.fao.org/worldfoodsituation/foodpricesindex/en/ | 2 Oct 2026 | 29 Oct 2026 |

Suggested caption: "Source: World Bank / FAO; author's calculations."

## How to run

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
python fig1_world_bank_indices.py
python fig2_fao_food_price_index.py
python -m pytest -q
```

The test checks that the FAO file reproduces the published changes (Sep 2026 vs Sep 2025, one decimal):
overall +5.8%, cereals +17.2%, vegetable oils +18.3%, sugar +14.7%, dairy -19.1%.

Downloaded files are cached in `data/` (not committed); delete them to download again.
If a publisher replaces a file at the same URL, results may change.

## Licence

Code: MIT (see `LICENSE`). Data remain under the publishers' terms (World Bank CC BY 4.0; FAO terms of use).
