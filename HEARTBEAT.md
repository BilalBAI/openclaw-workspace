# HEARTBEAT.md — Position Monitoring

All checks use radar and amm-trading-suite via CLI. Read `workspace-config.json` for tool paths.

---

## Cron Jobs (Auto-Running)

Scanner and monitor run automatically via cron:
- **:00** — `python -m radar.scanner --db radar.db`
- **:05** — `python run_monitor.py --db radar.db`

Logs: `/home/bilal/.openclaw/workspace/logs/`

---

## Every Six Hours (Read Cron Results)

### 1. Check latest scan results
Query radar.db for most recent `scan_runs` and `pnl_attribution`:
```bash
cd <radar_path> && source .venv/bin/activate
sqlite3 radar.db "SELECT id, scanned_at, spot, dvol FROM scan_runs ORDER BY id DESC LIMIT 2;"
sqlite3 radar.db "SELECT * FROM pnl_attribution ORDER BY run_id_t2 DESC LIMIT 1;"
```

### 2. Review PnL attribution
Check `logs/monitor.log` or query `pnl_attribution` table for delta/gamma/vega/theta/residual breakdown. Flag if residual is unusually large.

### 3. Query all positions
```bash
amm-trading univ3 query positions
amm-trading univ4 query positions
```
For each active position: is price still in range? Note any that have gone out of range.

### 4. Check wallet balance
```bash
amm-trading query balances
```
Sufficient ETH for gas?

### 5. Flag issues
After steps 1–4, check:
- **Delta breach:** Is net portfolio delta beyond +/-5% of notional? (from step 2)
- **Out-of-range LP:** Any position out of range? (from step 3)
- **Low gas balance:** Wallet ETH below buffer threshold? (from step 4)
- **IV shift:** Compare current DVOL to previous scan — significant move? (from step 1)
- **Expiring options:** Any open options in radar.db `trade_log` expiring within 24h?

If any flag triggers → alert the user with specifics and recommended action.
If nothing triggers → HEARTBEAT_OK, stay quiet.

---

## Daily (Once Per Day)

### 1. Hedge adequacy
```bash
cd <radar_path> && python -m radar.optimizer --db <radar.db> \
    --lp-pa <X> --lp-pb <X> --lp-s0 <X> --lp-capital <X> \
    --expiries <nearest> --put-call put \
    --no-short-options --delta-limit 5
```
Compare current hedge to optimizer recommendation. Flag if significantly suboptimal.

### 2. Vol regime assessment
Review scanner history in radar.db:
- DVOL trend over last 7 days
- IV vs RV spread
- Has the regime shifted? (low → high vol or vice versa)
- Should LP ranges be wider or narrower?

### 3. Strategy performance review
Which positions are carrying (positive net)? Which are bleeding? Update `portfolio/strategies.md`.

### 4. Daily summary
Compile into `memory/YYYY-MM-DD.md`:
- Total PnL (fees, IL, hedge PnL, gas costs, net)
- Per-position breakdown from PnL attribution
- Any flags or actions taken
- Vol regime notes

### 5. Memory maintenance
Distill key learnings into `MEMORY.md` if any long-term patterns emerged.

---

## Alerts (Immediate — Regardless of Schedule)

These override the hourly/daily cadence. If detected at any point, act immediately.

| Condition | Action |
|-----------|--------|
| Price exits LP range by >2x range width | Flag for close — rebalance unlikely to help |
| Portfolio delta breaches +/-5% notional | Immediate hedge adjustment needed |
| Option within 4h of expiry with no roll plan | Present roll/close options to user |
| Vol spike >20% in 1h (DVOL vs previous) | Hedge ratios may be broken — reassess all positions |
| Deribit margin utilization >80% | Reduce positions or add collateral |
| Pool TVL drops >20% in 24h | Liquidity risk — consider exiting |
| Unexpected wallet balance change | Alert user immediately — possible unauthorized tx |
