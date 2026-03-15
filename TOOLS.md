# TOOLS.md — Primary Tools & Data Sources

This workspace operates through two external tools. They are the core of everything you do.

---

## Hard Rules

1. **NEVER modify any file inside the radar or amm-trading-suite repositories.** No writes, no edits, no deletes, no moves — not even "helpful" fixes. If something is broken, tell the user.
2. **NEVER read source code** (`*.py`, `*.sol`, `*.js`, `*.ts`, `*.rs`) from either repository. The source is confidential. You may read: README/docs, CLI `--help` output, config JSON files (e.g., `tokens.json`, `pools.json`, `gas.json`), `results/` output files, and `radar.db`.
3. **NEVER read `.env`, `.env.*`, or `wallet.env` files** from any repository — including this workspace, radar, and amm-trading-suite. These contain secrets. If you need to know whether an env var is set, ask the user or run a CLI command that depends on it and observe the result.
4. **NEVER share, quote, summarize, or reproduce** source code or secret values from either tool in any output — conversation, files, logs, or memory.
5. **You MAY build auxiliary scripts** (wrappers, cron jobs, analysis) in THIS workspace that invoke the tools via CLI. Those scripts live here, never inside the tool repos.

---

## Tool Discovery

Paths are **not hardcoded**. On first session (or if `workspace-config.json` is missing/incomplete):

1. Ask the user for the **radar** install path
2. Ask the user for the **amm-trading-suite** install path
3. Ask the user for the **radar.db** path (often inside the radar repo)
4. Persist all paths to `workspace-config.json` in this workspace root
5. Verify by running: `python -m radar.scanner --help` and `amm-trading --help`

On every subsequent session, read `workspace-config.json` and verify the paths still work.

---

## Tool 1: radar — Analytics & Risk Engine

ETH options and LP portfolio risk system. Fetches market data, fits volatility surfaces, prices positions, attributes PnL, and optimizes hedges. All state lives in a single SQLite database (`radar.db`).

### Installation

```bash
cd <radar_path>
python3 -m venv .venv && source .venv/bin/activate
pip install -e .
pip install -e dashboard/   # optional: web UI
```

Requires Python >= 3.11. Dependencies: numpy, scipy, requests (+ dash, plotly for dashboard).

### Environment (.env inside radar repo)

```bash
DERIBIT_CLIENT_ID=<read-only API key>
DERIBIT_CLIENT_SECRET=<secret>
DERIBIT_TESTNET=false
```

If missing, trade sync is skipped but scanner still works with public API.

### CLI Commands

#### Scanner — Market Data + Vol Surface

```bash
python -m radar.scanner [--db <radar.db path>]
```

- Fetches ETH spot (Binance primary, Deribit fallback) + DVOL
- Fetches all active ETH option order books from Deribit
- Syncs Deribit trade history (if credentials configured)
- Auto-fits Wing vol surface per expiry
- Writes to: `scan_runs`, `order_book_snapshots`, `vol_surface_fits` tables
- **Intended cadence:** hourly via cron

#### PnL Attribution Monitor

```bash
python run_monitor.py --db <radar.db path>
python run_monitor.py --db <radar.db path> --run-t1 42 --run-t2 43   # specific runs
python run_monitor.py --db <radar.db path> --refit                   # force re-fit
```

- Compares two most recent scans
- Taylor decomposition: actual PnL → delta + gamma + vega + theta + residual
- Writes to: `pnl_attribution` table
- **Intended cadence:** hourly at :02 (after scanner)

#### Trade Recording

```bash
# LP position
python add_trade.py --db <radar.db path> \
    --type lp --action open \
    --pa 1672 --pb 2614 --s0 2100 --capital 1000000 \
    --quantity 1 --at "2026-03-01T00:00:00Z"

# Option
python add_trade.py --db <radar.db path> \
    --type option --action open \
    --strike 2200 --expiry 2026-04-24 --put-call put \
    --quantity 578.59 --price 85

# Perpetual
python add_trade.py --db <radar.db path> \
    --type perp --action open \
    --quantity 62.91 --price 2100
```

- Records trades to `trade_log` table
- **Must be run after every execution** via amm-trading-suite or manual Deribit trade
- Note: `--expiry` uses ISO format (`2026-04-24`), not Deribit format (`24APR26`)

#### Hedge Optimizer

