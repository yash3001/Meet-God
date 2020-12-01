#######################
####### Imports #######
#######################

from selenium import webdriver
from selenium.webdriver.support import expected_conditions as when
from selenium.webdriver.common.by import By as by
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import time; import getpass; import datetime; import threading; import os
from termcolor import colored
import re; import requests



################################
####### Global Variables #######
################################

currentVersion = "v3.6.1"

# Change these three variables to avoid typing again and again
USERNAME = ""
PASSWORD = ""
MEET_LINK = []
BROWSER_DRIVER = ""
# Choose the browser driver from the list below
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
MEET_SLEEP_TIME = 1200
END_PARTICIPANTS = 20
    
STATUS = "Starting"
MENU1 = colored("""
     --------------------------------------
    |            MAIN MENU                 |
    |--------------------------------------|
    | 1: Show bot status                   |
    | 2: Show Schedule                     |
    | 3: Show time until next meeting      |
    | 4: Add more meetings                 |
    | 5: Update/Delete an existing meeting |
    | 6: Leave the current meeting(if any) |
    | 7: Exit and shutdown the bot         |
    | 8: Show number of running threads    |
     --------------------------------------""", 'cyan')
    
MENU2 = colored("""
    
    > Choice(1-8): """, 'green')
    
MENU = MENU1 + MENU2
    
BANNER1 = colored('''
     ███▄ ▄███▓▓█████ ▓█████▄▄▄█████▓     ▄████  ▒█████  ▓█████▄ 
    ▓██▒▀█▀ ██▒▓█   ▀ ▓█   ▀▓  ██▒ ▓▒    ██▒ ▀█▒▒██▒  ██▒▒██▀ ██▌
    ▓██    ▓██░▒███   ▒███  ▒ ▓██░ ▒░   ▒██░▄▄▄░▒██░  ██▒░██   █▌
    ▒██    ▒██ ▒▓█  ▄ ▒▓█  ▄░ ▓██▓ ░    ░▓█  ██▓▒██   ██░░▓█▄   ▌
    ▒██▒   ░██▒░▒████▒░▒████▒ ▒██▒ ░    ░▒▓███▀▒░ ████▓▒░░▒████▓ 
    ░ ▒░   ░  ░░░ ▒░ ░░░ ▒░ ░ ▒ ░░       ░▒   ▒ ░ ▒░▒░▒░  ▒▒▓  ▒ 
    ░  ░      ░ ░ ░  ░ ░ ░  ░   ░         ░   ░   ░ ▒ ▒░  ░ ▒  ▒ 
    ░      ░      ░      ░    ░         ░ ░   ░ ░ ░ ░ ▒   ░ ░  ░ 
           ░      ░  ░   ░  ░                 ░     ░ ░     ░    
                                                          ░''', 'blue')
BANNER2 = colored('''
               ------------------------------------
              |   Meet God : The Google Meet Bot   |
               ------------------------------------''', 'red')
    
BANNER = BANNER1 + "\n" + BANNER2 + "\n"

VERSION_CHECK_URL = "https://raw.githubusercontent.com/yash3001/Meet-God/master/version.txt"

meetProcessAlive = False
    
usernameFieldPath = "identifierId"
usernameNextButtonPath = "identifierNext"
passwordFieldPath = "password"
passwordNextButtonPath = "passwordNext"
micBlockPath = "//div[@aria-label='Turn off microphone (ctrl + d)']"
cameraBlockPath = "//div[@aria-label='Turn off camera (ctrl + e)']"
joinButton1Path = "//span[contains(text(), 'Join')]"
statusPath = "//div[@role='status']"
joinButton2Path = "//span[contains(text(), 'Ask to join')]"
listButtonPath = "//div[@aria-label='Chat with everyone']"
listButtonCrossPath = "//button[@aria-label='Close']"
studentNumberPath = "//span[@class='rua5Nb']"
endButtonPath = "[aria-label='Leave call']"

e = threading.Event()


####################################
####### Function definitions #######
####################################

