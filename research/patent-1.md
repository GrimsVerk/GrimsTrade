# Patent 1: FRED release 486 now answers scripts, but has no as-known vintages; `patent-surge` stays parked (no gate)

Research run patent-1, 2026-11-26 (night run, WIDER lane, next-steps item 7(a)). Branch
`patent-1` (from `main` c1030c7), PR into `main`. Research only: keyless public data, no key,
no sign-up, no change to the gym, the daily runner or the live strategies.

Task: wide-27's O1 `patent-surge` (scored 6) was parked because FRED release 486 ("U.S.
Granted Patents by States, Territories, and Countries") did not answer scripts. Step 1 was to
retry it; step 2 (a W47 gate) only if a vintage-dated (as-known) per-country series could be had.

**Outcome: data reachable, as-known dating not. No card, no gate, no return read.** Family
counts are unchanged.

## What was tried (2026-11-26, 08:13-08:15 UTC)

One request at a time, 3-5 s apart (FRED's robots.txt asks for a 1 s crawl delay, ALFRED's 2 s).
Two User-Agents: a generic browser-like string (`Mozilla/5.0 (research script)`, not a copy of
any real person's or service's UA, no contact), dropped once curl's default (`curl/8.23.0`)
worked. Neither carries anything personal.

| Request | UA | Result |
|---|---|---|
| `fred.stlouisfed.org/robots.txt` (HTTP/2) | browser-like | stream reset by server (curl 92), no data |
| same, HTTP/1.1 | browser-like | timeout after 30 s, 0 bytes |
| same | curl default | **200**, 292 bytes |
| `fred.stlouisfed.org/release?rid=486` | browser-like | stream reset (curl 92) |
| same | curl default | **200**, 157 kB |
| `alfred.stlouisfed.org/robots.txt` | browser-like | stream reset (curl 92) |
| same | curl default | **200**, 234 bytes |
| `fred.stlouisfed.org/graph/fredgraph.csv?id=PATENT4NJPUTILITY` | curl default | **200**, 528 bytes, 29 rows |
| `fred.stlouisfed.org/series/PATENT4NJPUTILITY` | curl default | 200 |
| `alfred.stlouisfed.org/series?seid=PATENT4NJPUTILITY` | curl default | 200 |

So the earlier failures (wide-27, data-long-3, data-wide-2) were most likely the CDN refusing the
browser-like User-Agent, not a site-wide block: the same paths answer at once to curl's own UA.
That is a useful lesson for other FRED/ALFRED lanes.

**robots.txt.** FRED disallows only `/graph/graph-landing.php`, `/graph/image.php`,
`/graph/fredgraph.png`, `/searchresults`, `/fred-glance-widget.php` and `/seriesBeta`;
`fredgraph.csv`, `/release` and `/series` are allowed. ALFRED disallows only
`/graph/graph-landing.php`, `/graph/image.php`, `/graph/alfredgraph.png` and `/search`.

## What the data are (format and coverage only; no price or return was read)

- Release 486 holds 1,245 series. Per-country ids follow `PATENT4N<ISO2><TYPE>`, with TYPE one
  of UTILITY, DESIGN, PLANT, REISSUE, TOTAL (e.g. `PATENT4NJPUTILITY`, `PATENT4NCNTOTAL`).
- `PATENT4NJPUTILITY` is annual, 1992-2020 (29 observations). The last observation is 2020.
- **ALFRED's real-time period for this series starts 2021-03-19** (next vintage 2021-05-21,
  the last FRED update). The whole 1992-2020 history entered FRED on one day in 2021: there is
  no vintage at which the market could have seen, say, the 2005 count. A vintage-dated
  (as-known) series is **not obtainable** from FRED/ALFRED.
- The series also stops in 2020 with no update since May 2021, so even a pass could not be
  traded live from this source.

## Why no gate tonight

The brief's stop rule: if a vintage-dated (as-known) series isn't obtainable, record it and
stop. It isn't, so I stopped before writing a card and before reading any return.

A later lane could argue a fixed release lag instead of vintages: grants are public weekly in
the Official Gazette and annual grant counts are barely revised (both unverified here), so "count for year t is usable
from, e.g., 1 April t+1" would be a defensible as-known proxy (USPTO's PTMT country tables were
usually out in the first months of t+1, unverified here). That is a convention change for the
lead or the owner to accept, not one to take on my own. Costs to weigh against it: about 28
annual cross-sections (1993-2020 as signal years), the end in 2020 (no live use), and wide-27's
own caveat that patenting follows R&D and booms (a cycle confound the card would have to
control for).

## Next

1. 7(a) updated in `next-steps.md`: FRED and ALFRED answer scripts with curl's default UA;
   release 486 is first-vintage 2021-03-19 for its whole history and ends in 2020. `patent-surge`
   needs either an accepted fixed-lag convention (decision) or a dated source (PatentsView
   bulk, over 1 GB, dated by grant date, would also give a live feed).
2. Other lanes that gave up on FRED/ALFRED "not answering" should retry with curl's default UA,
   one request at a time, honouring the crawl delay.
