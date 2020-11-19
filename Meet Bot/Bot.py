from selenium import webdriver; import requests
from selenium.webdriver.support import expected_conditions as when
from selenium.webdriver.common.by import By as by
from selenium.webdriver.common.keys import Keys
import time; import getpass; import datetime; import multiprocessing; import os
from multiprocessing import Manager

USERNAME = ""
PASSWORD = ""
MEET_LINK = Manager().list([])

BROWSER_DRIVER = ""
#############################################################
#                   Google Chrome                           #
#           Linux: "ChromeDrivers/linux64/chromedriver"     #
#             Mac: "ChromeDrivers/mac64/chromedriver"       #
#         Windows: "ChromeDrivers/win32/chromedriver.exe"   #
#                                                           #
#                   Mozilla Firefox                         #
#     Linux (x32): "FirefoxDrivers/linux32/geckodriver"     #
#     Linux (x64): "FirefoxDrivers/linux64/geckodriver"     #
#             Mac: "FirefoxDrivers/mac64/geckodriver"       #
#   Windows (x32): "FirefoxDrivers/win32/geckodriver.exe"   #
#   Windows (x64): "FirefoxDrivers/win64/geckodriver.exe"   #
#############################################################

STATUS = Manager().list(["Idol"])
MENU = """
1: Show bot status
2: Show Schedule
3: Add more meetings
4: Update/Delete an existing meeting
5: Exit and shutdown the bot
6: Show Processes
"""

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
    clrscr()
    print("Initializing browser...")

    if BROWSER_DRIVER.lower().startswith("chrome"):
        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_argument("--disable-infobars")
        chromeOptions.add_argument("--disable-gpu")
        chromeOptions.add_argument("--disable-extensions")
        chromeOptions.add_argument("--window-size=800,800")
        chromeOptions.add_argument("--incognito")
        chromeOptions.add_experimental_option('excludeSwitches', ['enable-logging'])
        chromeOptions.add_experimental_option("prefs", {"profile.default_content_setting_values.media_stream_mic": 2,
                                                        "profile.default_content_setting_values.media_stream_camera": 2,
                                                        "profile.default_content_setting_values.notifications": 2
                                                        })
        chrome_options.add_argument("--mute-audio")

        driver = webdriver.Chrome(executable_path=BROWSER_DRIVER, options=chromeOptions)
    
    elif BROWSER_DRIVER.lower().startswith("firefox"):
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
    
    else:
        print("\nWrong driver path\nExiting...")
        time.sleep(1)
        exit()
    
    print("Success!")
    time.sleep(1)
    return(driver)

def login():
    clrscr()
    print("Logging into Google account...")
    driver.get('https://accounts.google.com/signin')

    # global USERNAME, PASSWORD
    # USERNAME = input("Enter your email address: ") if USERNAME == "" else USERNAME
    # PASSWORD = getpass.getpass("Enter your password: ") if PASSWORD == "" else PASSWORD

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
    time.sleep(1)


def attendMeet(link):
    global STATUS
    clrscr()
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

    print("\nNow attending Google Meet")
    STATUS[0] = "Attending meeting"
    time.sleep(2)
    clrscr()
    print(MENU+"\n"+"Answer: ", end="")

def endMeet():
    list = driver.find_element_by_xpath(listButtonCrossPath)
    list.click()
    time.sleep(1)
    endButton = driver.find_element_by_css_selector(endButtonPath)
    endButton.click()
    clrscr()
    print("\nSuccessfully ended Google Meet")
    time.sleep(2)
    print(MENU+"\n"+"Answer: ", end="")


def attendProcess(MEET_LINK, STATUS):
    while len(MEET_LINK) != 0:            
        link = MEET_LINK[0]
        currentTime = list(map(int, str(datetime.datetime.now()).split()[1].split('.')[0].split(':')))
        sleepTime = (int(link.split()[1].split(':')[0]) - currentTime[0])*3600 + (int(link.split()[1].split(':')[1]) - currentTime[1])*60 + (int(link.split()[1].split(':')[2]) - currentTime[2])
        STATUS[0] = "Waiting for next meeting"
        try:
            time.sleep(sleepTime)
        except Exception:
            clrscr()
            print("Omiting the next meeting because time is negative")
            MEET_LINK.pop(0)
            time.sleep(5)
            clrscr()
            print(MENU+"\n"+"Answer: ", end="")
            continue
        attendMeet(link.split()[0])
        MEET_LINK.pop(0)
        time.sleep(1200)
        while True:
            numPeople = driver.find_element_by_xpath(studentNumberPath).get_attribute('textContent')
            numPeople = int(str(numPeople[1:-1]))
            if numPeople < 2:
                endMeet()
                break
            else:
                time.sleep(5)
    clrscr()
    print("\n\nAll Meets completed successfully.")
    STATUS[0] = "idol"
    time.sleep(2)
    clrscr()
    print(MENU+"\n"+"Answer: ", end="")

def showStatus():
    global STATUS
    clrscr()
    print(f"The bot is {STATUS[0]}")
    input("\n\nPress Enter to go back to the main menu")

def showSchedule():
    global MEET_LINK
    clrscr()
    if len(MEET_LINK) > 0:
        for index, link in enumerate(MEET_LINK):
            print(f"{index+1}) {link.split()[0]} at {link.split()[1]}")
    else:
        print("No meetings scheduled currently")
    input("\n\n[Press Enter to go back to main menu]")

