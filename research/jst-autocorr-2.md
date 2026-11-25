# jst-autocorr-2: where does the autocorrelation of early JST annual equity returns come from?

Lane `jst-autocorr-2`, 2026-11-25 (UTC). Branch `jst-autocorr-2`. Descriptive; nothing is
selected or tuned. Card: [`cards/jst-autocorr-2.md`](cards/jst-autocorr-2.md), pushed before
the documentation was re-read and before any number was computed. The labels were committed
(3d3b79a) before the first run. Tables: [`results/jst-autocorr-2.md`](results/jst-autocorr-2.md).
Code: `lib/jstautocorr2.py`; tests: `tests/test_jstautocorr2.py`. Statistics only. JST R6 is
CC BY-NC-SA 4.0 (Jorda, Schularick and Taylor 2017; Jorda, Knoll, Kuvshinov, Schularick and
Taylor 2019). The Bank of England's "A millennium of macroeconomic data" v3.1 monthly sheet
(OGL v3, datahub mirror, 6 MB) is read locally and not committed.

## The answer on one screen

**Averaging is ruled out, and no documented flag explains the autocorrelation.** By the
card's rule, none of averaging/interpolation, war/closure/hyperinflation, thin market, or the
three together explains it. The remaining autocorrelation sits in data with no flag, and its
origin is open: it could be real, or it could come from construction the documentation does not
describe. About half of it is common across countries.

- **No early source is documented as an annual average.** The documentation (JST appendix,
  plus the original sources found keyless) states a single point in time for every source whose
  price timing is stated:
  - year-end: Sweden from 1891, Germany (Ronge), France, Switzerland, Norway from 1921, and
    Madrid 1927-1940;
  - a December average: the US (Shiller) and Australia (Brailsford et al.). A one-month average
    adds about +0.01 of lag-1 autocorrelation (Working's formula with averaging over 1/12 of the
    year: (1/72) / (1 - 1/36) = 0.014).
  - The documented year-end pairs are the *most* autocorrelated group: +0.25 over 316 pairs,
    against +0.09 for unknown timing and +0.00 for the December-average pairs. So the
    Working-1960 story (annual averages give about 0.25) does not fit the data where the timing
    is known.
- **Flag tests on insure-1870-1's decisive sample.** Pooled lag-1 acf of log returns over bills
  is A0 = +0.138 over 1,218 pairs. The 1966-2020 value on the same pairing is +0.033.

  | Flag | Acf flagged (pairs) | Acf rest (pairs) | Perm. p | Card reading |
  |---|---:|---:|---:|---|
  | averaged / interpolated | -0.00 (138) | +0.15 (1080) | 0.84 | not explained |
  | thin market | +0.26 (275) | +0.12 (943) | 0.19 | not explained |
  | disrupted (wars, closures, hyperinflation) | +0.06 (205) | +0.18 (1013) | 0.75 | not explained |
  | union of the three | +0.08 (520) | +0.19 (698) | 0.76 | not explained |

  Thin-market periods are the most autocorrelated (+0.26). The difference is not significant
  across the 46 source runs (p 0.19), and the rest stays at +0.12, far above its noise line of
  0.05. War and closure years *lower* the autocorrelation: the undisrupted pairs show +0.18.
- **Half of it is common across countries (description, not on the card).** The equal-weighted
  cross-country mean return has lag-1 acf +0.38 in 1872-1965 (93 years). By era it is +0.26
  in 1872-1913, +0.42 in 1919-1938 and +0.29 in 1946-1965; in 1966-2020 it is -0.02. Take
  each country's return minus that year's cross-country mean: the remainder has acf +0.066,
  against +0.138 for the raw returns. The thin periods keep more of it (+0.136), which is
  what country-specific stale prices would produce. The common half cannot be one country's
  index construction. It could be real multi-year co-movement (the 1920s boom and the 1929-32
  slide, post-war re-rating), or construction that was common to many early indices.
- **Independent UK series (description).** JST's UK capital gain is not the Bank of England's
  spliced monthly index. JST is closer to a point-in-time sample of it than to an annual
  average:
  - 1871-1907: correlation 0.69 with the Dec-Dec change, 0.71 with Jan-Jan and 0.46 with the
    annual average.
  - 1908-1963: 0.86, 0.86 and 0.63.
  - 1964-2016: Dec-Dec 0.996.

  The BoE index sampled in December is itself autocorrelated: +0.42 in 1871-1907 and +0.19 in
  1908-1963, against JST's +0.21 and +0.20. So the UK autocorrelation also shows up in a second
  series sampled at year-end. How the BoE index is built before 1914 was not read.

