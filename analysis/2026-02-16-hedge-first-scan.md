# Hedge-First Vol Surface Scan — Feb 16, 2026

## Market Snapshot

| Asset | Spot | DVOL (ATM IV) | 30d RV | IV-RV Gap |
|-------|------|---------------|--------|-----------|
| BTC | $67,922 | 52.5% | 74.2% | **-21.7 pts** |
| ETH | $1,971 | 70.4% | 96.1% | **-25.7 pts** |

**Key finding:** Both assets have IV trading 22-30 pts below realized vol. Options hedges are at a ~30% discount to fair value. Prime environment for hedge-first LP.

---

## BTC Vol Surface Detail

### DVOL (24h hourly candles)
- Range: 49.8 – 52.9
- Last: 52.45
- Trend: Slight uptick from morning lows (~50.6)

### Historical RV (latest hourly snapshots)
- 30d RV: 74.2% (trending down from ~76% highs last week)
- RV has been elevated since early Feb spike event

### Key ATM/Near-ATM Options (sorted by IV discount)

| Instrument | Type | IV | RV | Gap | Mark (BTC) | Mark ($) | OI | Bid/Ask |
|------------|------|-----|------|------|------------|---------|-----|---------|
| 27MAR26-74000 | Put | 47.95% | 74.2% | -26.3 | 0.1176 | $7,991 | 241 | 0.116/0.119 |
| 27MAR26-72000 | Put | 48.02% | 74.2% | -26.2 | 0.0971 | $6,598 | 350 | 0.0955/0.099 |
| 27MAR26-70000 | Put | 48.63% | 74.2% | -25.6 | 0.0792 | $5,382 | 4,690 | 0.079/0.0795 |
| 6MAR26-69000 | Put | 49.88% | 74.2% | -24.3 | 0.0520 | $3,532 | 83 | 0.0515/0.0525 |
| 6MAR26-74000 | Call | 49.36% | 74.2% | -24.8 | 0.0139 | $945 | 10 | 0.0135/0.014 |
| 6MAR26-71000 | Call | 49.37% | 74.2% | -24.8 | 0.0253 | $1,722 | 334 | 0.0245/0.0255 |
| 27MAR26-65000 | Call | 50.84% | 74.2% | -23.4 | 0.0893 | $6,067 | 951 | 0.0885/0.09 |
| 27FEB26-71000 | Call | 50.91% | 74.2% | -23.3 | 0.0172 | $1,170 | 265 | 0.0165/0.0175 |

### Best Liquidity (OI > 1000)
- 27MAR26-70000-P: **4,690 OI** — primary hedge candidate
- 27MAR26-90000-P: 3,164 OI
- 27MAR26-65000-C: 951 OI

---

## ETH Vol Surface Detail

### DVOL (24h hourly candles)
- Range: 70.0 – 72.1
- Last: 70.36
- Trend: Declining from ~72 highs early in the day

### Historical RV (latest hourly snapshots)
- 30d RV: 96.1% (down from ~101% peak)
- ETH has significantly higher realized vol than BTC — larger IV-RV discount

### Key ATM/Near-ATM Options (sorted by IV discount)

| Instrument | Type | IV | RV | Gap | Mark (ETH) | Mark ($) | OI | Bid/Ask |
|------------|------|-----|------|------|------------|---------|-----|---------|
| 20FEB26-1975 | Put | 64.46% | 96.1% | -31.6 | 0.0264 | $52 | 12,176 | 0.0255/0.027 |
| 20FEB26-2000 | Put | 64.32% | 96.1% | -31.8 | 0.0335 | $66 | 7,339 | 0.0325/0.034 |
| 27MAR26-2100 | Call | 65.97% | 96.1% | -30.1 | 0.0605 | $119 | 5,055 | 0.06/0.061 |
| 27MAR26-2200 | Put | 65.88% | 96.1% | -30.2 | 0.1572 | $310 | 26,904 | 0.1555/0.1585 |
| 27MAR26-1900 | Put | 67.98% | 96.1% | -28.1 | 0.0680 | $134 | 4,912 | 0.0675/0.0685 |
| 6MAR26-2050 | Put | 65.79% | 96.1% | -30.3 | 0.0801 | $158 | 128 | 0.0795/0.0805 |
| 27FEB26-1950 | Put | 67.28% | 96.1% | -28.8 | 0.0400 | $79 | 3,057 | 0.0395/0.0405 |

### Best Liquidity (OI > 5000)
- 27MAR26-2200-P: **26,904 OI** — outstanding liquidity
- 20FEB26-1975-P: **12,176 OI** — excellent near-term
- 27MAR26-2100-C: **5,055 OI** — strong call-side

---

## Strategy Recommendations

### Core Insight: LP + Vol Trade Combo

Full option hedging is expensive vs LP fees alone. The real play: treat LP and options as complementary:
- **LP**: earns fees (positive theta), suffers IL (short gamma)
- **Long options**: costs theta, earns gamma/vega from vol realization
- **Combined**: LP theta partially offsets option theta; option gamma partially offsets LP IL; the vol discount (IV << RV) is the edge

