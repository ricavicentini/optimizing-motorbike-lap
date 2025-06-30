import logging
import os

def setup_logger(name='lapopt', log_dir='outputs/logs'):
    os.makedirs(log_dir, exist_ok=True)
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(logging.Formatter('%(asctime)s — %(levelname)s — %(message)s'))
    logger.addHandler(ch)

    # File handler
    fh = logging.FileHandler(os.path.join(log_dir, f'{name}.log'))
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(logging.Formatter('%(asctime)s — %(levelname)s — %(module)s — %(message)s'))
    logger.addHandler(fh)

    return logger