# To check for updates
def versionCheck():
    global currentVersion
    clrscr()
    print("\n    Checking for MeetGod updates...")
    time.sleep(2)
    crawlVersionFile = requests.get(VERSION_CHECK_URL)
    crawlVersionFile = str(crawlVersionFile.content)
    crawlVersionFile = re.findall(r"([0-9]+)", crawlVersionFile)
    latestVersion = int(''.join(crawlVersionFile))

    currentVersion = re.findall(r"([0-9]+)", currentVersion)
    currentVersion = int(''.join(currentVersion))

    if currentVersion >= latestVersion:
        print(colored("\n    Kuddos! You are using the latest version!", "green"))
        time.sleep(3)
    elif currentVersion < latestVersion:
        print(colored("\n    You are using an older version of MeetGod.", "red"))
        print(colored("    Get the latest version at https://raw.githubusercontent.com/yash3001/Meet-God/master/version.txt", "yellow"))
        print(colored("    Every new version comes with fixes, improvements, new features, etc..", "yellow"))
        time.sleep(7)


# To initialize the browser, chrome for chromedriver and firefox for geckodriver
def initBrowser():
    clrscr()
    print("    Initializing browser... ")

    if BROWSER_DRIVER.lower().startswith("chrome"):
        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_argument("--disable-infobars")
        chromeOptions.add_argument("--disable-gpu")
        chromeOptions.add_argument("--disable-extensions")
        chromeOptions.add_argument("--window-size=800,800")
        chromeOptions.add_argument("--incognito")
        chromeOptions.add_argument("use-fake-device-for-media-stream")
        chromeOptions.add_argument("use-fake-ui-for-media-stream")
        chromeOptions.add_experimental_option('excludeSwitches', ['enable-logging'])
        # chromeOptions.add_experimental_option("prefs", {"profile.default_content_setting_values.media_stream_mic": 1,
        #                                                 "profile.default_content_setting_values.media_stream_camera": 1,
        #                                                 "profile.default_content_setting_values.notifications": 1
        #                                                 })

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
    
    elif len(BROWSER_DRIVER) == 0:
        print(colored("\n    Please enter the driver path in the source code\n    Exiting...", 'red'))
        time.sleep(3)
        exit()
    
    else:
        print(colored("\n    Wrong driver path\n    Exiting...", 'red'))
        time.sleep(3)
        exit()
    
    print(colored("    Success!", 'green'))
    time.sleep(3)
    return(driver)


# To login into the goggle account
def login():
    clrscr()
    print("    Logging into Google account... ")
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
    print(colored("    Success!", 'green'))
    time.sleep(1)


# To navigate to the meeting link and enter the meeting
def attendMeet(link):
    global STATUS, BROWSER_DRIVER
    clrscr()
    print("\n    Navigating to Google Meet... ")
    print(colored("    Success!", 'green'))
    print("\n    Entering Google Meet... ")
    driver.get(link)

    try:
        joinButton = WebDriverWait(driver, 10).until(when.element_to_be_clickable((by.XPATH, joinButton1Path)))
        status = driver.find_element_by_xpath(statusPath).get_attribute('textContent')
        if status == "No one else is here":
            print(colored("\n    No one is in the meeting, sleeping for 5 minutes for the last time then skipping", 'red'))
            time.sleep(5)
            clrscr()
            print(MENU, end="")
            time.sleep(300)
            if status == "No one else is here":
                clrscr()
                print(colored("\n    Omiting the current meeting because of timout error", 'red'))
                time.sleep(5)
                return 0
    except:
        joinButton = WebDriverWait(driver, 10).until(when.element_to_be_clickable((by.XPATH, joinButton2Path)))

    if BROWSER_DRIVER.lower().startswith("chrome"):
        micBlockButton = driver.find_element_by_xpath(micBlockPath)
        cameraBlockButton = driver.find_element_by_xpath(cameraBlockPath)
        time.sleep(0.5)
        cameraBlockButton.click()
        time.sleep(0.5)
        micBlockButton.click()

    time.sleep(1)
    joinButton.click()

    print(colored("    Success!", 'green'))
    time.sleep(1)

    try:
        joinButton = wait.until(when.element_to_be_clickable((by.XPATH, joinButton1Path)))   # For another prompt that pops up for Meets being recorded
        time.sleep(1)
        joinButton.click()
    except:
        pass

    while True:
        try:
            listButton = driver.find_element_by_xpath(listButtonPath)
            listButton.click()
            break
        except Exception:
            time.sleep(1)

    print(colored("\n    Now attending Google Meet", 'green'))
    STATUS = "Attending meeting"
    time.sleep(2)
    clrscr()
    print(MENU, end="")
    return 1


