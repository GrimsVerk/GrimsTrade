# A second bank with different IT, Netherlands, November 2026

Research, not financial advice. Researched 24 Nov 2026.

**The question.** Someone with a current account at one of the three large Dutch banks (ING, ABN
AMRO, Rabobank) wants a second bank so that one IT outage or one attack is unlikely to cut off both. The second
bank should be:
- safe;
- built on a technology stack as different as possible from the first bank's;
- cheap to keep.

ING is worked through in detail as the example; ABN AMRO and Rabobank facts are in section 3. The
same method applies with either of them as the first bank. The top two picks (Revolut, bunq) differ
from all three big banks in licence or ledger and cloud, so the conclusion barely changes.

**How to read it.** Facts carry a source and date. **UNVERIFIED** means the fact was seen only in a
search summary, on vendor marketing, or in a secondary source. Fees change, so check the bank's own
fee page.

## Summary

- **Most different from the big three (and ING in particular) while still safe and cheap: Revolut (Revolut Bank UAB, Lithuanian
  licence).** Every bank-specific layer (licence, ledger, cloud, supervisor) differs from ING's:
  - another country, supervisor and deposit guarantee scheme;
  - in-house core banking on Google Cloud;
  - in-house card processing (UNVERIFIED for today), where ING's cards are processed by Worldline.

  It still works like a Dutch account: NL IBAN, iDEAL, EUR 100k under the Lithuanian scheme.
  - Cost: Standard plan EUR 0 a year, plus about EUR 8 once for card delivery (UNVERIFIED).
  - Cash: 5 ATM withdrawals or EUR 200 a month free, then 2% (min EUR 1).
  - Weak points:
    - It runs on one cloud. On 20 Oct 2026 a Google Cloud outage (per Reuters a power event in
      London, europe-west2) left about 28 of its services partly unavailable.
    - It was fined for AML failings.
    - The guarantee is foreign: the Lithuanian scheme pays within 7 working days per its depositor
      sheet, with DNB as contact point and paying agent for branch customers under EU directive
      2014/49/EU art. 14(2). Cross-border payout is untested in practice.
- **Best Dutch-licensed alternative: bunq Core** (EUR 47.88 a year). Dutch deposit guarantee,
  in-house core on AWS, card processing in-house (2019 claim, UNVERIFIED for today).
  - Every ATM withdrawal costs money.
  - No credit rating and no CET1 figure found.
- **Safest conventional option with some difference: ASN Bank** (formerly de Volksbank). EUR 48 a
  year, with free euro ATM withdrawals and free note deposits at Geldmaat.
  - Ratings A/A2/A+; AWS cloud; a Visa Debit card.
  - It is a classic Dutch bank on the same Dutch rails as ING. Its card processor is unknown and
    may be ING's (Triodos shared ING's 2 May 2026 card outage), so its IT difference is weak until
    that is known.
- **Is a second account worth it?** At EUR 0 to 48 a year it gives a second EUR 100k guarantee and
  a second card, app and IBAN.
  - It does **not** protect against failures in rails every bank shares. The 16 May 2024 card
    outage hit 30-40% of shop card payments (ING, Rabobank and ABN AMRO named; one shared supplier,
    so likely all banks).
  - Geldmaat ATMs, iDEAL/Wero, SEPA clearing, TIPS and the Visa/Mastercard schemes are shared too.
  - For those, cash is the fallback. The DNB-chaired MOB advises EUR 70 per adult and EUR 30 per
    child at home for 72 hours and several payment methods; Rijksoverheid adds a debit card
    "possibly at different banks".

### Ranking for this purpose

Order: IT difference first, but a bank drops down when safety or everyday use is weak (BaFin
special monitor, DE IBAN, no iDEAL); then cost.

| # | Bank | Why | Cost per year |
|---|---|---|---|
| 1 | Revolut (LT licence, NL branch) | Most different stack and supervisor; NL IBAN, iDEAL, free cash allowance | EUR 0 (+ about EUR 8 card delivery once, UNVERIFIED) |
| 2 | bunq (NL) | Own core on AWS, own card processing, Dutch DGS | EUR 47.88 (Core); ATM from EUR 0.99 per withdrawal |
| 3 | ASN Bank (NL) | Strong ratings, Visa card, free cash and deposits; partly AWS | EUR 48 |
| 4 | Rabobank (NL) | Safest balance sheet (Aa3/AA-), but co-owns Geldmaat and is a classic big bank | EUR 43.20 (Standaard); EUR 0 only ages 18-27 |
| 5 | N26 (DE) | Different stack (Mambu core on AWS, 2016-17 vendor claim, UNVERIFIED now), but BaFin special monitor since Dec 2025, DE IBAN | EUR 0 (+ EUR 10 card, UNVERIFIED) |
| 6 | Trade Republic (DE) | Free, cheap cash from EUR 100, but a broker first, no iDEAL, cash in trust at partner banks (German, French, Irish schemes) and possibly money-market funds without guarantee (UNVERIFIED for the Dutch branch) | EUR 0 (+ EUR 5 card) |

