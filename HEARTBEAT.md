# HEARTBEAT.md — Position Monitoring

On each heartbeat, check what's due. All checks use radar and amm-trading-suite via CLI.
Read `workspace-config.json` for tool paths.

---

## Every 15 Minutes

### LP Range Check
```bash
amm-trading univ3 query position --token-id <id>
```
Is the current price still within the position's tick range? Repeat for each active position (query all via `amm-trading univ3 query positions`).

### Portfolio Net Delta
Check radar.db `pnl_attribution` or `trade_log` for latest Greeks. Is net delta within +/-5% of notional?

### Deribit Margin
If hedges are active on Deribit, verify margin utilization is acceptable (manual check or Deribit API if configured in radar).

---

## Every 1 Hour

### Fee Accrual Update
```bash
amm-trading univ3 query position --token-id <id>
```
Compare uncollected fees to last check. Note changes in `memory/` daily notes.

### PnL Attribution
```bash
cd <radar_path> && python run_monitor.py --db <radar.db>
```
Review delta/gamma/vega/theta/residual breakdown. Flag if residual is unusually large (model may be miscalibrated).

### IV vs RV Comparison
Check latest `scan_runs` in radar.db for DVOL. Compare to recent realized vol. Flag significant divergence — affects LP range width decisions and hedge ratios.

### Funding Rates
If using perps for delta hedging, check funding rates (CoinGlass or Deribit). High funding = hedging cost increasing.

### Gas Prices
Check current gas conditions. Flag if favorable for pending rebalances.

### Wallet Balance
```bash
amm-trading query balances
```
Sufficient ETH for gas? Above/below max balance target?

---

## Every 4 Hours

### Greeks Snapshot
```bash
cd <radar_path> && python -m radar.scanner --db <radar.db>
```
Then review portfolio Greeks via dashboard or monitor output. Note in `memory/` daily notes.

### Vol Surface Scan
```bash
cd <radar_path> && python -m dashboard --db <radar.db>
```
Check term structure and skew changes since last scan. Note shifts in `memory/` daily notes.

### Pool Health
```bash
amm-trading univ3 query pools
```
TVL changes, volume trends for active pools. Flag if TVL drops significantly.

### Options Expiry Check
Query radar.db `trade_log` for open options. Check if anything expires within 48h. If found, flag for roll or close decision.

### Hedge Adequacy
```bash
cd <radar_path> && python -m radar.optimizer --db <radar.db> \
    --lp-pa <X> --lp-pb <X> --lp-s0 <X> --lp-capital <X> \
    --expiries <nearest> --put-call put \
    --no-short-options --delta-limit 5
```
Compare current hedge to optimizer recommendation. Flag if current hedge is significantly suboptimal.

---

## Daily (Once Per Day)

### Full PnL Attribution
Run `python run_monitor.py` and compile a full daily summary:
- Total PnL (fees, IL, hedge PnL, gas costs, net)
- Per-position breakdown
- Write to `memory/YYYY-MM-DD.md`

### Strategy Performance Review
Which positions are carrying (positive net)? Which are bleeding? Update `portfolio/strategies.md` with current status.

### Vol Regime Assessment
Review scanner history in radar.db:
- DVOL trend over last 7 days
- IV vs RV spread
- Has the regime shifted? (low → high vol or vice versa)
- Should LP ranges be adjusted?

### Memory Maintenance
Distill today's daily notes into key learnings. Update `MEMORY.md` if any long-term patterns emerged.

---

## Alert Immediately (Regardless of Schedule)

These conditions require immediate action — do not wait for the next scheduled check:

| Condition | Detection | Action |
|-----------|-----------|--------|
| Price exits LP range | `amm-trading univ3 query position` shows out-of-range | Flag for rebalance or close |
| Portfolio delta breaches +/-5% | radar Greeks check | Immediate hedge adjustment |
| Option within 4h of expiry | radar.db `trade_log` expiry dates | Roll or close — present options to user |
| Vol spike >20% in 1h | radar scanner DVOL vs previous | Hedge ratios may be broken — reassess |
| Deribit margin utilization >80% | Deribit account check | Reduce positions or add collateral |
| Pool TVL drops >20% in 24h | `amm-trading univ3 query pools` | Liquidity risk — consider exiting |
| Unexpected wallet transaction | `amm-trading query balances` shows unexpected change | Alert user immediately |
