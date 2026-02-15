# HEARTBEAT.md

## Position Monitoring Checklist

On each heartbeat, check what's due based on `memory/heartbeat-state.json` timestamps:

### Every 15 minutes
- [ ] LP range check: is price in range for all active positions?
- [ ] Portfolio net delta: within ±5% notional limit?
- [ ] Deribit margin: sufficient margin for all open positions?

### Every 1 hour
- [ ] Fee accrual update: fees earned since last check
- [ ] IV vs RV comparison: any significant divergence?
- [ ] Funding rates: cost/income on any perpetual hedges
- [ ] Gas prices: favorable for pending rebalances?

### Every 4 hours
- [ ] Greeks snapshot: update `portfolio/greeks-snapshot.md`
- [ ] Vol surface scan: term structure and skew changes
- [ ] Pool health: TVL changes, volume trends for active pools
- [ ] Options expiry check: anything expiring within 48h?

### Daily (once per day)
- [ ] Full PnL attribution: fees, IL, hedge PnL, gas costs, net
- [ ] Strategy performance review: which positions are carrying, which are bleeding
- [ ] Vol regime assessment: has the regime shifted?
- [ ] Memory maintenance: distill daily notes into MEMORY.md

### Alert immediately (regardless of schedule)
- Price exits LP range
- Portfolio delta breaches ±5% limit
- Option within 4h of expiry with no roll plan
- Vol spike >20% in 1h
- Deribit margin utilization >80%
- Pool TVL drops >20% in 24h
- Smart contract exploit or governance attack on a pool's protocol