# To exit the meeting after ending
def endMeet():
    list = driver.find_element_by_xpath(listButtonCrossPath)
    list.click()
    time.sleep(1)
    endButton = driver.find_element_by_css_selector(endButtonPath)
    endButton.click()
    clrscr()
    print(colored("\n    Successfully ended Google Meet", 'green'))
    time.sleep(2)
    clrscr()
    print(MENU, end="")


# The seperate process that attends the meeting
def attendProcess():
    global MEET_LINK, STATUS, MEET_SLEEP_TIME, meetProcessAlive, e
    meetProcessAlive = True
    while len(MEET_LINK) != 0:            
        if not meetProcessAlive:
            return
        link = MEET_LINK[0]
        currentTime = list(map(int, str(datetime.datetime.now()).split()[1].split('.')[0].split(':')))
        sleepTime = (int(link.split()[1].split(':')[0]) - currentTime[0])*3600 + (int(link.split()[1].split(':')[1]) - currentTime[1])*60 + (int(link.split()[1].split(':')[2]) - currentTime[2])
        STATUS = "Waiting for next meeting"
        if sleepTime > 0:
            check = not e.wait(timeout=sleepTime)
            if not check:
                meetProcessAlive = False
                return
        else:
            time.sleep(1)
            clrscr()
            print(colored("    Omiting the next meeting because time is negative", 'yellow'))
            MEET_LINK.pop(0)
            time.sleep(5)
            clrscr()
            print(MENU, end="")
            continue
        if meetProcessAlive:
            flag = attendMeet(link.split()[0])
            MEET_LINK.pop(0)
            if not flag:
                continue
            result = not e.wait(timeout=MEET_SLEEP_TIME)
            if not result:
                meetProcessAlive = False
            while True:
                if meetProcessAlive:
                    try:
                        numPeople = driver.find_element_by_xpath(studentNumberPath).get_attribute('textContent')
                    except Exception:
                        try:
                            listButton = driver.find_element_by_xpath(listButtonPath)
                            listButton.click()
                            time.sleep(1)
                            numPeople = driver.find_element_by_xpath(studentNumberPath).get_attribute('textContent')
                        except Exception:
                            time.sleep(2)
                            continue
                    numPeople = int(str(numPeople[1:-1]))
                    if numPeople < END_PARTICIPANTS:
                        endMeet()
                        break
                    else:
                        time.sleep(2)
                else:
                    return
        else:
            return
    
    time.sleep(0.5)
    clrscr()
    print(colored("\n\n    All Meets completed successfully.", 'green'))
    STATUS = "Idle"
    time.sleep(2)
    clrscr()
    print(MENU, end="")
    meetProcessAlive = False


