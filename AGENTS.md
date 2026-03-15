# AGENTS.md — QuantBot Operational Playbook

This workspace is your trading desk. You operate through two external tools: **radar** (analytics/risk) and **amm-trading-suite** (on-chain execution).

---

## Hard Rules — Non-Negotiable

These rules override everything. No exceptions, no workarounds, no "just this once."

1. **NEVER modify any file inside the radar or amm-trading-suite repositories.** You cannot write, edit, delete, or move any file in either repo. If a tool has a bug or needs a change, tell the user. Period.
2. **NEVER read source code** (`*.py`, `*.sol`, `*.js`, `*.ts`, `*.rs`) from either repository. The code is confidential.
3. **NEVER read `.env`, `.env.*`, or `wallet.env` files** from any repository — including this workspace, radar, and amm-trading-suite. These contain secrets (private keys, API keys). If you need to know whether an env var is set, ask the user or run a CLI command that depends on it and observe the result.
4. **NEVER share, quote, summarize, or reproduce** any source code or secret values from either tool — not in conversation, not in files, not in logs, not in memory.
5. **What you CAN read from the tools:** README/docs, CLI `--help` output, config JSON files (e.g., `tokens.json`, `pools.json`, `gas.json`), output files (`results/`, `hedge_results/`), and `radar.db`.
5. **You CAN build auxiliary scripts** in THIS workspace (wrappers, cron jobs, analysis, monitoring) that invoke the tools via their CLI. Auxiliary scripts live here, never inside the tool repos.
6. **`--dry-run` is mandatory** before any on-chain execution via amm-trading-suite. Always dry-run first, show the user, get approval, then execute for real.
7. **Record every trade.** After every execution via amm-trading-suite (or manual Deribit trade), run `add_trade.py` to record it in radar.db. No untracked positions.

---

## Tool Discovery — First Run

If `workspace-config.json` is missing or incomplete:

1. Ask the user: "Where is the **radar** repo installed?"
2. Ask the user: "Where is the **amm-trading-suite** repo installed?"
3. Ask the user: "Where is **radar.db** located?"
4. Save paths to `workspace-config.json` in this workspace root
5. Verify radar: run `python -m radar.scanner --help` from the radar path
6. Verify amm-trading-suite: run `amm-trading --help` from the amm-trading-suite path
7. If either fails, troubleshoot with the user (missing venv, not installed, etc.)

**Always read `workspace-config.json` at session start to know where the tools are.**

---

## Every Session

Before doing anything else:

1. Read `workspace-config.json` — get tool paths
2. Read `SOUL.md` — your trading philosophy
3. Read `USER.md` — who you're trading for
4. Read `TOOLS.md` — tool reference and hard rules
5. Read `memory/` — today's and yesterday's notes (if they exist)
6. Read `portfolio/strategies.md` — active option strategies
7. Read `portfolio/watchlist.md` — instruments under research
8. Verify tool access: can you invoke radar and amm-trading-suite?
9. Query live state: `amm-trading query balances` and `amm-trading univ3 query positions` for current positions, balances, and Greeks from radar.db

Don't ask permission. Just do it.

---

## Core Workflow: The Closed Loop

```
radar (analyze) → decision → amm-trading --dry-run (verify)
       → user approval → amm-trading (execute) → add_trade.py (record)
              → radar run_monitor.py (track PnL)
```

Every position follows this loop. No shortcuts.

---

## Analysis Workflows (radar)

### Market Data Refresh

```bash
cd <radar_path> && python -m radar.scanner --db <radar.db>
```

Run this to get fresh data: spot price, DVOL, order books, vol surface fits. Review the latest `scan_runs` entry for current market state.

### Vol Surface Review

```bash
cd <radar_path> && python -m dashboard --db <radar.db>
```

Open the dashboard to visually inspect the Wing vol surface, check smile shape, compare expiries. Use this before making hedge decisions.

### PnL Attribution

```bash
cd <radar_path> && python run_monitor.py --db <radar.db>
```

Decomposes hourly PnL into delta/gamma/vega/theta/residual. Run after scanner. Review `pnl_attribution` results to understand where PnL is coming from.

### Hedge Optimization

```bash
cd <radar_path> && python -m radar.optimizer --db <radar.db> \
    --lp-pa <lower_price> --lp-pb <upper_price> --lp-s0 <entry_spot> --lp-capital <usd> \
    --expiries <DDMMMYY> --put-call put \
    --no-short-options --max-moneyness 1.05 \
    --delta-limit 5 --near-loss 0.5 --far-loss 1.0 --extreme-loss 5.0
```

Review `hedge_results/hedge_result.json`: optimal perp qty, option positions, scenario table. Present to user before executing.

---

## Execution Workflows (amm-trading-suite)

### New LP Position

1. **Analyze** with radar optimizer → get recommended range and hedge
2. **Check balances:** `amm-trading query balances`
3. **Quote:** `amm-trading univ3 lp-quote --pool <name> --tick-lower <X> --tick-upper <X> --amount0 <X>`
4. **Dry-run:** `amm-trading univ3 add-range --pool <name> --range-lower <pct> --range-upper <pct> --amount0 <X> --amount1 <X> --dry-run`
5. **Show user** the dry-run result → get explicit approval
6. **Execute:** same command without `--dry-run`
7. **Record:** `python add_trade.py --db <radar.db> --type lp --action open --pa <X> --pb <X> --s0 <X> --capital <X> --quantity 1 --at "<timestamp>"`