```bash
# Baseline: long-only puts
python -m radar.optimizer --db <radar.db path> \
    --lp-pa 1672 --lp-pb 2614 --lp-s0 2100 --lp-capital 1000000 \
    --expiries 24APR26 --put-call put \
    --no-short-options --max-moneyness 1.05 \
    --delta-limit 5 --near-loss 0.5 --far-loss 1.0 --extreme-loss 5.0

# Advanced: short options allowed
python -m radar.optimizer --db <radar.db path> \
    --expiries 24APR26 \
    --min-moneyness 0.85 --max-moneyness 1.15 \
    --max-qty 500 --vega-limit -500 \
    --perp-min -200 --perp-max 50
```

- Solves LP minimization: minimize theta cost subject to delta + scenario loss constraints
- Output: `hedge_results/hedge_result.json`
- Output contains: optimal perp qty, option positions with Greeks, 14-scenario stress table

#### Dashboard (Web UI)

```bash
python -m dashboard --db <radar.db path> [--port 8050] [--debug]
```

- Tab 1: Vol surface viewer/editor (Wing params, smile, 3D surface)
- Tab 2: Portfolio Greeks, positions, stress bar chart
- Runs on `http://localhost:8050`

### Database Schema (radar.db — SQLite)

| Table | Key Fields |
|-------|-----------|
| `scan_runs` | id, scanned_at, spot, deribit_idx, dvol |
| `order_book_snapshots` | run_id, instrument, expiry, strike, put_call, mark_usd, bid_usd, ask_usd, mark_iv, T_years |
| `vol_surface_fits` | run_id, expiry, T_years, + 14 Wing params (vr, sr, pc, cc, dc, uc, dsm, usm, VCR, SCR, SSR, F, Ref, ATM) |
| `trade_log` | id, traded_at, type (lp/option/perp), action, strike, expiry, put_call, pa, pb, s0, capital, quantity, price_usd |
| `pnl_attribution` | run_id_t1, run_id_t2, spot_t1, spot_t2, actual_pnl, delta_pnl, gamma_pnl, vega_pnl, theta_pnl, residual_pnl, positions_json |

### Greeks Conventions

| Greek | Unit | Notes |
|-------|------|-------|
| Delta | ETH | Positive = long |
| Gamma | $/USD² | Change in delta per $1 spot move |
| Vega | $/1%vol | $ change per 1% absolute vol move |
| Theta | $/day | $ decay per calendar day |

### Expiry Format Note

- Scanner & optimizer use Deribit format: `27MAR26`, `24APR26`
- `trade_log` (add_trade.py) uses ISO format: `2026-03-27`, `2026-04-24`
- Convert between them when recording trades after optimizer recommendations

---

## Tool 2: amm-trading-suite — On-Chain Execution

CLI toolkit for Uniswap V3/V4 liquidity management, swaps, position queries, and wallet operations. Supports Safe multisig mode.

### Installation

```bash
cd <amm_trading_suite_path>
python3 -m venv venv && source venv/bin/activate
pip install -e .
```

Requires Python >= 3.12. Dependencies: web3, python-dotenv, eth-account, requests.

Activation shortcut (if available):
```bash
source <amm_trading_suite_path>/activate.sh
```

### Environment

**`.env`** (in amm-trading-suite root):
```bash
RPC_URL=https://mainnet.infura.io/v3/YOUR_KEY
ETHERSCAN_API_KEY=...          # optional
POOL_MANAGER_ADDRESS=0x...     # V4 PoolManager
OWNER_ADDRESS=0x...            # Hook owner
```

**`wallet.env`** (in amm-trading-suite root):
```bash
PUBLIC_KEY=0x...
PRIVATE_KEY=...
SAFE_ADDRESS=0x...             # optional: enables Safe proposal mode
```

### Configuration Files (inside amm-trading-suite `config/` dir)

| File | Purpose |
|------|---------|
| `tokens.json` | Token symbol → address mapping |
| `gas.json` | EIP-1559 gas params and per-operation gas limits |
| `uniswap_v3/pools.json` | V3 pool configs (address, tokens, fee, tickSpacing) |
| `uniswap_v4/pools.json` | V4 pool configs (PoolKey format, hooks, dynamic fees) |

You may read these config files to understand available pools and tokens.

### Global CLI Flags

| Flag | Effect |
|------|--------|
| `--address 0x...` | Override wallet address (defaults to `PUBLIC_KEY`) |
| `--dry-run` | Simulate transaction without sending — **ALWAYS use this first** |
| `--direct` | Bypass Safe mode (if `SAFE_ADDRESS` is set) |
| `--refresh-cache` | Force pool data cache refresh |

### CLI Commands

#### General

```bash
amm-trading query balances [--address 0x...]
amm-trading wrap --amount <ETH_amount> [--dry-run]
amm-trading unwrap --amount <WETH_amount> [--dry-run]
amm-trading wallet generate
```

#### Uniswap V3

