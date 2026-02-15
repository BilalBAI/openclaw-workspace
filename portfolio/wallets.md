# Wallets

_Public wallet info only. NEVER put private keys, seed phrases, or API secrets in this file._

## Hot Wallet

- **Address:** (set during bootstrap — reference `HOT_WALLET_ADDRESS` from `.env.critical`)
- **Chain:** Ethereum + L2s (Arbitrum, Base, Optimism, Polygon)
- **Purpose:** Uniswap LP operations, fee collection, rebalances
- **Max balance target:** $X (sweep excess to cold/vault)
- **Current balances:**
  - ETH: —
  - USDC: —
  - Other: —
- **Last checked:** —

## Deribit Subaccount

- **Subaccount:** (reference `DERIBIT_SUBACCOUNT` from `.env.critical`)
- **API permissions:** Trade only — no withdrawals
- **Purpose:** Options hedging, perpetual hedges, standalone strategies
- **Collateral:**
  - BTC: —
  - ETH: —
  - USDC: —
- **Margin utilization:** —%
- **Last checked:** —

## Cold Wallet / Vault

- **Address:** (user's cold storage — not managed by QuantBot)
- **Purpose:** Long-term storage, excess capital from hot wallet sweeps
- **Notes:** QuantBot has no access to this wallet. Sweep requests go through the user.
