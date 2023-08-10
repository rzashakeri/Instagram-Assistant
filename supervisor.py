import subprocess
import time
from logging import getLogger

logger = getLogger(__name__)

while True:
    subprocess.call(["python", "main.py"])
    logger.info("Instagram Assistant has been started")
    time.sleep(0.5)
