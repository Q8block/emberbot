from datetime import datetime, timedelta
import pyautogui as pyautogui
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import csv
from webdriver_manager.chrome import ChromeDriverManager
import json
import traceback
import traceback
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
from email.mime.image import MIMEImage
import smtplib
from bs4 import BeautifulSoup
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.chrome import ChromeDriverManager
import sys

chosen_profile = 'Profile 1'
expiration_in_hours = 24
the_offer = 0.00
all_time_stamps = []
x = 0
starting_land_index = 0
ending_land_index = 0
min_price = 0.15
max_price = 0.1685



print("--------Welcome---------")
while True:
    strChoice = input("which profile would you like to choose?, 1, 2, 3 etc...?")
    if strChoice == '1':
        chosen_profile = 'Profile 1'
    elif strChoice == '2':
        chosen_profile = 'Profile 2'
    elif strChoice == '3':
        chosen_profile = 'Profile 3'
    elif strChoice == '4':
        chosen_profile = 'Profile 4'
    else:
        print(f"{strChoice} is not  a valid choice sir, please choose again")
        continue

    input_files = csv.DictReader(open("lands.csv", encoding='Latin1'))
    print(input_files)
    list_of_lands = []
    for row in input_files:
        list_of_lands.append(row)

    print(f"number of embersword lands: {str(len(list_of_lands))}")
    starting_land_index = int(input("starting id?..."))
    ending_land_index = int(input("ending id?..."))

    print(f"-----------{chosen_profile}------------")

    print(f"number of lands: {str(ending_land_index-starting_land_index)}")
    seconds = (ending_land_index-starting_land_index)*20
    mins = float(seconds/60)
    hours = float(mins/60)
    print(f"estimated time: {str(round(hours, 2))} hours")
    choice = input("confirm?  (y)(n)")
    if choice == 'y':
        break
    else:
        continue

# functions
def send_email(user, pwd, recipient, subject, body):



    FROM = user
    TO = recipient if isinstance(recipient, list) else [recipient]
    SUBJECT = subject
    TEXT = body

    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.login(user, pwd)
    server.sendmail(FROM, TO, message)
    server.close()
    print('successfully sent the mail')
def average(lst):
    return sum(lst) / len(lst)

options = Options()
options.add_argument(f'--user-data-dir=C:/Users/Ahmad/AppData/Local/Google/Chrome/User Data/{chosen_profile}')
options.add_argument("--profile-directory=Default")
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)



# Name,X-axis,Y-axis,Owner,Offer/Price,URL

input('click anything to start!')
# for idx, val in enumerate(ints):
for index, item in enumerate(list_of_lands, start=1):
        if index < starting_land_index:
            print(f"skipping {index}  item id: {item['id']}")
            continue
        if index >= ending_land_index:
            print("job done!")
            sys.exit()
        starting_time = time.perf_counter()
        try:
            # get offer value
            driver.get(item['URL'])
            time.sleep(1.5)

            driver.implicitly_wait(3)

            #detect price
            try:
                price = driver.find_element_by_class_name('Price--amount')
                float_price = float(price.text)

                if min_price <= float_price < max_price:
                    the_offer = float_price + 0.001
                elif float_price < min_price:
                    the_offer = min_price
                elif float_price >= max_price:
                    the_offer = min_price
            except:
                print("couldnt find price")
            print(f"{str((index-starting_land_index)+1)}/{ending_land_index-starting_land_index}")
            if float_price > max_price:
                print(f"I think there is no offer, let's make a {min_price} bid")
            else:
                print(f"detected highest offer price: {float_price}, offering {the_offer}")
            # click the make offer button
            makeoffer = driver.find_element_by_xpath("//*[contains(text(), 'Make offer')]")
            time.sleep(1.5)
            Hover = ActionChains(driver).move_to_element(makeoffer).move_to_element(makeoffer)
            Hover.click().perform()
            driver.implicitly_wait(2)

            driver.find_element_by_xpath("//input[@placeholder='Amount']").send_keys(str(round(the_offer, 3)))
            try:
                driver.find_element_by_id("tos").click()
            except:
                y = ""

            # fill the form
            # modal = driver.find_element_by_class_name('Modalreact__Dialog-sc-xyql9f-0')
            # custom_date_select = modal.find_element_by_xpath("//input[@value='7 days']")
            # custom_date_select.click()
            #
            # buttons = modal.find_elements_by_css_selector('li > button')
            # buttons[-1].click()
            #
            # number_of_hours = expiration_in_hours
            #
            # expiry_time = datetime.now() + timedelta(hours=number_of_hours)
            # expiry_time = expiry_time.strftime("%m%d%I%M%p")
            #
            # time.sleep(1.5)
            # # make sure you open the browser and don't touch your keyboard when this code is running
            # dateimepicker = modal.find_element_by_class_name('Buttonreact__StyledButton-sc-glfma3-0')
            # dateimepicker.click()
            # pyautogui.write(expiry_time)
            # pyautogui.write('\n')
            #
            # submit the form
            driver.implicitly_wait(2)
            driver.find_element_by_xpath("//*[contains(text(), 'Make Offer')]").click()
            driver.implicitly_wait(2)
            time.sleep(1.5)

            #sign form
            try:
                driver.find_element_by_xpath(
                    "/html/body/div[11]/div/div/div/section/div/div/section/div/div/div/div/div/div/div/button").click()
            except:
                y = ""
            try:
                driver.find_element_by_xpath(
                    "/html/body/div[13]/div/div/div/section/div/div/section/div/div/div/div/div/div/div/button").click()
            except:
                y=""

            #sign metamask
            attempts = 0
            while attempts < 5:
                time.sleep(2.5)
                try:
                    attempts += 1
                    main_page = driver.current_window_handle
                    login_page = any
                    for handle in driver.window_handles:
                        if handle != main_page:
                            login_page = handle
                    driver.switch_to.window(login_page)
                    if attempts == 4:
                        driver.close()
                        print("unsuccessful, there might be a fee, closing metamask")
                        time.sleep(2)
                        driver.implicitly_wait(10)
                        driver.switch_to.window(main_page)
                        time.sleep(2)
                        break
                    else:
                        driver.find_element_by_xpath("//button[@data-testid='request-signature__sign']").click()
                        time.sleep(2)
                        driver.implicitly_wait(10)
                        driver.switch_to.window(main_page)
                        time.sleep(2)

                    break
                except:
                    print("something went wrong with signing metamask, retrying...")

            ending_time = time.perf_counter()
            time_stamp = ending_time - starting_time
            all_time_stamps.append(time_stamp)
            print(f"offer successful!.")
            print("average offer time: " + str(round(average(all_time_stamps), 2)))
            print(f"{str((index-starting_land_index)+1)}/{ending_land_index-starting_land_index}")
            print("--------------------")
        except:
            print("something went wrong, going to next loop ")
            time.sleep(10)
seconds = round(sum(all_time_stamps), 2)
print(f"summery:")
print(f"time taken: {str(seconds)}")
print("average offer time: " + str(round(average(all_time_stamps), 2)))

