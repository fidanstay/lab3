#Kodun Məqsədi və İş Prinsipi
Bu Python kodu Selenium və BeautifulSoup kitabxanalarını istifadə edərək AzTU SSO sistemində tələbə davamiyyəti haqqında məlumatları əldə etmək və istifadəçiyə göstərmək üçün yazılmışdır. Kodun məqsədi, istifadəçi tərəfindən daxil edilmiş login məlumatları ilə sistemə giriş edib, davamiyyət məlumatlarını avtomatik çıxarmaqdır.

Kodun Əsas Hissələri və Addım-addım İzahı
1. Məlumatların İstifadəçidən Alınması
Kodun başlanğıcında, istifadəçidən istifadəçi adı və şifrə tələb olunur:

python
Copy code
istifadeci_adi = input("İstifadəçi adınızı daxil edin: ")
parol = input("Şifrənizi daxil edin: ")
Bu məlumatlar daha sonra giriş üçün istifadə olunur.

2. Selenium ilə Brauzerin Başladılması
Kod ChromeDriver istifadə edərək brauzer açır və tələb olunan saytı yükləyir:

python
Copy code
driver = webdriver.Chrome()
driver.get('https://sso.aztu.edu.az/')
3. Form Sahələrinin Tapılması və Doldurulması
Kod istifadəçi adı və şifrə sahələrini taparaq istifadəçinin daxil etdiyi məlumatları yazır:

python
Copy code
istifadeci = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "UserId")))
sifre = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "Password")))
istifadeci.send_keys(istifadeci_adi)
sifre.send_keys(parol)
4. Giriş Düyməsinə Klikləmə
Giriş forması doldurulduqdan sonra giriş düyməsinə basılır:

python
Copy code
giris_duymesi = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/section/div/div[1]/div/div/form/div[3]/button')))
giris_duymesi.click()
5. Navigasiya və Davamiyyət Səhifəsinin Yüklənməsi
Sistemə uğurlu girişdən sonra lazımi səhifələrə keçid edilir:

Tələbə bölməsi
Kafedralar bölməsi
Python kursu
Davamiyyət səhifəsi
python
Copy code
driver.find_element(By.XPATH, '/html/body/div/aside[1]/div/nav/ul/li[1]/a').click()
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="menu6i"]/a/span[2]/span'))).click()
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="menu6i"]/ul/li[3]/a'))).click()
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="main_content"]/div[1]/div/div[2]/a[7]'))).click()
6. Davamiyyət Məlumatlarının Çıxarılması
BeautifulSoup kitabxanası istifadə olunaraq davamiyyət səhifəsindən tarixlər və statuslar götürülür:

python
Copy code
soup = BeautifulSoup(driver.page_source, 'html.parser')
tarixler = soup.find_all('font', {'style': 'font-size:11px;'})
davamiyyet = soup.find_all('span', {'class': 'attend-label'})
Daha sonra bu məlumatlar dövr vasitəsilə formatlanır və istifadəçiyə göstərilir:

python
Copy code
for tarix, davam in zip(tarixler, davamiyyet):
    tarix_metin = tarix.get_text().strip()
    davamiyyet_metin = davam.get_text().strip()
    status = {
        "i/e": "Tələbə dərsdə iştirak edib.",
        "q/b": "Tələbə dərsdə iştirak etməyib."
    }.get(davamiyyet_metin, f"Naməlum status: {davamiyyet_metin}")
    print(f"Tarix: {tarix_metin}, Status: {status}")
7. Xətaların İdarə Edilməsi
Kod iki əsas xətanı idarə edir:

Gözləmə xətası (TimeoutException): Yanlış login məlumatları daxil edildikdə istifadəçiyə xəbərdarlıq edilir.
Digər xətalar: Ümumi xətalar konsola yazdırılır:
python
Copy code
except TimeoutException:
    print("Yanlış istifadəçi adı və ya şifrə. Yenidən cəhd edin.")
except Exception as e:
    print(f"Xəta baş verdi: {e}")
8. Brauzerin Bağlanması
Kod istənilən halda brauzeri bağlayır:

finally:
    driver.quit()
Tələb olunan Kitabxanalar
Kodun işləməsi üçün aşağıdakı Python kitabxanalarını quraşdırmalısınız:

Selenium
bash
Copy code
pip install selenium
BeautifulSoup (bs4)
bash
Copy code
pip install beautifulsoup4
ChromeDriver
Brauzerin versiyasına uyğun ChromeDriver-i yükləyib sisteminizdə quraşdırın.
Vacib Qeydlər
XPath və Elementlər: AzTU sistemindəki hər hansı dəyişiklik XPath-ların işləməsinə mane ola bilər. XPath-ları sistemin aktual vəziyyətinə uyğun yeniləməlisiniz.
Giriş Məlumatları: Kod yalnız doğru istifadəçi adı və şifrə ilə işləyir.
Etik İstifadə: Kod yalnız şəxsi məlumatlarınıza giriş üçün nəzərdə tutulub. Başqa şəxslərin məlumatlarına icazəsiz giriş qanunlara ziddir.