**Recommendation for timing tests on JST annual data:**

1. **Never use a rotation or random-date null on JST annual equity before 1966.** The pooled
   autocorrelation (+0.14 to +0.19 depending on pairing) is not explained by any documented
   construction feature, and half of it is common across countries. A rotation null assumes
   zero autocorrelation and so turns it into "timing" (jst-autocorr-1: most of insure-1870-1's
   gap). Use an AR(1)-matched or block-bootstrap null that keeps each country's (and the
   common) lag-1 structure. This applies to every row, usable or not.
2. **Drop these years from any timing test:**
   - war, closure and hyperinflation years: 1914-1918 and 1939-1945 everywhere, plus the
     documented closures, the Spanish civil war, the Portuguese revolution, German and
     Australian price controls, and CPI above 50%;
   - the interpolated or non-calendar years: Switzerland 1914-16, the Netherlands 1944-46,
     Spain 1937-40, Portugal 1975-77.
3. **Exclude these periods, or use them only with an AR-preserving null and flag them as
   suspect.** Each has a high acf on the undisrupted pairs, above its noise line, and a
   documented or likely stale-price mechanism:
   - Norway 1881-1920 (JST Oslo microdata, 22 shares quoted monthly in 1881): +0.65.
   - Portugal 1870-1987 (JST Lisbon microdata, timing not stated): +0.38.
   - Belgium 1870-1914 (SCOB): +0.38. Annaert and Van Hyfte (2006): "Infrequent trading of
     stocks induces serial correlation in the indices".
   - Germany 1890-1913 (Eube): +0.42. Eube notes that his replacement of missing prices
     "zu einer Versteifung des Indextrends (Autokorrelation) führt", though for at most 1% of
     prices.
   - Spain IGBM 1941-2017: +0.29, timing not stated.
4. **Usable with a standard null by the card's rule** (documented year-end, broad, acf at or
   below its noise line, 91 scored years): Switzerland 1926-1959 (Pictet), Germany 1871-1889
   and 1914-1959 (Ronge, without the war and price-freeze years). Two more meet the substance
   of the rule but not its letter:
   - the US (Shiller, December average of daily closes; the card rule says "averaged", but the
     smoothing is about 0.01; acf +0.06);
   - Norway 1921-2000 (Klovland, latest bid of December, acf -0.09; thin label unknown).
5. **Everything else (1,308 scored years): AR-preserving null only.** The price timing or the
   market depth is not stated, so these rows are not cleared, even where their own acf is
   small: Denmark 1923-1999 +0.01, Japan 1887-1940 +0.02, Netherlands 1901-1995 +0.16.

**For insure-1870-1 and the SUMMARY claim.** jst-autocorr-1's reading stands, now with the
source question answered as far as the documentation allows. The early timing evidence
(p_S 0.020) is "consistent with autocorrelation that is not an averaging artefact, of
unknown origin (partly common across countries, highest in thin markets)". It is not
independent evidence of timing. A re-test would need the AR-preserving null of point 1.
Nothing changes for the live rule.

## How sure

- **Most labels are "unknown".** A label needed a quote. Timing is stated for 12 of 56
  source periods (plus four interpolated spans), and thin/broad for 17. The Italian, Japanese, Portuguese, Dutch and Danish
  sources, Grossman (2002), Barclays and the IGBM were not reachable keyless or say nothing.
  The flag tests therefore compare documented-flagged data against a mix of unflagged and
  unknown data, and an undocumented averaged source hidden in "unknown" cannot be excluded.
  But "unknown" is the *less* autocorrelated group (+0.09), so a hidden averaged source would
  have to be offset by others.
- **Power.** The thin split has 275 flagged pairs and 46 shuffle units. A real thin-market
  effect of the observed size (+0.13) is not significant at that size, so "not explained" is
  partly "not shown". The other flags point the wrong way (flagged acf lower), so more data
  would not turn them into explanations.
- **Pairing differs from jst-autocorr-1.** Pairs here never cross a documented source change,
  and each (segment, source) run is demeaned on its own, so A0 is +0.138 here against
  jst-autocorr-1's +0.165-0.170. Shorter runs bias each run's acf down a little (about
  -1/n per run).
