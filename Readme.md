# Binance Futures Testnet — Trading Bot

A modular Python CLI application to place orders on Binance USDT-M Futures Testnet.
Supports Market, Limit, and Stop-Market order types with structured logging and full error handling.

---

## Project Structure

```
trading_bot/
├── bot/
│   ├── __init__.py
│   ├── client.py          # Binance API wrapper — signing, HTTP, error handling
│   ├── orders.py          # Order construction and placement logic
│   ├── validators.py      # Input validation before any API call
│   └── logging_config.py  # Dual-handler logger (file + console)
├── logs/
│   └── trading.log        # Auto-created on first run
├── cli.py                 # CLI entry point (argparse)
├── .env                   # API credentials — never commit this
├── .env.example           # Template for credentials
├── .gitignore
└── requirements.txt
```

---

## Setup

### 1. Get Testnet API Keys

- Go to [testnet.binancefuture.com](https://testnet.binancefuture.com)
- Login with GitHub → API keys are auto-generated
- Copy your API Key and Secret immediately

### 2. Clone and Install

```bash
git clone https://github.com/YOUR_USERNAME/trading_bot.git
cd trading_bot
pip install -r requirements.txt
```

### 3. Configure Credentials

```bash
cp .env.example .env
```

Open `.env` and fill in your keys:

```
BINANCE_API_KEY=your_api_key_here
BINANCE_API_SECRET=your_api_secret_here
```

---

## How to Run

### Market Order

```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.002
```

### Limit Order

```bash
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.002 --price 200000
```

### Stop-Market Order (bonus)

```bash
python cli.py --symbol BTCUSDT --side SELL --type STOP_MARKET --quantity 0.002 --stop-price 90000
```

### All Available Arguments

| Argument | Required | Description |
|---|---|---|
| `--symbol` | Yes | Trading pair, e.g. `BTCUSDT` |
| `--side` | Yes | `BUY` or `SELL` |
| `--type` | Yes | `MARKET`, `LIMIT`, or `STOP_MARKET` |
| `--quantity` | Yes | Order size in base asset |
| `--price` | For LIMIT | Limit price in USDT |
| `--stop-price` | For STOP_MARKET | Trigger price in USDT |

---

## Sample Output

```
┌─── Order Request ───────────────────┐
│  symbol        : BTCUSDT
│  side          : SELL
│  order_type    : LIMIT
│  quantity      : 0.001
│  price         : 200000.0
└────────────────────────────────────┘

2026-05-19 14:13:49 | INFO     | Placing order | LIMIT SELL BTCUSDT qty=0.001 price=200000.0
2026-05-19 14:13:51 | INFO     | Order success | id=13157835346 status=NEW executedQty=0.0000

┌─── Order Response ──────────────────┐
│  Order ID     : 13157835346
│  Status       : NEW
│  Orig Qty     : 0.0010
│  Executed Qty : 0.0000
│  Avg Price    : 0.00 USDT
└────────────────────────────────────┘

[SUCCESS] LIMIT SELL order placed!
```

---

## Architecture

```
User Input (CLI args)
       ↓
   cli.py          → parse args, print output, wire all layers
       ↓
validators.py      → validate symbol, side, type, quantity, price rules
       ↓                      ↘ raises ValueError early (no API call wasted)
   orders.py       → build correct params per order type
       ↓
   client.py       → HMAC-SHA256 sign, POST to Binance, handle HTTP errors
       ↓
Binance Testnet API (testnet.binancefuture.com)

logging_config.py watches every layer:
  → File handler  (DEBUG)  : logs/trading.log — full request/response detail
  → Console handler (INFO) : clean output for user
```

---

## Logging

All activity is logged to `logs/trading.log` automatically.

- `DEBUG` — full request params, raw API responses
- `INFO` — order placement and success confirmation
- `ERROR` — validation failures, HTTP errors, network issues

Example log entries:

```
2026-05-19 14:13:49 | INFO     | Placing order | LIMIT SELL BTCUSDT qty=0.001 price=200000.0
2026-05-19 14:13:49 | DEBUG    | Request → /fapi/v1/order | params: {'symbol': 'BTCUSDT', 'side': 'SELL', ...}
2026-05-19 14:13:51 | INFO     | Order success | id=13157835346 status=NEW executedQty=0.0000
```

---

## Error Handling

| Scenario | Handled By | Behaviour |
|---|---|---|
| Invalid symbol / side / type | `validators.py` | Prints clear message, exits before API call |
| Missing price on LIMIT order | `validators.py` | Explains exactly what is missing |
| Order value below 100 USDT | `validators.py` | Warns about Binance minimum notional |
| HTTP 400 / API error | `client.py` | Logs Binance error code and message |
| Network timeout | `client.py` | Logs timeout, exits cleanly |
| Missing API keys | `cli.py` | Warns user to check `.env` file |

---

## Assumptions

- Minimum order notional is 100 USDT as required by Binance Futures
- Supported symbols are `BTCUSDT`, `ETHUSDT`, `BNBUSDT` — easily extended in `validators.py`
- Testnet API keys may expire; regenerate at testnet.binancefuture.com if you get error `-2015`
- MARKET orders on testnet may show status `NEW` instead of `FILLED` due to limited testnet liquidity — this is expected behaviour on the testnet environment, not a bug

---

## Requirements

```
requests==2.31.0
python-dotenv==1.0.0
```

Install with:

```bash
pip install -r requirements.txt
```

---

## Notes on Testnet vs Production

This bot targets `https://demo-fapi.binance.com`. To point to production, change `BASE_URL` in `bot/client.py` to `https://fapi.binance.com` and replace credentials. No other code changes needed — this separation is intentional.