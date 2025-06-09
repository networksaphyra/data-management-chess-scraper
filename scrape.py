import csv
import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

usernames = [
  "KAYatDay","CryBabyCarly","yneves","jfourmes","Bingowingsgal",
  "TrudyNini","PawnMorphy","chessed64squares","jsinanan","MiaSahely",
  "JonLiMusic","Laurarrgh","sassywater1","berkantercan","heyitsp",
  "tcutter","Sneakiest_Of_Snakes","dimailuka","olita21","BUITRONGHAO",
  "jasonpsweeney","emircan","movingwithmat","Dicomaniaque","chessonearth",
  "JasminOcelli","supermatt69","Pes_chess1","Sashastrong","roaring_lion23",
  "smalltowngoose","th3d4rkness","HiNope","afbdreds","BrandonBizzell",
  "LifeIsAllAboutChess23","Mashenka97","PedroPinhata","anishnaik12","ItsMrSkyChess",
  "ViniMarques","MasterDallas","sigmaMaleBrain","nelsi","voloshanenko",
  "AlexandraMtz","Grigalashvili","Alexxorio","kamnur_0911","Henry940622"
]

options = Options()
options.headless = False
options.add_argument("--window-size=1920,1080")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

results = []

def scrape_rapid_stats(username, retries=2):
  for attempt in range(retries):
    try:
      url = f"https://www.chess.com/member/{username}/stats/rapid?days=0"
      driver.get(url)

      wait = WebDriverWait(driver, 15)
      wait.until(lambda d: d.find_element(By.CLASS_NAME, "rating-block-container").text.strip() != "")
      rating_block = driver.find_element(By.CLASS_NAME, "rating-block-container")
      rapid_rating = rating_block.text.strip().split("\n")[0]

      containers = wait.until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "transition-up-container"))
      )

      valid_containers = [
        el for el in containers if 'icon-block-large-content' in el.get_attribute("class")
      ]

      if len(valid_containers) >= 2:
        second_container = valid_containers[1]
        child_div = second_container.find_element(By.TAG_NAME, "div")
        raw_games_text = child_div.text.strip()
        rapid_games = raw_games_text.split()[0]
      else:
        raise Exception("Not enough valid containers found")

      return [rapid_rating, rapid_games]

    except Exception as e:
      print(f"Attempt {attempt+1} failed for {username}: {e}")
      time.sleep(2 + random.random())

  return [None, None]

for username in usernames:
  rating, games = scrape_rapid_stats(username)

  if rating is None or games is None:
    print(f"{username} ultimately failed. Marking as N/A.")
    rating = "N/A"
    games = "N/A"
  else:
    print(f"{username}: Rapid Rating={rating}, Rapid Games={games}")

  results.append([username, rating, games])
  time.sleep(1.5 + random.random())

driver.quit()

with open("chess_rapid_data.csv", "w", newline="", encoding="utf-8") as f:
  writer = csv.writer(f)
  writer.writerow(["Username", "Rapid Rating", "Rapid Games Played"])
  writer.writerows(results)

print("All data saved to chess_rapid_data.csv")