- **Choices made after the card, before any number** (all in commit 3d3b79a, before the first
  run):
  - **Source periods split at documented construction changes:** Sweden 1891 (Aurell lists to
    ten year-end stocks) and 1902; Belgium 1915 (the thin-trading statement covers 1832-1914);
    Australia 1936 (47 stocks by 1935); Denmark 1914 (yearbook index); Madrid 1927 (Moore to
    the BdE archive). jst-autocorr-1 had shown acf for the unsplit periods.
  - **Thin rule refined:** a documented missing-price share counts as "thin" only if material.
    France carries forward 16% of 19th-century prices and is thin; Eube replaces at most 1%
    and is broad.
  - Australia's 1941-47 price controls (Brailsford et al.) and Germany's price freeze to 1948
    (Ronge) were added to the disruption years.
- **Versions of the JST documentation disagree.** The QJE appendix (`RORE_documentation.pdf`,
  used here) splits the UK at 1908 and Norway at 1921. The 2017 FRBSF working-paper appendix
  splits the UK at 1929, Norway at 1915 and Denmark at 1893, and its Table A.29 also gives the
  UK at 1929. Which version R6 follows was not checked against the data.
- **The common-component and UK checks are descriptions, not tests.** The world mean changes
  composition as countries enter. The BoE index's own early sources were not read.

## Documentation behind the labels

Each country lists its stated price timing, then its stated market depth, then the source.
"Not stated" means no keyless text said it. JST's paper-wide line ("equity prices ... compare
end-of-year prices of shares") is not counted as a statement for any one source, per the card.

- **US, 1870-2020 (Shiller)**
  - Timing: December average. Shiller's prices are "monthly averages of daily closing prices",
    and JST matches Dec-Dec (jst-autocorr-1).
  - Market depth: not stated.
  - Source: Shiller data page; jst-autocorr-1.
- **Australia, 1882-2008 (Brailsford, Handley and Maheswaran)**
  - Timing: December average. "Each data point in the index series represents the average
    value of the index in December of that year" (1882-1957: the average of December high and
    low prices).
  - Market depth: thin to 1935. "only five stocks included in the index in 1875, twelve in
    1905 and forty seven in 1935". Price controls ran Nov 1941 to Feb 1947.
  - Source: the 2007/08 predecessor of BHM 2012 (AEMC annexure).
- **Australia, 1870-1881 (IMM London listings)**: timing not stated; depth not stated.
- **France, 1870-2010 (Le Bris and Hautcoeur)**
  - Timing: year-end in substance. "monthly prices ... for the first Friday of each month";
    the index is chained "from January to January".
  - Market depth: thin. "when a price was missing, the previous listed price was used ...
    almost 16 per cent of the total [19th century], compared to only 4.5 per cent after 1914".
  - Source: Le Bris and Hautcoeur 2009 version (PSE).
- **UK, 1870-1907 (Grossman 2002)**
  - Timing: not stated. Full text was not reachable. Grossman's 2015 indices are
    end-of-January.
  - Market depth: not stated.
  - Source: Grossman 2015 (Wesleyan WP 2014-001).
- **UK, 1908-1963 (Barclays)**: timing not stated; depth broad (the largest 30).
- **Switzerland, 1900-1925 (Moore)**
  - Timing: year-end, with 1914-16 non-calendar. "for 1914 the December 1913-July 1914
    return, for 1915 the July 1914-July 1916 return".
  - Market depth: not stated.
  - Source: JST paper, footnote 22.
- **Switzerland, 1926-1959 (Pictet / Raetzer)**
  - Timing: year-end. "valeurs de l'indice ... relevées à la fin des années étudiées".
  - Market depth: broad. "50 titres cotés à Zurich et choisis au hasard".
  - Source: Pictet 1998 study, reprint.
- **Spain, 1927-1940 (Madrid, BdE archive)**
  - Timing: year-end, with 1937-40 interpolated. "we take the prices of securities in
    end-1936 and end-1940".
  - Market depth: not stated.
  - Source: JST paper, footnote 22.
- **Spain, 1900-1926 (Moore) and 1941- (IGBM)**: timing not stated; depth not stated.
- **Germany, 1870-1889 and 1914-1959 (Ronge)**
  - Timing: year-end. The index runs "ab Ultimo 1870 bis Ultimo 1959" on weekly weekend
    closes, with annual horizons "bei Desinvestition zum Jahresende".
  - Market depth: broad. "30 Standardwerten" by market cap. No trading July 1914 to Nov 1918;
    price freeze 1943-1948.
  - Source: Ronge 2002 (HISTAT ZA 8281 excerpt).