```bash
# Queries (read-only)
amm-trading univ3 query pools
amm-trading univ3 query position --token-id <id>
amm-trading univ3 query positions [--address 0x...]
amm-trading univ3 quote --pool <name> --token-in <symbol> --amount <X>
amm-trading univ3 lp-quote --pool <name> --tick-lower <X> --tick-upper <X> --amount0 <X>

# Liquidity (write — always --dry-run first)
amm-trading univ3 add --pool <name> --tick-lower <X> --tick-upper <X> --amount0 <X> --amount1 <X> [--slippage <bps>] [--dry-run]
amm-trading univ3 add-range --pool <name> --range-lower <pct> --range-upper <pct> --amount0 <X> --amount1 <X> [--slippage <bps>] [--dry-run]
amm-trading univ3 remove --token-id <X> --percent <X> [--collect-fees] [--burn] [--dry-run]
amm-trading univ3 migrate --token-id <X> --tick-lower <X> --tick-upper <X> [--dry-run]

# Swaps
amm-trading univ3 swap --pool <name> --token-in <symbol> --amount <X> [--slippage <bps>] [--dry-run]
```

#### Uniswap V4

```bash
# Queries (read-only)
amm-trading univ4 query pools
amm-trading univ4 query position --token-id <id>
amm-trading univ4 query positions [--address 0x...]
amm-trading univ4 quote --pool <name> --token-in <symbol> --amount <X>

# Liquidity (write — always --dry-run first)
amm-trading univ4 add --pool <name> --tick-lower <X> --tick-upper <X> --amount0 <X> --amount1 <X> [--slippage <bps>] [--dry-run]
amm-trading univ4 add-range --pool <name> --range-lower <pct> --range-upper <pct> --amount0 <X> --amount1 <X> [--slippage <bps>] [--dry-run]
amm-trading univ4 remove --token-id <X> --percent <X> [--collect-fees] [--burn] [--dry-run]

# Swaps (supports native ETH)
amm-trading univ4 swap --pool <name> --token-in <symbol> --amount <X> [--slippage <bps>] [--dry-run]

# Hook management (owner-only)
amm-trading univ4 hook set-fee --pool <name> --fee <bps>
amm-trading univ4 hook add-provider --pool <name> --address 0x...
amm-trading univ4 hook remove-provider --pool <name> --address 0x...
amm-trading univ4 hook add-router --address 0x...
amm-trading univ4 hook remove-router --address 0x...
amm-trading univ4 hook query --pool <name>

# Pool initialization
amm-trading univ4 pool init --pool <name> [--sqrt-price <X>]
```

#### Safe Wallet

```bash
amm-trading safe info
amm-trading safe register-delegate
```

When `SAFE_ADDRESS` is set, all fund-touching operations are **proposed** to Safe TX Service (not executed directly). Safe owners approve in the Safe{Wallet} app.

### Output

All results are written as JSON to the `results/` directory inside amm-trading-suite:
- `results/balances_0x....json`
- `results/univ3_pools.json`
- `results/univ3_position_<id>.json`
- `results/univ3_swap_<hash>.json`
- etc.

You may read these output files to parse results.

### Key V4 Differences from V3

| Feature | V3 | V4 |
|---------|----|----|
| Native ETH | No (WETH wrapping) | Yes (use `ETH` symbol) |
| Dynamic fees | No | Yes (via hooks) |
| Gas cost | Higher | Lower (singleton + flash accounting) |
| Custom logic | No | Hooks (fee control, LP whitelisting, etc.) |

---

## Secondary: External Data Sources

These are supplementary. The primary workflow runs through radar + amm-trading-suite.

| Tool | Use Case |
|------|----------|
| CoinGecko | Spot prices, market caps, token info |
| Dune Analytics | Custom queries for pool activity, LP behavior |
| DefiLlama | TVL, yields, protocol comparison |
| Etherscan | Transaction verification, contract inspection |
| Laevitas / Greeks.live | Options analytics, vol commentary |
| CoinGlass | Funding rates, open interest, liquidations |
| Blocknative | Gas estimation, mempool monitoring |

---

## Secrets — Three Scopes

**NEVER store secrets in markdown files. NEVER log, print, or echo secret values.**

| Scope | File | Contains |
|-------|------|----------|
| This workspace | `.env` | Service API keys (Etherscan, Dune, CoinGecko, Infura, Alchemy, Graph) |
| radar | `<radar_path>/.env` | Deribit API credentials (read-only, for trade sync) |
| amm-trading-suite | `<amm_path>/.env` + `<amm_path>/wallet.env` | RPC URL, wallet keys, Safe address |

All `.env` files are gitignored in their respective repos. Never commit them.
