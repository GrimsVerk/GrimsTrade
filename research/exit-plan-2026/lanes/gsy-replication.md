<!-- Copied 2026-11-18 by the night lead from branch gsy-1, commit 35d155f, research/results/gsy-1-replication.md (lane gsy-1, draft PR #55). Source of truth stays there. -->
# gsy-1: replication of GSY on French industries

Card: `cards/gsy-runup.md`, step 2. Written by `lib/gsy.py replicate`.

## Step 2. Replication of GSY's conditional crash probability (descriptive)

Monthly value-weighted French industries. Episode: the first month an industry's 24-month return is at least the threshold, raw and net of the market, with no run-up month in that industry in the 24 months before. `Crash`: a peak-to-trough fall of 40% or more within the next 24 months (peak counted from the signal month on). `Strict`: a month-end 40% or more below the signal month's level within 24 months. `Base`: the same two shares over every industry-month in the window (no condition). Only episodes whose 24 months after end by 2025-10 count.

| Industries | Window (signal months) | Threshold | Episodes | Crash | Strict | Median return next 6 m | Median return next 24 m | Base crash | Base strict |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 49 | 1928-07 to 2014-12 (GSY) | 100% | 104 | 38% | 22% | 3% | 9% | 15% | 10% |
| 49 | 1928-07 to 2014-12 (GSY) | 150% | 51 | 51% | 37% | -6% | -1% | 15% | 10% |
| 49 | 1928-07 to 2001-12 | 100% | 84 | 42% | 25% | 3% | 8% | 14% | 10% |
| 49 | 1928-07 to 2001-12 | 150% | 39 | 56% | 41% | -3% | -1% | 14% | 10% |
| 49 | 2002-01 to 2023-10 | 100% | 30 | 27% | 13% | 3% | 12% | 12% | 9% |
| 49 | 2002-01 to 2023-10 | 150% | 17 | 35% | 18% | -7% | 6% | 12% | 9% |
| 49 | 2015-01 to 2023-10 | 100% | 10 | 30% | 20% | 3% | 15% | 8% | 5% |
| 49 | 2015-01 to 2023-10 | 150% | 5 | 40% | 0% | 4% | 16% | 8% | 5% |
| 30 | 1928-07 to 2014-12 (GSY) | 100% | 50 | 34% | 22% | 2% | 10% | 12% | 9% |
| 30 | 1928-07 to 2014-12 (GSY) | 150% | 17 | 47% | 29% | -7% | 18% | 12% | 9% |
| 30 | 1928-07 to 2001-12 | 100% | 41 | 37% | 22% | 1% | 15% | 12% | 9% |
| 30 | 1928-07 to 2001-12 | 150% | 12 | 50% | 33% | -10% | 17% | 12% | 9% |
| 30 | 2002-01 to 2023-10 | 100% | 14 | 21% | 21% | 7% | 19% | 11% | 9% |
| 30 | 2002-01 to 2023-10 | 150% | 9 | 33% | 11% | 2% | 18% | 11% | 9% |
| 30 | 2015-01 to 2023-10 | 100% | 5 | 20% | 20% | 13% | 36% | 7% | 6% |
| 30 | 2015-01 to 2023-10 | 150% | 4 | 25% | 0% | 4% | 20% | 7% | 6% |
| 10 | 1928-07 to 2014-12 (GSY) | 100% | 7 | 57% | 43% | 4% | -25% | 9% | 7% |
| 10 | 1928-07 to 2014-12 (GSY) | 150% | 2 | 0% | 0% | -16% | 40% | 9% | 7% |
| 10 | 1928-07 to 2001-12 | 100% | 6 | 67% | 50% | -3% | -30% | 9% | 7% |
| 10 | 1928-07 to 2001-12 | 150% | 1 | 0% | 0% | -20% | 84% | 9% | 7% |
| 10 | 2002-01 to 2023-10 | 100% | 3 | 33% | 0% | 7% | 1% | 7% | 5% |
| 10 | 2002-01 to 2023-10 | 150% | 3 | 33% | 0% | 4% | -4% | 7% | 5% |
| 10 | 2015-01 to 2023-10 | 100% | 2 | 50% | 0% | 8% | 17% | 4% | 4% |
| 10 | 2015-01 to 2023-10 | 150% | 2 | 50% | 0% | 6% | -10% | 4% | 4% |

**Added after the table above was seen (a re-reading, not the card's definition):** the same episodes, keeping only those whose industry had at least 10 firms in the signal month (a small-industry filter GSY may have used; not checked in the paper).

| Industries | Window | Threshold | Episodes | Crash | Strict |
|---|---|---:|---:|---:|---:|
| 49 | 1928-07 to 2014-12 (GSY) | 100% | 53 | 40% | 25% |
| 49 | 1928-07 to 2014-12 (GSY) | 150% | 21 | 62% | 52% |
| 49 | 1928-07 to 2001-12 | 100% | 43 | 42% | 26% |
| 49 | 1928-07 to 2001-12 | 150% | 16 | 69% | 56% |
| 49 | 2002-01 to 2023-10 | 100% | 16 | 25% | 19% |
| 49 | 2002-01 to 2023-10 | 150% | 8 | 38% | 25% |
| 30 | 1928-07 to 2014-12 (GSY) | 100% | 33 | 36% | 30% |
| 30 | 1928-07 to 2014-12 (GSY) | 150% | 9 | 44% | 33% |
| 30 | 1928-07 to 2001-12 | 100% | 27 | 37% | 30% |
| 30 | 1928-07 to 2001-12 | 150% | 6 | 50% | 33% |
| 30 | 2002-01 to 2023-10 | 100% | 9 | 22% | 22% |
| 30 | 2002-01 to 2023-10 | 150% | 6 | 33% | 17% |

49 industries, 100%, 1928-2014: every episode.

| Signal month | Industry | Crash | Strict | Next 6 m | Next 24 m |
|---|---|---|---|---:|---:|
| 192807 | Aero | yes | yes | 67% | -30% |
| 192810 | Autos | yes | yes | 3% | -62% |
| 192812 | ElcEq | yes | no | 42% | -40% |
| 192812 | Hardw | yes | no | 36% | -33% |
| 192901 | Chems | yes | yes | 17% | -40% |
| 192904 | Banks | yes | yes | -34% | -62% |
| 192906 | Util | yes | yes | -23% | -35% |
| 193305 | Beer | yes | no | 29% | -2% |
| 193309 | Banks | no | no | 57% | 155% |
| 193310 | Agric | no | no | 30% | 31% |
| 193312 | Ships | no | no | -8% | 5% |
| 193403 | Autos | no | no | -24% | 88% |
| 193403 | Aero | no | no | -36% | 64% |
| 193403 | Chips | no | no | -5% | 200% |
| 193403 | Other | no | no | -2% | 43% |
| 193404 | Chems | no | no | -1% | 62% |
| 193404 | Rubbr | no | no | -7% | 71% |
| 193405 | Trans | no | no | -12% | 25% |
| 193405 | Whlsl | no | no | 8% | 27% |
| 193405 | Insur | no | no | 17% | 43% |
| 193406 | Mines | no | no | -10% | 26% |
| 193406 | Paper | yes | no | 77% | 145% |
| 193406 | Boxes | no | no | 18% | 49% |
| 193502 | Mach | no | no | 38% | 182% |
| 193503 | Fun | no | no | 77% | 256% |
| 193510 | LabEq | no | no | -4% | 10% |
| 193609 | PerSv | yes | yes | 44% | -38% |
| 193610 | Cnstr | yes | yes | 13% | 37% |
| 193612 | RlEst | yes | yes | -35% | -58% |
| 193702 | Toys | yes | yes | -23% | -38% |
| 193702 | Steel | yes | yes | -6% | -35% |
| 193910 | Toys | no | no | 26% | -3% |
| 193910 | Aero | no | no | 2% | -8% |
| 194205 | Fun | no | no | 23% | 124% |
| 194304 | Books | no | no | 24% | 146% |
| 194304 | MedEq | no | no | 6% | 56% |
| 194308 | PerSv | no | no | 24% | 72% |
| 194406 | Cnstr | no | no | 16% | 127% |
| 194410 | RlEst | yes | no | 34% | 88% |
| 194510 | Beer | yes | no | 28% | -18% |
| 194603 | Fun | yes | yes | -19% | -38% |
| 194604 | Meals | no | no | -25% | -34% |
| 195412 | Aero | no | no | -5% | 50% |
| 195603 | Coal | no | no | -6% | -26% |
| 195603 | Paper | yes | yes | -18% | -36% |
| 195811 | Drugs | no | no | 26% | 34% |
| 195904 | Toys | no | no | 15% | 188% |
| 196005 | LabEq | no | no | -7% | -22% |
| 196511 | Aero | no | no | 1% | 36% |
| 196601 | Mines | no | no | -5% | 33% |
| 196602 | Toys | yes | no | -14% | -24% |
| 196706 | Cnstr | no | no | 26% | 33% |
| 196706 | LabEq | no | no | 5% | 5% |
| 196708 | Fun | no | no | 3% | 26% |
| 196712 | Meals | no | no | 24% | 40% |
| 196805 | PerSv | yes | yes | 18% | -69% |
| 196806 | RlEst | yes | no | 47% | -24% |
| 196810 | Rubbr | yes | yes | -9% | -44% |
| 196810 | Whlsl | yes | yes | 1% | -47% |
| 196812 | Other | yes | yes | -21% | -72% |
| 197104 | Coal | yes | yes | -25% | -41% |
| 197205 | Fun | yes | yes | -2% | -54% |
| 197312 | Gold | no | no | -3% | -24% |
| 197504 | Coal | no | no | -5% | 43% |
| 197611 | Clths | no | no | -2% | 17% |
| 197612 | Aero | no | no | 11% | 63% |
| 197805 | Hlth | no | no | 9% | 129% |
| 197808 | Softw | no | no | -23% | 109% |
| 198001 | Gold | yes | no | 34% | -18% |
| 198002 | Mines | no | no | 4% | -8% |
| 198010 | Cnstr | yes | yes | -12% | -36% |
| 198010 | Oil | yes | no | -10% | -25% |
| 198708 | Smoke | no | no | -18% | 51% |
| 198806 | Gold | no | no | -13% | -2% |
| 199011 | Smoke | no | no | 19% | 21% |
| 199209 | Toys | no | no | 0% | 21% |
| 199707 | Soda | no | no | 3% | -0% |
| 199903 | Softw | yes | no | 2% | -38% |
| 199911 | Hardw | yes | yes | 20% | -51% |
| 199912 | Chips | yes | yes | 23% | -53% |
| 200001 | Coal | yes | no | -15% | 36% |
| 200107 | Hlth | yes | no | -6% | -25% |
| 200110 | Smoke | yes | no | 19% | 10% |
| 200110 | Guns | no | no | 29% | -3% |
| 200202 | Ships | yes | no | -12% | 9% |
| 200210 | Gold | no | no | 9% | 97% |
| 200407 | Coal | no | no | 32% | 133% |
| 200412 | Cnstr | no | no | 21% | 15% |
| 200604 | Mines | no | no | -2% | 96% |
| 200705 | Steel | yes | yes | -7% | -58% |
| 200712 | Agric | yes | no | 10% | -26% |
| 201010 | Gold | no | no | 7% | -3% |
| 201010 | Mines | yes | no | 11% | -10% |
| 201011 | Soda | no | no | 21% | 46% |
| 201011 | Fun | no | no | 9% | -0% |
| 201011 | Autos | no | no | 6% | -10% |
| 201012 | Coal | yes | yes | -4% | -59% |
| 201102 | Txtls | no | no | -8% | 55% |
| 201102 | FabPr | no | no | -3% | 21% |
| 201102 | Mach | no | no | -13% | 7% |
| 201102 | Ships | no | no | -6% | 50% |
| 201102 | RlEst | no | no | -17% | 29% |
| 201309 | Txtls | no | no | 11% | 51% |
| 201405 | Ships | no | no | -2% | -11% |
