from selenium import webdriver; import requests
from selenium.webdriver.support import expected_conditions as when
from selenium.webdriver.common.by import By as by
from selenium.webdriver.common.keys import Keys
import time; import getpass; import datetime; import threading

USERNAME = ""
PASSWORD = ""
MEET_LINK = []
BROWSER_DRIVER = "/usr/local/bin/geckodriver"

usernameFieldPath = "identifierId"
usernameNextButtonPath = "identifierNext"
passwordFieldPath = "password"
passwordNextButtonPath = "passwordNext"
joinButton1Path = "//span[contains(text(), 'Join')]"
joinButton2Path = "//span[contains(text(), 'Ask to join')]"
listButtonPath = "/html/body/div[1]/c-wiz/div[1]/div/div[6]/div[3]/div[6]/div[3]/div/div[2]/div[3]"
listButtonCrossPath = "/html/body/div[1]/c-wiz/div[1]/div/div[6]/div[3]/div[3]/div/div[2]/div[1]/div[2]/div/button"
studentNumberPath = "/html/body/div[1]/c-wiz/div[1]/div/div[6]/div[3]/div[3]/div/div[2]/div[2]/div[1]/div[1]/span/div/span[2]"
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
    
    firefoxProfile = webdriver.FirefoxProfile()
    firefoxProfile.set_preference("media.volume_scale", "0.0")
    
    driver = webdriver.Firefox(executable_path=BROWSER_DRIVER, options=firefoxOptions, firefox_profile=firefoxProfile)
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


def attendMeet(link):
    print("\nNavigating to Google Meet...")
    print("Success!")
    print("Entering Google Meet...")
    driver.get(link)

    try:
        joinButton = wait.until(when.element_to_be_clickable((by.XPATH, joinButton1Path)))
    except:
        joinButton = wait.until(when.element_to_be_clickable((by.XPATH, joinButton2Path)))
    time.sleep(1)
    joinButton.click()

    print("Success!")
    time.sleep(1)

    try:
        joinButton = wait.until(when.element_to_be_clickable((by.XPATH, joinButton1Path)))   # For another prompt that pops up for Meets being recorded
        time.sleep(1)
        joinButton.click()
    except:
        pass

    while True:
        try:
            list = driver.find_element_by_xpath(listButtonPath)
            list.click()
            break
        except Exception:
            time.sleep(1)

    print("Now attending Google Meet")

def endMeet():
    list = driver.find_element_by_xpath(listButtonCrossPath)
    list.click()
    time.sleep(1)
    endButton = driver.find_element_by_css_selector(endButtonPath)
    endButton.click()
    print("\nSuccessfully ended Google Meet")


if __name__ == "__main__":

    try:
        driver = initBrowser()
        wait = webdriver.support.ui.WebDriverWait(driver, 5)
        login()

        if len(MEET_LINK) == 0:
            MEET_LINK.append(input("Enter the meet link and time: "))
        while len(MEET_LINK) != 0:            
            link = MEET_LINK[0]
            currentTime = list(map(int, str(datetime.datetime.now()).split()[1].split('.')[0].split(':')))
            sleepTime = (int(link.split()[1].split(':')[0]) - currentTime[0])*3600 + (int(link.split()[1].split(':')[1]) - currentTime[1])*60 + (int(link.split()[1].split(':')[2]) - currentTime[2])
            time.sleep(sleepTime)
            attendMeet(link.split()[0])
            # time.sleep(1800)
            while True:
                numPeople = driver.find_element_by_xpath(studentNumberPath).get_attribute('textContent')
                numPeople = int(str(numPeople[1:-1]))
                if numPeople < 2:
                    endMeet()
                    break
                else:
                    time.sleep(5)
            print("\n\nMeet completed successfully.")
            MEET_LINK.pop(0)

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
