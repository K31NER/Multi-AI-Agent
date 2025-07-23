import logging

def init_logger():
    logging.basicConfig(
        filemode="a",
        filename="Costos.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )