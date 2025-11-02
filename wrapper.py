import os
import time
from datetime import datetime

while True:
    os.system("python main.py")  # starts bot
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Bot stopped. Restarting in 2 seconds...")
    time.sleep(2)
