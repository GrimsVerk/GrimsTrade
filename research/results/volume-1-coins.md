# Volume 1, card 2: cross-sectional weekly IC of volume in the top-100 coin book

Script `lib/volume1_coins.py`, card 2 in `research/volume-1.md`. IC = mean over Fridays
(2019-04-05 to 2025-11-09) of the rank correlation across eligible coins between the
feature and the coming week's risk-adjusted return. Chance = 95th percentile of |IC|
with the feature panel circularly shifted in time (500 shifts of >= 52 weeks, the
same for all six). **Family chance level (maxT): 0.043.**

| Candidate | Weeks | Coins | IC | t | Weeks > 0 | 2019-21 | 2022-25 | Chance | Family | Verdict |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| `vol_chg4` | 344 | 89 | -0.020 | -2.3 | 44% | -0.011 | -0.027 | 0.017 | 0.043 | no |
| `vol_chg13` | 344 | 89 | +0.003 | +0.2 | 54% | -0.010 | +0.012 | 0.013 | 0.043 | no |
| `vol_z52` | 344 | 89 | -0.019 | -1.8 | 44% | -0.013 | -0.022 | 0.016 | 0.043 | no |
| `vw_trend13` | 344 | 89 | -0.010 | -0.9 | 49% | -0.022 | -0.002 | 0.034 | 0.043 | no |
| `updown13` | 344 | 89 | -0.019 | -1.7 | 45% | -0.031 | -0.011 | 0.043 | 0.043 | no |
| `pv_div13` | 344 | 89 | +0.007 | +0.7 | 52% | +0.002 | +0.010 | 0.024 | 0.043 | no |
