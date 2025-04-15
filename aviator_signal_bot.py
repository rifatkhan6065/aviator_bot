import requests
from bs4 import BeautifulSoup
import time

BOT_TOKEN = '7931347886:AAHiJHuiQXdXpEw-Zkexee5caC3-zWwKbEk'
CHAT_ID = '8146895791'

# Send message to Telegram
def send_signal(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    requests.post(url, data=data)

# Scrape multipliers from the site
def fetch_multipliers():
    try:
        res = requests.get("https://www.ck444.net/m/home?r=zjo4378")
        soup = BeautifulSoup(res.text, 'html.parser')

        # Adjust based on site's actual structure
        multiplier_tags = soup.find_all("span", class_="recent-multiplier")
        multipliers = [float(tag.text.replace("x", "")) for tag in multiplier_tags[:10]]
        return multipliers
    except Exception as e:
        print("Error fetching:", e)
        return []

# Logic to decide signals
def check_for_signals(multipliers):
    red_count = sum(1 for m in multipliers[:3] if m < 2)
    if red_count >= 3:
        send_signal("Signal: 3+ Reds! Big multiplier incoming. Get Ready!")
    
    high_count = sum(1 for m in multipliers[:5] if m > 5)
    if high_count >= 4:
        send_signal("Warning: Too many highs! Crash expected soon.")

# Main loop
while True:
    multipliers = fetch_multipliers()
    if multipliers:
        print("Multipliers:", multipliers)
        check_for_signals(multipliers)
    time.sleep(10)  # Run every 15 seconds