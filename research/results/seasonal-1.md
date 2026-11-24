# seasonal-1: `seasonal-20y` results

Card `cards/seasonal-20y.md`; script `lib/seasonal1.py` (one real run). Sharpe on weekly returns, annualised; difference = rule minus comparator on the same weeks; SE from 2000 paired stationary-bootstrap draws (mean block 8 weeks, seed 0).

## Readings (card labels)

| Test | Standalone vs hold | Overlay vs tsmom12 |
|---|---|---|
| US-ind10 | absent | absent |
| US-Mkt | absent | absent |
| US-NoDur | absent | absent |
| US-Durbl | absent | absent |
| US-Manuf | absent | absent |
| US-Enrgy | absent | absent |
| US-HiTec | absent | absent |
| US-Telcm | absent | absent |
| US-Shops | absent | absent |
| US-Hlth | absent | absent |
| US-Utils | absent | absent |
| US-Other | absent | absent |
| US-ind10-late | absent | absent |
| geo13 | absent | absent |
| geo-Japan | absent | absent |
| geo-Canada | absent | absent |
| geo-UK | absent | absent |
| geo-Australia | absent | absent |
| geo-HongKong | absent | absent |
| geo-Germany | absent | absent |
| geo-Singapore | absent | absent |
| geo-France | absent | absent |
| geo-Switzerland | absent | absent |
| geo-Belgium | absent | absent |
| geo-Netherlands | absent | absent |
| geo-Austria | absent | absent |
| geo-Spain | absent | absent |
| six | absent | absent |

Pick bar (primary `six`, overlay vs `tsmom12`): z >= 4.69 (BAR.md); 3.29 = the counting method decides.

## Overlay vs `tsmom12`

