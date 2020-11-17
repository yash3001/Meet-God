from selenium import webdriver; import requests
from selenium.webdriver.support import expected_conditions as when
from selenium.webdriver.common.by import By as by
from selenium.webdriver.common.keys import Keys
import time; import getpass

USERNAME = ""
PASSWORD = ""
MEET_LINK = "https://meet.google.com/qwe-auqz-vpo"
BROWSER_DRIVER = "/usr/local/bin/geckodriver"

usernameFieldPath = "identifierId"
usernameNextButtonPath = "identifierNext"
passwordFieldPath = "password"
passwordNextButtonPath = "passwordNext"
joinButton1Path = "//span[contains(text(), 'Join')]"
joinButton2Path = "//span[contains(text(), 'Ask to join')]"
listButtonPath = "/html/body/div[1]/c-wiz/div[1]/div/div[6]/div[3]/div[6]/div[3]/div/div[2]/div[3]"
endButtonPath = "[aria-label='Leave call']"

def initBrowser():
    print("Initializing browser...")
    firefoxOptions = webdriver.FirefoxOptions()
    firefoxOptions.add_argument("--width=800"), firefoxOptions.add_argument("--height=800")
    # firefoxOptions.headless = True
    firefoxOptions.set_preference("layers.acceleration.disabled", True)
    firefoxOptions.set_preference("browser.privatebrowsing.autostart", True)
    firefoxOptions.set_preference("permissions.default.microphone", 2)
    firefoxOptions.set_preference("permissions.default.camera", 2)
    driver = webdriver.Firefox(executable_path=BROWSER_DRIVER, options=firefoxOptions)
    print("Success!")
    return(driver)

def login():
    print("\nLogging into Google account...")
    driver.get('https://accounts.google.com/signin')

    global USERNAME, PASSWORD
    USERNAME = input("Enter your email address: ") if USERNAME == "" else USERNAME
    PASSWORD = getpass.getpass("Enter your password: ") if PASSWORD == "" else PASSWORD

    usernameField = wait.until(when.element_to_be_clickable((by.ID, usernameFieldPath)))
    time.sleep(1)
    usernameField.send_keys(USERNAME)

    usernameNextButton = wait.until(when.element_to_be_clickable((by.ID, usernameNextButtonPath)))
    usernameNextButton.click()

    passwordField = wait.until(when.element_to_be_clickable((by.NAME, passwordFieldPath)))
    time.sleep(1)
    passwordField.send_keys(PASSWORD)

    passwordNextButton = wait.until(when.element_to_be_clickable((by.ID, passwordNextButtonPath)))
    passwordNextButton.click()

    time.sleep(3)
    print("Success!")


def attendMeet():
    print("\nNavigating to Google Meet...")
    print("Success!")
    print("Entering Google Meet...")
    global MEET_LINK
    MEET_LINK = input("Enter the meet link: ") if MEET_LINK == "" else MEET_LINK
    driver.get(MEET_LINK)

    try:
        joinButton = wait.until(when.element_to_be_clickable((by.XPATH, joinButton1Path)))
    except:
        joinButton = wait.until(when.element_to_be_clickable((by.XPATH, joinButton2Path)))
    time.sleep(1)
    joinButton.click()

    print("Success!")
    time.sleep(1)
    print("Now attending Google Meet")

    try:
        joinButton = wait.until(when.element_to_be_clickable((by.XPATH, joinButton1Path)))   # For another prompt that pops up for Meets being recorded
        time.sleep(1)
        joinButton.click()
    except:
        pass


def endMeet():
    list = driver.find_element_by_xpath(listButtonPath)
    list.click()
    time.sleep(1)
    endButton = driver.find_element_by_css_selector(endButtonPath)
    endButton.click()
    print("\nSuccessfully ended Google Meet")


if __name__ == "__main__":

    try:
        DURATION = 5
        driver = initBrowser()
        wait = webdriver.support.ui.WebDriverWait(driver, 5)
        login()
        attendMeet()
        time.sleep(DURATION)
        endMeet()
        print("\n\nMeet completed successfully.")
        print("Press Enter to exit.")
        input()
        print("Cleaning up and exiting...")
        driver.quit()

    except KeyboardInterrupt:
        print("\n\nCTRL ^C\nThrew a wrench in the works.")
        print("Press Enter to exit.")
        input()
        print("Cleaning up and exiting...")
        driver.quit()

    # except Exception:
    #     print("An error occured")
    #     print("Press Enter to exit.")
    #     input()
    #     print("Cleaning up and exiting...")
    #     driver.quit()
