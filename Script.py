"""
Important Notes:

Whenever you add a new group ID to the GROUPS_IDS tuple, 
you must also add a corresponding topic ID to the TOPICS_IDS tuple.

The order of the group IDs in GROUPS_IDS must match the order of the topic IDs in TOPICS_IDS. 
For example, the first group ID in GROUPS_IDS will correspond to the first topic ID in TOPICS_IDS, 
the second group ID will correspond to the second topic ID, and so on.

Failing to match the number of group IDs with topic IDs will result in errors when sending messages.
"""

from time import sleep
from requests import get, exceptions

# Constants
API_URL = "https://progres.mesrs.dz/api/infos"
HEADERS = {"Source": "Python Script"}
REQUEST_TIMEOUT = 15

BOT_TOKEN = "YOUR_BOT_TOKEN"
GROUPS_IDS = ("GROUP_ID", )
TOPICS_IDS = ("TOPIC_ID", )
GROUPS_LENGTH = len(GROUPS_IDS)

THRESHOLD = 5

LOOP_TIME = 10
# End Constants

def sendMessage(text):
  print(text)
  try:
    for index in range(GROUPS_LENGTH):
      response = get(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={GROUPS_IDS[index]}&message_thread_id={TOPICS_IDS[index]}&text={text}&disable_notification=true")
      if response.status_code == 200:
        print(f"Sent To Telegram - Group ID: {GROUPS_IDS[index]}")
      else:
        print(f"Telegram Returned: {response.status_code} - Group ID: {GROUPS_IDS[index]}")
      sleep(1)
  except Exception as E:
    print("Failed 'sendMessage' Function: ", E)

sendMessage("🔆 تمت إعادة تشغيل البوت 🔆")

# Variables
apiIsUp = True

botStartedNow = True

thresholdCounter = 1
# End Variables

while True:
  try:
    get(API_URL, headers=HEADERS, timeout=REQUEST_TIMEOUT)
    
    if thresholdCounter > 1: 
      thresholdCounter -= 1
    
    if (botStartedNow and thresholdCounter == 1) or (not apiIsUp and thresholdCounter == 1):
      sendMessage("✅ بروغرس يشتغل ✅")
      botStartedNow = False
      apiIsUp = True
  except exceptions.RequestException:    
    if thresholdCounter < THRESHOLD:
      thresholdCounter += 1
    
    if apiIsUp and thresholdCounter == THRESHOLD:
      sendMessage("❌ بروغرس متوقف ❌")
      apiIsUp = False
  except Exception as E:
    print("Unexpected Error: ", E)

  sleep(LOOP_TIME)
