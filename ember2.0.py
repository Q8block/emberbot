import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import chromedriver_autoinstaller
import csv
import pathlib
import sys

chromedriver_autoinstaller.install()

options = webdriver.ChromeOptions()

# userpath = '/Users/username/Library/Application Support/Google/Chrome'
#
# options.add_argument(f"--user-data-dir={userpath}")

options.add_argument("user-data-dir=selenium")
scriptDirectory = pathlib.Path().absolute()

# For windows
options.add_argument(f'user-data-dir={scriptDirectory}\\chrome_data')

# For Mac
# options.add_argument(f'user-data-dir={scriptDirectory}/chrome_data')

options.add_experimental_option("excludeSwitches", ["enable-logging"])

offer_limit = 2
min_price = 0.04
max_price = 0.06
the_offer = 0
const = 4.3721581
starting_vox_id = 0
ending_vox_id = 0
range_max = 0
range_min = 0


f = open('lands.csv', mode='r', encoding="utf8")
data = csv.reader(f)
row_list = []

for row in data:
    row_list.append(row)
f.close()

driver = webdriver.Chrome(options=options)

vox_list = []

#skip to 3698
#filtering
for i in row_list:
    if i[0] == 'Name':
        continue
    # if int(i[0]) <= 257:
    #     continue
    vox_list.append(i)

time.sleep(2)


if 'account' not in driver.current_url:
    while True:
        driver.get('https://opensea.io/login')
        time.sleep(3)
        driver.refresh()
        metamask_div = driver.find_element(By.XPATH, '//span[contains(text(),"MetaMask")]')
        metamask_div.click()
        while len(driver.window_handles) == 1:
            time.sleep(0.5)
            continue
        driver.switch_to.window(driver.window_handles[1])

        if 'download' in driver.current_url:
            input('Download the metamask extension and set password  '
                  'then press Enter to continue automation...')
            # if len(driver.window_handles) > 1:
            #     for window in driver.window_handles[1:]:
            #         driver.switch_to.window(window)
            #         driver.close()
            print('Restarting chrome driver to start automation..')
            driver.quit()
            driver = webdriver.Chrome(options=options)
            continue
        break

    for i in range(10):
        pass_textbox = driver.find_elements(By.ID, 'password')
        if pass_textbox:
            pass_textbox[0].send_keys('Sabola1992!')
            pass_textbox[0].submit()
            break
        time.sleep(0.5)

    time.sleep(2)

    driver.switch_to.window(driver.window_handles[0])

    time.sleep(2)


time.sleep(2)
x = 0
ind = 0

for row in vox_list[1:]:

    while True:
        try:

            x = x+1
            ind = ind+1

            if x >= 5:
                print('skipping this one!')
                x = 0
                break
            old_time = time.time()

            driver.get(row[5])

            # check if there is a window open
            if len(driver.window_handles) != 1:
                time.sleep(0.2)
                driver.switch_to.window(driver.window_handles[1])
                driver.close()

            for i in range(6):
                time.sleep(0.8)

                # detect price
                try:
                    price = driver.find_element_by_class_name('Price--amount')
                    float_price = float(price.text)

                    if min_price <= float_price < max_price:
                        the_offer = float_price + 0.001
                    elif float_price < min_price:
                        the_offer = min_price
                    elif float_price >= max_price:
                        the_offer = max_price
                except:
                    print("couldnt find price")
                    the_offer = min_price
                    float_price = 0.000

                #extra security
                if the_offer > offer_limit:
                    the_offer = offer_limit

                print('-------------------------------')
                print(f'price detected: {float_price}')
                print(f'offering: {the_offer}')
                print(f'-----------------------------')

                make_offer_btn = driver.find_elements(By.XPATH, '//button[text()="Make offer"]')

                if make_offer_btn:
                    driver.execute_script("arguments[0].click();", make_offer_btn[0])
                    break

            for i in range(20):
                amount_txtbox = driver.find_elements(By.XPATH, '//input[@placeholder="Amount"]')

                if amount_txtbox:
                    amount_txtbox[0].send_keys(str(round(the_offer, 3)))
                    break

                time.sleep(0.2)

            tos = driver.find_elements(By.ID, 'tos')

            if tos:
                tos[0].click()

            if not amount_txtbox:
                for i in range(80):
                    if len(driver.window_handles) != 1:
                        break
                    time.sleep(0.2)

                if len(driver.window_handles) > 1:
                    driver.switch_to.window(driver.window_handles[1])

                    if 'notification.html#connect' in driver.current_url:
                        print('Connect pop up detect: Connecting now...')
                        next_button = driver.find_element(By.XPATH, '//button[text()="Next"]')
                        next_button.click()
                        time.sleep(1)
                        connect_button = driver.find_element(By.XPATH, '//button[text()="Connect"]')
                        connect_button.click()
                        driver.close()
                        driver.switch_to.window(driver.window_handles[0])
                        continue
                    if 'signature-request' in driver.current_url:
                        print('Signature pop up detected: Signing authentication request..')
                        sign_button = driver.find_element(By.XPATH, '//button[text()="Sign"]')
                        sign_button.click()

                        time.sleep(1)
                        driver.switch_to.window(driver.window_handles[0])

                        for i in range(20):
                            amount_txtbox = driver.find_elements(By.XPATH, '//input[@placeholder="Amount"]')

                            if amount_txtbox:
                                amount_txtbox[0].send_keys('0.001')
                                break

                            time.sleep(0.2)

                        tos = driver.find_elements(By.ID, 'tos')

                        if tos:
                            tos[0].click()
                else:
                    print("Make offer button didn't work for some reason ")
                    continue

            for i in range(20):
                make_offer_btn1 = driver.find_elements(By.XPATH, '//button[text()="Make offer"]')
                if make_offer_btn1:
                    make_offer_btn1[1].click()
                    break

                time.sleep(0.2)

            for i in range(20):
                sign_btn1 = driver.find_elements(By.XPATH, '//button[text()="Sign"]')
                print(sign_btn1)
                if sign_btn1:
                    sign_btn1[0].click()
                    break

                time.sleep(0.2)

            # input()

            for i in range(50):
                if len(driver.window_handles) != 1:
                    break
                time.sleep(0.2)

            driver.switch_to.window(driver.window_handles[1])

            for i in range(20):
                scrolldown_btn = driver.find_elements(By.CLASS_NAME, 'signature-request-message__scroll-button')

                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

                sign_btn = driver.find_elements(By.XPATH, '//button[text()="Sign"]')

                if scrolldown_btn and sign_btn:
                    scrolldown_btn[0].click()

                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

                    sign_btn[0].click()
                    x = 0
                    break

                time.sleep(0.2)
            break
        except Exception as e:
            print(e)
            print('Some error occurred while making offer, trying again....')
            time.sleep(2)

    driver.switch_to.window(driver.window_handles[0])

    print('#' + str(ind) + '/'+ str(len(vox_list)) + ' Made offer in ' + str(round(time.time() - old_time, 2)) + ' secs')