# To determine the driver
def determineDriver():
    global BROWSER_DRIVER
    clrscr()
    if os.name == "posix":
        while True:
            choice = input("    What platform are you on?\n    1) Linux\n    2) Mac\n    > Answer(1 or 2): ")
            if choice.lower() == "1" or choice.lower() == 'linux':
                clrscr()
                choice = input("    What is your architecture?\n    1) 64bit\n    2) 32bit\n    > Answer(1 or 2): ")
                clrscr()
                if choice.lower() == "1" or choice.lower() == '64bit':
                    choice = input("    What Browser do you use?\n    1) Firefox\n    2) Chromium\n    > Answer(1 or 2): ")
                    if choice.lower() == "1" or choice.lower() == 'firefox':
                        BROWSER_DRIVER = "FirefoxDrivers/linux64/geckodriver"
                        break
                    elif choice.lower() == "2" or choice.lower() == 'chromium':
                        BROWSER_DRIVER = "ChromeDrivers/linux64/chromedriver"
                        break
                    else:
                        print(colored("\n    Wrong input, try again", 'red'))
                        time.sleep(3)
                        clrscr()
                        continue
                elif choice.lower() == "2" or choice.lower() == '32bit':
                    choice = input("    What Browser do you use?\n    1) Firefox\n    2) Chromium\n    > Answer(1 or 2): ")
                    if choice.lower() == "1" or choice.lower() == 'firefox':
                        BROWSER_DRIVER = "FirefoxDrivers/linux32/geckodriver"
                        break
                    elif choice.lower() == "2" or choice.lower() == 'chromium':
                        BROWSER_DRIVER = "ChromeDrivers/linux64/chromedriver"
                        break
                    else:
                        print(colored("\n    Wrong input, try again", 'red'))
                        time.sleep(3)
                        clrscr()
                        continue
                else:
                    print(colored("\n    Wrong input, try again", 'red'))
                    time.sleep(3)
                    clrscr()
                    continue

            elif choice.lower() == "2" or choice.lower() == 'mac':
                clrscr()
                choice = input("    What Browser do you use?\n    1) Firefox\n    2) Chromium\n    > Answer(1 or 2): ")
                if choice.lower() == "1" or choice.lower() == 'firefox':
                    BROWSER_DRIVER = "FirefoxDrivers/mac64/geckodriver"
                    break
                elif choice.lower() == "2" or choice.lower() == 'chromium':
                    BROWSER_DRIVER = "ChromeDrivers/mac64/chromedriver"
                    break
                else:
                    print(colored("\n    Wrong input, try again", 'red'))
                    time.sleep(3)
                    clrscr()
                    continue
            else:
                print(colored("\n    Wrong input, try again", 'red'))
                time.sleep(3)
                clrscr()
                continue

    elif os.name == 'nt':
        while True:
            choice = input("    What is your architecture?\n    1) 64bit\n    2) 32bit\n    > Answer(1 or 2): ")
            if choice.lower() == "1" or choice.lower() == '64bit':
                clrscr()
                choice = input("    What Browser do you use?\n    1) Firefox\n    2) Chrome\n    > Answer(1 or 2): ")
                if choice.lower() == "1" or choice.lower() == 'firefox':
                    BROWSER_DRIVER = "FirefoxDrivers/win64/geckodriver.exe"
                    break
                elif choice.lower() == "2" or choice.lower() == 'chromium':
                    BROWSER_DRIVER = "ChromeDrivers/win32/chromedriver.exe"
                    break
                else:
                    print(colored("    Wrong input, try again", 'red'))
                    time.sleep(3)
                    clrscr()
                    continue
            elif choice.lower() == "2" or choice.lower() == '32bit':
                clrscr()
                choice = input("    What Browser do you use?\n    1) Firefox\n    2) Chrome\n    > Answer(1 or 2): ")
                if choice.lower() == "1" or choice.lower() == 'firefox':
                    BROWSER_DRIVER = "FirefoxDrivers/win32/geckodriver.exe"
                    break
                elif choice.lower() == "2" or choice.lower() == 'chromium':
                    BROWSER_DRIVER = "ChromeDrivers/win32/chromedriver.exe"
                    break
                else:
                    print(colored("    Wrong input, try again", 'red'))
                    time.sleep(3)
                    clrscr()
                    continue
            else:
                print(colored("    Wrong input, try again", 'red'))
                time.sleep(3)
                clrscr()
                continue

    else:
        print(colored("    Platform not supported\n    Exiting...", 'red'))
        time.sleep(3)
        exit()


# To show the bot status
def showStatus():
    global STATUS
    clrscr()
    print(colored(f"    The bot is {STATUS}", 'yellow'))
    input(colored("\n\n    > [Press Enter to go back to the main menu] ", 'green'))


# To print the remaining meetings and their timings
def showSchedule():
    global MEET_LINK
    clrscr()
    if len(MEET_LINK) > 0:
        for index, link in enumerate(MEET_LINK):
            print(colored(f"    {index+1}) {link.split()[0]} at {link.split()[1]}", 'cyan'))
    else:
        print(colored("    No meetings scheduled currently", 'yellow'))
    input(colored("\n\n    > [Press Enter to go back to the main menu] ", 'green'))


