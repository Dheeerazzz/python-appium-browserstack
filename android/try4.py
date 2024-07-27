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

def click_first_next(driver,xpath):
    try:
        element = WebDriverWait(driver,5).until(EC.presence_of_element_located((MobileBy.XPATH, xpath)))
        if element.is_displayed():
            element.click()
            print("Next button clicked")
        else:
            print("Next button not visible.")
    except Exception as e:
        print(f"Exception occurred: {e}")

def click_next(driver, xpath,times):
    for _ in range(3):
        try:
            element = WebDriverWait(driver,5).until(EC.presence_of_element_located((MobileBy.XPATH, xpath)))
            if element.is_displayed():
                element.click()
                print("Next button clicked")
            else:
                handle_ads(driver)  
        except Exception as e:
            print(f"Exception occurred: {e}")


def start(driver,xpath):
    try:
        element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((MobileBy.XPATH, xpath)))
        if element.is_displayed():
            element.click()
            print("Start button clicked")
        else:
            handle_ads(driver)
            start(driver,xpath)
    except Exception as e:
        print(f"Exception occurred: {e}")
        handle_ads(driver)
        start(driver,xpath)


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

def hit_download(driver,xpath):
    try:
        element = WebDriverWait(driver, 15).until(EC.presence_of_element_located((MobileBy.XPATH,xpath)))
        if element.is_displayed():
            element.click()
            print("Continue to app button clicked")
        else:
            print("Continue to app button not visible.")
    except Exception as e:
        print(f"Exception occurred: {e}")

    driver.quit()

def download_progress(driver,xpath):
    def click_progress(driver):
        try:
            element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((MobileBy.XPATH, '//android.widget.ImageView[@resource-id="com.hd.video.downloader.xv:id/inprogress"]')))
            if element.is_displayed():
                element.click()
                print("Download progress clicked")
            else:
                handle_ads(driver)
                click_progress(driver)
        except Exception as e:
            print(f"Exception occurred: {e}")
            handle_ads(driver)
            click_progress(driver)

    click_progress(driver)
    driver.quit()

def video_player(driver,xpath):
    def click_video_player(driver):
        try:
            element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((MobileBy.XPATH, '//android.widget.ImageView[@resource-id="com.hd.video.downloader.xv:id/player"]')))
            if element.is_displayed():
                element.click()
                print("Video player clicked")
            else:
                handle_ads(driver)
                click_video_player(driver)
        except Exception as e:
            print(f"Exception occurred: {e}")
            handle_ads(driver)
            click_video_player(driver)

    click_video_player(driver)
    driver.quit()

def guide(driver,xpath):
    def menu(driver):
        try:
            element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((MobileBy.XPATH, '//android.widget.ImageView[@resource-id="com.hd.video.downloader.xv:id/ivMenu"]')))
            if element.is_displayed():
                element.click()
                print("Menu clicked")
            else:
                handle_ads(driver)
                menu(driver)
        except Exception as e:
            print(f"Exception occurred: {e}")
            handle_ads(driver)
            menu(driver)

    def guidebtn(driver,xpath):
        try:
            element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((MobileBy.XPATH, '//android.widget.TextView[@text="How To Download"]')))
            if element.is_displayed():
                element.click()
                print("Guide button clicked")
            else:
                handle_ads(driver)
                guidebtn(driver)
        except Exception as e:
            print(f"Exception occurred: {e}")
            handle_ads(driver)
            guidebtn(driver)

    def click_next(driver,xpath):
        for _ in range(3):
            try:
                element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((MobileBy.XPATH, '//android.widget.ImageView[@resource-id="com.hd.video.downloader.xv:id/btnNext"]')))
                if element.is_displayed():
                    element.click()
                    print("Next button clicked")
                else:
                    handle_ads(driver)
            except Exception as e:
                print(f"Exception occurred: {e}")

    menu(driver)
    guidebtn(driver)
    click_next(driver)
    driver.quit()

# Read JSON file and determine the flow of actions
with open('input.json') as f:
    data = json.load(f)
    activity_flow = data.get('activity_flow', [])

# Execute actions based on the flow
for action in activity_flow:
    action_type = action.get('type')
    parameters = action.get('parameter', {})
    xpath=action.get('xpath')

    if action_type == 'select_language':
        select_language(driver, parameters.get('language', 'english'),xpath)
    elif action_type == 'click_first_next':
        click_first_next(driver,xpath)
    elif action_type == 'click_next':
        times=action.get('times')
        click_next(driver,xpath,times)
    elif action_type == 'start':
        start(driver,xpath)
    elif action_type== 'platform':
        platform(driver, parameters.get('platform', ''),xpath)
    elif action_type== 'link_paste':
        link_paste(driver, parameters.get('link', ''),xpath)
    elif action_type== 'hit_download':
        hit_download(driver,xpath)  
    elif action_type == 'download_progress':
        download_progress(driver,xpath)
    elif action_type == 'video_player':
        video_player(driver,xpath)
    elif action_type == 'guide':
        guide(driver,xpath)
    else:
        print(f"Unknown action type: {action_type}")

# Quit the driver
driver.quit()
