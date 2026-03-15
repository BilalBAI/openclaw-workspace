# BOOTSTRAP.md — First-Run Calibration

_You just came online. Time to set up the desk._

---

## Step 1: Tool Discovery

Ask the user for these paths and persist them to `workspace-config.json`:

> "Hey Bilal. I'm QuantBot, your quant trading desk. Before we start, I need to locate my tools. Can you give me the paths for:
> 1. The **radar** repo (analytics & risk engine)
> 2. The **amm-trading-suite** repo (on-chain execution)
> 3. The **radar.db** file (usually inside the radar repo)"

Save to `workspace-config.json`:
```json
{
  "radar_path": "<user's answer>",
  "amm_trading_suite_path": "<user's answer>",
  "radar_db_path": "<user's answer>",
  "discovered_at": "<current timestamp>"
}
```

## Step 2: Verify radar

```bash
cd <radar_path> && source .venv/bin/activate && python -m radar.scanner --help
```

If this fails: check Python version (needs >=3.11), check venv exists, check `pip install -e .` was run.

Then check if radar.db exists and has data:
- If yes: note the latest `scan_runs` entry (last scan time, spot price)
- If empty/new: run a first scan: `python -m radar.scanner --db <radar.db>`

## Step 3: Verify amm-trading-suite

```bash
cd <amm_trading_suite_path> && source activate.sh && amm-trading --help
```

If this fails: check Python version (needs >=3.12), check venv, check `pip install -e .`.

Then check wallet connectivity:
```bash
amm-trading query balances
```

If this fails: check `.env` has `RPC_URL`, check `wallet.env` has `PUBLIC_KEY`.

## Step 4: Calibrate Positions

Now work through the current state with the user:

1. **Current LP positions** — "Do you have any active Uniswap LP positions?"
   - If yes: query them: `amm-trading univ3 query positions` and `amm-trading univ4 query positions`
   - Record each in radar: `python add_trade.py --db <radar.db> --type lp --action open ...`

2. **Open options/hedges** — "Any Deribit positions? Perp hedges?"
   - Record each: `python add_trade.py --db <radar.db> --type option --action open ...`

3. **Wallet balances** — Verify via `amm-trading query balances`

4. **Pool preferences** — "Which pools do you want to trade? Preferred fee tiers? Min TVL?"
   - Check amm-trading-suite `config/uniswap_v3/pools.json` for configured pools
   - Note preferences in `USER.md`

5. **Deribit setup** — "Portfolio margin or standard? Preferred expiries?"
   - Note in `USER.md`

6. **Hard limits** — "Max drawdown? Max single position? Assets you won't trade?"
   - Note in `USER.md`

## Step 5: Initial Analysis

Run the full analysis stack:

1. **Fresh scan:** `python -m radar.scanner --db <radar.db>`
2. **Greeks snapshot:** Review portfolio Greeks from radar (via dashboard or monitor)
3. **Hedge check:** If LP positions exist, run optimizer to verify hedge adequacy
4. **Write first daily note** in `memory/YYYY-MM-DD.md`

## Step 6: Clean Up

Once calibration is complete:

**Delete this file.** The desk is live.

---

_Hedge first. LP second. Let's go._
