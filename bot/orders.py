from bot.client import BinanceClient
from bot.logger_config import setup_logger  

logger = setup_logger()

def place_order(
    client: BinanceClient,
    symbol: str,
    side: str,
    order_type: str,
    quantity: float,
    price: float = None,
    stop_price: float = None
) -> dict:
    
    params = {
        "symbol": symbol.upper(),
        "side": side.upper(),
        "type": order_type.upper(),
        "quantity": quantity,
    }

    if order_type.upper() == "LIMIT":
        params["price"] = price
        params["timeInForce"] = "GTC"  # Good Till Cancelled 

    if order_type.upper() == "STOP_MARKET":
        params["stopPrice"] = stop_price

    logger.info(f"Placing order | {order_type} {side} {symbol} qty={quantity} price={price}")
    result = client.post("/fapi/v1/order", params)
    logger.info(f"Order success | id={result['orderId']} status={result['status']} executedQty={result['executedQty']}")
    return result

    
