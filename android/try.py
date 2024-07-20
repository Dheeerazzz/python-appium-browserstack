from appium import webdriver
from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import json


bs_username = 'dheerajsurakasul_Q7m2uU'
bs_access_key = 'zfFk58FFmpo2EXcoxaVY'
bs_caps = {
    'browserstack.user': bs_username,
    'browserstack.key': bs_access_key,
    'device': 'Google Pixel 5',
    'os_version': '12.0',
    'real_mobile': 'true',
    'app': 'bs://09d8827c201d28a823cbd178971695e15bd5eb57',
    'name': 'Appium Test with BrowserStack',
    'autoGrantPermissions': False
}
driver = webdriver.Remote(
    command_executor='https://hub-cloud.browserstack.com/wd/hub',
    desired_capabilities=bs_caps
)



#mapping of language names to indices
language_indices = {
    'french': 1,
    'spanish': 2,
    'arabic': 3,
    'german': 4,
    'english': 5,
    'bengali': 6,
    'nepali': 7
}
with open('input2.json') as f:
    data = json.load(f)
    action=(data['action'].lower())
    selected_language = data['language']

print('action performing : ',action)

#get the index for the selected language
index = language_indices.get(selected_language.lower())
print(selected_language, index)

#function to handle ads
def handle_ads(driver):
    elements_to_check = [
        (MobileBy.XPATH, '//android.widget.TextView[@text="Continue to app"]', "Continue to app clicked"),
        (MobileBy.XPATH, '//android.widget.TextView[@text="Skip video"]', "Skip video clicked"),
        (MobileBy.XPATH, '//android.widget.ImageView[@resource-id="com.hd.video.downloader.xv:id/close_icon"]', "Close icon clicked"),
        (MobileBy.XPATH,'//android.widget.RelativeLayout/android.widget.FrameLayout/android.webkit.WebView/android.webkit.WebView/android.view.View/android.view.View/android.view.View/android.view.View[1]/android.view.View/android.view.View[1]/android.view.View/android.view.View[6]/android.view.View/android.widget.TextView',"bottom close clicked")
]

    for locator, xpath, message in elements_to_check:
        try:
            element = WebDriverWait(driver,3).until(EC.presence_of_element_located((locator, xpath)))
            if element.is_displayed():
                element.click()
                print(message)
                break
        except (TimeoutException, NoSuchElementException):
            continue


#select language based on index
def initial(driver):
    try:
        xpath = f'(//android.widget.LinearLayout[@resource-id="com.hd.video.downloader.xv:id/ll"])[{index}]'
        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((MobileBy.XPATH, xpath)))
        if element.is_displayed():
            element.click()
            print(f"Selected language: {selected_language}")
        else:
            handle_ads(driver)
            initial(driver)
    except Exception as e:
        print(f"Exception occurred: {e}")
        handle_ads(driver)
        initial(driver)
initial(driver)


#to click on next button
try:
    element = WebDriverWait(driver,5).until(EC.presence_of_element_located((MobileBy.XPATH, '//android.widget.ImageView[@resource-id="com.hd.video.downloader.xv:id/next"]')))
    if element.is_displayed():
        element.click()
        print("Next button clicked")
    else:
        print("Next button not visible.")
except Exception as e:
    print(f"Exception occurred: {e}")

#to handle 3 instances of next buttons
for _ in range(3):
    try:
        element = WebDriverWait(driver,5).until(EC.presence_of_element_located((MobileBy.XPATH, '//android.widget.ImageView[@resource-id="com.hd.video.downloader.xv:id/btnNext"]')))
        if element.is_displayed():
            element.click()
            print("Next button clicked")
        else:
            handle_ads(driver)  
    except Exception as e:
        print(f"Exception occurred: {e}")

#to interact with start button
def start(driver):
    try:
        element = WebDriverWait(driver,5).until(EC.presence_of_element_located((MobileBy.XPATH, '//android.widget.ImageView[@resource-id="com.hd.video.downloader.xv:id/start"]')))
        if element.is_displayed():
            element.click()
            print("Start button clicked")
        else:
            handle_ads(driver)
            start(driver)
    except Exception as e:
        print(f"Exception occurred: {e}")
        handle_ads(driver)
        start(driver)
start(driver)
############################## uptohere default for every action ###################################

def history():
    def menu(driver):
        try:
            element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((MobileBy.XPATH, '//android.widget.ImageView[@resource-id="com.hd.video.downloader.xv:id/ivMenu"]')))
            if element.is_displayed():
                element.click()
                print("Start button clicked")
            else:
                handle_ads(driver)
                menu(driver)
        except Exception as e:
            print(f"Exception occurred: {e}")
            handle_ads(driver)
            menu(driver)
    def historybtn(driver):
        try:
            element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((MobileBy.XPATH, '//android.widget.TextView[@text="History"]')))
            if element.is_displayed():
                element.click()
                print("Start button clicked")
            else:
                handle_ads(driver)
                historybtn(driver)
        except Exception as e:
            print(f"Exception occurred: {e}")
            handle_ads(driver)
            historybtn(driver)
            driver.quit()

    menu(driver)
    historybtn(driver)
    handle_ads(driver)

def social_media():
    # Function to interact with fb
    def fb(driver):
        try:
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((MobileBy.XPATH, f'//android.widget.ImageView[@resource-id="com.hd.video.downloader.xv:id/{platform}"]'))
            )
            if element.is_displayed():
                element.click()
                print(f"{platform.capitalize()} button clicked")
            else:
                handle_ads(driver)
        except Exception as e:
            print(f"Exception occurred: {e}")
            handle_ads(driver)  
    fb(driver)

    def link_paste(driver):
        try:
            element = WebDriverWait(driver,6).until(EC.presence_of_element_located((MobileBy.XPATH, '//android.widget.EditText[@resource-id="com.hd.video.downloader.xv:id/et_text"]')))
            if element.is_displayed():
                print(link)
                element.send_keys(link)
                print("Link pasted")
            else:
                    handle_ads(driver)
                    link_paste(driver)
        except Exception as e:
                print(f"Exception occurred: {e}")
                handle_ads(driver)
                link_paste(driver)
    link_paste(driver)

    try:
        element = WebDriverWait(driver,15).until(EC.presence_of_element_located((MobileBy.XPATH, '//android.widget.ImageView[@resource-id="com.hd.video.downloader.xv:id/loginBtn1"]')))
        if element.is_displayed():
            element.click()
            print("Continue to app button clicked")
        else:
            print("Continue to app button not visible.")
    except Exception as e:
        print(f"Exception occurred: {e}")

    driver.quit()

if action=='download post':
    with open('input2.json') as f:
        data = json.load(f)
        platform = data['platform'].lower()
        link = data['link']
    social_media()
elif action=='history':
    history()