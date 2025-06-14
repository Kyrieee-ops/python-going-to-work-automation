from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
import os

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def init_browser():
    options = Options() #optionsの呼び出し
    options.page_load_strategy = 'normal' #ページ全体がロードするまで待機
    # ブラウザを最大化した状態で起動するオプションを追加
    options.add_argument('--start-maximized')
    options.add_argument('--enable-webgl')  # WebGLを有効化
    options.add_argument('--ignore-gpu-blocklist')
    
    return webdriver.Chrome(options=options) # PATHが通っていればこれでOK

def login(browser):
    try:
        target_url = "https://id.jobcan.jp/users/sign_in"
        
        # 認証情報の取得
        user_email_value = os.getenv("JOBCAN_EMAIL")
        user_clientcode_value = os.getenv("JOBCAN_CLIENT_CODE")
        user_password_value = os.getenv("JOBCAN_PASSWORD")
        
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

        print("ログイン処理が完了しました")
        return True

    except Exception as e:
        print(f"エラーが発生しました: {e}")
    finally:
        pass

def attendance(browser):
    
    try:
        # 現在のウィンドウハンドルを記録
        original_window = browser.current_window_handle

        # 勤怠ページへ遷移
        attendance_link = browser.find_element(By.LINK_TEXT, "勤怠")
        attendance_link.click()
        print("勤怠入力画面に遷移しました")
       
        # 新しいウィンドウ/タブに切り替え
        WebDriverWait(browser, 10).until(
            lambda d: len(d.window_handles) > 1
        )
        browser.switch_to.window(browser.window_handles[1])
        print("新しいタブに切り替えました")

        # ここで新しいタブの要素を操作
        # 打刻修正画面の操作前に待機処理を入れておかないとエラーになる可能性があるため、5秒待機
        modify = WebDriverWait(browser, 5).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="sidemenu"]/div[2]/div/a[2]'))
        )
        # modify = browser.find_element(By.XPATH, '//*[@id="sidemenu"]/div[2]/div/a[2]')

        modify.click()
        print("打刻修正リンクをクリックしました")
        browser.save_screenshot('sucess_1.png')

        # 打刻修正リンククリック後、テキストボックスに入力できるまでに時間がかかるため、5秒待機処理
        working_time = WebDriverWait(browser, 5).until(
            EC.presence_of_element_located((By.NAME, "time"))
        )
        working_time.send_keys("0900")
        print("出勤時刻を入力しました")
        
        button = browser.find_element(By.ID, "insert_button")
        button.click()
        print("打刻処理が完了しました")
        browser.save_screenshot('sucess_2.png')
        return True

        
    except Exception as e:
        print(f"勤怠処理でエラーが発生しました: {str(e)}")
        browser.save_screenshot('error.png')
        return False
    
# メイン処理フロー
def main():
    browser = init_browser()
    # ログイン処理に成功したら、勤怠入力処理を行う
    try:
        if login(browser):
            attendance(browser)  # ログイン成功時のみ勤怠処理実行
    finally:
        browser.quit()  # 必ずブラウザを閉じる

# main関数を呼び出す
if __name__ == "__main__":
    load_dotenv()  # 環境変数読み込み
    main()
