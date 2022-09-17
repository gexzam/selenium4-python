import re
from data import *
from time import sleep
from datetime import datetime
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.common.exceptions import TimeoutException


# Chrome setup on Dokku
options = Options()
options.add_argument("--headless")
options.add_argument("--window-size=1461,841")
options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(service=Service("/app/.chromedriver/bin/chromedriver"), options = options)


def login():
    driver.get("https://url-here.com")
    print("Login...")
    login_button = wait(driver, 10)\
                    .until(EC.presence_of_element_located(
                        (By.CSS_SELECTOR, '#navbar > ul.nav.navbar-nav.navbar-right > li.visible-lg.visible-md > a')
                    ))
    login_button.click()

    #Wait to modal for login input
    wait(driver, 8).until(EC.presence_of_all_elements_located((By.ID, 'myModal')))

    #Insert user
    wait(driver, 2)\
        .until(EC.element_to_be_clickable((By.ID, 'd_uname')))\
        .send_keys(USER)

    #Insert password
    wait(driver, 2)\
        .until(EC.element_to_be_clickable((By.ID, 'd_upass')))\
        .send_keys(PASSW)

    #Click on Login button (enter to dashboard)
    wait(driver, 1)\
        .until(EC.element_to_be_clickable((By.ID, 'desktoplogin')))\
        .click()

    print("Logueado")

    #Click on 'Available Jobs by State' button
    wait(driver, 5)\
        .until(EC.presence_of_element_located((By.LINK_TEXT , 'Available Jobs by State')))\
        .click()


#CHECK JOBS WORK STARTS HERE


#Function to make match between item and list
def match (item: str, list: list) -> bool:
    if item in list: return True


def check_jobs():
    print("\n\n/////////////////////////////////// START \n")
    
    while(True):
        try:
            #Go to direct URL state, where 9 is Florida
            florida = driver.get('https://url-here.com/index.php?state=9')

            #Wait for availablejobs div
            wait(driver, 3)\
            .until(EC.presence_of_element_located((By.CSS_SELECTOR , '#availablejobs > div.left.even')))
            break
        except TimeoutException:
            print("Empty list, nothing to do...")
    
    available_jobs = driver.find_elements(By.CSS_SELECTOR, "#availablejobs > div.left.even")

    if available_jobs:
        now = datetime.now().strftime("%m/%d/%Y, %H:%M")
        jobs_count = len(available_jobs)
        print(now)
        print(f"### {jobs_count} JOBS AVAILABLES ###\n")
        print("checking...\n")
        
        #Iterate with each available job (item) and check if match with zipcode, appliance and brand
        for item in available_jobs:
            job_refer = item.find_element(By.CSS_SELECTOR, 'div.span-12 div:nth-child(2)').text
            zipcode = item.find_element(By.CSS_SELECTOR, 'div.span-12 div:nth-child(5)').text
            zipcode = re.search("\d\d\d\d\d", zipcode).group()
            appliance = item.find_element(By.CSS_SELECTOR, 'div.span-12 div:nth-child(11)').text
            brand = item.find_element(By.CSS_SELECTOR, 'div.span-12 div:nth-child(14)').text
            print(f"JOB ITEM: {job_refer} - {zipcode} - {appliance} - {brand}")
            print(f"JOB ITEM: {job_refer} - {zipcode}")
            
            #if match(zipcode, zipcode_accepted) and match(appliance, appliance_accepted) and match(brand, brands_accepted):
            if match(zipcode, zipcode_accepted):
                item.find_element(By.CSS_SELECTOR, "div.span-3.last.prepend-top.left > button").click()
                alert = wait(driver, 1).until(EC.alert_is_present())
                alert.accept()
                print(f">>>>>>>>>>>  TOTAL MATCH!: job - {job_refer} | zc - {zipcode} | Booked at {now}")


def run():
    login()
    while (True):
        check_jobs() #Execute this function infitely
        print("\n --- loading... --- \n")
        sleep(0.1)


if __name__ == '__main__':
    run()