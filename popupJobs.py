
#Tried to use the html code to switch page but it didnt work.
from selenium import webdriver
from time import sleep
from selenium.webdriver import ActionChains


def startJobsSites(job_dict):
    driver = webdriver.Chrome("C:/Users/alleballe/Downloads/chromedriver.exe")
    for key in job_dict:
        driver.get(key)
    sleep(23232)
    driver.close()


# driver = webdriver.Chrome("C:/Users/alleballe/Downloads/chromedriver.exe")
# driver.get("https://se.indeed.com/Internship-jobb")
# print(driver.title)
# #assert "Python" in driver.title
# elem = driver.find_element_by_class_name("pagination-list")
# elem = elem.find_element_by_xpath("//li/a[@aria-label='Nästa']")
# print(elem)
# assert "No results found." not in driver.page_source
# assert elem
#
# action = ActionChains(driver).click(elem)
# action.perform()
# print(elem)
#
# driver.close()