#######################
####### Imports #######
#######################

from selenium import webdriver
from selenium.webdriver.support import expected_conditions as when
from selenium.webdriver.common.by import By as by
from selenium.webdriver.common.keys import Keys
import time; import getpass; import datetime; import multiprocessing; import os
from multiprocessing import Manager
from termcolor import colored



################################
####### Global Variables #######
################################

# Change these three variables to avoid typing again and again
USERNAME = ""
PASSWORD = ""
MEET_LINK = Manager().list([])

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

STATUS = Manager().list(["Idol"])
MENU1 = colored("""
 --------------------------------------
|            MAIN MENU                 |
|--------------------------------------|
| 1: Show bot status                   |
| 2: Show Schedule                     |
| 3: Add more meetings                 |
| 4: Update/Delete an existing meeting |
| 5: Exit and shutdown the bot         |
| 6: Show Processes                    |
 --------------------------------------""", 'cyan')

MENU2 = colored("""

Answer: """, 'green')

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

usernameFieldPath = "identifierId"
usernameNextButtonPath = "identifierNext"
passwordFieldPath = "password"
passwordNextButtonPath = "passwordNext"
joinButton1Path = "//span[contains(text(), 'Join')]"
joinButton2Path = "//span[contains(text(), 'Ask to join')]"
listButtonPath = "//div[@aria-label='Chat with everyone']"
listButtonCrossPath = "//button[@aria-label='Close']"
studentNumberPath = "//span[@class='rua5Nb']"
endButtonPath = "[aria-label='Leave call']"



####################################
####### Function definitions #######
####################################

# To initialize the browser, chrome for chromedriver and firefox for geckodriver
def initBrowser():
    clrscr()
    print("Initializing browser... ")

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
    
    elif len(BROWSER_DRIVER) == 0:
        print(colored("\nPlease enter the driver path in the source code\nExiting...", 'red'))
        time.sleep(3)
        exit()
    
    else:
        print(colored("\nWrong driver path\nExiting...", 'red'))
        time.sleep(3)
        exit()
    
    print(colored("Success!", 'green'))
    time.sleep(3)
    return(driver)


# To login into the goggle account
def login():
    clrscr()
    print("Logging into Google account... ")
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
    print(colored("Success!", 'green'))
    time.sleep(1)


# To navigate to the meeting link and enter the meeting
def attendMeet(link):
    global STATUS
    clrscr()
    print("\nNavigating to Google Meet... ")
    print(colored("Success!", 'green'))
    print("\nEntering Google Meet... ")
    driver.get(link)

    try:
        joinButton = wait.until(when.element_to_be_clickable((by.XPATH, joinButton1Path)))
    except:
        joinButton = wait.until(when.element_to_be_clickable((by.XPATH, joinButton2Path)))
    time.sleep(1)
    joinButton.click()

    print(colored("Success!", 'green'))
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

    print(colored("\nNow attending Google Meet", 'green'))
    STATUS[0] = "Attending meeting"
    time.sleep(2)
    clrscr()
    print(MENU, end="")


# To exit the meeting after ending
def endMeet():
    list = driver.find_element_by_xpath(listButtonCrossPath)
    list.click()
    time.sleep(1)
    endButton = driver.find_element_by_css_selector(endButtonPath)
    endButton.click()
    clrscr()
    print(colored("\nSuccessfully ended Google Meet", 'green'))
    time.sleep(2)
    clrscr()
    print(MENU, end="")


# The seperate process that attends the meeting
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
            print(colored("Omiting the next meeting because time is negative", 'yellow'))
            MEET_LINK.pop(0)
            time.sleep(5)
            clrscr()
            print(MENU, end="")
            continue
        attendMeet(link.split()[0])
        MEET_LINK.pop(0)
        time.sleep(1200)
        while True:
            numPeople = driver.find_element_by_xpath(studentNumberPath).get_attribute('textContent')
            numPeople = int(str(numPeople[1:-1]))
            if numPeople < 20:
                endMeet()
                break
            else:
                time.sleep(5)
    clrscr()
    print(colored("\n\nAll Meets completed successfully.", 'green'))
    STATUS[0] = "idol"
    time.sleep(2)
    clrscr()
    print(MENU, end="")


# To show the bot status
def showStatus():
    global STATUS
    clrscr()
    print(colored(f"The bot is {STATUS[0]}", 'yellow'))
    input(colored("\n\n[Press Enter to go back to the main menu] ", 'green'))


