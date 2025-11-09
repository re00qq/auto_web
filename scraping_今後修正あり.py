from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime
import time

driver = webdriver.Chrome()

target_url = 'https://www.jrupo.com/page/service/login.html'
driver.get(target_url)

# ページが完全に読み込まれるまで待機（最大で10秒）
wait = WebDriverWait(driver, 10)

# search_box = wait.until(EC.presence_of_element_located((By.ID, 'APjFqb')))
 
# # 検索ボックスを見つけてキーワードを入力し、Enterを押す
# search_box = driver.find_element(By.ID, 'APjFqb')
# search_box.send_keys('ジョブルポ')
# search_box.send_keys(Keys.RETURN)

# # ページクリック
# selector = '{{ CSSセレクタ }}'
# element = driver.find_element_by_css_selector(selector)
# element.click()
 
driver.find_element(By.NAME,"username").send_keys("任意のメールアドレス")
time.sleep(4)
# NAME属性が”password”であるHTML要素を取得し、パスワード文字列をキーボード送信
driver.find_element(By.ID,"password").send_keys('任意のパスワード')
time.sleep(3)
# CLASS属性が”sessions_button--wide”であるHTML要素を取得してクリック
driver.find_element(By.ID,'login').click()
time.sleep(3)
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

# dates = driver.find_elements(By.XPATH, '//*[@id="list"]/div/div[2]/div/table')

# # 平日だけをクリック
# for date in dates:
#     date_text = date.text
#     date_obj = datetime.datetime.strptime(date_text.strip(), '%d日')  # 日付フォーマットに合わせて変更
#     if date_obj.weekday() < 5:  # 平日かどうかをチェック（0:月曜日, 4:金曜日）

# # 特定の要素までスクロール
# element = driver.find_element(By.CSS_SELECTOR,'#list > div > div.row > div > table > tbody > tr:nth-child(1) > td.text-right > div > div.margin_top_8 > button')
# scroll_to_element(element)

# class名からtable要素を取得
table = driver.find_element(By.CSS_SELECTOR, "table.table.table-hover.vert-align")

# テーブルの行（trタグ）を取得
rows = table.find_elements(By.TAG_NAME, "tr")

# # 各行のセル（tdタグ）を取得して出力
# for row in rows:
#     cells = row.find_elements(By.TAG_NAME, "td")
#     if cells:  # ヘッダー行（th）をスキップ
#         data = [cell.text for cell in cells]
#     date_text = cells[0].text.strip()  # 1列目の日付
#     try:
#         date_obj = datetime.strptime(date_text, "%d")
#         weekday = date_obj.weekday()  # 0=月曜, 6=日曜
#         if weekday < 5:
#             print(f"{date_text} は平日です。")
#         else:
#             print(f"{date_text} は週末（土日）です。")
#     except ValueError:
#         print(f"無効な日付: {date_text}")

for i in range(len(rows)):
    # DOM変化でStaleElementを避けるため、ループごとにtrを再取得
    table = driver.find_element(By.CSS_SELECTOR, "table.table.table-hover.vert-align")
    rows = table.find_elements(By.TAG_NAME, "tr")
    row = rows[i]

    date_str = row.get_attribute("data-date")

    # 文字列を日付に変換
    date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d")

    # 平日判定
    if date_obj.weekday() < 5:
        print(f"{date_str} は平日です")
        
        try:
            # # CSSセレクタでボタンを取得
            # button = row.find_element(By.XPATH, '//*[@id="list"]/div/div[2]/div/table/tbody/tr/td[1]/div/div[1]/button')
            # WebDriverWait(driver, 10).until(EC.element_to_be_clickable(button))
            # button.click()
            # time.sleep(4)
            
            button = row.find_element(By.XPATH, './/td[1]/div/div[1]/button')

            # ボタンが画面内にあるようスクロール
            driver.execute_script("arguments[0].scrollIntoView(true);", button)
            time.sleep(2)

            # JavaScriptでクリック
            driver.execute_script("arguments[0].click();", button)
            
            # 勤怠入力
            punch_in = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, 'js-punch-in-time'))
            )
            
            punch_in.clear()
            punch_in.send_keys('09:30')
            time.sleep(1)

            punch_out = driver.find_element(By.ID, 'js-punch-out-time')
            punch_out.clear()
            punch_out.send_keys('18:30')
            time.sleep(1)

            break_time = driver.find_element(By.XPATH, '//*[@id="js-attendance-section"]/div[2]/div[2]/div/div/input')
            break_time.clear()
            break_time.send_keys('01:00')
            time.sleep(1)

            save_button = driver.find_element(By.XPATH, '/html/body/div[3]/div/div/div[5]/button[1]')
            save_button.click()
            time.sleep(2)
            

        except Exception as e:
            print(f"{date_str} の勤怠入力でエラー: {e}")
            driver.find_element(By.CLASS_NAME,'close').click()
            time.sleep(3)
            
    else:
        print(f"{date_str} は週末です")


# # スクロールを停止
# # stop_scrolling()
# # dates.click()

# # 勤怠入力
# element = WebDriverWait(driver, 10).until(
#     EC.element_to_be_clickable((By.ID, 'js-punch-in-time'))
# )
# element.send_keys('09:30')
# time.sleep(5)
# driver.find_element(By.ID, 'js-punch-out-time').send_keys('18:30')
# time.sleep(3)
# driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
# time.sleep(3)
# element1 = driver.find_element(By.XPATH, '//*[@id="js-attendance-section"]/div[2]/div[2]/div/div/input')
# element1.send_keys('01:00')
# time.sleep(3)
# element2 = driver.find_element(By.XPATH, '/html/body/div[3]/div/div/div[5]/button[1]')
# element2.click()
# time.sleep(4)

# # 再度スクロール
# resume_scrolling()

# # 1秒待機
# driver.implicitly_wait(4)



driver.quit()