- **Germany, 1890-1913 (Eube)**
  - Timing: not stated for the annual figure. Prices are "in der Regel Monatsendwerte", from
    actual trades only.
  - Market depth: broad. 415 titles; replaced missing prices at most 1%, and Eube notes they
    add autocorrelation.
  - Source: Eube 1998 (HISTAT ZA 8467, OCR).
- **Sweden, 1871-1890 (Aurell lists)**
  - Timing: not stated ("bi-monthly prices").
  - Market depth: thin. "Trading activity was quite low ... 10 to 30 [firms] in the 1870s".
  - Source: Waldenström 2014 (IFN WP 1027).
- **Sweden, 1891-1901 (ten most traded)**
  - Timing: year-end. "year-end market prices ... were collected".
  - Market depth: thin (ten stocks).
  - Source: same.
- **Sweden, 1902-2002**
  - Timing: year-end. "the market value of listed stocks at the end of the measurement
    period".
  - Market depth: not stated.
  - Source: same.
- **Belgium, 1870-2015 (SCOB)**
  - Timing: not stated ("gathered on a monthly basis").
  - Market depth: thin to 1914. "many stocks on the BSE ... did not trade very frequently".
  - Source: Annaert and Van Hyfte 2006; Annaert 2010.
- **Norway, 1881-1920 (JST Oslo microdata)**
  - Timing: not stated.
  - Market depth: thin. "monthly quotations of 22 shares" in 1881, 82 by 1913.
  - Source: Klovland 2004, ch. 8 (same exchange lists).
- **Norway, 1921-2000 (Klovland)**
  - Timing: year-end. "the latest bid price of the month"; JST matches Dec-Dec
    (jst-autocorr-1).
  - Market depth: not stated.
  - Source: Klovland 2004.
- **Finland, 1895-1912 (Poutvaara)**
  - Timing: not stated for the annual figure ("last monthly bid price").
  - Market depth: thin. "quotations for three banks".
  - Source: Nyberg and Vaihekoski (EFMA 2009).
- **Finland, 1913-1990 (Nyberg and Vaihekoski)**
  - Timing: not stated for the annual figure ("from month-end to month-end").
  - Market depth: broad (53 series a month on average). Closures got zero returns.
  - Source: same.
- **Denmark, 1873-1900 (Green)**: timing not stated; depth not stated.
- **Denmark, 1901-1913 (yearbook selection)**
  - Timing: not stated. The yearbook gives "den første Notering i hver Maaned" (the first
    quotation of each month).
  - Market depth: thin ("selection").
  - Source: Statistisk Aarbog 1914.
- **Denmark, 1914-1922 and 1923-1999 (LoN / UN / IMF)**: timing not stated; depth not stated.
  Nielsen-Risager's own returns run December to December, but JST takes its price index
  elsewhere.
- **Netherlands, 1900-1995 (Eichholtz, Koedijk and Otten)**: timing not stated ("details from
  the authors on request"); depth not stated; 1944-46 non-calendar.
- **Italy, all sources**: timing not stated. Genova 1870-1887 is "selected stocks" (thin);
  the other sources' depth is not stated.
- **Japan, 1882-1940 (Fujino and Akiyama)**: timing not stated; depth not stated; weighted by
  clearing volumes.
- **Portugal, 1870-1987 (JST Lisbon microdata)**: timing not stated; depth not stated;
  1975-77 interpolated.

Blocked or unavailable (each fetched once, never evaded):
- Cambridge Core (Annaert et al. 2011, Grossman 2002, Moore);
- the NBER appendix PDF (403);
- CEPR RePEc (403);
- core.ac.uk (403);
- HAL (bot challenge);
- econstor (bot challenge);
- BoF and utupub (403);
- CESifo (challenge);
- the Atlanta Fed Grossman PDF (404);
- FRED fredgraph (timed out).

## Logged

`tries.md`: six `note` rows, idea `jst-autocorr-2`: the pooled acf, the four flag splits and the
usability tally. No strategy try, nothing selectable. Downloads in this lane: about 6 MB for the
BoE monthly CSV plus about 53 MB of source PDFs and their text (local cache only; the JST
documentation copies came from jst-autocorr-1's cache, not re-fetched).