Not a fit:
- ABN AMRO: IT closest to ING's, co-owns Geldmaat, EUR 51.60.
- Triodos: Fitch BBB, EUR 60, and its 2 May 2026 card outage was the same day and the same kind as
  ING's.
- Knab: EUR 72, and now an Austrian BAWAG branch that shares one EUR 100k with all BAWAG brands.
- Wise and Vivid: payment institutions, not banks, so no deposit guarantee.
- ING-DiBa: same group as ING.

**A combination that follows from this research** (not advice):
- Keep the first bank and add Revolut Standard at EUR 0.
- If the app offers a choice, order the card on the other scheme from the first bank's card.
- Keep the advised cash at home.
- If a Dutch deposit guarantee matters more than maximum IT difference, take bunq Core or ASN
  instead, for about EUR 48 a year.
- Keep only a buffer, not large balances, at a neobank.

## 1. One of the big three in detail: ING Netherlands

### Stack (public facts)

- **No mainframe.** ING NL switched its mainframe off after a seven-year programme (about 2022,
  inferred from "a farewell party about two years ago") and moved to a modular microservices architecture. No core-banking vendor is named (CIO interview,
  banken.nl, 12 Nov 2024):
  https://www.banken.nl/nieuws/25684/de-bank-in-je-broekzak-cio-edwin-entrop-over-het-innovatieve-dna-van-ing
- **Private cloud.**
  - ING Private Cloud ran about 30% of global infrastructure (ing.com, 2 Dec 2021):
    https://ing.com/news/2021/12/ing-invests-in-cloud-banking.html
  - About 68% of compute on its own VMware private cloud (2025 annual report via search snippet,
    UNVERIFIED).
  - VMware Cloud Foundation 9.0 chosen (Broadcom, 2 Dec 2025, UNVERIFIED).
- **Public cloud:** Azure, Google Cloud and Oracle Cloud for some workloads, for example a wholesale
  GenAI tool on Google Cloud. UNVERIFIED (trade press):
  https://evidentinsights.com/insights/articles/ing-genai-in-wholesale-banking (Aug 2025)
  - Retail core banking is not shown on public cloud.
- **Thought Machine:** ING invested in 2021. ING Bank Slaski (Poland) runs Vault for a loan
  product. No evidence that ING NL is migrating to Vault.
- **Card issuing processing:** Worldline, for ING NL, Belgium and Germany; the partnership is
  "over three decades" old (Worldline, 30 Jan 2023):
  https://worldline.com/en/home/top-navigation/media-relations/press-release/pr-2023_01_30_01.html
- **Card brand:** Maestro is being replaced by Debit Mastercard (iCulture, UNVERIFIED as the
  default for all customers).
- **Cheapest package:** ING Go, about EUR 4 a month (banken.nl, UNVERIFIED).

### Outages 2023-2026

| Date | What failed | Duration | Stated cause | Source |
|---|---|---|---|---|
| 1 Feb 2023 | App and internet banking (about 9M customers); card payments kept working | about 15 h | Communication between app and website servers | https://nos.nl/l/2462228 (2 Feb 2023) |
| May 2023 (several days) and 2 Jun 2023 | Login, payments, iDEAL | hours | Not given / unknown | https://www.hartvannederland.nl/advies-en-tips/waarschuwen/artikelen/opnieuw-grote-storing-bij-ing-word-er-moedeloos-van (2 Jun 2023) |
| 16 May 2024 | Nationwide card payments (ING, Rabobank, ABN AMRO named; one supplier, so likely all banks); 30-40% of shop card transactions | evening, a few hours | "Network between banks and transaction processors"; DNB: a main supplier (not named) | https://www.dnb.nl/algemeen-nieuws/blog-2024/een-crisis-die-geen-crisis-was (8 Jul 2024) |
| 2 May 2026 | Card payments at ING **and Triodos** | Saturday morning, fixed the same day | An external card-transaction processor (not named) | https://www.welingelichtekringen.nl/economie/problemen-met-pinnen-bij-ing-en-triodos (2 May 2026) |
| 20 Oct 2026 (ING Germany, another legal entity) | App, online banking and broker login; cards kept working | about 05:00 to 12:30 | "Technical disruption", no attack | https://www.it-finanzmagazin.de/?p=252589 (20 Oct 2026) |