# To print the remaining meetings and their timings
def showSchedule():
    global MEET_LINK
    clrscr()
    if len(MEET_LINK) > 0:
        for index, link in enumerate(MEET_LINK):
            print(colored(f"{index+1}) {link.split()[0]} at {link.split()[1]}", 'cyan'))
    else:
        print(colored("No meetings scheduled currently", 'yellow'))
    input(colored("\n\n[Press Enter to go back to the main menu] ", 'green'))


# To add more meetings
def addMeetings():
    global MEET_LINK, STATUS, meetProcess
    flag = 'y'
    clrscr()
    while flag.lower() == "y" or flag.lower() == "yes":
        url = input("Enter the meeting url: ")
        timming = input("Enter the time for joining in 24 hour format (HH:MM:SS): ")
        MEET_LINK.append(url.strip()+" "+timming.strip())
        flag = input(colored("\nMeeting added successfully.\n\nAdd new meeting? (y/N): ", 'green'))
    if len(multiprocessing.active_children()) == 2:
        meetProcess = multiprocessing.Process(target=attendProcess, args=(MEET_LINK, STATUS))
        meetProcess.start()
    sortMeetings()


# To modify or delete a meeting
def modifyMeeting():
    global MEET_LINK, STATUS, meetProcess
    choice = '1'
    while choice != '0':
        clrscr()
        print(colored("The current meeting schedule is:\n", 'yellow'))
        if len(MEET_LINK) > 0:
            for index, link in enumerate(MEET_LINK):
                print(colored(f"{index+1}) {link.split()[0]} at {link.split()[1]}", 'yellow'))
        else:
            print(colored("No meetings scheduled currently", 'yellow'))
            input(colored("\n\n[Press Enter to go back to the main menu] ", 'green'))
            return
    
        index = input(colored("\n\nEnter the meeting number to modify: ", 'green'))
        index = int(index) - 1
        while True:
            clrscr()
            print(colored(f"The chosen meeting is:\n{MEET_LINK[index].split()[0]} at {MEET_LINK[index].split()[1]}", 'cyan'))
            choice = input(colored("\n\n1: Change the meet link\n2: Change the meet timing\n3: Delete this meeting\n\nChoice: ", 'green'))
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
                print(colored("\nWrong input, try again", 'red'))
                time.sleep(3)

        clrscr()
        print(colored("The updated meeting schedule is:\n", 'cyan'))
        if len(MEET_LINK) > 0:
            for index, link in enumerate(MEET_LINK):
                print(colored(f"{index+1}) {link.split()[0]} at {link.split()[1]}", 'cyan'))
        else:
            print(colored("No meetings scheduled currently", 'yellow'))
    
        choice = input(colored("\n\n0: go back to main menu.\n1: Keep modifying more meetings\nAnswer: ", 'green'))
    

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


# For clearing the terminal except the banner
def clrscr():
    global BANNER
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
    print(len(multiprocessing.active_children()))
    print(multiprocessing.active_children())
    input(colored("\n\n[Press enter to go back to the main menu] ", 'green'))



#############################
####### Main function #######
#############################

if __name__ == "__main__":
    clrscr()
    USERNAME = input("Enter the username for gmail account: ") if USERNAME == "" else USERNAME
    PASSWORD = getpass.getpass("Enter the password for your gmail account: ") if PASSWORD == "" else PASSWORD

    clrscr()
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
            ans = input(MENU)
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
                print(colored("Cleaning up and exiting...", 'green'))
                driver.quit()
                meetProcess.terminate()
                time.sleep(3)
                clrscrAll()
                break
            elif ans == '6':
                showProcesses()
            else:
                print(colored("Wrong input, Try again", 'yellow'))
                time.sleep(3)

        meetProcess.join()
        

    except KeyboardInterrupt:
        clrscr()
        print(colored("\n\nCTRL ^C\nThrew a wrench in the works.", 'yellow'))
        print(colored("Press Enter to exit.", 'yellow'))
        input()
        print(colored("Cleaning up and exiting...", 'yellow'))
        try:
            driver.quit()
        except Exception:
            pass
        try:
            meetProcess.terminate()
        except Exception:
            pass
        time.sleep(3)
        clrscrAll()

    except Exception:
        print(colored("An error occured", 'red'))
        print(colored("Press Enter to exit.", 'red'))
        input()
        print(colored("Cleaning up and exiting...", 'red'))
        try:
            driver.quit()
        except Exception:
            pass
        try:
            meetProcess.terminate()
        except Exception:
            pass
        time.sleep(3)
        clrscrAll()