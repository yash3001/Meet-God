# from termcolor import colored

# MENU1 = colored("""
#  --------------------------------------
# |            MAIN MENU                 |
# |--------------------------------------|
# | 1: Show bot status                   |
# | 2: Show Schedule                     |
# | 3: Add more meetings                 |
# | 4: Update/Delete an existing meeting |
# | 5: Exit and shutdown the bot         |
# | 6: Show Processes                    |
#  --------------------------------------""", 'cyan')

# MENU2 = colored("""

# > Choice: """, 'green')

# MENU = MENU1 + MENU2

# BANNER1 = colored('''
#  ███▄ ▄███▓▓█████ ▓█████▄▄▄█████▓     ▄████  ▒█████  ▓█████▄ 
# ▓██▒▀█▀ ██▒▓█   ▀ ▓█   ▀▓  ██▒ ▓▒    ██▒ ▀█▒▒██▒  ██▒▒██▀ ██▌
# ▓██    ▓██░▒███   ▒███  ▒ ▓██░ ▒░   ▒██░▄▄▄░▒██░  ██▒░██   █▌
# ▒██    ▒██ ▒▓█  ▄ ▒▓█  ▄░ ▓██▓ ░    ░▓█  ██▓▒██   ██░░▓█▄   ▌
# ▒██▒   ░██▒░▒████▒░▒████▒ ▒██▒ ░    ░▒▓███▀▒░ ████▓▒░░▒████▓ 
# ░ ▒░   ░  ░░░ ▒░ ░░░ ▒░ ░ ▒ ░░       ░▒   ▒ ░ ▒░▒░▒░  ▒▒▓  ▒ 
# ░  ░      ░ ░ ░  ░ ░ ░  ░   ░         ░   ░   ░ ▒ ▒░  ░ ▒  ▒ 
# ░      ░      ░      ░    ░         ░ ░   ░ ░ ░ ░ ▒   ░ ░  ░ 
#        ░      ░  ░   ░  ░                 ░     ░ ░     ░    
#                                                       ░''', 'blue')
# BANNER2 = colored('''
#            ------------------------------------
#           |   Meet God : The Google Meet Bot   |
#            ------------------------------------''', 'red')

# BANNER3 = colored('''

# . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . ''', 'yellow')

# BANNER = BANNER1 + "\n" + BANNER2 + BANNER3

# print(BANNER)
# print(MENU)


# print('1'.lower())
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

BROWSER_DRIVER = ""

       if len(BROWSER_DRIVER) == 0:
            if os.name == "posix":
                while True:
                    choice = input("What platform are you on?\n1) Linux\n2) Mac\n> Answer(1 or 2): ")
                    if choice.lower() == "1" or choice.lower() == 'linux':
                        choice = input("What is your architecture?\n1) 64bit\n2) 32bit\n> Answer(1 or 2):")
                        if choice.lower() == "1" or choice.lower() == '64bit':
                            choice = input("What Browser do you use?\n1) Firefox\n2) Chromium\n> Answer(1 or 2):")
                            if choice.lower() == "1" or choice.lower() == 'firefox':
                                BROWSER_DRIVER = "FirefoxDrivers/linux64/geckodriver"
                                break
                            elif choice.lower() == "2" or choice.lower() == 'chromium':
                                BROWSER_DRIVER = "ChromeDrivers/linux64/chromedriver"
                                break
                            else:
                                print(colored("Wrong input, try again", 'red'))
                                time.sleep(3)
                                continue
                        elif choice.lower() == "2" or choice.lower() == '32bit':
                            choice = input("What Browser do you use?\n1) Firefox\n2) Chromium\n> Answer(1 or 2):")
                            if choice.lower() == "1" or choice.lower() == 'firefox':
                                BROWSER_DRIVER = "FirefoxDrivers/linux32/geckodriver"
                                break
                            elif choice.lower() == "2" or choice.lower() == 'chromium':
                                BROWSER_DRIVER = "ChromeDrivers/linux64/chromedriver"
                                break
                            else:
                                print(colored("Wrong input, try again", 'red'))
                                time.sleep(3)
                                continue
                        else:
                            print(colored("Wrong input, try again", 'red'))
                            time.sleep(3)
                            continue

                    elif choice.lower() == "2" or choice.lower() == 'mac':
                        choice = input("What Browser do you use?\n1) Firefox\n2) Chromium\n> Answer(1 or 2):")
                        if choice.lower() == "1" or choice.lower() == 'firefox':
                            BROWSER_DRIVER = "FirefoxDrivers/mac64/geckodriver"
                            break
                        elif choice.lower() == "2" or choice.lower() == 'chromium':
                            BROWSER_DRIVER = "ChromeDrivers/mac64/chromedriver"
                            break
                        else:
                            print(colored("Wrong input, try again", 'red'))
                            time.sleep(3)
                            continue
                    else:
                        print(colored("Wrong input, try again", 'red'))
                        time.sleep(3)
                        continue

            elif os.name == 'nt':
                choice = input("What is your architecture?\n1) 64bit\n2) 32bit\n> Answer(1 or 2):")
                if choice.lower() == "1" or choice.lower() == '64bit':
                    choice = input("What Browser do you use?\n1) Firefox\n2) Chrome\n> Answer(1 or 2):")
                    if choice.lower() == "1" or choice.lower() == 'firefox':
                        BROWSER_DRIVER = "FirefoxDrivers/win64/geckodriver.exe"
                        break
                    elif choice.lower() == "2" or choice.lower() == 'chromium':
                        BROWSER_DRIVER = "ChromeDrivers/win32/chromedriver.exe"
                        break
                    else:
                        print(colored("Wrong input, try again", 'red'))
                        time.sleep(3)
                        continue
                elif choice.lower() == "2" or choice.lower() == '32bit':
                    choice = input("What Browser do you use?\n1) Firefox\n2) Chrome\n> Answer(1 or 2):")
                    if choice.lower() == "1" or choice.lower() == 'firefox':
                        BROWSER_DRIVER = "FirefoxDrivers/win32/geckodriver.exe"
                        break
                    elif choice.lower() == "2" or choice.lower() == 'chromium':
                        BROWSER_DRIVER = "ChromeDrivers/win32/chromedriver.exe"
                        break
                    else:
                        print(colored("Wrong input, try again", 'red'))
                        time.sleep(3)
                        continue
                else:
                    print(colored("Wrong input, try again", 'red'))
                    time.sleep(3)
                    continue
            
            else:
                print(colored("Platform not supported\nExiting...", 'red'))
                time.sleep(3)
                exit()