| Test | Window | Rule | Comparator | Difference | SE | z (weeks) |
|---|---|---:|---:|---:|---:|---:|
| US-ind10 | whole | 0.82 | 0.99 | -0.17 | 0.08 | -2.21 (4189) |
| US-ind10 | before 1981 | 0.94 | 1.18 | -0.24 | 0.13 | -1.89 (1848) |
| US-ind10 | from 1981 | 0.75 | 0.88 | -0.14 | 0.10 | -1.41 (2341) |
| US-ind10 | before 2008 | 0.92 | 1.09 | -0.17 | 0.09 | -1.88 (3257) |
| US-ind10 | from 2008 | 0.53 | 0.71 | -0.18 | 0.14 | -1.26 (932) |
| US-Mkt | whole | 0.48 | 0.86 | -0.38 | 0.08 | -4.50 (4189) |
| US-Mkt | before 1981 | 0.54 | 0.97 | -0.43 | 0.14 | -3.01 (1848) |
| US-Mkt | from 1981 | 0.45 | 0.80 | -0.35 | 0.10 | -3.40 (2341) |
| US-Mkt | before 2008 | 0.52 | 0.93 | -0.41 | 0.10 | -4.19 (3257) |
| US-Mkt | from 2008 | 0.37 | 0.68 | -0.31 | 0.18 | -1.73 (932) |
| US-NoDur | whole | 0.66 | 0.88 | -0.22 | 0.09 | -2.36 (4189) |
| US-NoDur | before 1981 | 0.61 | 1.08 | -0.47 | 0.15 | -3.05 (1848) |
| US-NoDur | from 1981 | 0.70 | 0.79 | -0.09 | 0.11 | -0.77 (2341) |
| US-NoDur | before 2008 | 0.69 | 1.03 | -0.34 | 0.11 | -3.06 (3257) |
| US-NoDur | from 2008 | 0.57 | 0.41 | +0.15 | 0.15 | +1.00 (932) |
| US-Durbl | whole | 0.55 | 0.56 | -0.01 | 0.09 | -0.09 (4189) |
| US-Durbl | before 1981 | 0.59 | 0.78 | -0.19 | 0.13 | -1.55 (1848) |
| US-Durbl | from 1981 | 0.54 | 0.46 | +0.08 | 0.12 | +0.67 (2341) |
| US-Durbl | before 2008 | 0.62 | 0.66 | -0.04 | 0.10 | -0.38 (3257) |
| US-Durbl | from 2008 | 0.45 | 0.44 | +0.01 | 0.20 | +0.07 (932) |
| US-Manuf | whole | 0.58 | 0.74 | -0.16 | 0.09 | -1.69 (4189) |
| US-Manuf | before 1981 | 0.50 | 0.84 | -0.35 | 0.15 | -2.27 (1848) |
| US-Manuf | from 1981 | 0.64 | 0.68 | -0.04 | 0.11 | -0.38 (2341) |
| US-Manuf | before 2008 | 0.65 | 0.82 | -0.17 | 0.11 | -1.60 (3257) |
| US-Manuf | from 2008 | 0.38 | 0.50 | -0.12 | 0.17 | -0.72 (932) |
| US-Enrgy | whole | 0.41 | 0.64 | -0.23 | 0.09 | -2.60 (4189) |
| US-Enrgy | before 1981 | 0.84 | 0.99 | -0.16 | 0.14 | -1.10 (1848) |
| US-Enrgy | from 1981 | 0.14 | 0.44 | -0.30 | 0.11 | -2.68 (2341) |
| US-Enrgy | before 2008 | 0.57 | 0.80 | -0.22 | 0.10 | -2.24 (3257) |
| US-Enrgy | from 2008 | -0.10 | 0.24 | -0.33 | 0.20 | -1.66 (932) |
| US-HiTec | whole | 0.49 | 0.70 | -0.21 | 0.09 | -2.20 (4189) |
| US-HiTec | before 1981 | 0.59 | 0.83 | -0.24 | 0.15 | -1.56 (1848) |
| US-HiTec | from 1981 | 0.45 | 0.63 | -0.18 | 0.11 | -1.60 (2341) |
| US-HiTec | before 2008 | 0.56 | 0.70 | -0.14 | 0.11 | -1.31 (3257) |
| US-HiTec | from 2008 | 0.29 | 0.68 | -0.39 | 0.16 | -2.42 (932) |
| US-Telcm | whole | 0.57 | 0.76 | -0.18 | 0.08 | -2.20 (4189) |
| US-Telcm | before 1981 | 0.68 | 0.76 | -0.08 | 0.12 | -0.66 (1848) |
| US-Telcm | from 1981 | 0.54 | 0.78 | -0.24 | 0.12 | -2.07 (2341) |
| US-Telcm | before 2008 | 0.67 | 0.83 | -0.16 | 0.10 | -1.62 (3257) |
| US-Telcm | from 2008 | 0.32 | 0.56 | -0.24 | 0.16 | -1.47 (932) |
| US-Shops | whole | 0.55 | 0.78 | -0.23 | 0.09 | -2.68 (4189) |
| US-Shops | before 1981 | 0.59 | 0.95 | -0.36 | 0.14 | -2.62 (1848) |
| US-Shops | from 1981 | 0.55 | 0.71 | -0.17 | 0.11 | -1.46 (2341) |
| US-Shops | before 2008 | 0.53 | 0.74 | -0.21 | 0.10 | -2.13 (3257) |
| US-Shops | from 2008 | 0.62 | 0.91 | -0.29 | 0.18 | -1.67 (932) |
| US-Hlth | whole | 0.49 | 0.77 | -0.28 | 0.09 | -3.12 (4189) |
| US-Hlth | before 1981 | 0.78 | 0.94 | -0.17 | 0.14 | -1.19 (1848) |
| US-Hlth | from 1981 | 0.31 | 0.66 | -0.34 | 0.11 | -3.07 (2341) |
| US-Hlth | before 2008 | 0.57 | 0.84 | -0.27 | 0.10 | -2.60 (3257) |
| US-Hlth | from 2008 | 0.25 | 0.53 | -0.28 | 0.17 | -1.60 (932) |
| US-Utils | whole | 0.66 | 0.88 | -0.22 | 0.10 | -2.26 (4189) |
| US-Utils | before 1981 | 0.79 | 1.08 | -0.28 | 0.15 | -1.88 (1848) |
| US-Utils | from 1981 | 0.59 | 0.79 | -0.20 | 0.13 | -1.57 (2341) |
| US-Utils | before 2008 | 0.78 | 1.05 | -0.27 | 0.12 | -2.32 (3257) |
| US-Utils | from 2008 | 0.37 | 0.47 | -0.09 | 0.18 | -0.51 (932) |
| US-Other | whole | 0.58 | 0.74 | -0.17 | 0.09 | -1.79 (4189) |
| US-Other | before 1981 | 0.66 | 0.88 | -0.22 | 0.16 | -1.41 (1848) |
| US-Other | from 1981 | 0.53 | 0.67 | -0.13 | 0.11 | -1.20 (2341) |
| US-Other | before 2008 | 0.61 | 0.81 | -0.20 | 0.11 | -1.81 (3257) |
| US-Other | from 2008 | 0.48 | 0.54 | -0.06 | 0.15 | -0.39 (932) |
| US-ind10-late | whole | 0.74 | 0.95 | -0.20 | 0.08 | -2.71 (4189) |
| US-ind10-late | before 1981 | 0.86 | 1.12 | -0.26 | 0.12 | -2.13 (1848) |
| US-ind10-late | from 1981 | 0.67 | 0.85 | -0.18 | 0.09 | -1.87 (2341) |
| US-ind10-late | before 2008 | 0.86 | 1.05 | -0.19 | 0.09 | -2.28 (3257) |
| US-ind10-late | from 2008 | 0.43 | 0.66 | -0.23 | 0.15 | -1.52 (932) |
| geo13 | whole | 0.44 | 0.48 | -0.03 | 0.12 | -0.30 (2180) |
| geo13 | before 1981 | - | - | - | - | - |
| geo13 | from 1981 | 0.44 | 0.48 | -0.03 | 0.12 | -0.30 (2180) |
| geo13 | before 2008 | 0.53 | 0.67 | -0.14 | 0.17 | -0.82 (1248) |
| geo13 | from 2008 | 0.31 | 0.17 | +0.14 | 0.13 | +1.06 (932) |
| geo-Japan | whole | 0.45 | 0.51 | -0.06 | 0.12 | -0.48 (2180) |
| geo-Japan | before 1981 | - | - | - | - | - |
| geo-Japan | from 1981 | 0.45 | 0.51 | -0.06 | 0.12 | -0.48 (2180) |
| geo-Japan | before 2008 | 0.36 | 0.51 | -0.15 | 0.17 | -0.86 (1248) |
| geo-Japan | from 2008 | 0.56 | 0.51 | +0.05 | 0.17 | +0.29 (932) |
| geo-Canada | whole | 0.22 | 0.32 | -0.10 | 0.12 | -0.88 (1428) |
| geo-Canada | before 1981 | - | - | - | - | - |
| geo-Canada | from 1981 | 0.22 | 0.32 | -0.10 | 0.12 | -0.88 (1428) |
| geo-Canada | before 2008 | 0.45 | 0.64 | -0.19 | 0.19 | -0.97 (496) |
| geo-Canada | from 2008 | 0.06 | 0.11 | -0.05 | 0.16 | -0.31 (932) |
| geo-UK | whole | 0.24 | 0.21 | +0.03 | 0.13 | +0.23 (1188) |
| geo-UK | before 1981 | - | - | - | - | - |
| geo-UK | from 1981 | 0.24 | 0.21 | +0.03 | 0.13 | +0.23 (1188) |
| geo-UK | before 2008 | 0.48 | 0.88 | -0.40 | 0.25 | -1.61 (256) |
| geo-UK | from 2008 | 0.18 | 0.03 | +0.15 | 0.15 | +1.03 (932) |
| geo-Australia | whole | 0.35 | 0.39 | -0.04 | 0.18 | -0.25 (1158) |
| geo-Australia | before 1981 | - | - | - | - | - |
| geo-Australia | from 1981 | 0.35 | 0.39 | -0.04 | 0.18 | -0.25 (1158) |
| geo-Australia | before 2008 | 0.88 | 1.56 | -0.68 | 0.36 | -1.91 (226) |
| geo-Australia | from 2008 | 0.21 | 0.08 | +0.13 | 0.19 | +0.70 (932) |
| geo-HongKong | whole | 0.22 | 0.26 | -0.04 | 0.19 | -0.18 (1036) |
| geo-HongKong | before 1981 | - | - | - | - | - |
| geo-HongKong | from 1981 | 0.22 | 0.26 | -0.04 | 0.19 | -0.18 (1036) |
| geo-HongKong | before 2008 | 0.33 | 1.65 | -1.32 | 0.63 | -2.11 (104) |
| geo-HongKong | from 2008 | 0.20 | 0.04 | +0.17 | 0.19 | +0.87 (932) |
| geo-Germany | whole | 0.15 | 0.22 | -0.06 | 0.15 | -0.42 (984) |
| geo-Germany | before 1981 | - | - | - | - | - |
| geo-Germany | from 1981 | 0.15 | 0.22 | -0.06 | 0.15 | -0.42 (984) |
| geo-Germany | before 2008 | 0.61 | 1.33 | -0.72 | 0.38 | -1.86 (52) |
| geo-Germany | from 2008 | 0.12 | 0.15 | -0.03 | 0.16 | -0.17 (932) |
| geo-Singapore | whole | 0.41 | 0.22 | +0.20 | 0.18 | +1.11 (984) |
| geo-Singapore | before 1981 | - | - | - | - | - |
| geo-Singapore | from 1981 | 0.41 | 0.22 | +0.20 | 0.18 | +1.11 (984) |
| geo-Singapore | before 2008 | 0.10 | 0.80 | -0.69 | 0.62 | -1.12 (52) |
| geo-Singapore | from 2008 | 0.47 | 0.15 | +0.32 | 0.19 | +1.67 (932) |
| geo-France | whole | 0.14 | 0.04 | +0.11 | 0.15 | +0.70 (867) |
| geo-France | before 1981 | - | - | - | - | - |
| geo-France | from 1981 | 0.14 | 0.04 | +0.11 | 0.15 | +0.70 (867) |
| geo-France | before 2008 | - | - | - | - | - |
| geo-France | from 2008 | 0.14 | 0.04 | +0.11 | 0.15 | +0.70 (867) |
| geo-Switzerland | whole | -0.00 | 0.03 | -0.03 | 0.16 | -0.18 (832) |
| geo-Switzerland | before 1981 | - | - | - | - | - |
| geo-Switzerland | from 1981 | -0.00 | 0.03 | -0.03 | 0.16 | -0.18 (832) |
| geo-Switzerland | before 2008 | - | - | - | - | - |
| geo-Switzerland | from 2008 | -0.00 | 0.03 | -0.03 | 0.16 | -0.18 (832) |
| geo-Belgium | whole | 0.20 | 0.21 | -0.01 | 0.22 | -0.05 (810) |
| geo-Belgium | before 1981 | - | - | - | - | - |
| geo-Belgium | from 1981 | 0.20 | 0.21 | -0.01 | 0.22 | -0.05 (810) |
| geo-Belgium | before 2008 | - | - | - | - | - |
| geo-Belgium | from 2008 | 0.20 | 0.21 | -0.01 | 0.22 | -0.05 (810) |
| geo-Netherlands | whole | 0.61 | 0.32 | +0.29 | 0.22 | +1.34 (732) |
| geo-Netherlands | before 1981 | - | - | - | - | - |
| geo-Netherlands | from 1981 | 0.61 | 0.32 | +0.29 | 0.22 | +1.34 (732) |
| geo-Netherlands | before 2008 | - | - | - | - | - |
| geo-Netherlands | from 2008 | 0.61 | 0.32 | +0.29 | 0.22 | +1.34 (732) |
| geo-Austria | whole | 0.03 | 0.15 | -0.12 | 0.17 | -0.72 (728) |
| geo-Austria | before 1981 | - | - | - | - | - |
| geo-Austria | from 1981 | 0.03 | 0.15 | -0.12 | 0.17 | -0.72 (728) |
| geo-Austria | before 2008 | - | - | - | - | - |
| geo-Austria | from 2008 | 0.03 | 0.15 | -0.12 | 0.17 | -0.72 (728) |
| geo-Spain | whole | 0.20 | 0.30 | -0.09 | 0.22 | -0.42 (693) |
| geo-Spain | before 1981 | - | - | - | - | - |
| geo-Spain | from 1981 | 0.20 | 0.30 | -0.09 | 0.22 | -0.42 (693) |
| geo-Spain | before 2008 | - | - | - | - | - |
| geo-Spain | from 2008 | 0.20 | 0.30 | -0.09 | 0.22 | -0.42 (693) |
| six | whole | 0.88 | 1.06 | -0.18 | 0.07 | -2.76 (1657) |
| six | before 1981 | - | - | - | - | - |
| six | from 1981 | 0.88 | 1.06 | -0.18 | 0.07 | -2.76 (1657) |
| six | before 2008 | 0.42 | 0.79 | -0.37 | 0.16 | -2.34 (725) |
| six | from 2008 | 1.13 | 1.23 | -0.10 | 0.05 | -1.96 (932) |

