# Lane `inv`: investors with proven records, what they DID about bubbles, exits and cash

Lane of the exit-plan-2026 research (night lead, 2026-11-18). Research only, no advice to trade.

Rules used here:

- **Action** = documented in a filing, an annual letter, audited/reported fund returns, or reported
  by reputable press at the time (13F, Berkshire letters, fund NAVs). **Talk** = forecasts,
  interviews, memos. Verdict per investor: *action-backed*, *mixed*, or *talk only*.
- Every fact has a source. "(unverified)" = from memory or one weak source; do not rely on it.
- Events after the model's knowledge cutoff (mid-2026) were checked on the web on 2026-11-18.
- Numbers computed here come from `research/exit-plan-2026/scripts/inv_drawdowns.py` and
  `inv_burry_check.py` (Yahoo daily closes, fetched 2026-11-18; price only).

**Market context, 2026-11-18.** On 2026-11-05 the S&P 500 fell 4.4% in a day (worst since April
2025) and the Nasdaq 5.5%, leaving the Nasdaq >10% below its 2026-10-06 record
([AP via Boston.com, 2026-11-05](https://www.boston.com/news/national-news/2026/11/05/a-brutal-sell-off-for-ai-stocks-sends-wall-street-reeling-and-the-sp-500-tumbles-4-4/)).
Nvidia closed at 155.46 on 2026-11-17, down 35% from its 2026-10-06 close of 239.24 (script).
The S&P closed at 7,340.53 on 2026-11-17, less than 10% below its high (script). Whether this is
"the pop" is unknowable today; this lane is about rules, not about this call.

---

## Summary table

| Investor | What they did (documented) | Outcome | Verdict |
|---|---|---|---|
| Buffett / Berkshire | Avoided tech 1998-2000; cash built from lack of bargains; deployed 2008; sat out 2020; net seller 2023-25 | 1999 -19.9% vs S&P +21.0%, then +30% vs -38% over 2000-02 | action-backed |
| Grantham / GMO | Underweight US/tech from ~1997; out of growth before 2000 and 2007 | Right in the end, but lost ~35% of assets 1998-2001; many later calls early or wrong | mixed |
| Howard Marks / Oaktree | "bubble.com" Jan 2000; cut risk 2005-07; deployed heavily in late 2008 | Strong distressed returns after 2008 (unverified numbers) | action-backed |
| Druckenmiller | Bought $6bn tech near the March 2000 top; Nvidia long 2022-24, sold 2024 | Lost ~$3bn and left Soros 2000; sold Nvidia "too early", called it "a big mistake" | mixed |
| Klarman / Baupost | Cash as residual of bottom-up search, often large | 2008 roughly -7% to -13% (unverified) | action-backed (but private) |
| Templeton | Shorted ~84 dot-com stocks timed to IPO lockup expiries, 1999-2000 | Reported large profit (amount unverified) | action-backed (book source) |
| Robertson / Tiger | Refused tech, closed Tiger 2000-03-30 | Lost assets $22bn -> $6bn before the top; vindicated only after closing | mixed |
| Burry | 2005-08 MBS CDS; then repeated crash calls (2015-2023); 2025 AI puts | 2008 huge win; 2023 index puts lost; 2025 puts: direction partly right, P&L unknown | mixed |
| Hussman | Hedged most of the time since ~2009 | Fund ~-1.5% to -4.4%/yr over 10 years while S&P compounded strongly | talk + costly action |
| Dalio / Bridgewater | Pure Alpha +9.4% in 2008; "cash is trash" Jan 2020 | Pure Alpha II ~-20% in early 2020 | mixed |
| Shiller (+Greenspan) | Valuation warning Dec 1996 | S&P doubled to 2000; 2002 trough still above Dec-1996 level | talk (right long-run, early) |

---

## 1. Warren Buffett / Berkshire Hathaway

### Documented actions

| Date | Action | Source |
|---|---|---|
| 1969-05-29 | Announces he will wind up the Buffett Partnership: "I am not attuned to this market environment" and will not spoil a decent record playing a game he does not understand. Liquidation procedure in the 1969-10-09 letter (recommends Bill Ruane); cash distributions from ~1970-01; the 1973-74 crash (S&P ~-48%) came 3-4 years later. Note: he quit managing others' money, he did not short or time the market. | [GuruFocus transcription](https://gurufocus.com/news/6620/warren-buffett-partnership-letter-in-may-1969); [Novel Investor](https://novelinvestor.com/notes/buffett-partnership-letters-by-warren-buffett/); J. Miller, *Warren Buffett's Ground Rules* (2016) |
| 1998-2000 | Avoids tech completely. BRK-A falls 48.9% from $80,900 (June 1998) to $41,300 on 2000-03-10, the day the Nasdaq peaked. Barron's 1999-12-27: "What's Wrong, Warren?" | [Inc.](https://www.inc.com/phil-rosen/berkshire-hathaway-warren-buffett-warning-sign-stock-market/91436294) |
| 1999-2002 | BRK market value per share **1999 -19.9% vs S&P +21.0%** (worst relative year ever); then **2000 +26.6% vs -9.1%, 2001 +6.5% vs -11.9%, 2002 -3.8% vs -22.1%**: 2000-02 about **+30% vs -38%**. | [Berkshire 2024 letter, table p.15](https://www.berkshirehathaway.com/letters/2024ltr.pdf) |
| 2008-09 | Deploys cash into the crisis: $14.5bn of high-yield fixed income with equity kickers from Wrigley, Goldman Sachs and GE ("I had to sell portions of some holdings that I would have preferred to keep"); BNSF announced 2009-11-03. Mistakes in the same year: bought ConocoPhillips "when oil and gas prices were near their peak", costing "several billion dollars"; $244m in two Irish banks written down 89% by year-end. Pledge: "always run Berkshire with more than ample cash". | [Berkshire 2008 letter, p.~17](https://www.berkshirehathaway.com/letters/2008ltr.pdf) |
| 2008 | BRK **-31.8% vs S&P -37.0%**; 2009 +2.7% vs +26.5% (lagged the rebound). Peak-to-trough BRK-B **-53.9%** (2007-12-10 to 2009-03-05) vs S&P -56.8%. | [2024 letter table](https://www.berkshirehathaway.com/letters/2024ltr.pdf); script |
| 2020 | Sells all airline stocks (disclosed at the 2020-05-02 meeting); does NOT deploy the cash pile in the crash (the Fed acted first). 2020 BRK +2.4% vs S&P +18.4%. | 2024 letter table; 2020 AGM (unverified link) |
| 2024 | Large net seller (Apple, Bank of America). Marketable equities fall from $354bn to $272bn during 2024. | [2024 letter, p.~8](https://www.berkshirehathaway.com/letters/2024ltr.pdf) |
| 2025 | Cash record ~$382bn at 2025-09-30; 12th straight quarter of net stock selling. Buffett steps down as CEO at end-2025; Greg Abel CEO from 2026. | [Fortune, 2025-11-01](https://fortune.com/2025/11/01/warren-buffett-stocks-net-selling-berkshire-hathaway-q3-earnings-investment-portfolio-cash/) |
| 2026-02-28 | Abel's first letter (Buffett stays chairman): year-end 2025 cash and T-bills ~$373bn; cash pile "not a retreat from deal-making", a strategic asset to act "when others are fearful"; Abel manages the stock portfolio himself. | [AP via NY1, 2026-02-28](https://ny1.com/nyc/all-boroughs/ap-top-news/2026/02/28/warren-buffetts-successor-greg-abel-publishes-his-first-letter-to-berkshire-hathaway-shareholders); [Irish Times, 2026-02-28](https://www.irishtimes.com/business/2026/02/28/greg-abel-tells-berkshire-hathaway-investors-its-cash-pile-is-not-a-retreat-from-deal-making/) |
| 2026 Q2 | Under Abel: net BUYER of ~$19.8bn of stocks, ending 14 quarters of net selling; cash ~$365bn at 2026-06-30. | [investinglive](https://investinglive.com/Education/berkshire-s-cash-pile-starts-moving-under-greg-abel-learn-the-lessons-behind-the-news/), [247wallst, 2026-08-08](https://247wallst.com/investing/2026/08/08/berkshire-hathaway-just-did-something-it-hasnt-done-in-more-than-3-years/) |
| 2026 Q3 | Small net seller (~$0.4bn) but net buyer of >$11bn over 9 months; buybacks of its own stock $9.6bn in Q3 (>$14bn in 2026). Cash ~$357bn net of unsettled T-bill purchases (AP: $377bn gross). | [Kiplinger](https://www.kiplinger.com/investing/stocks/stocks-berkshire-hathaway-bought-sold-q3-2026), [AP via NY1, 2026-11-07](https://ny1.com/nyc/all-boroughs/ap-top-news/2026/11/07/berkshire-hathaway-buys-back-96-billion-of-its-own-stock-but-its-profits-declined) |

### Talk (dated)

- 2025-02-22 letter: "Despite what some commentators currently view as an extraordinary cash
  position at Berkshire, the great majority of your money remains in equities." and "Berkshire will
  never prefer ownership of cash-equivalent assets over the ownership of good businesses"
  ([2024 letter](https://www.berkshirehathaway.com/letters/2024ltr.pdf)). The cash pile is a
  by-product of finding nothing cheap, not a market forecast.
- 2009-02 letter (on 2008): "neither Charlie Munger ... nor I can predict the winning and losing
  years in advance. (In our usual opinionated view, we don't think anyone else can either.)" and a
  shambles economy "does not tell us whether the stock market will rise or fall"
  ([2008 letter, p.3](https://www.berkshirehathaway.com/letters/2008ltr.pdf)).
- 2008-10-16, NYT op-ed "Buy American. I Am.": his personal account would soon be wholly in US
  stocks if prices stayed attractive; "if you wait for the robins, spring will be over"
  ([NYT](https://www.nytimes.com/2008/10/17/opinion/17buffett.html), paywalled; wording via
  [domain-b, 2008-10-20](https://domain-b.com/investments/world_markets/20081020_warren_buffett.html)). The S&P closed at 946 that day and fell another **28.5%** to 676.5 on
  2009-03-09 (script): early by about five months, right over years.
- 1986 letter: "be fearful when others are greedy and greedy only when others are fearful"
  ([1986 letter](https://www.berkshirehathaway.com/letters/1986.html)).

### Verdict: **action-backed**, with the cost of being early documented. He never sold everything
to wait for a crash. Cash built up because he found nothing cheap, and he spent it only when
prices were plainly cheap (2008), or not at all (2020). In 1999 he was early by over a year and
paid with a -20% year against a +21% market.

### Berkshire as a "defensive holding" (for parking)

Computed from daily closes (script; price only):

| Episode | BRK-B peak-to-trough | S&P 500 peak-to-trough |
|---|---|---|
| Dot-com (BRK-A, June 1998 to 2000-03-10) | -48.9% (Inc.) | S&P rose in this window |
| Dot-com 2000-2002 | -24.7% (Jan to Mar 2000, then recovered) | -49.1% (2000-03-24 to 2002-10-09) |
| GFC 2007-2009 | **-53.9%** | -56.8% |
| COVID Feb-Mar 2020 | -29.4% | -33.9% |
| 2022 bear | **-26.6%** (2022-03-28 to 10-12) | -25.4% |
| Tariff shock Feb-May 2025 | -8.8% | -18.9% |
| 2026 to 2026-11-17 | -8.4% | -9.1% |

Beta of BRK-B to the S&P (daily returns): 0.66 over 2000-2025, 0.81 over 2016-2025 (script).
2026 year to 2026-11-17: BRK-B +16.7%, S&P +7.2% (script).

Reading: in a **slow, valuation-driven bust** (2000-02) Berkshire was an excellent hedge. In a
**liquidity crash** (2008, 2020) it fell almost as much as the market (-54% vs -57%). Calendar-year
numbers (2008: -31.8%) understate this. It is a lower-beta stock, not a safe place: unsuitable as
the "crash-safe" bucket for money that must keep its value through a 6-week window or a sharp crash;
reasonable as a lower-AI-exposure equity holding for someone who would otherwise hold the index.
New risks: Buffett no longer CEO since 2026, a large Apple stake, insurance cat losses.

---

## 2. Jeremy Grantham / GMO

### Method
GMO defines a bubble as a price more than **2 standard deviations above the long-term real price
trend** (a "superbubble" at 3 sigma); on a normal curve a 2-sigma event is about once in 44 years,
in GMO's sample of 330 cases about once in 31 years; Grantham calls the threshold arbitrary
([Outlook Business](https://www.outlookbusiness.com/perspective/looking-at-bubbles-the-statistical-way-936)).
He claims all major 2-sigma equity bubbles eventually returned to trend (28 of 28, per a 2015 talk,
[Advisor Perspectives](https://www.advisorperspectives.com/articles/2015/06/29/grantham-stocks-will-continue-upward-until-the-election)).
Note the claim is about *eventually*, with no timing.

### Documented actions and results

| Date | Action / result | Source |
|---|---|---|
| 1997-2000 | Underweight US growth/tech ("by the end of 1998, we were as light as we could get"). Core EAFE portfolios ~14.9%/yr in 1998-99 vs index 25.9%. **GMO assets fell from ~$31bn (mid-1998) to ~$20bn (mid-2001)**; Exxon Mobil and Bechtel among clients that fired GMO in 2000. Afterwards value beat growth strongly and those who stayed were rewarded. | [Institutional Investor](https://www.institutionalinvestor.com/article/b1hjlb0qs4c807/GMO-Is-Feeling-Pain-Reminiscent-of-the-Late-1990s); [MoneyWeek](https://moneyweek.com/investments/jeremy-grantham-on-long-term-investing-in-a-short-term-market) |
| 2007 | April 2007 letter "It Is Everywhere, in Every Asset Class": a global bubble in all risk assets; GMO's asset-allocation funds were defensive into 2008. | GMO quarterly letter 2007 Q1 (link unverified) |
| 2010s-2020s | GMO's 7-year forecasts of US large-cap real returns near or below zero for much of 2013-2024, while the S&P compounded ~10%+ a year; GMO's 2019 letter says the value underperformance lasted over 10 years against 5 in the late 1990s. | [GMO 3Q 2019 letter](https://www.gmo.com/americas/research-library/3q-2019-gmo-quarterly-letter); forecast-vs-outcome numbers unverified |

### Talk (dated)

- 2021-01-05 "Waiting for the Last Dance": US market a superbubble. S&P that day 3,727; it rose
  to 4,797 (2022-01-03, +29%), then fell to 3,577 (2022-10-12): only **4% below** his call date,
  and by 2026-11-17 it was 7,341, **+97%** from the call (script).
- 2022-01-20 "Let the Wild Rumpus Begin": superbubble deflating
  ([GMO PDF](https://www.gmo.com/globalassets/articles/viewpoints/2022/gmo_let-the-wild-rumpus-begin_1-22.pdf)).
  Right about 2022 (-25%); wrong that it would go far lower.
- 2026-01-28 GMO "Valuing AI: Extreme bubble, new golden era, or both" (with Edward Chancellor)
  ([GMO](https://www.gmo.com/americas/research-library/valuing-ai-extreme-bubble-new-golden-era-or-both/)).
  2026-01: "slim to none" chance the AI bubble does not burst
  ([ThinkAdvisor, 2026-01-20](https://www.thinkadvisor.com/amp/2026/01/20/jeremy-grantham-slim-to-none-chance-ai-bubble-wont-burst/)).
  2026-06: expensive AI names could fall ~70% (Diary of a CEO, via secondary reports, unverified).

### Verdict: **mixed**. 2000 and 2007-08 calls were acted on and right, but early, and cost GMO a
third of its assets. Since 2013 his US-equity views have mostly been early or wrong, and an
investor following his 2021 "superbubble" call would have missed a near doubling. The 2-sigma rule
says *what* is a bubble, not *when* it ends.

---

## 3. Howard Marks / Oaktree

### Documented actions
- 2000-01-03 memo "bubble.com": warned on tech/internet valuations two months before the Nasdaq top
  ([Oaktree memo archive](https://www.oaktreecapital.com/insights/memos); date and title well
  documented, wording not rechecked here). Oaktree did not invest in tech; its business is credit,
  so this is a view, not a trade.
- 2005-2007: warned of loose credit ("The Race to the Bottom", 2007-02; caution in 2005-07 is
  Marks' own account, details unverified). In 2008 raised a $10.9bn distressed fund (OCM
  Opportunities Fund VII(b), the largest ever per Preqin) and, per Oaktree, invested **~$600m a
  week in the last 15 weeks of 2008** after Lehman; profit figures differ by source
  ([Oaktree, "Commemorating 25 years"](https://www.oaktreecapital.com/insights/insight-commentary/education/commemorating-25-years-of-mastering-the-market-cycle);
  [Institutional Investor](https://www.institutionalinvestor.com/article/b150qfyrndkrzm/howard-marks-the-distressed-debt-king);
  [Business Insider](https://businessinsider.in/howard-marks-made-billions-piling-into-the-market-at-the-depths-of-the-financial-crisis-heres-why-hes-continuing-to-buy-now-and-what-it-would-take-for-him-to-stop/articleshow/66148612.cms)).
  Note: they bought from September 2008, well before the March 2009 low.
- He describes the method as **"taking the temperature" of the market** with a checklist of
  investor behaviour (eager vs reluctant lenders, easy vs hard capital, high vs low valuations,
  "it's different this time"), and moving the risk dial gradually, not all-in/all-out
  (*The Most Important Thing*, 2011, ch. "Knowing where we stand" / "Calibrating"; page unverified).

### Talk (dated)
- 2025-01-07 memo "On Bubble Watch": US stocks expensive (S&P forward P/E ~22) but not a full
  bubble outside some areas (Oaktree site; wording not rechecked).
- **2025-12-09 memo "Is It a Bubble?"** (read in full): "If that enthusiasm doesn't produce a bubble
  conforming to the historical pattern, that will be a first." Bottom line: "no one should go all-in
  without acknowledging that they face the risk of ruin if things go badly. But by the same token,
  no one should stay all-out and risk missing out on one of the great technological steps forward.
  A moderate position, applied with selectivity and prudence, seems like the best approach." Also
  flags debt financing of the build-out as the new amplifier
  ([Oaktree PDF](https://www.oaktreecapital.com/docs/default-source/memos/is-it-a-bubble.pdf)).

### Verdict: **action-backed**. Marks never calls tops; he scales risk with a behavioural checklist
and keeps capital to deploy when others must sell. His AI advice is explicitly neither all-in nor
all-out.

---

## 4. Stanley Druckenmiller

| Date | Action / result | Source |
|---|---|---|
| 1999-2000 | Short tech in 1999, lost, flipped; in March 2000 bought ~$6bn of tech near the top; within ~6 weeks lost ~$3bn and left Soros (April 2000). Quantum -21.7% in 2000 to that point. In his words he was "an emotional basket case" who knew he should not chase. | [Quartr](https://quartr.com/insights/investment-strategy/stanley-druckenmiller-breaking-the-bank); [WSWS 2000 (citing WSJ)](https://www.wsws.org/en/articles/2000/05/soro-m05.pdf); sizes differ between sources |
| 1981-2010 | Duquesne Capital: no losing year, ~30%/yr average (widely reported; audited numbers not public, unverified). | [MoneyWeek](https://moneyweek.com/441992/the-worlds-greatest-investors-stanley-druckenmiller) |
| 2022-2024 | Nvidia top holding of his family office (~$400m in 2022); sold in 2024 (fully out by Q3 2024, 13F) at ~$800-950 pre-split because "it tripled in a year, and I thought the valuation was stretched". 2024-10: "I own none today... It was a big mistake." | [Fortune, 2024-10-18](https://fortune.com/2024/10/18/billionaire-investor-druckenmiller-sold-nvidia-regrets-huang-musk-ellison/) |
| 2025-2026 | 13Fs: exited Palantir; Q1 2026 new stakes in Broadcom, Intel, Arm (13F reading by Motley Fool). | [Fool, 2026-05-24](https://fool.com/investing/2026/05/24/why-billionaire-stanley-druckenmiller-dumped-nvidi/) |

### Verdict: **mixed**. One of the best records ever, yet he chased the 2000 top (lesson: FOMO
hits professionals) and sold Nvidia far too early on valuation alone (lesson: valuation is not a
timing signal). He is a trader who changes his mind fast; copying 13Fs (45 days stale) is useless.

---

## 5. Seth Klarman / Baupost

- *Margin of Safety* (1991): buy only with a margin of safety; holding cash when nothing qualifies
  is acceptable; avoid leverage. Out of print, sells for $1,000+ used (paid source, not bought).
- Baupost letter (2009, quoted): cash balances "are determined not from any top-down asset
  allocation decision, but as a residual of our bottom-up search for investment opportunity"
  ([distressed-debt-investing.com quoting the letter](https://www.distressed-debt-investing.com/2009/12/wisdom-from-seth-klarman-part-6.html?m=1)).
- Reopened to new money in early 2008, gathered ~$4bn and deployed it in the crash; 2008 return
  roughly -7% to -13% (secondary sources, unverified); returned ~5% of capital to investors at
  end-2010 when bargains were scarce; often 30-50% in cash
  ([Fool, 2010-11-11](https://www.fool.com/investing/general/2010/11/11/klarman-finds-opportunities-scarce.aspx);
  [Wikipedia](https://en.wikipedia.org/wiki/Seth_Klarman)).

### Verdict: **action-backed**, but letters are private, so numbers are second-hand. The key rule:
cash is what is left after you cannot find bargains, never a bet on a crash date.

---

## 6. Sir John Templeton

- 1999-2000: shorted ~84 Nasdaq stocks (sources say 80-88), ~$2.2m each, timed to start ~11 days
  before each IPO **lockup expiry** (insiders free to sell); covered quickly when a stock rose. He
  called the valuations "insane"
  ([Investing.com citing Forbes](https://m.investing.com/analysis/when-the-unicorns-become-horses-again--tech-bubble-repeats-200470464?ampMode=1);
  L. Templeton & S. Phillips, *Investing the Templeton Way*, 2008, described by
  [Redwheel](https://www.redwheel.com/at/de/professional/?p=1694)). Profit reported as large
  (~$90m often quoted, **unverified**).
- Mechanism backed by research: Internet stocks fell up to 33% over six months relative to the
  index around lockup ends (Ofek & Richardson, "DotCom Mania", J. Finance 2003,
  [NBER w8630](https://www.nber.org/papers/w8630)).
- Talk: "Bull markets are born on pessimism, grow on skepticism, mature on optimism and die on
  euphoria" (1994 Templeton Foundation maxims; widely quoted, page unverified).

### Verdict: **action-backed** (single book-and-press source for the size). Note the method: a
specific supply trigger (insider selling), many small positions, cut losers fast. Not a call on
the index top.

---

## 7. Julian Robertson / Tiger Management

- Refused to own tech in 1998-2000; Tiger assets fell from ~$21-22bn (1998) to ~$6bn by March 2000
  through losses and redemptions. On **2000-03-30** he told investors he would return all capital
  and close the funds, blaming the Internet craze; he said he no longer understood the market
  ([CNN Money, 2000-03-30](https://money.cnn.com/2000/03/30/mutualfunds/q_funds_tiger/);
  [Globe and Mail](https://www.theglobeandmail.com/report-on-business/wizard-of-wall-street-hangs-up-his-hat/article25459132/);
  [InvestmentNews](https://www.investmentnews.com/alternatives/hedge-fund-guru-julian-robertson-dies-at-90/225681);
  letter text at [HedgeFundAlpha](https://hedgefundalpha.com/investor-letters/archives-julian-robertson-closing-letter-investors/)).
- The Nasdaq had peaked on 2000-03-10, twenty days before; his value stance was vindicated
  over 2000-2002, but Tiger was already closed.

### Verdict: **mixed**. Right about the bubble, ruined by being early: he gave up three weeks
after the top. Lesson: if your plan only works if the top comes soon, the plan can break you first.

---

## 8. Michael Burry / Scion

| Date | Action / result | Source |
|---|---|---|
| 2005-2008 | Bought CDS on subprime mortgage bonds; Scion returned ~489% net from Nov 2000 to June 2008 vs ~3% for the S&P. Investors had tried to redeem in 2006-07 while the trade bled premium. | M. Lewis, *The Big Short* (2010) (figure widely quoted, page unverified) |
| 2015-2022 | Repeated public crash/bubble warnings (index funds as a bubble 2019, "Mother of all crashes" 2021, Tesla short 2021); mostly not followed by the predicted crash on his timetable. | press (unverified detail) |
| Jan-Mar 2023 | Tweeted "Sell" in Jan 2023; later said he was wrong to say sell. | [etf.com](https://www.etf.com/sections/news/michael-burry-makes-new-bet-against-blackrocks-soxx) |
| Q2-Q3 2023 | 13F: puts on SPY (~$886m notional) and QQQ (~$739m notional) at 2023-06-30; closed by 2023-09-30 with indexes only modestly lower: likely a loss. Notional ≠ money at risk (Scion AUM ~$238m). | [Fool, 2023-08-16](https://www.fool.com/investing/2023/08/16/big-short-michael-burry-16-billion-against-stock); [Market Rebellion](https://marketrebellion.com/news/no-michael-burry-didnt-risk-93-of-his-portfolio-on-put-options) |
| 2025-09-30 | 13F: puts on Nvidia (~$187m notional) and Palantir (~$912m notional; Burry says he paid ~$9.2m premium). Public thesis: hyperscalers stretch server depreciation lives, understating depreciation by ~$176bn over 2026-28. | [Fortune, 2025-11-04](https://fortune.com/2025/11/04/big-short-investor-michael-burry-nvidia-palantir-puts-alex-karp/); [techstrong.ai](https://techstrong.ai/features/tech-investor-michael-burry-alleges-accounting-irregularities-at-hyperscalers-in-pursuit-of-ai-boom/) |
| 2025-11-10 | Scion's SEC registration terminated; stops managing outside money ("I am still running my money"); launches paid Substack. | [CP24/Reuters, 2025-11-13](https://www.cp24.com/news/money/2025/11/13/investor-michael-burry-of-big-short-fame-deregisters-scion-asset-management/); [Hedgeweek](https://www.hedgeweek.com/burry-still-active-in-markets-after-scion-de-registration/) |
| 2025-09-30 to 2026-11-17 | Palantir: 182.42 -> low 107.27 (2026-06-25, -41%) -> high 209.05 (2026-10-09, +15%) -> 156.56 (-14%). Nvidia: 186.58 -> high 239.24 (2026-10-06, +28%) -> 155.46 (-17%). Direction right so far, with violent swings both ways; strikes, expiries and P&L are not public. | script (Yahoo closes) |

### Verdict: **mixed**. One historic, documented win (2008), many public alarms that did not pay
on his timetable. A permanent bear eventually looks right once; that is not a timing record.
His 2025 AI shorts cannot be scored yet; option P&L depends on strikes and expiries we cannot see.

---

## 9. John Hussman / Hussman Funds

- Hussman Strategic Growth Fund (HSGFX) was hedged against market risk most of the time from ~2009
  on, on valuation grounds, repeatedly forecasting large losses. 10-year annualised return roughly
  **-1.5% to -4.4%** depending on the as-of date, while the S&P 500 compounded strongly over the
  same years; assets fell from ~$5.2bn (2009) to ~$0.34bn
  ([Yahoo Finance HSGFX](https://finance.yahoo.com/quote/HSGFX/performance?p=HSGFX);
  [Zacks, as of 2024-06-30](https://zacks.com/funds/mutual-fund/quote/HSGFX/performance);
  [InvestmentNews 2009](https://www.investmentnews.com/mutual-funds/john-hussman/24069)).
- His valuation work (market cap / gross value added) may be right about low 10-12-year returns,
  but acting on it as a timing signal destroyed most of his investors' opportunity.

### Verdict: the **cost of a permanent bear**, documented in a public mutual fund's NAV.

---

## 10. Ray Dalio / Bridgewater

- 2008: Pure Alpha **+9.4%** while the S&P lost 37% (Bridgewater had warned of a debt crisis).
  2019: -0.5%.
- 2020-01-21, Davos: "cash is trash"; Pure Alpha II then lost ~20% by March 2020 and was down
  18.6% as of August 2020; Dalio: "we should have made money rather than lost money in this move
  the way we did in 2008"
  ([Institutional Investor](https://www.institutionalinvestor.com/article/b1jsw5lw26ncfq/In-Disappointing-Year-Bridgewater-s-Flagship-Fund-Returns-0-5);
  [Fortune, 2020-09-15](https://fortune.com/2020/09/15/the-losses-continue-to-pile-up-for-hedge-fund-king-ray-dalio/);
  [Business Insider](https://businessinsider.in/finance/news/ray-dalio-was-blindsided-by-the-coronavirus-market-rout-and-now-his-flagship-fund-is-down-20-this-year/amp_articleshow/74658093.cms)).

### Verdict: **mixed**. A systematic macro process caught a slow debt crisis (2008) and missed a
sudden shock (2020). Shocks are not forecastable even by the largest macro shop.

---

## 11. Robert Shiller and "irrational exuberance" (1996)

- 1996-12-03: Shiller and John Campbell presented their valuation (CAPE) evidence to the Fed board;
  1996-12-05: Greenspan's "irrational exuberance" speech
  ([Fed speech text](https://www.federalreserve.gov/boarddocs/speeches/1996/19961205.htm);
  Shiller, *Irrational Exuberance*, 2000, preface; page unverified).
- S&P 500 close 1996-12-05: **744.38**. It then rose to **1,527.46** (2000-03-24, +105%) and the
  2002-10-09 trough was **776.76**, still **above** the warning-day level (script). Someone who sold
  on the warning and bought back at the exact 2002 bottom would have done slightly worse than
  holding (before dividends and interest).
- Shiller's book came out in March 2000, at the top: the valuation case was right in the end,
  but 3+ years early.

### Verdict: **talk**, right about long-run returns, useless as a sell date.

---

## 12. Evidence on professional market timers overall

- **Graham & Harvey (1996)**, 237 newsletters, 1980-1992: no evidence that letters raise equity
  weights before rises or cut them before falls; only a few beat a buy-and-hold mix of the same
  volatility; letters called direction correctly ~49% of the time before rises
  (J. Financial Economics 42(3):397-421; [NBER w4890](https://www.nber.org/papers/w4890);
  [Duke](https://scholars.duke.edu/publication/774086)).
- **Hulbert Financial Digest** data (Kumar & Pons, 1980-2001): ~20-40% of timing letters beat
  buy-and-hold risk-adjusted, depending on method; but winners rarely repeat: the top 20 timers of
  the 2000-02 bear did no better than average in 2007-09; the best timers mostly *reduced
  volatility* (~25% less) rather than adding return
  ([CXO Advisory](https://www.cxoadvisory.com/investing-expertise/classic-papers-the-value-of-investment-newsletters/);
  [Validea, Hulbert](https://blog.validea.com/?p=11804)).
- Mutual fund timing: classic studies (Treynor & Mazuy 1966; Henriksson 1984; Becker, Ferson,
  Myers & Schill 1999, J. Financial Economics) found little or no aggregate timing ability among
  fund managers (citations from memory, unverified details).
- Sharpe (1975, Financial Analysts Journal, "Likely Gains from Market Timing"): a timer switching
  annually between stocks and cash needs to be right roughly 3 times in 4 just to match buy-and-hold
  (from memory, unverified exact figure).

---

## Cross-investor lessons (rules, not predictions)

1. **Nobody with a documented record times tops to the month.** Buffett was 1+ year early (1999),
   Grantham 2-3 years (1997-2000), Robertson quit 3 weeks after the top, Shiller/Greenspan 3+
   years early, Burry's 2023 call lost. The ones who were right also said explicitly they cannot
   time (Buffett, Marks, Klarman).
2. **Being early is expensive and can end you before you are proved right.** Tiger closed, GMO lost
   ~35% of assets, Hussman's fund shrank >90%, Berkshire had its worst relative year. Size any
   bubble bet so that being 1-3 years early is survivable.
3. **The winners scale, they do not flip.** Buffett let cash accumulate over years and net-sold
   gradually; Marks moves a risk dial with a temperature checklist; Klarman's cash is a residual.
   Marks' Dec 2025 AI advice: neither all-in nor all-out.
4. **Re-entry is where the money was made, and it needs prepared, unemotional rules.** Buffett
   2008, Oaktree and Baupost 2008 deployed into panic (and were early there too: Buffett's op-ed
   came 28.5% before the bottom). Several who called a top missed or fumbled re-entry
   (Robertson closed; Grantham/Hussman stayed bearish through 2009-2021 and 2023-2026 gains).
5. **Chasing kills even the best.** Druckenmiller bought $6bn of tech at the 2000 top out of FOMO
   and lost $3bn in six weeks; he also sold Nvidia too early on valuation. Valuation tells you
   expected long-run returns, not the date.
6. **Specific mechanical triggers beat general bubble talk.** Templeton's lockup shorts used a
   dated supply event; contrast Burry/Hussman's general bearishness.
7. **Shocks are not forecastable even by the best macro shops** (Dalio 2020). Crash protection for
   a short window must come from the asset itself (cash, short government bills), not from a call.

## Implications for a fixed-date exit playbook (small portfolio, sell window to 2026-12-31, re-entry planned)

- The sale is **forced by the calendar, not by a signal.** The investors above would say: do not
  turn a calendar-driven sale into a market-timing bet. Spread the sales over the window (e.g. in
  2-4 tranches) rather than waiting for a perfect indicator; this is the Buffett/Marks "scale,
  don't flip" rule and it caps the regret either way.
- **Parking money that must be crash-safe over weeks belongs in cash or short government bills /
  money-market funds**, not in Berkshire. Berkshire fell 54% in 2008-09 and 29% in Feb-Mar 2020
  (script); its strength is slow valuation busts (2000-02), not crashes.
- If you want some equity exposure while waiting, Berkshire is a reasonable *lower-beta,
  low-AI* holding (beta ~0.7-0.8, +16.7% vs S&P +7.2% in 2026 to 2026-11-17), but it should count as
  equity, not as the safe part.
- **Write the re-entry rule now**, before the drop (Marks/Buffett: deploy when others must sell):
  e.g. buy back in tranches at pre-set drawdown levels or dates, with a time stop so that "no pop"
  does not mean staying out for years (the Grantham/Hussman failure mode). Accept being early on
  re-entry too: Buffett and Oaktree were.
- Expect an AI-led sell-off, if it deepens, to be uneven: Nvidia is already -35% from its October high while
  the S&P is <10% off (2026-11-17). A broad-index re-entry plan does not need to hit the exact
  bottom; the Shiller 1996 case shows how much ground a warning can concede and still be beaten by
  holding.

## Could not verify (open items)

- 1969 partnership letter checked only via a transcription (GuruFocus); full NYT op-ed text
  (paywall).
- Templeton's profit (~$90m) and exact number of shorts.
- Oaktree 2008 profit (sources differ); Marks' 2005-07 de-risking details; "bubble.com" and
  "On Bubble Watch" wording (not re-read).
- Baupost cash levels and 2008 return (private letters).
- Druckenmiller 2000 trade size (sources say $6bn bought, ~$3bn lost; one source much smaller).
- Burry's 2025-26 option P&L (strikes/expiries not public), and his later 2026 positions.
- Mutual-fund timing study details and Sharpe (1975) figure (from memory).
- GMO 7-year forecast vs outcome numbers.