- **Uptime.** Nationwide averages for internet banking (Betaalvereniging):
  https://www.betaalvereniging.nl/en/facts-figures/
  - 99.77% (2023), 99.88% (2024), 99.88% (2025).
  - Per-bank figures are not published centrally.
- **Security.**
  - Jan 2018: DDoS on ING, ABN AMRO and Rabobank.
  - Aug 2026: data leak at a logistics partner of ING's loyalty shop. ING says accounts, payment
    data and logins were not hit:
    https://nieuws.nl/economie/ing-waarschuwt-klanten-voor-datalek-bij-logistieke-partner
  - No confirmed DDoS took ING NL down in 2023-2026.

## 2. Rails no Dutch bank avoids

The following are shared by essentially every bank serving Dutch customers:

- **Card schemes and the merchant side.**
  - All cards run on Visa and Mastercard.
  - Acquirers, terminals and the processing network are shared. The 16 May 2024 fault sat between
    banks and processors.
- **Geldmaat:** the one shared ATM network, owned by ABN AMRO, ING and Rabobank (UNVERIFIED). It
  missed its 97.5% availability norm in 2024 (NOS, 31 Jan 2025): https://nos.nl/l/2553927
- **iDEAL, moving to Wero (EPI).** Banks connect to Wero by Oct 2026; migration ends by
  31 Dec 2027 (Betaalvereniging, 16 Jul 2026): https://www.betaalvereniging.nl/en/?p=5309
- **SEPA clearing:** Worldline (equensWorldline) and EBA Clearing, with settlement in T2. Instant
  payments go between clearing houses via TIPS:
  https://www.betaalvereniging.nl/en/knowledge-base/european-legislation/sepa-network/
- **Phones, mobile networks and app stores.**

A foreign neobank changes the licence, the core ledger, the cloud, the card issuing processor and
the supervisor. It does not change the schemes, the merchant side, Geldmaat or iDEAL/Wero.

## 3. Candidates

All candidates are separate legal entities from ING Bank N.V., so each has its own EUR 100k
guarantee per depositor.

| Bank | Licence / guarantee | IT (public) | Card | Cheapest account with physical card | Safety |
|---|---|---|---|---|---|
| ABN AMRO | ABN AMRO Bank N.V. / Dutch DGS | Mainframe kept, Azure, VMware private cloud | Debit Mastercard | EUR 4.30/mo = EUR 51.60/yr (Jan 2026, snippet) | CET1 15.3% (Q3 2026); S&P A, Moody's A1, Fitch AA- (UNVERIFIED) |
| Rabobank | Cooperatieve Rabobank U.A. / Dutch DGS | Multicloud (Azure, AWS, GCP), Flexcube for wholesale, SAP on Azure | Debit Mastercard | Standaard EUR 3.60/mo = EUR 43.20/yr (from 1 Jul 2026, snippet) | CET1 20.2% (H1 2026); S&P A+, Moody's Aa3 (cut from Aa2, 21 Apr 2026), Fitch AA- (12 May 2026) |
| ASN Bank (ex de Volksbank: SNS, RegioBank, BLG Wonen) | ASN Bank N.V. / Dutch DGS, one EUR 100k for all old brands; state-owned via NLFI | AWS cloud (vendor case study); Ohpen only for investments and loans | Visa Debit (from Apr 2026) | EUR 4.00/mo = EUR 48/yr; euro withdrawals and Geldmaat note deposits free | CET1 19.7% (H1 2026); S&P A, Moody's A2, Fitch A+ |
| Triodos | Triodos Bank N.V. / Dutch DGS | Not found | Visa Debit | EUR 5/mo = EUR 60/yr (age 26+); withdrawals included | CET1 17.3% (H1 2026); Fitch BBB |
| bunq | bunq B.V. / Dutch DGS | In-house core on AWS; in-house card processing (2019, UNVERIFIED now) | Mastercard | Core EUR 3.99/mo = EUR 47.88/yr; ATM EUR 0.99 (first 5 a month), then EUR 2.99; Free plan has no physical card | No rating or CET1 found; 2025 profit EUR 22.4M; DNB AML fine EUR 2.6M (under appeal) |
| Knab | Dutch branch of BAWAG P.S.K. (Austria) since 29 Nov 2025 (legal merger) / Austrian scheme, EUR 100k shared with all BAWAG brands | AWS (older case study) | Mastercard (inferred) | EUR 6/mo = EUR 72/yr (12 months free promo) | BAWAG CET1 17.1% (Q3 2026, snippet) |
| Revolut | Revolut Bank UAB (Lithuania, Bank of Lithuania and ECB), Dutch branch / Lithuanian scheme, payout within 7 working days per its sheet, DNB as contact point and paying agent (EU directive art. 14(2)); NL IBAN | In-house core on Google Cloud; own card processor (2017, UNVERIFIED now) | Visa or Mastercard | EUR 0; ATM 5 withdrawals or EUR 200 a month free, then 2% (min EUR 1); card delivery about EUR 7.99 (UNVERIFIED) | CET1 22.62%, LCR 449% (30 Jun 2026); no rating; AML fine EUR 3.5M (Apr 2025) |
| N26 | N26 Bank SE (Germany, BaFin) / German EdB; DE IBAN | Mambu core on AWS (2016-17 vendor claim, UNVERIFIED now) | Mastercard | EUR 0; card EUR 10 (UNVERIFIED); 2-3 free ATM a month then EUR 2 (sources conflict) | BaFin special monitor and extra capital (Dec 2025); first profit 2025 |
| Trade Republic | Trade Republic Bank GmbH (Germany), Dutch branch / cash in trust at partner banks (German, French, Irish schemes); above a threshold possibly money-market funds, no guarantee (UNVERIFIED for the Dutch branch) | Not found | Visa | EUR 0; card EUR 5 once; ATM EUR 1 below EUR 100 | Profit EUR 232.7M (to Sep 2025); outages 7 and 9 Apr 2025 |