### Strategy 1: ETH "Vol Harvest" — HIGH CONVICTION

**Hedge (Deribit, deploy first):**
- Long ETH-27MAR26-1900-P
  - IV: 68.0% | Gap: -28.1 pts | Cost: $134/contract | OI: 4,912
- Long ETH-27MAR26-2100-C
  - IV: 66.0% | Gap: -30.1 pts | Cost: $119/contract | OI: 5,055
- Combined strangle: $253/contract

**LP (on-chain, deploy second):**
- Pool: WETH/USDC 30bps, Ethereum mainnet
- Range: $1,900 – $2,100 (aligned with hedge strikes)
- Duration: 39 days to 27MAR26 expiry

**Per 100 ETH (~$197K) economics over 39 days:**
- Strangle breakeven move: ±12.9%
- Expected 39d move at 96% RV: ±31.4% (1σ)
- Vol trade expected profit: ~$18,000-$22,000
- LP fee income (25-35% APR): ~$5,300-$7,400
- LP IL (at 96% RV): ~-$8,000 to -$12,000
- Net expected: **~$15,000-$17,400 (+7.6-8.8%)**

**Why highest conviction:**
- ETH has the biggest IV-RV gap (30+ pts)
- 27MAR26-2200-P has 26,904 OI — exceptional liquidity for scaling
- Strangle breakeven is comfortable vs expected moves
- LP range naturally matches hedge strikes

### Strategy 2: BTC "Range Fortress" — MODERATE CONVICTION

**Hedge (Deribit, deploy first):**
- Long BTC-27MAR26-70000-P
  - IV: 48.6% | Gap: -25.6 pts | Cost: $5,382/contract | OI: 4,690
- Long BTC-6MAR26-71000-C
  - IV: 49.4% | Gap: -24.8 pts | Cost: $1,722/contract | OI: 334
  - Note: 18-day expiry — plan to roll near 6MAR
- Combined: ~$7,104/BTC

**LP (on-chain, deploy second):**
- Pool: WBTC/USDC 30bps, Ethereum mainnet
- Range: $64,000 – $72,000
- Duration: 39 days (put hedge); 18 days (call hedge, then roll)

**Per 1.5 BTC (~$102K) economics over 39 days:**
- Vol trade expected profit: ~$7,000-$10,000
- LP fee income (20-30% APR): ~$2,200-$3,300
- LP IL: ~-$3,000 to -$5,000
- Hedge cost: ~$10,656
- Net expected: **~$5,500-$7,600 (+5.4-7.5%)**

**Why moderate vs high:**
- Smaller IV-RV gap than ETH
- Call hedge needs rolling at 6MAR (execution risk)
- Higher per-contract cost limits scaling

### Strategy 3: ETH "Quick Rotate" — OPPORTUNISTIC, 4-DAY

**Hedge (Deribit):**
- Long ETH-20FEB26-1975-P
  - IV: 64.5% | Gap: -31.6 pts | Cost: $52/contract | OI: 12,176
  - Breakeven: 2.6% move over 4 days
  - Expected 4d move at 96% RV: 10.0%

**LP:**
- Pool: WETH/USDC 5bps (tight, high-volume)
- Range: $1,925 – $2,025 (~±2.5%)
- 4-day hold, exit Feb 20

**Why opportunistic:**
- Highest probability single trade (expected move 4x breakeven)
- Extremely liquid (12K+ OI)
- Short duration limits capital commitment
- Quick reinvestment cycle

---

## Deployment Plan

1. Execute Deribit hedges FIRST (all option buys)
2. Deploy LP positions on-chain SECOND (WETH/USDC first, then WBTC/USDC)
3. Strategy 3 (quick rotate) exits Feb 20 — reassess for rollover
4. Monitor net delta daily; rebalance if ±5% notional breached
5. Strategy 2 call hedge rolls at 6MAR expiry → buy new 27MAR26 call
6. Full portfolio review at 14-day mark (Mar 2)
7. All positions close/roll by 27MAR26

## Risk Notes

- **Vol regime shift:** If RV compresses toward IV, vol trade edge shrinks. Monitor daily RV.
- **Gas costs:** ETH mainnet LP entry/exit + rebalances. Budget 0.01-0.05 ETH per LP operation.
- **Correlation risk:** BTC and ETH positions are correlated. A crypto-wide vol crush hits both.
- **Liquidity risk:** All selected strikes have strong OI. Entry/exit should be clean.
- **All strategies are defined-risk:** Long options only, no naked shorts. Max loss is premiums paid + LP IL.
- **Delta management:** LP delta shifts as price moves. Perp hedges on Deribit can flatten delta if needed.

## Data Sources
- Deribit public API: options books, DVOL, historical vol (pulled 2026-02-16 18:52 UTC)
- CoinGecko: spot prices
- Fee APR estimates: based on typical Uniswap V3 concentrated LP ranges for WETH/USDC and WBTC/USDC 30bps pools