# To show the remaining time until next meeting
def showRemainingTime():
    flag = True
    def printTime():
        global MEET_LINK
        if len(MEET_LINK) > 0:
            currentTime = list(map(int, str(datetime.datetime.now()).split()[1].split('.')[0].split(':')))
            remainingTime = (int(MEET_LINK[0].split()[1].split(':')[0]) - currentTime[0])*3600 + (int(MEET_LINK[0].split()[1].split(':')[1]) - currentTime[1])*60 + (int(MEET_LINK[0].split()[1].split(':')[2]) - currentTime[2])
            if remainingTime > 0:
                while(flag == True):
                    clrscr()
                    currentTime = list(map(int, str(datetime.datetime.now()).split()[1].split('.')[0].split(':')))
                    remainingTime = (int(MEET_LINK[0].split()[1].split(':')[0]) - currentTime[0])*3600 + (int(MEET_LINK[0].split()[1].split(':')[1]) - currentTime[1])*60 + (int(MEET_LINK[0].split()[1].split(':')[2]) - currentTime[2])
                    seconds = f" {remainingTime % 60} secs"
                    minutes = f" {remainingTime//60} mins" if remainingTime//60 > 0 else ""
                    hours = f" {remainingTime//3600} hrs" if remainingTime//3600 > 0 else ""
                    days = f" {remainingTime//86400} days" if remainingTime//86400 > 0 else ""
                    print(colored(f"    Remaining time:{days}{hours}{minutes}{seconds}", 'yellow'))
                    print(colored("\n\n    > [Press Enter to go back to the main menu] ", 'green'), end="")
                    time.sleep(1)
            else:
                clrscr()
                print(colored("\n    Waiting for extra 5 minutes to join the meeting as no one is there", 'yellow'))   
        else:
            clrscr()
            print(colored("    No meetings scheduled currently", 'yellow'))
            print(colored("\n\n    > [Press Enter to go back to the main menu] ", 'green'), end="")
    
    printTimeThread = threading.Thread(target=printTime)
    printTimeThread.start()
    input()
    flag = False
    printTimeThread.join()


# To add more meetings
def addMeetings():
    global MEET_LINK, STATUS, e, meetProcess
    flag = 'y'
    clrscr()
    while flag.lower() == "y" or flag.lower() == "yes":
        url = input("    > Enter the meeting url: ")
        timming = input("    > Enter the time for joining in 24 hour format (HH:MM:SS): ")
        MEET_LINK.append(url.strip()+" "+timming.strip())
        flag = input(colored("\n    Meeting added successfully.\n\n    > Add new meeting? (y/N): ", 'green'))
    if threading.active_count() == 1 and STATUS == "Idle":
        sortMeetings()
        meetProcess = threading.Thread(target=attendProcess)
        meetProcess.start()
        return
    elif STATUS == "Waiting for next meeting":
        e.set()
        time.sleep(0.5)
        sortMeetings()
        e = threading.Event()
        meetProcess = threading.Thread(target=attendProcess)
        meetProcess.start()
        return
    sortMeetings()


# To modify or delete a meeting
def modifyMeeting():
    global MEET_LINK, STATUS, meetProcessAlive, e
    choice = '1'
    while choice != '0':
        clrscr()
        print(colored("    The current meeting schedule is:\n", 'yellow'))
        if len(MEET_LINK) > 0:
            for index, link in enumerate(MEET_LINK):
                print(colored(f"    {index+1}) {link.split()[0]} at {link.split()[1]}", 'yellow'))
        else:
            print(colored("    No meetings scheduled currently", 'yellow'))
            input(colored("\n\n    > [Press Enter to go back to the main menu] ", 'green'))
            return
    
        index = input(colored("\n\n    > Enter the meeting number to modify: ", 'green'))
        index = int(index) - 1
        while True:
            clrscr()
            print(colored(f"    The chosen meeting is:\n{MEET_LINK[index].split()[0]} at {MEET_LINK[index].split()[1]}", 'cyan'))
            choice = input(colored("\n\n    1: Change the meet link\n    2: Change the meet timing\n    3: Delete this meeting\n\n    > Choice: ", 'green'))
            if choice == "1":
                newLink = input("\n    > Enter the new link: ").strip()
                MEET_LINK[index] = newLink + " " + MEET_LINK[index].split()[1]
                break
            elif choice == "2":
                newTime = input("\n    > Enter the new timings: ").strip()
                MEET_LINK[index] = MEET_LINK[index].split()[0] + " " + newTime
                if index == 0 and STATUS == "Waiting for next meeting":
                    e.set()
                    time.sleep(0.5)
                    e = threading.Event()
                    meetProcess = threading.Thread(target=attendProcess)
                    sortMeetings()
                    meetProcess.start()
                break

            elif choice == "3":
                MEET_LINK.pop(index)
                if index == 0 and STATUS == "Waiting for next meeting":
                    e.set()
                    time.sleep(0.5)
                    e = threading.Event()
                    meetProcess = threading.Thread(target=attendProcess)
                    meetProcess.start()
                break

            else:
                print(colored("\n    Wrong input, try again", 'red'))
                time.sleep(3)

        clrscr()
        print(colored("    The updated meeting schedule is:\n", 'cyan'))
        if len(MEET_LINK) > 0:
            for index, link in enumerate(MEET_LINK):
                print(colored(f"    {index+1}) {link.split()[0]} at {link.split()[1]}", 'cyan'))
        else:
            print(colored("    No meetings scheduled currently", 'yellow'))
    
        choice = input(colored("\n\n    0: go back to main menu.\n    1: Keep modifying more meetings\n    > Choice: ", 'green'))
    

