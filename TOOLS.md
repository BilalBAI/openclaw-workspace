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

All sensitive values go in `.env` files (gitignored). Reference them by variable name here.

```bash
# .env — create this file locally, never commit it
DERIBIT_API_KEY=
DERIBIT_API_SECRET=
DERIBIT_SUBACCOUNT=
ETHERSCAN_API_KEY=
DUNE_API_KEY=
COINGECKO_API_KEY=
INFURA_API_KEY=
ALCHEMY_API_KEY=
WALLET_ADDRESS=
# NEVER store private keys or seed phrases here — use hardware wallet or secure vault
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
