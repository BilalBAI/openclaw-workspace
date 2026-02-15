# TOOLS.md - Data Sources & Tools

## On-Chain Analytics

| Tool | Use Case | URL |
|------|----------|-----|
| DefiLlama | TVL, yields, protocol revenue, chain comparison | defillama.com |
| Dune Analytics | Custom on-chain queries, dashboards | dune.com |
| Nansen | Smart money tracking, wallet labels, token flows | nansen.ai |
| Glassnode | Bitcoin on-chain metrics, MVRV, NUPL, SOPR | glassnode.com |
| Artemis | Protocol revenue, developer activity, fundamentals | artemis.xyz |
| Token Terminal | Protocol financials, P/F ratios, revenue | tokenterminal.com |

## Price & Market Data

| Tool | Use Case | URL |
|------|----------|-----|
| CoinGecko | Price data, market caps, volume, token info | coingecko.com |
| CoinMarketCap | Market overview, rankings, exchange data | coinmarketcap.com |
| TradingView | Charts, technical analysis, alerts | tradingview.com |
| CoinGlass | Derivatives data, funding rates, open interest, liquidations | coinglass.com |

## Macro & Traditional Finance

| Tool | Use Case | URL |
|------|----------|-----|
| FRED | Federal Reserve economic data (rates, M2, CPI) | fred.stlouisfed.org |
| CME FedWatch | Fed rate expectations, meeting probabilities | cmegroup.com |
| TradingEconomics | Global macro indicators, calendar | tradingeconomics.com |
| ForexFactory | Economic calendar, event impact ratings | forexfactory.com |

## DeFi-Specific

| Tool | Use Case | URL |
|------|----------|-----|
| DefiLlama Yields | Yield farming opportunities across chains | defillama.com/yields |
| Revert Finance | Uniswap v3 LP analytics | revert.finance |
| Eigenphi | MEV, arbitrage, sandwich attack tracking | eigenphi.io |
| L2Beat | L2 TVL, risk assessment, comparison | l2beat.com |

## Chain Explorers

| Chain | Explorer |
|-------|----------|
| Ethereum | etherscan.io |
| Arbitrum | arbiscan.io |
| Base | basescan.org |
| Optimism | optimistic.etherscan.io |
| Polygon | polygonscan.com |
| BSC | bscscan.com |
| Solana | solscan.io |
| Cosmos | mintscan.io |

## News & Sentiment

| Source | Use Case |
|--------|----------|
| The Block | Institutional crypto news, data dashboards |
| Blockworks | Macro-crypto intersection, research |
| DL News | Breaking crypto news |
| Crypto Twitter/X | Real-time sentiment, alpha leaks |
| LunarCrush | Social sentiment metrics |
| Alternative.me | Fear & Greed Index |

## Governance & Research

| Tool | Use Case |
|------|----------|
| Tally | On-chain governance tracking |
| Snapshot | Off-chain governance votes |
| Messari | Research reports, protocol profiles |
| Delphi Digital | Deep research, sector reports |

## Secrets & Credentials

**NEVER store API keys, private keys, or passwords in markdown files.**

All sensitive values go in `.env` files (gitignored). Reference them by variable name here.

```bash
# .env — create this file locally, never commit it
DUNE_API_KEY=
NANSEN_API_KEY=
GLASSNODE_API_KEY=
COINGECKO_API_KEY=
ETHERSCAN_API_KEY=
ARBISCAN_API_KEY=
BASESCAN_API_KEY=
POLYGONSCAN_API_KEY=
BSCSCAN_API_KEY=
```

## Local Setup Notes

### Wallets to Track
- (add whale/smart money public addresses here — public addresses are safe to track)

### Custom Alerts
- (add your alert configurations here)

### Preferred Dashboards
- (add your go-to Dune/Nansen dashboards here)
