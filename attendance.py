from logging import log
from selenium import webdriver
from time import sleep
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from dotenv import load_dotenv
import os


options = Options() #optionsの呼び出し
options.page_load_strategy = 'normal' #ページ全体がロードするまで待機
# ブラウザを最大化した状態で起動するオプションを追加
options.add_argument('--start-maximized')

options.add_argument('--enable-webgl')  # WebGLを有効化
options.add_argument('--ignore-gpu-blocklist')
browser = webdriver.Chrome(options=options)  # PATHが通っていればこれでOK

load_dotenv()  # .envファイルを読み込み

# 認証情報の取得
user_email_value = os.getenv("JOBCAN_EMAIL")
user_clientcode_value = os.getenv("JOBCAN_CLIENT_CODE")
user_password_value = os.getenv("JOBCAN_PASSWORD")

def main():
    target_url = "https://id.jobcan.jp/users/sign_in"

    try:
        #ブラウザオープン
        browser.get(target_url) 

        # スタッフコード入力フィールドを特定
        user_email = browser.find_element(By.ID,  "user_email")
        user_email.send_keys(user_email_value)

        # 「複数の会社に登録されていますか？」リンクをクリック
        company_link = browser.find_element(By.ID, "client_code_link")
        company_link.click()
        
        # 会社コード入力欄が表示されるまで待機
        user_clientcode = browser.find_element(By.ID, "user_client_code")
        user_clientcode.send_keys(user_clientcode_value)

        # パスワード入力フィールドを特定
        user_password = browser.find_element(By.ID, "user_password")
        user_password.send_keys(user_password_value)

        # ログインボタンを特定
        login_button = browser.find_element(By.NAME, "commit")
        login_button.click()

        sleep(60)
        print("ログイン処理が完了しました")

    except Exception as e:
        print(f"エラーが発生しました: {e}")
    finally:
        pass

# main関数を呼び出す
if __name__ == "__main__":
    main()
