# ETHUSDT LP with Deribit Put Hedge — Strategy Understanding & Research Questions

This document captures my current understanding of your strategy and the key questions to investigate as we research and backtest. The goal is to evaluate a USDT-denominated payoff while maintaining crypto exposure only to open/close with the LP, and using a Deribit put as downside protection.

## 1) Understanding of the Strategy
- Asset and pool: ETH/USDT on Uniswap V3, with a concentrated liquidity position in a defined price range [P_lower, P_upper].
- Hedge: A Deribit put option (downside protection) is used to hedge the LP's downside risk when ETH price falls below P_lower.
- Denomination and objective: All PnL is benchmarked in USDT; the strategy aims to avoid crypto exposure by only acquiring crypto when opening the LP and selling crypto immediately when closing the LP, thereby keeping exposures in stablecoins.
- Payoff intuition:
  - Below P_lower: Put hedge pays to offset ETH losses in USDT; LP exposure in ETH is managed but hedged.
  - In range: Fees earned from the LP provide positive carry; put cost is amortized.
  - Above P_upper: Realized upside in USDT from selling ETH as it moves through the range; net USDT profit potential.
- Overall position: Synthetic structure that behaves like a synthetic covered call/short strangle with a protective put, but always evaluated in USDT terms.

## 2) Core Edge Questions (Current Hypotheses)
- Edge driver: Are LP fees and IL projections favorable enough to overcome put premium and hedging costs?
- Hedge sizing: What is the correct Deribit put notional to hedge ETH exposure across the range at entry and during movement?
- Range economics: How does width of [P_lower, P_upper] affect liquidity capture, IL risk, and hedge cost?
- Expiry alignment: Should put expiry align with expected LP holding period, and what roll strategy minimizes carry?
- Basis and settlement: Any basis risk between on-chain ETH and Deribit settlement (index-based) and how to model it?

## 3) Metrics to Track
- Net carry: Fees earned minus IL, minus hedge cost, minus gas.
- Delta/Gamma exposure: How the LP delta and hedge delta combine across price paths.
- Hedge effectiveness: Downside protection cost vs actual drawdown avoided.
- Break-even analysis: What range width and put strike/expiry give a positive carry.
- Roll efficiency: Costs and timing of rolling hedges vs rebalancing LP range.

## 4) Research Gaps / Questions for You
- What is your target annualized carry (net of hedges) you want to achieve from this strategy?
- Do you have a preferred put expiry window (e.g., weekly, monthly) to pair with typical LP holding periods?
- Should we allow dynamic rebalancing of the LP range in response to volatility regime, or fix the range for a given horizon?
- Are there preferred Deribit risk controls or budget limits (per-contract notional, max hedging cost per period)?
- Do you want to simulate in a fully synthetic way (no on-chain costs) at first, then layer gas and slippage, or incorporate those costs from the start?

## 5) Next Steps for Research
- Pull current ETH/USDT Uniswap V3 pool metrics: fee APR, liquidity, and expected IL for candidate ranges.
- Retrieve Deribit put pricing for candidate strikes near P_lower and with chosen expiries.
- Build a simple payoff calculator to show USDT PnL across price paths (below P_lower, within range, above P_upper).
- Run backtests with historical ETH price data to estimate carry and protection effectiveness.

## 6) Versioning
- This document will be updated as we gather data and refine assumptions. I will append findings and refinements rather than rewriting the file.

---
End of initial strategy research note.