## Standalone vs hold

| Test | Window | Rule | Comparator | Difference | SE | z (weeks) |
|---|---|---:|---:|---:|---:|---:|
| US-ind10 | whole | 0.73 | 0.86 | -0.13 | 0.07 | -1.89 (4189) |
| US-ind10 | before 1981 | 0.83 | 0.94 | -0.11 | 0.12 | -0.98 (1848) |
| US-ind10 | from 1981 | 0.68 | 0.82 | -0.13 | 0.09 | -1.53 (2341) |
| US-ind10 | before 2008 | 0.88 | 0.96 | -0.08 | 0.08 | -0.99 (3257) |
| US-ind10 | from 2008 | 0.47 | 0.64 | -0.17 | 0.12 | -1.41 (932) |
| US-Mkt | whole | 0.48 | 0.79 | -0.30 | 0.08 | -3.62 (4189) |
| US-Mkt | before 1981 | 0.48 | 0.87 | -0.39 | 0.14 | -2.74 (1848) |
| US-Mkt | from 1981 | 0.50 | 0.74 | -0.25 | 0.10 | -2.40 (2341) |
| US-Mkt | before 2008 | 0.49 | 0.85 | -0.35 | 0.10 | -3.57 (3257) |
| US-Mkt | from 2008 | 0.49 | 0.65 | -0.16 | 0.16 | -1.02 (932) |
| US-NoDur | whole | 0.63 | 0.86 | -0.23 | 0.09 | -2.63 (4189) |
| US-NoDur | before 1981 | 0.52 | 0.82 | -0.29 | 0.14 | -2.08 (1848) |
| US-NoDur | from 1981 | 0.71 | 0.90 | -0.19 | 0.11 | -1.75 (2341) |
| US-NoDur | before 2008 | 0.67 | 0.95 | -0.29 | 0.10 | -2.76 (3257) |
| US-NoDur | from 2008 | 0.55 | 0.58 | -0.03 | 0.14 | -0.23 (932) |
| US-Durbl | whole | 0.43 | 0.57 | -0.14 | 0.08 | -1.63 (4189) |
| US-Durbl | before 1981 | 0.51 | 0.69 | -0.18 | 0.14 | -1.29 (1848) |
| US-Durbl | from 1981 | 0.41 | 0.53 | -0.12 | 0.11 | -1.12 (2341) |
| US-Durbl | before 2008 | 0.57 | 0.65 | -0.08 | 0.10 | -0.74 (3257) |
| US-Durbl | from 2008 | 0.26 | 0.52 | -0.26 | 0.17 | -1.54 (932) |
| US-Manuf | whole | 0.60 | 0.73 | -0.13 | 0.09 | -1.49 (4189) |
| US-Manuf | before 1981 | 0.51 | 0.78 | -0.27 | 0.15 | -1.85 (1848) |
| US-Manuf | from 1981 | 0.66 | 0.70 | -0.04 | 0.11 | -0.39 (2341) |
| US-Manuf | before 2008 | 0.71 | 0.82 | -0.10 | 0.11 | -0.98 (3257) |
| US-Manuf | from 2008 | 0.36 | 0.52 | -0.16 | 0.15 | -1.08 (932) |
| US-Enrgy | whole | 0.47 | 0.65 | -0.17 | 0.09 | -1.95 (4189) |
| US-Enrgy | before 1981 | 0.88 | 0.96 | -0.08 | 0.14 | -0.58 (1848) |
| US-Enrgy | from 1981 | 0.26 | 0.49 | -0.24 | 0.11 | -2.14 (2341) |
| US-Enrgy | before 2008 | 0.67 | 0.84 | -0.18 | 0.10 | -1.75 (3257) |
| US-Enrgy | from 2008 | 0.07 | 0.27 | -0.21 | 0.18 | -1.13 (932) |
| US-HiTec | whole | 0.53 | 0.67 | -0.14 | 0.08 | -1.70 (4189) |
| US-HiTec | before 1981 | 0.57 | 0.79 | -0.22 | 0.16 | -1.38 (1848) |
| US-HiTec | from 1981 | 0.53 | 0.61 | -0.09 | 0.10 | -0.89 (2341) |
| US-HiTec | before 2008 | 0.54 | 0.64 | -0.10 | 0.10 | -1.01 (3257) |
| US-HiTec | from 2008 | 0.51 | 0.80 | -0.29 | 0.15 | -1.91 (932) |
| US-Telcm | whole | 0.46 | 0.64 | -0.18 | 0.08 | -2.30 (4189) |
| US-Telcm | before 1981 | 0.67 | 0.73 | -0.06 | 0.11 | -0.52 (1848) |
| US-Telcm | from 1981 | 0.38 | 0.62 | -0.24 | 0.11 | -2.21 (2341) |
| US-Telcm | before 2008 | 0.55 | 0.72 | -0.18 | 0.10 | -1.87 (3257) |
| US-Telcm | from 2008 | 0.27 | 0.43 | -0.16 | 0.15 | -1.11 (932) |
| US-Shops | whole | 0.54 | 0.78 | -0.24 | 0.08 | -2.94 (4189) |
| US-Shops | before 1981 | 0.34 | 0.74 | -0.40 | 0.12 | -3.24 (1848) |
| US-Shops | from 1981 | 0.67 | 0.81 | -0.14 | 0.11 | -1.32 (2341) |
| US-Shops | before 2008 | 0.52 | 0.77 | -0.26 | 0.09 | -2.78 (3257) |
| US-Shops | from 2008 | 0.61 | 0.79 | -0.18 | 0.16 | -1.12 (932) |
| US-Hlth | whole | 0.56 | 0.80 | -0.25 | 0.09 | -2.88 (4189) |
| US-Hlth | before 1981 | 0.73 | 0.84 | -0.11 | 0.13 | -0.85 (1848) |
| US-Hlth | from 1981 | 0.43 | 0.77 | -0.34 | 0.10 | -3.23 (2341) |
| US-Hlth | before 2008 | 0.61 | 0.84 | -0.23 | 0.10 | -2.34 (3257) |
| US-Hlth | from 2008 | 0.39 | 0.68 | -0.29 | 0.17 | -1.76 (932) |
| US-Utils | whole | 0.64 | 0.80 | -0.16 | 0.09 | -1.78 (4189) |
| US-Utils | before 1981 | 0.80 | 0.91 | -0.11 | 0.16 | -0.73 (1848) |
| US-Utils | from 1981 | 0.57 | 0.75 | -0.19 | 0.11 | -1.64 (2341) |
| US-Utils | before 2008 | 0.79 | 0.95 | -0.16 | 0.12 | -1.33 (3257) |
| US-Utils | from 2008 | 0.40 | 0.51 | -0.11 | 0.15 | -0.76 (932) |
| US-Other | whole | 0.53 | 0.65 | -0.12 | 0.08 | -1.42 (4189) |
| US-Other | before 1981 | 0.59 | 0.73 | -0.14 | 0.15 | -0.96 (1848) |
| US-Other | from 1981 | 0.52 | 0.62 | -0.10 | 0.10 | -0.97 (2341) |
| US-Other | before 2008 | 0.61 | 0.76 | -0.15 | 0.11 | -1.39 (3257) |
| US-Other | from 2008 | 0.46 | 0.45 | +0.01 | 0.13 | +0.05 (932) |
| US-ind10-late | whole | 0.70 | 0.86 | -0.16 | 0.07 | -2.32 (4189) |
| US-ind10-late | before 1981 | 0.81 | 0.94 | -0.13 | 0.11 | -1.19 (1848) |
| US-ind10-late | from 1981 | 0.65 | 0.82 | -0.17 | 0.09 | -1.90 (2341) |
| US-ind10-late | before 2008 | 0.84 | 0.96 | -0.12 | 0.08 | -1.45 (3257) |
| US-ind10-late | from 2008 | 0.46 | 0.64 | -0.18 | 0.13 | -1.47 (932) |
| geo13 | whole | 0.25 | 0.31 | -0.07 | 0.11 | -0.62 (2180) |
| geo13 | before 1981 | - | - | - | - | - |
| geo13 | from 1981 | 0.25 | 0.31 | -0.07 | 0.11 | -0.62 (2180) |
| geo13 | before 2008 | 0.18 | 0.32 | -0.13 | 0.17 | -0.81 (1248) |
| geo13 | from 2008 | 0.33 | 0.31 | +0.02 | 0.13 | +0.19 (932) |
| geo-Japan | whole | 0.16 | 0.29 | -0.14 | 0.10 | -1.32 (2180) |
| geo-Japan | before 1981 | - | - | - | - | - |
| geo-Japan | from 1981 | 0.16 | 0.29 | -0.14 | 0.10 | -1.32 (2180) |
| geo-Japan | before 2008 | 0.09 | 0.19 | -0.10 | 0.17 | -0.58 (1248) |
| geo-Japan | from 2008 | 0.23 | 0.43 | -0.20 | 0.14 | -1.37 (932) |
| geo-Canada | whole | 0.22 | 0.39 | -0.18 | 0.11 | -1.63 (1428) |
| geo-Canada | before 1981 | - | - | - | - | - |
| geo-Canada | from 1981 | 0.22 | 0.39 | -0.18 | 0.11 | -1.63 (1428) |
| geo-Canada | before 2008 | 0.28 | 0.48 | -0.20 | 0.22 | -0.88 (496) |
| geo-Canada | from 2008 | 0.19 | 0.35 | -0.16 | 0.12 | -1.35 (932) |
| geo-UK | whole | 0.35 | 0.35 | +0.00 | 0.12 | +0.01 (1188) |
| geo-UK | before 1981 | - | - | - | - | - |
| geo-UK | from 1981 | 0.35 | 0.35 | +0.00 | 0.12 | +0.01 (1188) |
| geo-UK | before 2008 | 0.62 | 1.08 | -0.45 | 0.23 | -2.01 (256) |
| geo-UK | from 2008 | 0.31 | 0.22 | +0.09 | 0.13 | +0.67 (932) |
| geo-Australia | whole | 0.41 | 0.39 | +0.02 | 0.16 | +0.11 (1158) |
| geo-Australia | before 1981 | - | - | - | - | - |
| geo-Australia | from 1981 | 0.41 | 0.39 | +0.02 | 0.16 | +0.11 (1158) |
| geo-Australia | before 2008 | 0.88 | 1.56 | -0.68 | 0.36 | -1.91 (226) |
| geo-Australia | from 2008 | 0.35 | 0.21 | +0.14 | 0.18 | +0.79 (932) |
| geo-HongKong | whole | 0.34 | 0.24 | +0.11 | 0.18 | +0.61 (1036) |
| geo-HongKong | before 1981 | - | - | - | - | - |
| geo-HongKong | from 1981 | 0.34 | 0.24 | +0.11 | 0.18 | +0.61 (1036) |
| geo-HongKong | before 2008 | 0.33 | 1.65 | -1.32 | 0.63 | -2.11 (104) |
| geo-HongKong | from 2008 | 0.35 | 0.10 | +0.25 | 0.18 | +1.42 (932) |
| geo-Germany | whole | 0.37 | 0.43 | -0.06 | 0.15 | -0.38 (984) |
| geo-Germany | before 1981 | - | - | - | - | - |
| geo-Germany | from 1981 | 0.37 | 0.43 | -0.06 | 0.15 | -0.38 (984) |
| geo-Germany | before 2008 | 0.61 | 1.33 | -0.72 | 0.38 | -1.86 (52) |
| geo-Germany | from 2008 | 0.36 | 0.39 | -0.03 | 0.15 | -0.18 (932) |
| geo-Singapore | whole | 0.35 | 0.21 | +0.15 | 0.16 | +0.93 (984) |
| geo-Singapore | before 1981 | - | - | - | - | - |
| geo-Singapore | from 1981 | 0.35 | 0.21 | +0.15 | 0.16 | +0.93 (984) |
| geo-Singapore | before 2008 | 0.10 | 0.80 | -0.69 | 0.62 | -1.12 (52) |
| geo-Singapore | from 2008 | 0.37 | 0.17 | +0.20 | 0.17 | +1.16 (932) |
| geo-France | whole | 0.34 | 0.41 | -0.07 | 0.16 | -0.43 (867) |
| geo-France | before 1981 | - | - | - | - | - |
| geo-France | from 1981 | 0.34 | 0.41 | -0.07 | 0.16 | -0.43 (867) |
| geo-France | before 2008 | - | - | - | - | - |
| geo-France | from 2008 | 0.34 | 0.41 | -0.07 | 0.16 | -0.43 (867) |
| geo-Switzerland | whole | 0.30 | 0.34 | -0.04 | 0.18 | -0.24 (832) |
| geo-Switzerland | before 1981 | - | - | - | - | - |
| geo-Switzerland | from 1981 | 0.30 | 0.34 | -0.04 | 0.18 | -0.24 (832) |
| geo-Switzerland | before 2008 | - | - | - | - | - |
| geo-Switzerland | from 2008 | 0.30 | 0.34 | -0.04 | 0.18 | -0.24 (832) |
| geo-Belgium | whole | 0.24 | 0.33 | -0.09 | 0.19 | -0.46 (810) |
| geo-Belgium | before 1981 | - | - | - | - | - |
| geo-Belgium | from 1981 | 0.24 | 0.33 | -0.09 | 0.19 | -0.46 (810) |
| geo-Belgium | before 2008 | - | - | - | - | - |
| geo-Belgium | from 2008 | 0.24 | 0.33 | -0.09 | 0.19 | -0.46 (810) |
| geo-Netherlands | whole | 0.62 | 0.58 | +0.04 | 0.19 | +0.22 (732) |
| geo-Netherlands | before 1981 | - | - | - | - | - |
| geo-Netherlands | from 1981 | 0.62 | 0.58 | +0.04 | 0.19 | +0.22 (732) |
| geo-Netherlands | before 2008 | - | - | - | - | - |
| geo-Netherlands | from 2008 | 0.62 | 0.58 | +0.04 | 0.19 | +0.22 (732) |
| geo-Austria | whole | 0.32 | 0.44 | -0.12 | 0.17 | -0.67 (728) |
| geo-Austria | before 1981 | - | - | - | - | - |
| geo-Austria | from 1981 | 0.32 | 0.44 | -0.12 | 0.17 | -0.67 (728) |
| geo-Austria | before 2008 | - | - | - | - | - |
| geo-Austria | from 2008 | 0.32 | 0.44 | -0.12 | 0.17 | -0.67 (728) |
| geo-Spain | whole | 0.11 | 0.43 | -0.32 | 0.20 | -1.60 (693) |
| geo-Spain | before 1981 | - | - | - | - | - |
| geo-Spain | from 1981 | 0.11 | 0.43 | -0.32 | 0.20 | -1.60 (693) |
| geo-Spain | before 2008 | - | - | - | - | - |
| geo-Spain | from 2008 | 0.11 | 0.43 | -0.32 | 0.20 | -1.60 (693) |
| six | whole | 0.84 | 0.91 | -0.07 | 0.08 | -0.86 (1657) |
| six | before 1981 | - | - | - | - | - |
| six | from 1981 | 0.84 | 0.91 | -0.07 | 0.08 | -0.86 (1657) |
| six | before 2008 | 0.27 | 0.48 | -0.21 | 0.17 | -1.25 (725) |
| six | from 2008 | 1.16 | 1.21 | -0.05 | 0.06 | -0.82 (932) |

