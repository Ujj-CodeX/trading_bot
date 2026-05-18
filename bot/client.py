import hmac
import hashlib
import time
import requests

from bot.logger_config import setup_logger


logger = setup_logger()

BASE_URL  = " https://testnet.binancefuture.com"

class BinanceClient:
    def __init__(self, api_key: str, api_secret: str):
        self.api_key = api_key
        self.api_secret = api_secret

        self.session = requests.Session()
        self.session.headers.update({
            "X-MBX-APIKEY": self.api_key

        })

    def _sign(self, params: dict) -> dict:
        """
        Binance ka rule: har request mein timestamp + signature chahiye.
        Signature = HMAC-SHA256(query_string, secret_key)
        Timestamp isliye: replay attack rokta hai (5 second window)
        """

        params["timestamp"] = int(time.time() * 1000)  # milliseconds
        query_string = "&".join([f"{k}={v}" for k, v in params.items()])
        signature = hmac.new(self.api_secret.encode("utf-8"), query_string.encode("utf-8"), hashlib.sha256).hexdigest()
        params["signature"] = signature
        return params
    
    def post(self, endpoint: str, params: dict) -> dict:
        signed_params = self._sign(params)
        logger.debug(f"Request → {endpoint} | params: { {k: v for k, v in params.items() if k != 'signature'} }")

        try:
            response = self.session.post(
                f"{BASE_URL}{endpoint}",
                params=signed_params,
                timeout=10
            )
            response.raise_for_status()       # 4xx/5xx pe exception uthao
            data = response.json()
            logger.debug(f"Response ← status={response.status_code} | body={data}")
            return data

        except requests.exceptions.HTTPError as e:
            error_body =  e.response.json() if e.response else {}
            logger.error(f"HTTP error | code={error_body.get('code')} msg={error_body.get('msg')}")
            raise
        except requests.exceptions.ConnectionError :
            logger.error("Network unreachable — check internet connection")
            raise

        except requests.exceptions.Timeout:
            logger.error("Request timed out — Binance might be slow or down")
            raise


    


