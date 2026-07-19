import logging
import colorama
from colorama import Fore, Style

colorama.init(autoreset=True)

class ColoredFormatter(logging.Formatter):
    """Custom formatter to add colors to logs"""
    
    COLORS = {
        logging.DEBUG: Fore.CYAN,
        logging.INFO: Fore.GREEN,
        logging.WARNING: Fore.YELLOW,
        logging.ERROR: Fore.RED,
        logging.CRITICAL: Fore.RED + Style.BRIGHT,
    }

    def format(self, record):
        color = self.COLORS.get(record.levelno, Fore.WHITE)
        message = super().format(record)
        return f"{color}{message}{Style.RESET_ALL}"

def setup_logger(name="NetGuard"):
    """Configure et retourne un logger"""
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Console Handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    
    formatter = ColoredFormatter('%(asctime)s - [%(levelname)s] - %(message)s', datefmt='%H:%M:%S')
    ch.setFormatter(formatter)
    
    # Éviter d'ajouter plusieurs handlers si le logger existe déjà
    if not logger.handlers:
        logger.addHandler(ch)
        
    return logger

logger = setup_logger()