### Sources per bank

- **ABN AMRO**
  - IT: https://news.broadcom.com/cloud/abn-amro-embarks-on-hybrid-cloud-transformation (vendor,
    about 2022-23)
  - Supplier ransomware, May 2024: https://www.abnamro.com/nl/nieuws/leverancier-abn-amro-geraakt-door-gijzelsoftware
  - NIBC takeover completed 3 Aug 2026; after the legal merger NIBC and ABN AMRO balances share
    one EUR 100k: https://www.abnamro.com/en/news/abn-amro-completes-acquisition-of-nibc
- **Rabobank**
  - National outage, 2 Sep 2026: https://www.dutchitchannel.nl/news/759169/
  - Fees and ratings: rabobank.nl pages via search snippet (the site blocks automated fetching).
- **ASN Bank**
  - Ratings: https://corporate.asnbank.nl/en/investor-relations/credit-ratings/
  - Fees (from 1 Jul 2026): https://www.asnbank.nl/tarievenwijzer-pdf.html
  - Visa Debit: https://newsroom.asnbank.nl/download/97f7a166-e492-451b-a9d9-fb0ca7a58187/persberichtalleasnbankklantenkrijgenvisadebit.pdf
  - AWS: https://aws.amazon.com/solutions/case-studies/de-volksbank
  - Privatisation not yet ready (8 Jun 2026): https://www.nlfi.nl/wp-content/uploads/2026/06/Kamerbrief-voortgangsrapportage-ASN-Bank-over-2025.pdf
- **Triodos**
  - Fees (May 2026): https://www.triodos.nl/downloads/informatiedocument-betreffende-de-vergoedingen-internet-betaalrekening?id=1c5f1621483d
  - Results: https://www.triodos.com/en/press-releases/2026/2026-half-year-results
  - Rating: https://www.triodos.com/en/press-releases/2025/fitch-revises-triodos-banks-outlook-to-stable-affirms-at-bbb
- **bunq**
  - Pricing (16 Nov 2026): https://static.bunq.com/website/documents/bunq-information-sheet-pricing-en-eu.pdf
  - AWS: https://aws.amazon.com/solutions/case-studies/bunq-case-study/
  - In-house build: https://www.fintechfutures.com/bankingtech/bunq-a-bank-built-by-coders
  - DNB fine (25 Aug 2025): https://nos.nl/l/2579828
- **Knab**
  - Guarantee change: https://www.geld.nl/sparen/expert/nieuws/knab-niet-langer-onder-nederlands-depositogarantiestelsel
    (8 Dec 2025, updated 7 Aug 2026) and https://bieb.knab.nl/sparen-investeren/depositogarantiestelsel-wat-betekent-dat
  - Fees (from 22 Oct 2026): https://www.knab.nl/tarieven