## Average exposure (sum of weights)

| Test | Start | overlay | alone | tsmom12 | hold |
|---|---|---:|---:|---:|---:|
| US-ind10 | 1945-07-25 | 37% | 49% | 76% | 100% |
| US-Mkt | 1945-07-25 | 39% | 50% | 78% | 100% |
| US-NoDur | 1945-07-25 | 39% | 49% | 80% | 100% |
| US-Durbl | 1945-07-25 | 34% | 50% | 69% | 100% |
| US-Manuf | 1945-07-25 | 38% | 50% | 76% | 100% |
| US-Enrgy | 1945-07-25 | 36% | 48% | 76% | 100% |
| US-HiTec | 1945-07-25 | 38% | 48% | 78% | 100% |
| US-Telcm | 1945-07-25 | 36% | 49% | 77% | 100% |
| US-Shops | 1945-07-25 | 38% | 49% | 77% | 100% |
| US-Hlth | 1945-07-25 | 38% | 50% | 76% | 100% |
| US-Utils | 1945-07-25 | 38% | 48% | 80% | 100% |
| US-Other | 1945-07-25 | 37% | 50% | 74% | 100% |
| US-ind10-late | 1945-07-25 | 37% | 49% | 76% | 100% |
| geo13 | 1984-01-25 | 29% | 49% | 61% | 100% |
| geo-Japan | 1984-01-25 | 28% | 49% | 59% | 100% |
| geo-Canada | 1998-06-24 | 38% | 58% | 67% | 100% |
| geo-UK | 2003-01-25 | 36% | 51% | 69% | 100% |
| geo-Australia | 2003-08-25 | 31% | 43% | 72% | 100% |
| geo-HongKong | 2005-12-25 | 28% | 49% | 58% | 100% |
| geo-Germany | 2006-12-25 | 35% | 53% | 69% | 100% |
| geo-Singapore | 2006-12-25 | 31% | 52% | 59% | 100% |
| geo-France | 2009-03-25 | 36% | 51% | 67% | 100% |
| geo-Switzerland | 2009-11-24 | 30% | 49% | 67% | 100% |
| geo-Belgium | 2010-04-24 | 23% | 41% | 62% | 100% |
| geo-Netherlands | 2011-10-25 | 35% | 49% | 74% | 100% |
| geo-Austria | 2011-11-24 | 29% | 47% | 61% | 100% |
| geo-Spain | 2012-07-25 | 29% | 48% | 60% | 100% |
| six | 1994-02-01 | 47% | 63% | 76% | 100% |

## Placebo (US ten-industry book, monthly arithmetic, standalone minus hold)

s = 0 is the true rule; s > 0 replaces the same month by months 12 j + s before.

| s | Sharpe difference | Months |
|---:|---:|---:|
| 0 | -0.129 | 963 |
| 1 | -0.166 | 963 |
| 2 | -0.292 | 963 |
| 3 | -0.216 | 963 |
| 4 | -0.146 | 963 |
| 5 | -0.164 | 963 |
| 6 | -0.255 | 963 |
| 7 | -0.227 | 963 |
| 8 | -0.184 | 963 |
| 9 | -0.224 | 963 |
| 10 | -0.209 | 963 |

Rank of the true difference among the 11 (1 = highest): 1.