def addMeetings():
    global MEET_LINK, STATUS, meetProcess
    flag = 'y'
    clrscr()
    while flag.lower() == "y" or flag.lower() == "yes":
        url = input("Enter the meeting url: ")
        timming = input("Enter the time for joining in 24 hour format (HH:MM:SS): ")
        MEET_LINK.append(url.strip()+" "+timming.strip())
        flag = input("Meeting added successfully.\nAdd new meeting? (y/N): ")
    if len(multiprocessing.active_children()) == 2:
        meetProcess = multiprocessing.Process(target=attendProcess, args=(MEET_LINK, STATUS))
        meetProcess.start()
    sortMeetings()

def modifyMeeting():
    global MEET_LINK, STATUS, meetProcess
    choice = '1'
    while choice != '0':
        clrscr()
        print("The current meeting schedule is:\n")
        if len(MEET_LINK) > 0:
            for index, link in enumerate(MEET_LINK):
                print(f"{index+1}) {link.split()[0]} at {link.split()[1]}")
        else:
            print("No meetings scheduled currently")
            input("\n\n[Press Enter to go back to main menu]")
            return
    
        index = input("\n\nEnter the meeting number to modify: ")
        index = int(index) - 1
        while True:
            clrscr()
            print(f"The chosen meeting is:\n{MEET_LINK[index].split()[0]} at {MEET_LINK[index].split()[1]}")
            choice = input("\n\n1: Change the meet link\n2: Change the meet timing\n3: Delete this meeting\n\nChoice: ")
            if choice == "1":
                newLink = input("\nEnter the new link: ").strip()
                MEET_LINK[index] = newLink + " " + MEET_LINK[index].split()[1]
                break
            elif choice == "2":
                newTime = input("\nEnter the new timings: ").strip()
                MEET_LINK[index] = MEET_LINK[index].split()[0] + " " + newTime
                if index == 0 and STATUS[0] == "Waiting for next meeting":
                    meetProcess.terminate()
                    time.sleep(0.1)
                    meetProcess = multiprocessing.Process(target=attendProcess, args=(MEET_LINK, STATUS))
                    sortMeetings()
                    meetProcess.start()
                break

            elif choice == "3":
                MEET_LINK.pop(index)
                if index == 0 and STATUS[0] == "Waiting for next meeting":
                    meetProcess.terminate()
                    time.sleep(0.1)
                    meetProcess = multiprocessing.Process(target=attendProcess, args=(MEET_LINK, STATUS))
                    meetProcess.start()
                break

            else:
                print("\nWrong input, try again")
                time.sleep(1)

        clrscr()
        print("The updated meeting schedule is:\n")
        if len(MEET_LINK) > 0:
            for index, link in enumerate(MEET_LINK):
                print(f"{index+1}) {link.split()[0]} at {link.split()[1]}")
        else:
            print("No meetings scheduled currently")
    
        choice = input("\n\n0: go back to main menu.\n1: Keep modifying more meetings\nAnswer: ")
    

def sortMeetings():
    global MEET_LINK
    if len(MEET_LINK) > 1:
        length = len(MEET_LINK)
        m = []
        for link in MEET_LINK:
            m.append(link)
        m = [l.split()[1]+" "+l.split()[0] for l in m]
        m.sort()
        m = [l.split()[1]+" "+l.split()[0] for l in m]
        for item in m:
            MEET_LINK.append(item)
        for _ in range(length):
            MEET_LINK.pop(0)

def clrscr():
    if os.name == 'posix':
        _ = os.system('clear')
    else:
        _ = os.system('cls')

def showProcesses():
    clrscr()
    print(len(multiprocessing.active_children()))
    print(multiprocessing.active_children())
    input("\n\nEnter to continue: ")


if __name__ == "__main__":

    USERNAME = input("Enter the username for gmail account: ") if USERNAME == "" else USERNAME
    PASSWORD = getpass.getpass("Enter the password for your gmail account: ") if PASSWORD == "" else PASSWORD

    if len(MEET_LINK) == 0:
        print("Enter the meet schedule")
        addMeetings()
    else:
        sortMeetings()

    try:
        driver = initBrowser()
        wait = webdriver.support.ui.WebDriverWait(driver, 5)
        login()
        meetProcess = multiprocessing.Process(target=attendProcess, args=(MEET_LINK, STATUS))
        meetProcess.start()

        while True:
            clrscr()
            ans = input(MENU+"\nAnswer: ")
            if ans == '1':
                showStatus()
            elif ans == '2':
                showSchedule()
            elif ans == '3':
                addMeetings()
            elif ans == '4':
                modifyMeeting()
            elif ans == '5':
                clrscr()
                print("Cleaning up and exiting...")
                driver.quit()
                meetProcess.terminate()
                time.sleep(3)
                clrscr()
                break
            elif ans == '6':
                showProcesses()
            else:
                print("Wrong input, Try again")
                time.sleep(3)

        meetProcess.join()
        

    except KeyboardInterrupt:
        clrscr()
        print("\n\nCTRL ^C\nThrew a wrench in the works.")
        print("Press Enter to exit.")
        input()
        print("Cleaning up and exiting...")
        try:
            driver.quit()
        except Exception:
            pass
        try:
            meetProcess.terminate()
        except Exception:
            pass
        time.sleep(3)
        clrscr()

    except Exception:
        print("An error occured")
        print("Press Enter to exit.")
        input()
        print("Cleaning up and exiting...")
        try:
            driver.quit()
        except Exception:
            pass
        try:
            meetProcess.terminate()
        except Exception:
            pass
        time.sleep(3)
        clrscr()