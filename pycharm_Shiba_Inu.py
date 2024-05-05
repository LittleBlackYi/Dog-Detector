from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.action_chains import ActionChains
import os
import requests

try:
    PATH = "/Applications/chromedriver-mac-arm64/chromedriver"
    s = Service(PATH)
    driver = webdriver.Chrome(service=s)
    driver.get("https://www.google.com/imghp?hl=zh-TW&tab=ri&ogbl")

    search = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="APjFqb"]'))
    )
    keyword = "Shiba Inu"
    search.send_keys(keyword)
    search.send_keys(Keys.RETURN)

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "YQ4gaf"))
    )
    print("找到了")
    # 點擊第一張圖片
    first_image = driver.find_element(By.CLASS_NAME, 'mNsIhb')
    actions = ActionChains(driver)
    actions.click(first_image)
    actions.perform()

    # 資料夾路徑
    path = os.path.join(keyword)
    print("path =", path)
    os.mkdir(path)

    # 點擊下一張圖片的按鈕 80 次
    for i in range(80):
        time.sleep(1)
        next_page = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="Sva75c"]/div[2]/div[2]/div[2]/div[2]/c-wiz/div/div/div/div/div[1]/div/div[2]/button[2]'))
        )
        next = ActionChains(driver)
        next.click(next_page)
        next.perform()
        print("No.", i)

        try:
            # 舊版 selenium 寫法為 driver.find_elements_by_css_selector('.sFlh5c.pT0Scc.iPVvYb')
            # 要用單引號，不然會報錯
            # 這裡的 class name 有很多個，所以要用 CSS_SELECTOR，並用 . 來連接
            img = driver.find_element(By.CSS_SELECTOR, '.sFlh5c.pT0Scc.iPVvYb')
            response = requests.get(img.get_attribute("src"), headers={'User-Agent': 'Mozilla/5.0'})
            save_as = os.path.join(path, keyword + str(i) + '.jpg')
            with open(save_as, 'wb') as f:
                f.write(response.content)
        except Exception as e:
            print(f"Error at image {i}: {e}")

except WebDriverException as e:
    print(e.stacktrace)
finally:
    driver.quit()  # 確保瀏覽器在程式結束時關閉
