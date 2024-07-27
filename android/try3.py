import os
from appium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from appium.webdriver.common.mobileby import MobileBy
from appium.webdriver.common.touch_action import TouchAction
import json
import time
import requests

# Set proxy environment variables
# Define the proxy URL
proxy_url = 'http://prkqetmf:3rz31yf8w731@45.127.248.127:5128'

# BrowserStack capabilities
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
    'autoGrantPermissions': False,
    'browserName': 'chrome',
    'chromeOptions': {
        'args': [
            f'--proxy-server={proxy_url}'
        ]
    }
}


# Initialize the Appium driver with desired capabilities
driver = webdriver.Remote(
    command_executor='https://hub-cloud.browserstack.com/wd/hub',
    desired_capabilities=bs_caps
)

screen_size = driver.get_window_size()
width = screen_size['width']
height = screen_size['height']
center_x = width / 2
center_y = height / 2
touch_action = TouchAction(driver)


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
index = language_indices.get(selected_language.lower())

def get_ip_address():
    try:
        response = requests.get('https://api.ipify.org')
        if response.status_code == 200:
            return response.text.strip()
        else:
            print(f"Failed to retrieve IP address. Status code: {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"Error fetching IP address: {str(e)}")
        return None
ip_address = get_ip_address()
if ip_address:
    print(f"My public IP address is: {ip_address}")

def go_and_back(elements_to_check):
        for locator, xpath, message in elements_to_check:
            try:
                element = WebDriverWait(driver, 3).until(EC.presence_of_element_located((locator, xpath)))
                if element.is_displayed():
                    element.click()
                    count += 1
                    print(message)
                    if "com.android.chrome" in driver.current_package:
                        swipe_to_bottom(driver)
                        driver.back()  
                    break
            except (TimeoutException, NoSuchElementException):
                continue
        
def handle_ads_first(driver):
    xpath_continue_to_app = '//android.widget.TextView[@text="Continue to app"]'
    center_x = driver.get_window_size()['width'] // 2
    center_y = driver.get_window_size()['height'] // 2
    touch_action = TouchAction(driver)

    try:
        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath_continue_to_app)))
        
        if element.is_displayed():
            count = 0  
            elements_to_check = [
                (By.XPATH, '//android.view.View[@content-desc="Install"]', "b1 clicked"),
                (By.XPATH, '(//android.view.View[@content-desc="Install"])[1]', "b2 clicked"),
                (By.XPATH, '//android.widget.RelativeLayout/android.widget.FrameLayout/android.webkit.WebView/android.webkit.WebView/android.view.View[3]/android.view.View/android.view.View/android.widget.TextView', "b3 clicked")
            ]
            go_and_back(elements_to_check)

            if count == 0:
                touch_action.tap(x=center_x, y=center_y).perform()
                print('Center click')
                if "com.android.chrome" in driver.current_package:
                        #swipe_to_bottom(driver)
                        time.sleep(5)
                        driver.back()  
    except TimeoutException:
        print("Continue to app button not found within timeout. Proceeding with default action.")
    except WebDriverException as we:
        print(f"WebDriverException occurred: {we}")

def swipe_to_bottom(driver):
    try:
        touch_action = TouchAction(driver)
        window_size = driver.get_window_size()
        width = window_size['width']
        height = window_size['height']
        start_x = width // 2
        start_y = height // 2
        end_x = start_x
        end_y = height // 4 
        touch_action.press(x=start_x, y=start_y).move_to(x=end_x, y=end_y).release().perform()
        print("Scrolled to bottom of the page using TouchActions.")
        
    except WebDriverException as we:
        print(f"WebDriverException occurred while scrolling with TouchActions: {we}")

handle_ads_first(driver)



#function to handle ads
def handle_ads(driver):
    elements_to_check = [
        (MobileBy.XPATH, '//android.widget.TextView[@text="Continue to app"]', "Continue to app clicked"),
        (MobileBy.XPATH, '//android.widget.TextView[@text="Skip video"]', "Skip video clicked"),
        (MobileBy.XPATH, '//android.widget.Button', "cross button clicked"),
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


def handle_elements(driver):
    elements_to_check = [
        (By.XPATH, '//android.view.View[@content-desc="Install"]', "Install button clicked"),
        (By.XPATH, '//android.widget.Button[@resource-id="com.hd.video.downloader.xv:id/native_ad_qurka_action"]', "Alternative action button clicked"),
        (By.XPATH, '(//android.view.View[@content-desc="Install"])[1]', "Install button clicked")
    ]
    
    try:
        for locator, xpath, message in elements_to_check:
            try:
                element = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((locator, xpath)))
                if element.is_displayed():
                    element.click()
                    print(message)
                    if "com.android.chrome" in driver.current_package:
                        #swipe_to_bottom(driver)
                        time.sleep(5)
                        driver.back() 
                    break
            except TimeoutException:
                continue
            except WebDriverException as we:
                print(f"WebDriverException occurred: {we}")
                continue

        else:
            print("No suitable element found to click.")

    except Exception as e:
        print(f"Exception occurred: {e}")

handle_elements(driver)

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


driver.quit()


