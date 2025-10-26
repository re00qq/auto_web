# サンプルコード
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime
import time

service = Service(executable_path='./chromedriver.exe')
driver = webdriver.Chrome(service=service)

target_url = 'https://www.jrupo.com/page/service/login.html'
driver.get(target_url)


# ページが完全に読み込まれるまで待機（最大で10秒）
#wait = WebDriverWait(driver, 10)
#search_box = wait.until(EC.presence_of_element_located((By.ID, 'APjFqb')))
 
# 検索ボックスを見つけてキーワードを入力し、Enterを押す
#search_box = driver.find_element(By.ID, 'APjFqb')
#search_box.send_keys('ジョブルポ')
#search_box.send_keys(Keys.RETURN)

#ページクリック
#selector = '{{ CSSセレクタ }}'
#element = driver.find_element_by_css_selector(selector)
#element.click()
 
driver.find_element(By.NAME,"username").send_keys("yokubo@urban-web.co.jp")
time.sleep(1)
# NAME属性が”password”であるHTML要素を取得し、パスワード文字列をキーボード送信
driver.find_element(By.ID,"password").send_keys('poi1poi1')
time.sleep(1)
# CLASS属性が”sessions_button--wide”であるHTML要素を取得してクリック
driver.find_element(By.ID,'login').click()
time.sleep(5)
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

driver.find_element(By.CLASS_NAME,'btn-primary').click()
time.sleep(3)

current_date = datetime.datetime.now()

# 特定の場所までスクロール

def scroll_to_element(element):
    driver.execute_script("arguments[0].scrollIntoView();", element)

# スクロールを停止
def stop_scrolling():
    driver.execute_script("window.scrollTo(0, 0);")

# 再度スクロール
def resume_scrolling():
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

dates = driver.find_elements(By.XPATH, '//*[@id="list"]/div/div[2]/div/table')

# 平日だけをクリック
for date in dates:
    date_text = date.text
    date_obj = datetime.datetime.strptime(date_text, '%d')  # 日付フォーマットに合わせて変更
    if date_obj.weekday() < 5:  # 平日かどうかをチェック（0:月曜日, 4:金曜日）

        # 特定の要素までスクロール
        element = driver.find_element(By.XPATH, '//*[@id="list"]/div/div[2]/div/table/tbody/tr[{}]/td[1]/div/div[1]/button')
        scroll_to_element(element)

        # スクロールを停止
        stop_scrolling()
        element.click()
        driver.find_element(By.ID, 'js-punch-in-time').send_keys('09:30')
        time.sleep(2)
        driver.find_element(By.ID, 'js-punch-out-time').send_keys('18:30')
        time.sleep(2)
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        time.sleep(3)
        element1 = driver.find_element(By.XPATH, '//*[@id="js-attendance-section"]/div[2]/div[2]/div/div/input')
        element1.send_keys('01:00')
        time.sleep(4)
        element2 = driver.find_element(By.XPATH, '/html/body/div[3]/div/div/div[5]/button[1]')
        element2.click()
        time.sleep(5)

        # 再度スクロール
        resume_scrolling()

        # 1秒待機
        driver.implicitly_wait(4)

driver.quit()