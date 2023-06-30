from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

from config import username, password, resident_map

# boilerplate
options = Options()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()), options=options
)
wait = WebDriverWait(driver, 10)

# Decl Vars
ticket_list_xpath = "/html/body/div[1]/div[18]/div/main/div/div/div/div[2]/div/div/div/div[1]/table/tbody"
ticket_property_xpath = "/html/body/div[1]/div[19]/div/main/div/div/div/div/div[2]/div/div/table/tbody/tr[6]/td[2]/strong/a"
ticket_unit_xpath = "/html/body/div[1]/div[19]/div/main/div/div/div/div/div[2]/div/div/table/tbody/tr[11]/td[2]/a/strong"
property_xpath = "/html/body/table[2]/tbody/tr[2]/td/table/tbody/tr[1]/td[4]/a"


# Functions


def login(username, password):
    username_input = driver.find_element(By.NAME, "username")
    password_input = driver.find_element(By.NAME, "password")
    username_input.send_keys(username)
    password_input.send_keys(password)
    password_input.send_keys(Keys.ENTER)


def scrape_page():
    property_element = driver.find_element(
        By.XPATH,
        ticket_property_xpath,
    )
    unit_element = driver.find_element(
        By.XPATH,
        ticket_unit_xpath,
    )
    property = property_element.get_attribute("innerHTML")
    unit = unit_element.get_attribute("innerHTML")
    return property, unit


def new_tab():
    driver.execute_script("window.open('about:blank', '_blank');")
    driver.switch_to.window(driver.window_handles[-1])


def switch_to_primary_tab():
    driver.switch_to.window(driver.window_handles[0])


def nav_to_property(property):
    change_property_link = driver.find_element(
        By.XPATH, "//a[contains(., 'CHANGE PROPERTY')]"
    )
    change_property_link.click()
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    property_link = driver.find_element(By.XPATH, f"//a[contains(., '{property}')]")
    property_link.click()


def nav_to_unit(unit):
    search = driver.find_element(By.NAME, "search_input")
    search.clear()
    search.send_keys(unit)
    search.send_keys(Keys.ENTER)


# open first page
driver.get("https://residentmap.kmcmh.com/#/support_desk")
driver.maximize_window()

login(username, password)


def open_ticket():
    switch_to_primary_tab()
    property, unit = scrape_page()
    new_tab()
    driver.get(resident_map)
    login(username, password)
    nav_to_property(property)
    nav_to_unit(unit)
