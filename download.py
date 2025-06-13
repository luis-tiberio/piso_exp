from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import datetime
import os
import shutil
from webdriver_manager.chrome import ChromeDriverManagerfrom selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

download_dir = "/tmp"
os.makedirs(download_dir, exist_ok=True)

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--window-size=1920,1080")

prefs = {
    "download.default_directory": download_dir,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
}
chrome_options.add_experimental_option("prefs", prefs)

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)


def login(driver):
    driver.get("https://spx.shopee.com.br/")
    try:
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, '//*[@placeholder="Ops ID"]')))
        driver.find_element(By.XPATH, '//*[@placeholder="Ops ID"]').send_keys('Ops35683')
        driver.find_element(By.XPATH, '//*[@placeholder="Senha"]').send_keys('@Shopee123')
        WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div[2]/div/div/div[1]/div[3]/form/div/div/button'))
        ).click()

        time.sleep(15)
        try:
            popup = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "ssc-dialog-close"))
            )
            popup.click()
        except:
            print("Nenhum pop-up foi encontrado.")
            driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.ESCAPE)
    except Exception as e:
        print(f"Erro no login: {e}")
        driver.quit()
        raise


def get_data(driver):
    try:
        driver.get("https://spx.shopee.com.br/#/staging-area-management/list/outbound")
        time.sleep(8)
        driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[2]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div/div/span/span/button').click()
        time.sleep(8)
        WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[4]/ul/li[1]/span/div/div/span'))
        ).click()

        driver.get("https://spx.shopee.com.br/#/taskCenter/exportTaskCenter")
        time.sleep(15)

        # 👉 Mantendo o botão de download exatamente como no seu código original:
        WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="fms-container"]/div[2]/div[2]/div/div/div/div[1]/div[8]/div/div[1]/div/div[2]/div[1]/div[1]/div[2]/div/div/div/table/tbody[2]/tr[1]/td[7]/div/div/button'))
        ).click()

        time.sleep(15)  # Aguarda o download
        rename_downloaded_file(download_dir)

    except Exception as e:
        print(f"Erro ao coletar dados: {e}")
        driver.quit()
        raise

def rename_downloaded_file(download_dir):
    try:
        files = [f for f in os.listdir(download_dir) if os.path.isfile(os.path.join(download_dir, f))]
        files = [os.path.join(download_dir, f) for f in files]
        newest_file = max(files, key=os.path.getctime)

        current_hour = datetime.datetime.now().strftime("%H")
        new_file_name = f"EXP-{current_hour}.csv"
        new_file_path = os.path.join(download_dir, new_file_name)

        if os.path.exists(new_file_path):
            os.remove(new_file_path)

        shutil.move(newest_file, new_file_path)
        print(f"Arquivo salvo como: {new_file_path}")
    except Exception as e:
        print(f"Erro ao renomear o arquivo: {e}")

def main():
    try:
        login(driver)
        get_data(driver)
        print("Download finalizado com sucesso.")
    except Exception as e:
        print(f"Erro: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
