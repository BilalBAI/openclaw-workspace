# HEARTBEAT.md

## Market Monitoring Checklist

On each heartbeat, check what's due based on `memory/heartbeat-state.json` timestamps:

### Every 30 minutes
- [ ] Portfolio positions: any approaching stops or targets?
- [ ] BTC/ETH price action: significant moves (>2% in 1h)?
- [ ] Funding rates: extreme readings on major pairs?

### Every 2 hours
- [ ] Top movers scan: what's pumping/dumping and why?
- [ ] Stablecoin flows: USDT/USDC mint/burn activity
- [ ] Exchange inflow/outflow anomalies

### Every 6 hours
- [ ] Macro calendar: upcoming events in next 12h?
- [ ] DeFi yield check: significant changes in farming positions?
- [ ] Governance votes: any active votes on held protocols?
- [ ] Watchlist review: any watchlist assets hitting entry zones?

### Daily (once per day)
- [ ] Portfolio performance summary
- [ ] Market regime check: has anything shifted?
- [ ] Thesis review: any theses need updating?
- [ ] Memory maintenance: distill daily notes into MEMORY.md

### Alert immediately (regardless of schedule)
- Position hits stop loss or take profit
- Major protocol exploit or hack
- Surprise macro event (emergency rate decision, major regulatory action)
- Flash crash or extreme volatility (>10% move in BTC/ETH in <1h)
