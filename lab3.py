import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup

# Dövrün idarə olunması üçün dəyişən
ugurlu_giris = False

while not ugurlu_giris:
    # 1. İstifadəçi məlumatlarını daxil edin
    istifadeci_adi = input("İstifadəçi adınızı daxil edin: ")
    parol = input("Şifrənizi daxil edin: ")

    try:
        # 2. ChromeDriver-i başladın
        driver = webdriver.Chrome()

        # 3. Sayta keçid edin
        driver.get('https://sso.aztu.edu.az/')

        # 4. İstifadəçi adı və parol sahələrini tapın və məlumatları daxil edin
        istifadeci = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "UserId")))
        sifre = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "Password")))
        istifadeci.send_keys(istifadeci_adi)
        sifre.send_keys(parol)

        # 5. Giriş düyməsini tapıb klikləyin
        giris_duymesi = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/section/div/div[1]/div/div/form/div[3]/button')))
        giris_duymesi.click()

        # 6. Səhifənin yüklənməsini gözləyin
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div/aside[1]/div/nav/ul/li[1]/a')))

        # 7. Tələbə bölməsinə keçid edin
        driver.find_element(By.XPATH, '/html/body/div/aside[1]/div/nav/ul/li[1]/a').click()

        # 8. Kafedralar bölməsinə klikləyin
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="menu6i"]/a/span[2]/span'))).click()

        # 9. Python kursunu seçin
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="menu6i"]/ul/li[3]/a'))).click()

        # 10. Davamiyyət bölməsinə keçin
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="main_content"]/div[1]/div/div[2]/a[7]'))).click()

        # 11. Səhifənin tam yüklənməsini gözləyin
        time.sleep(10)

        # 12. Davamiyyət məlumatlarını çıxarın
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        tarixler = soup.find_all('font', {'style': 'font-size:11px;'})
        davamiyyet = soup.find_all('span', {'class': 'attend-label'})

        # 13. Məlumatları konsola yazdırın
        if tarixler and davamiyyet:
            for tarix, davam in zip(tarixler, davamiyyet):
                tarix_metin = tarix.get_text().strip()
                davamiyyet_metin = davam.get_text().strip()

                # Davamiyyət statusunun tərcüməsi
                status = {
                    "i/e": "Tələbə dərsdə iştirak edib.",
                    "q/b": "Tələbə dərsdə iştirak etməyib."
                }.get(davamiyyet_metin, f"Naməlum status: {davamiyyet_metin}")

                print(f"Tarix: {tarix_metin}, Status: {status}")
        else:
            print("Davamiyyət məlumatları tapılmadı.")

        # 14. Uğurlu girişdən sonra dövrdən çıxın
        ugurlu_giris = True

    except TimeoutException:
        print("Yanlış istifadəçi adı və ya şifrə. Yenidən cəhd edin.")
    except Exception as e:
        print(f"Xəta baş verdi: {e}")
    finally:
        # Brauzeri bağlayın
        driver.quit()
