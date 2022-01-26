from datetime import datetime, timedelta
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


# functions
def average(lst):
    return sum(lst) / len(lst)

options = Options()
options.add_argument('--user-data-dir=C:/Users/Ahmad/AppData/Local/Google/Chrome/User Data/Profile 1')
options.add_argument("--profile-directory=Default")
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
base = "https://opensea.io"

min_price = 0.155
max_price = 0.21
min_Y = 0
max_Y = 2
min_X = 0
max_X = 1
x = 0
lands_successfully_offered = 0
total_lands = 0
all_time_stamps = []
input('click anything to start!')



while True:
    driver.get(
        f"https://opensea.io/assets/embersword-land?search[categories][0]=virtual-worlds&search[chains][0]=MATIC&search"
        f"[numericTraits][0][name]=y-coordinate&search[numericTraits][0][ranges][0][max]={max_Y}&search[numericTraits][0]"
        f"[ranges][0][min]={min_Y}&search[numericTraits][1][name]=x-coordinate&search[numericTraits][1][ranges][0]"
        f"[min]={min_X}&search[numericTraits][1][ranges][0][max]={max_X}&search[sortAscending]=true&search"
        f"[sortBy]=PRICE&search[stringTraits][0][name]=Type&search[stringTraits][0][values][0]=Land")
    driver.implicitly_wait(2)
    obj = driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
    soup = BeautifulSoup(obj, 'html.parser')
    result = soup.findAll("article", {"class": ["AssetSearchList--asset"]})

    for eachavalue in result:
        driver.implicitly_wait(5)
        url = (base + eachavalue.find("a").get("href"))
        driver.get(url)
        time.sleep(2)
        starting_time = time.perf_counter()
        total_lands += 1
        try:
            # get offer value

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
            # number_of_hours = 36
            #
            # expiry_time = datetime.now() + timedelta(hours=number_of_hours)
            # expiry_time = expiry_time.strftime("%m%d%I%M%p")
            #
            # time.sleep(2)
            # # make sure you open the browser and don't touch your keyboard when this code is running
            # dateimepicker = modal.find_element_by_class_name('Buttonreact__StyledButton-sc-glfma3-0')
            # dateimepicker.click()
            # pyautogui.write(expiry_time)
            # pyautogui.write('\n')

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
            while True:
                time.sleep(2.5)
                try:
                    attempts += 1
                    main_page = driver.current_window_handle
                    login_page = any
                    for handle in driver.window_handles:
                        if handle != main_page:
                            login_page = handle
                    driver.switch_to.window(login_page)
                    if attempts >= 3:
                        driver.close()
                        print("unsuccessful, skipping this land")
                        time.sleep(2)
                        driver.implicitly_wait(10)
                        driver.switch_to.window(main_page)
                        time.sleep(2)
                        break
                    else:
                        driver.find_element_by_xpath("//button[@data-testid='request-signature__sign']").click()
                        print("successful offer")
                        lands_successfully_offered += 1
                        time.sleep(2)
                        driver.implicitly_wait(10)
                        driver.switch_to.window(main_page)
                        time.sleep(2)

                    break
                except:
                    print("metamask loaded slowly, retrying...")

            ending_time = time.perf_counter()
            time_stamp = ending_time - starting_time
            all_time_stamps.append(time_stamp)
            print("average offer time: " + str(round(average(all_time_stamps), 2)))
            print(f"{lands_successfully_offered}/{total_lands} lands offered")
            print("--------------------")


        except:
            print("something went wrong, going to next loop ")
            time.sleep(10)
    try:
        if min_X >= 199:
            min_Y = min_Y + 3
            max_Y = max_Y + 3
            min_X = 0
            max_X = 1
            continue

        if min_Y >= 199:
            print("WE HAVE DONE IT")
            print(f"summery:")
            print(f"time taken: {round(sum(all_time_stamps), 2)}")
            break

        min_X = min_X + 2
        max_X = max_X + 2
    except:
        y=""

