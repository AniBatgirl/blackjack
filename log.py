import logging

FORMAT='%(asctime)s - %(name)s -%(message)s'
logging.basicConfig(
    format=FORMAT,
    level=logging.INFO,
    filename="log.log",
    filemode="a"

)

logging.info("info")
logging.warning("ahoj")
logging.error("eror")
logging.critical("crit")
