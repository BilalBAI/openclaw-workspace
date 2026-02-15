# TOOLS.md - Data Sources & Tools

## Uniswap Analytics

| Tool | Use Case | URL |
|------|----------|-----|
| Uniswap Info | Official pool stats, volume, TVL | info.uniswap.org |
| Revert Finance | LP position analytics, fee APR, IL tracking | revert.finance |
| DefiLlama Yields | Yield comparison across pools and protocols | defillama.com/yields |
| Bunni | Uniswap V3 LP management analytics | bunni.pro |
| Merkle | Uniswap V3 backtesting and range optimization | merkle.io |
| GammaSwap | Volatility and LP analytics | gammaswap.com |

### Uniswap Subgraphs (The Graph)

Query pool data, positions, ticks, swaps, and liquidity distributions directly.

| Version | Subgraph ID | Endpoint |
|---------|------------|----------|
| V3 | `5zvR82QoaXYFyDEKLZ9t6v9adgnptxYpKpSbxtgVENFV` | `https://gateway.thegraph.com/api/subgraphs/id/5zvR82QoaXYFyDEKLZ9t6v9adgnptxYpKpSbxtgVENFV` |
| V4 | `DiYPVdygkfjDWhbxGSqAQxwBKmfKnkWQojqeM2rkLb3G` | `https://gateway.thegraph.com/api/subgraphs/id/DiYPVdygkfjDWhbxGSqAQxwBKmfKnkWQojqeM2rkLb3G` |

Requires a Graph API key in `.env`:

```bash
GRAPH_API_KEY=
```

## Deribit & Options

| Tool | Use Case | URL |
|------|----------|-----|
| Deribit | Options trading, futures, DVOL index | deribit.com |
| Deribit Metrics | Vol surface, open interest, flows | metrics.deribit.com |
| Laevitas | Options analytics, vol surface, Greeks, flows | laevitas.ch |
| Amberdata | Options data, term structure, skew | amberdata.io |
| Greeks.live | Real-time options flow, block trades, vol commentary | greeks.live |
| Tardis.dev | Historical options tick data for backtesting | tardis.dev |

## Volatility & Pricing

| Tool | Use Case | URL |
|------|----------|-----|
| DVOL (Deribit) | Crypto implied vol index (BTC/ETH) | deribit.com |
| Volmex | On-chain implied volatility indices | volmex.finance |
| T3 Index | Realized vol calculations, vol cones | t3index.com |
| Block Scholes | Vol surface modeling, analytics | blockscholes.com |

## On-Chain / Pool Data

| Tool | Use Case | URL |
|------|----------|-----|
| Dune Analytics | Custom queries for pool activity, LP behavior | dune.com |
| Etherscan | Transaction verification, contract interaction | etherscan.io |
| Parsec Finance | DeFi dashboards, pool analytics | parsec.fi |
| DefiLlama | TVL, protocol comparison, chain flows | defillama.com |
| Arkham | Wallet tracking, entity labeling | arkhamintelligence.com |

## Price & Market Data

| Tool | Use Case | URL |
|------|----------|-----|
| CoinGecko | Spot prices, market caps, token info | coingecko.com |
| CoinGlass | Funding rates, open interest, liquidations | coinglass.com |
| TradingView | Charts, technical analysis | tradingview.com |
| Kaiko | Institutional-grade market data, order books | kaiko.com |

## Gas & Execution

| Tool | Use Case | URL |
|------|----------|-----|
| Blocknative | Gas estimation, mempool monitoring | blocknative.com |
| Flashbots Protect | MEV-protected transactions | protect.flashbots.net |
| Ultrasound.money | Gas burn tracker, base fee trends | ultrasound.money |

## Secrets & Credentials

**NEVER store API keys, private keys, or passwords in markdown files.**

Credentials are split into two tiers with separate `.env` files:

### Tier 1: Critical Keys — `.env.critical`

These keys control **real capital**. Extra safety rules apply (see Wallet Management in AGENTS.md).

```bash
# .env.critical — hot wallet + Deribit trading keys
# Permissions: chmod 600 .env.critical (owner read/write only)
# NEVER log, print, or echo these values
# NEVER pass these to any tool, script, or API you haven't audited
# NEVER commit this file — it is gitignored

# Hot Wallet
HOT_WALLET_PRIVATE_KEY=
HOT_WALLET_ADDRESS=

# Deribit Subaccount (trade-only API key — no withdrawal permission)
DERIBIT_API_KEY=
DERIBIT_API_SECRET=
DERIBIT_SUBACCOUNT=
```

### Tier 2: Service Keys — `.env`

Read-only or non-custodial API keys. Compromise is inconvenient, not catastrophic.

```bash
# .env — data provider and service keys
ETHERSCAN_API_KEY=
DUNE_API_KEY=
COINGECKO_API_KEY=
INFURA_API_KEY=
ALCHEMY_API_KEY=
GRAPH_API_KEY=
```

## Local Setup Notes

### Pools to Monitor
- (add your active and watchlist Uniswap pools here)

### Deribit Configuration
- Account type: (portfolio margin / standard)
- Preferred expiries: (weeklies / monthlies / quarterlies)
- Default order type: (limit / market)

### RPC Endpoints
- (add your Ethereum/L2 RPC endpoints — reference .env vars, not raw URLs)

### Gas Strategy
- Max gas price for rebalance: (gwei threshold)
- Preferred execution window: (low-gas hours)