# To sort the meetings according to their timings
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


# To leave the current meeting(if any)
def leaveCurrentMeeting():
    global STATUS, e, meetProcessAlive
    if STATUS == "Attending meeting":
        e.set()
        meetProcessAlive = False
        time.sleep(0.5)
        endMeet()
        time.sleep(0.5)
        e = threading.Event()
        meetProcess = threading.Thread(target=attendProcess)
        sortMeetings()
        meetProcess.start()
    else:
        clrscr()
        print(colored("    You are not in a meeting currently", 'yellow'))
        input(colored("\n    [Press enter to go back to the main menu] ", 'yellow'))


# For clearing the terminal except the banner
def clrscr():
    if os.name == 'posix':
        _ = os.system('clear')
    else:
        _ = os.system('cls')
    print(BANNER+"\n\n")


# For clearing everything
def clrscrAll():
    if os.name == 'posix':
        _ = os.system('clear')
    else:
        _ = os.system('cls')


# To show the running processes (for developement purposes)
def showProcesses():
    clrscr()
    print("   ", threading.active_count())
    input(colored("\n\n    > [Press enter to go back to the main menu] ", 'green'))



#############################
####### Main function #######
#############################

if __name__ == "__main__":
    try:
        versionCheck()
        clrscr()

        print(colored("    Now starting the bot...", 'cyan'))
        time.sleep(3)
        clrscr()

        USERNAME = input("    > Enter the username for gmail account: ") if USERNAME == "" else USERNAME
        PASSWORD = getpass.getpass("    > Enter the password for your gmail account: ") if PASSWORD == "" else PASSWORD
        clrscr()

        if len(MEET_LINK) == 0:
            print("    Enter the meet schedule")
            addMeetings()
        else:
            sortMeetings()

        if len(BROWSER_DRIVER) == 0:
            determineDriver()

        driver = initBrowser()
        wait = WebDriverWait(driver, 5)
        login()
        meetProcess = threading.Thread(target=attendProcess)
        meetProcess.start()
        meetProcess.setDaemon(True)
        while True:
            clrscr()
            ans = input(MENU)
            if ans == '1':
                showStatus()
            elif ans == '2':
                showSchedule()
            elif ans == '3':
                showRemainingTime()
            elif ans == '4':
                addMeetings()
            elif ans == '5':
                modifyMeeting()
            elif ans == '6':
                leaveCurrentMeeting()
            elif ans == '7':
                clrscr()
                print(colored("    Cleaning up and exiting...", 'green'))
                try:
                    driver.quit()
                except Exception:
                    pass
                meetProcessAlive = False
                e.set()
                time.sleep(3)
                clrscrAll()
                break
            elif ans == '8':
                showProcesses()
            else:
                print(colored("    Wrong input, Try again", 'red'))
                time.sleep(3)

        # meetProcess.join()
        

    except KeyboardInterrupt:
        clrscr()
        print(colored("\n\n    CTRL ^C\n    Threw a wrench in the works.", 'yellow'))
        print(colored("    Press Enter to exit.", 'yellow'))
        input()
        print(colored("    Cleaning up and exiting...", 'yellow'))
        try:
            driver.quit()
        except Exception:
            pass
        meetProcessAlive = False
        e.set()
        time.sleep(3)
        clrscrAll()

    except Exception:
        print(colored("    An error occured", 'red'))
        print(colored("    Press Enter to exit.", 'red'))
        input()
        print(colored("    Cleaning up and exiting...", 'red'))
        try:
            driver.quit()
        except Exception:
            pass
        meetProcessAlive = False
        e.set()
        time.sleep(3)
        clrscrAll()
