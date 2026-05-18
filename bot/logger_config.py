import logging
import os

def setup_logger(name: str = "trading_bot" ) -> logging.Logger:
    os.makedirs("logs", exist_ok=True)

    logger =  logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if logger.handlers:
        return logger
    

    # file handler at debug level
    fh =  logging.FileHandler("logs/trading_bot.log")
    fh.setLevel(logging.DEBUG)
    

    # console handler at info level , give user a clean output without debug info
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    fmt = logging.Formatter("%(asctime)s |  %(levelname)-8s  | %(message)s" ,
                            datefmt="%Y-%m-%d %H:%M:%S")
    fh.setFormatter(fmt)
    ch.setFormatter(fmt)

    logger.addHandler(fh)
    logger.addHandler(ch)

    




    return logger