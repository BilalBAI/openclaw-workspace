import json, urllib.request, datetime

path = "/home/bilal/.openclaw/workspace/.crypto_prices.json"
try:
    data = json.load(open(path))
except:
    data = {}

ids = ["bitcoin","ethereum","solana","binancecoin","ripple","dogecoin","uniswap","aave","lido-dao","hyperliquid"]
url = "https://api.coingecko.com/api/v3/simple/price?ids=" + ",".join(ids) + "&vs_currencies=usd&include_24hr_change=true"

req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req) as f:
    new = json.loads(f.read().decode())

out = {}
for k in ids:
    price = new.get(k, {}).get("usd")
    change24 = new.get(k, {}).get("usd_24h_change")
    last = data.get(k, {}).get("last_check_price", price)
    if last and last != 0:
        since_last = (price - last) / last * 100
    else:
        since_last = 0.0
    out[k] = {"usd": price, "usd_24h_change": change24, "since_last": since_last}

# Update the file
for k, v in out.items():
    data[k] = {
        "usd": v["usd"],
        "usd_24h_change": v["usd_24h_change"],
        "last_check_price": v["usd"],
        "last_check_time": datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "yesterday_price": data.get(k, {}).get("last_check_price", v["usd"])
    }

with open(path, "w") as f:
    json.dump(data, f, indent=2)

print(json.dumps(out, indent=2))
