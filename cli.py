import argparse
import os
from dotenv import load_dotenv
from bot.client import BinanceClient
from bot.orders import place_order
from bot.validators import validate_order
from bot.logging_config import setup_logger

load_dotenv()
logger = setup_logger()

def print_request_summary(args):
    print("\n┌─── Order Request ───────────────────┐")
    fields = ["symbol", "side", "order_type", "quantity", "price", "stop_price"]
    for f in fields:
        val = getattr(args, f, None)
        if val is not None:
            print(f"│  {f:<14}: {val}")
    print("└────────────────────────────────────┘\n")

def print_order_response(resp: dict):
    print("┌─── Order Response ──────────────────┐")
    print(f"│  Order ID     : {resp.get('orderId')}")
    print(f"│  Status       : {resp.get('status')}")
    print(f"│  Orig Qty     : {resp.get('origQty')}")
    print(f"│  Executed Qty : {resp.get('executedQty')}")
    avg = resp.get('avgPrice', '0')
    print(f"│  Avg Price    : {avg} USDT")
    print("└────────────────────────────────────┘\n")

def main():
    parser = argparse.ArgumentParser(
        description="Binance Futures Testnet — Trading Bot",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("--symbol",     required=True,  help="e.g. BTCUSDT")
    parser.add_argument("--side",       required=True,  choices=["BUY","SELL"])
    parser.add_argument("--type",       required=True,  dest="order_type",
                        choices=["MARKET","LIMIT","STOP_MARKET"])
    parser.add_argument("--quantity",   required=True,  type=float)
    parser.add_argument("--price",      type=float,     default=None)
    parser.add_argument("--stop-price", type=float,     default=None, dest="stop_price")
    args = parser.parse_args()

    # Step 1: Validate
    try:
        validate_order(
            args.symbol, args.side, args.order_type,
            args.quantity, args.price, args.stop_price
        )
    except ValueError as e:
        logger.error(f"Validation failed:\n  {e}")
        print(f"\n[VALIDATION ERROR]\n  {e}\n")
        return

    print_request_summary(args)

    # Step 2: Load credentials
    api_key    = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")

    if not api_key or not api_secret:
        print("[ERROR] API keys not found. Check your .env file.")
        return

    # Step 3: Place order
    client = BinanceClient(api_key, api_secret)
    try:
        resp = place_order(
            client, args.symbol, args.side, args.order_type,
            args.quantity, args.price, args.stop_price
        )
        print_order_response(resp)
        print(f"[SUCCESS] {args.order_type} {args.side} order placed!\n")

    except Exception as e:
        logger.error(f"Order failed: {e}")
        print(f"\n[FAILED] Could not place order. See logs/trading.log for details.\n")

if __name__ == "__main__":
    main()