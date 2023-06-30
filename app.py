from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

from config import username, password


def login(username, password):
    username_input = driver.find_element(By.NAME, "username")
    password_input = driver.find_element(By.NAME, "password")
    username_input.send_keys(username)
    password_input.send_keys(password)
    password_input.send_keys(Keys.ENTER)


def click_last_ticket():
    tbody_element = driver.find_element(By.TAG_NAME, "tbody")
    link_element = tbody_element.find_element(By.XPATH, "//tbody/tr[last()]/td/a")
    link_element.click()


# def scrape_page():
#     elements = driver.find_element(
#         By.XPATH,
#         "/html/body/div[1]/div[19]/div/main/div/div/div/div/div[2]/div/div/table/tbody/tr[6]/td[2]/strong/a[1]",
#     )
#     print(elements)


options = Options()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()), options=options
)

# open first page
driver.get("https://residentmap.kmcmh.com/#/support_desk")
driver.maximize_window()

login(username, password)

wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_element_located((By.TAG_NAME, "tbody")))

click_last_ticket()

# wait.until(
#     EC.presence_of_element_located(
#         elements=driver.find_element(
#             By.XPATH,
#             "/html/body/div[1]/div[19]/div/main/div/div/div/div/div[2]/div/div/table/tbody/tr[6]/td[2]/strong/a[1]",
#         )
#     )
# )
# scrape_page()

# Open new tab
driver.execute_script("window.open('about:blank', '_blank');")
driver.switch_to.window(driver.window_handles[-1])
driver.get("https://kingsley.residentmap.com/login.php?goto=%2Findex.php")

login(username, password)
