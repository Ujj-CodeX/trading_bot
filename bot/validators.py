VALID_SYMBOLS = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'ADAUSDT', 'XRPUSDT', 'SOLUSDT', 'DOTUSDT', 'DOGEUSDT', 'AVAXUSDT', 'SHIBUSDT']
VALID_SIDES = ['BUY', 'SELL']
VALID_TYPES = ['LIMIT', 'MARKET', 'STOP_LOSS']
MIN_NOTIONAL = 100 # Binance minimum notional value for orders

def validate_order(symbol, side, order_type, quantity, price=None, stop_price=None):
    error = []

    if symbol not in VALID_SYMBOLS:
        error.append(f"Invalid symbol: {symbol}. Must be one of {VALID_SYMBOLS}")

    if side not in VALID_SIDES:
        error.append(f"Invalid side: {side}. Must be 'BUY' or 'SELL'")
    
    if order_type.upper() not in VALID_TYPES:
        error.append(f"Invalid order type: {order_type}. Must be one of {VALID_TYPES}")
    if quantity <= 0:
        error.append("Quantity must be greater than 0")


    if order_type.upper() == 'LIMIT':
        if price is None or price <= 0:
            error.append("Price must be greater than 0 for LIMIT orders")
        elif price * quantity < MIN_NOTIONAL:
            error.append(f"Notional value (price * quantity) must be at least {MIN_NOTIONAL} USDT")

    if order_type.upper() == 'STOP_MARKET':
        if stop_price is None or stop_price <= 0:
            error.append("Stop price must be greater than 0 for STOP_MARKET orders")

    if error:
        raise ValueError("\n ".join(error))
    