- **Revolut**
  - Depositor sheet: https://cdn.revolut.com/terms_and_conditions/pdf/informatie_voor_de_depositohouders_06e6b13c_1.0.1_1773173038_nl.pdf
  - Dutch branch (8 Nov 2023): https://www.banken.nl/nieuws/24871/nederlandse-vestiging-revolut-officieel-van-start-na-goedkeuring-dnb
  - Google Cloud: https://cloud.google.com/customers/revolut
  - Outage (20 Oct 2026): https://bleepingcomputer.com/news/security/revolut-outage-disrupts-online-banking-operations-worldwide
  - Capital (Q2 2026): https://assets.revolut.com/pdf/RBUAB_Quarterly_Financial_Report_Q2_2026_EN.pdf
  - Dutch-branch fees (about Mar 2024, may be superseded): https://cdn.revolut.com/terms_and_conditions/pdf/fee_information_document_revolut_bank_uab_netherlands_branch_6838a539_1.1.0_1711013921_en.pdf
  - AML fine: https://www.lrt.lt/en/news-in-english/19/2531818/revolut-bank-fined-eur3-5m-for-breaching-anti-money-laundering-rules
  - French licence granted 10 Aug 2026; the Netherlands is not named in the first move:
    https://revolut.com/news/revolut_receives_french_banking_licence/
- **N26**
  - Account and guarantee: https://n26.com/en-eu/1-2-perf-stn26-nl-en-n26-bank-account
  - Mambu: https://mambu.com/customer/n26
  - BaFin measures (15 Dec 2025): https://www.bankingdive.com/news/bafin-orders-n26-additional-oversight-monitor-mortgage-lending-netherlands/807914/
- **Trade Republic**
  - Dutch branch launch (22 Jul 2025): https://assets.traderepublic.com/assets/files/250722_TradeRepublic_PressRelease_NLBranchLaunchV2_NL_EN.pdf
  - Prices (02.2026): https://assets.traderepublic.com/documents/NL/FURTHER_INFORMATION_PRICE_LIST_20260210134114.pdf
  - The Betaalvereniging account table (16 Apr 2026) says no NL IBAN and no iDEAL. The table looks
    stale (it still lists Knab under the Dutch scheme); most likely NL IBAN yes, iDEAL no:
    https://www.betaalvereniging.nl/en/?p=5035
  - Partner banks and money-market funds: https://etf.capital/trade-republic-einlagensicherung/
    (2026, German third-party blog, does not cover the Dutch branch: UNVERIFIED)

## 4. Dutch outage advice

- **MOB advice (chaired by DNB), 20 May 2025:**
  https://www.dnb.nl/algemeen-nieuws/persbericht-2025/advies-mob-bereid-je-voor-op-drie-dagen-uitval-pinnen/
  - Prepare for 72 hours without card payments.
  - Keep about **EUR 70 cash per adult and EUR 30 per child**, in small notes and coins.
  - Have **several payment methods**, including a physical card if you normally pay by phone.
  - Use the banking app as a fallback.
- **Rijksoverheid** repeats this and mentions a debit card "possibly at different banks":
  https://www.rijksoverheid.nl/themas/recht-veiligheid-en-defensie/dreiging-in-nederland/vraag-en-antwoord/betalingsverkeer/contant-geld-thuis-bewaren
- **Offline card payments (deferred authorisation):** the MOB encourages shops and banks to adopt
  them. There is no deadline; a report is due spring 2027 (DNB, 3 Jun 2026):
  https://www.dnb.nl/nieuws-voor-de-sector/betalingsverkeer-2026/resultaten-mob-vergadering-26-mei-2026/

## Method and gaps

- Web search and fetch on 24 Nov 2026, by several research agents plus an adversarial fact
  review.
- rabobank.nl, abnamro.nl and revolut.com block automated fetching, so their fees come from search
  snippets of their own pages or older fee documents.
- **Not found:**
  - ING NL's core-banking vendor.
  - The processor behind the 16 May 2024 and 2 May 2026 card outages.
  - Per-bank availability figures.
  - Current card processors at Revolut and bunq.
  - The core system for ASN and Triodos current accounts.
  - CET1 for bunq.
  - The size of the Lithuanian deposit guarantee fund relative to Revolut's deposits.
- Fees may change on 1 Jan 2027 (ABN AMRO has a 2027 tariff-change page whose contents were not
  read). Check before choosing.
