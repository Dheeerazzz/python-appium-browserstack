#to go to download progress
# click on download progress icon - '//android.widget.ImageView[@resource-id="com.hd.video.downloader.xv:id/inprogress"]'

#to go to video player
#click video player logo- '//android.widget.ImageView[@resource-id="com.hd.video.downloader.xv:id/player"]'

#to go to guide
# click on menu-'//android.widget.ImageView[@resource-id="com.hd.video.downloader.xv:id/ivMenu"]'
#click guide button - '//android.widget.TextView[@text="How To Download"]'
#click next in guide - use 'click_next(xpath,times=3)' - '//android.widget.TextView[@resource-id="com.hd.video.downloader.xv:id/txtOK"]'

#to go to premium 
#menu-'//android.widget.ImageView[@resource-id="com.hd.video.downloader.xv:id/ivMenu"]'
#click premium button -  '//android.widget.ImageView[@resource-id="com.hd.video.downloader.xv:id/premium"]'
# continue button - '//android.widget.TextView[@resource-id="com.hd.video.downloader.xv:id/btnContinue"]'



from appium import webdriver
from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import json

# BrowserStack credentials and setup
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

def handle_ads(driver):
    elements_to_check = [
        (MobileBy.XPATH, '//android.widget.TextView[@text="Continue to app"]', "Continue to app clicked"),
        (MobileBy.XPATH, '//android.widget.TextView[@text="Skip video"]', "Skip video clicked"),
        (MobileBy.XPATH, '//android.widget.ImageView[@resource-id="com.hd.video.downloader.xv:id/close_icon"]', "Close icon clicked"),
        (MobileBy.XPATH, '//android.widget.RelativeLayout/android.widget.FrameLayout/android.webkit.WebView/android.webkit.WebView/android.view.View/android.view.View/android.view.View/android.view.View[1]/android.view.View/android.view.View[1]/android.view.View/android.view.View[6]/android.view.View/android.widget.TextView', "bottom close clicked")
    ]
    for locator, xpath, message in elements_to_check:
        try:
            element = WebDriverWait(driver, 3).until(EC.presence_of_element_located((locator, xpath)))
            if element.is_displayed():
                element.click()
                print(message)
                break
        except (TimeoutException, NoSuchElementException):
            continue

def select_language(driver, language,xpath):
    try:
        language_indices = {
            'french': 1,
            'spanish': 2,
            'arabic': 3,
            'german': 4,
            'english': 5,
            'bengali': 6,
            'nepali': 7
        }
        index = language_indices.get(language.lower())
        print(index)
        
        xpat= xpath+f'[{index}]'
        print(xpat)
        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((MobileBy.XPATH, xpat)))
        if element.is_displayed():
            element.click()
            print(f"Selected language: {language}")
        else:
            handle_ads(driver)
            select_language(driver, language,xpat)
    except Exception as e:
        print(f"Exception occurred: {e}")
        handle_ads(driver)
        select_language(driver, language,xpat)

def click_next(driver, xpath, times):
    for i in range(1,times+1):
        try:
            element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((MobileBy.XPATH, xpath)))
            
            if element.is_displayed():
                element.click()
                print("Next button clicked")
                #return 
        except Exception as e:
            print(f"Exception occurred: {e}")
            handle_ads(driver)
            click_next(driver,xpath,i)



def platform(driver,platform,xpath):
        try:
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((MobileBy.XPATH, xpath + f'{platform}"]'))
            )
            if element.is_displayed():
                element.click()
                print(f"{platform.capitalize()} button clicked")
            else:
                handle_ads(driver)
        except Exception as e:
            print(f"Exception occurred: {e}")
            handle_ads(driver)

def link_paste(driver,link,xpath):
    try:
        element = WebDriverWait(driver, 6).until(EC.presence_of_element_located((MobileBy.XPATH,xpath)))
        if element.is_displayed():
            print(link)
            element.send_keys(link)
            print("Link pasted")
        else:
            handle_ads(driver)
            link_paste(driver,link,xpath)
    except Exception as e:
        print(f"Exception occurred: {e}")
        handle_ads(driver)
        link_paste(driver,link,xpath)




# Read JSON file and determine the flow of actions
with open('premium.json') as f:
    data = json.load(f)
    activity_flow = data.get('activity_flow', [])

# Execute actions based on the flow
for action in activity_flow:
    action_type = action.get('type')
    parameters = action.get('parameter', {})
    xpath=action.get('xpath')

    if action_type == 'select_language':
        select_language(driver, parameters.get('language', 'english'),xpath)
    elif action_type == 'click_next':
        times=action.get('times')
        click_next(driver,xpath,times)
    elif action_type== 'platform':
        platform(driver, parameters.get('platform', ''),xpath)
    elif action_type== 'link_paste':
        link_paste(driver, parameters.get('link', ''),xpath)
    elif action_type=='handle_ads':
        handle_ads(driver)
    else:
        print(f"Unknown action type: {action_type}")

# Quit the driver
driver.quit()
