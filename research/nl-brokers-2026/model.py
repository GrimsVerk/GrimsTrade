# Cost model: 12 equal monthly buys of M (Jan-Dec 2027), flat prices.
# 2027 holding fees on the average month-end value (M,2M..12M -> 6.5M), steady state on 12M.
# Platform costs only (fund TER shown separately; same fund -> same TER everywhere).
def plat(M, per_buy=0.0, pct=0.0, fixed=0.0, pct_buy=0.0, min_year=0.0):
    y1 = 12*per_buy + 12*M*pct_buy + max(pct*6.5*M + fixed, min_year if min_year else 0)
    ss = max(pct*12*M + fixed, min_year if min_year else 0)
    return y1, ss
P = {
 'ING Zelf op de Beurs (Topselectie, periodic)': dict(pct=0.0024),
 'Trade Republic (savings plan)': dict(),
 'Scalable FREE (savings plan)': dict(),
 'DEGIRO (Tradegate core, EUR 1, manual)': dict(per_buy=1.0),
 'BUX Basic (plan)': dict(pct=0.0020),
 'BUX Plus (plan)': dict(fixed=35.88),
 'Saxo Bronze AutoInvest': dict(pct=0.0012),
 'ABN AMRO Zelf Beleggen Basis (free-list ETF)': dict(pct=0.0020),
 'Rabobank Zelf Beleggen (periodic ETF)': dict(pct=0.0024, pct_buy=0.0010, min_year=20.0),
 'IBKR Fixed (EUR 3/buy, secondary)': dict(per_buy=3.0),
 'LYNX (EUR 6/buy, unverified)': dict(per_buy=6.0),
 'Meesman (0.31% fee + 0.20% entry)': dict(pct=0.0031, pct_buy=0.0020),
 'Brand New Day (0.44% service + 0.05% swing)': dict(pct=0.0044, pct_buy=0.0005),
 'Peaks (EUR 1.99/mo + 0.50%)': dict(pct=0.0050, fixed=23.88),
}
import sys
Ms=[int(x) for x in sys.argv[1:]] or [250,500,1000]
print('| Provider | '+' | '.join(f'{m}/mo: 2027 / later yr' for m in Ms)+' |')
for k,v in P.items():
    cells=[]
    for M in Ms:
        y1,ss=plat(M,**v); cells.append(f'{y1:.2f} / {ss:.2f}')
    print('| '+k+' | '+' | '.join(cells)+' |')
for M in Ms:
    avgcash=sum(12*M-k*M for k in range(1,13))/12  # cash left after each start-of-month buy
    print(M,'avg cash parked 2027',avgcash,'interest diff 1.00% vs 2.50%:',round(avgcash*0.015,2),' 1.25 vs 3.35:',round(avgcash*0.021,2), 'full-year savings interest on 12M at 1.25%:',12*M*0.0125, 'at 3.35%:', round(12*M*0.0335,2))
    print(M,'fund TER 0.14% 2027:',round(6.5*M*0.0014,2),'later:',round(12*M*0.0014,2),' leakage 0.24% later:',round(12*M*0.0024,2))