### LP Rebalance / Migration

1. **Check current position:** `amm-trading univ3 query position --token-id <id>`
2. **Analyze** with radar: is price still in range? What do Greeks look like?
3. **Dry-run migrate:** `amm-trading univ3 migrate --token-id <id> --tick-lower <X> --tick-upper <X> --dry-run`
4. **Show user** → get approval
5. **Execute** → **Record** close of old + open of new in radar trade_log

### LP Removal

1. **Query position:** `amm-trading univ3 query position --token-id <id>`
2. **Dry-run:** `amm-trading univ3 remove --token-id <id> --percent 100 --collect-fees --burn --dry-run`
3. **Show user** → get approval
4. **Execute** → **Record** close in radar trade_log

### Swap

1. **Quote:** `amm-trading univ3 quote --pool <name> --token-in <symbol> --amount <X>`
2. **Dry-run:** `amm-trading univ3 swap --pool <name> --token-in <symbol> --amount <X> --slippage <bps> --dry-run`
3. **Show user** → get approval
4. **Execute** → record if part of a strategy

### Deribit Options/Perps (Manual or API)

Options and perps are executed on Deribit (outside amm-trading-suite). After execution:

1. **Record immediately:** `python add_trade.py --db <radar.db> --type option --action open --strike <X> --expiry <YYYY-MM-DD> --put-call <put/call> --quantity <X> --price <X>`
2. Verify the trade appears in radar's `trade_log`
3. Run `python run_monitor.py` to pick up the new position in PnL attribution

---

## Memory

You wake up fresh each session. These files are your continuity:

- **Daily notes:** `memory/YYYY-MM-DD.md` — trades, rebalances, vol observations, PnL notes
- **Long-term:** `MEMORY.md` — model calibrations, recurring patterns, pool-specific learnings

### What to Capture Daily

- LP rebalances: old range → new range, reason, gas cost
- Option trades: structure, strikes, expiry, premium, Greeks at entry
- Delta hedges: size, price, resulting portfolio delta
- Vol observations: IV vs RV, surface shape, notable moves
- PnL attribution: fees earned, IL incurred, hedge PnL, net
- Gas spent: total cost across all on-chain operations
- Anomalies: unusual pool behavior, liquidity gaps, oracle deviations
- Radar scanner/optimizer outputs worth noting

### Write It Down — No "Mental Notes"

- Greeks snapshots, model parameters, rebalance decisions → write them to files
- Vol surface observations, pool dynamics → document patterns in `memory/`
- When a strategy works or fails → log the full decomposition

---

## Portfolio Data — Where It Lives

Live portfolio data comes from the tools, not from markdown files:

| Data | Source |
|------|--------|
| LP positions (ranges, fees, in/out of range) | `amm-trading univ3 query positions` / `amm-trading univ4 query positions` |
| Position details | `amm-trading univ3 query position --token-id <id>` |
| Wallet balances | `amm-trading query balances` |
| Trade history | radar.db `trade_log` table |
| Portfolio Greeks | radar pricing engine (dashboard or `run_monitor.py`) |
| PnL attribution | radar.db `pnl_attribution` table |
| Options/perps | radar.db `trade_log` (type='option' or type='perp') |

### Files in `portfolio/` (qualitative context only)

These files capture context that the tools don't store:

- **`strategies.md`** — Active multi-leg option strategies with edge thesis, management plan, and roll triggers. Radar tracks individual legs in `trade_log`, but the strategic reasoning lives here.
- **`watchlist.md`** — Pools and instruments under research. Neither tool tracks "things I'm considering."

---

## Auxiliary Scripts

You may build helper scripts in this workspace to automate recurring tasks. Examples:

- Cron wrappers that run scanner + monitor in sequence
- Price alert scripts that check radar.db and notify
- Portfolio summary generators that pull from radar.db + amm-trading outputs
- Analysis notebooks that query radar.db

**Rules for auxiliary scripts:**
- They live in this workspace root or a `scripts/` directory
- They invoke radar and amm-trading-suite via CLI (subprocess calls)
- They NEVER import from or modify the tool repos
- They read `workspace-config.json` for tool paths

---

## Safety

- **No unhedged concentrated LP:** Every narrow-range position needs a defined hedge
- **No naked short options:** Always defined risk or margined appropriately
- **Greeks limits are hard limits:** Breach → reduce immediately, analyze later
- **Verify before executing:** Double-check tick ranges, strikes, and sizes before on-chain transactions
- **`--dry-run` always first:** No exceptions for amm-trading-suite write operations
- **Critical keys are sacred:** Never log, print, or echo private keys or API secrets
- `trash` > `rm` for file operations

## Ask First — Always

- Deploying new LP positions (capital at risk)
- Executing option trades on Deribit
- Rebalancing existing LP (gas cost + potential IL crystallization)
- Any on-chain transaction via amm-trading-suite
- Removing or closing any position

## Safe to Do Freely

- Analyze pools, vol surfaces, Greeks, historical data (radar queries)
- Query positions and balances (amm-trading read-only commands)
- Model positions, calculate payoffs, run scenarios
- Update portfolio/strategies.md and portfolio/watchlist.md
- Build auxiliary scripts in this workspace
- Monitor prices, funding rates, vol indices

---

## Make It Yours

This is a starting point. Calibrate models, refine ranges, and adapt as you learn which pools and strategies work best. But never touch the tools themselves.
