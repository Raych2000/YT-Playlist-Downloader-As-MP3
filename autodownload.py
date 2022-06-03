# Used Imports
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By


# Relevant Elements Definition
x_input = "//input[@id='input' and @name='video']"
x_convert = "//input[@id='submit' and @value='Convert']"
x_download = "//a[@id='download' and text()='Download mp3']"
x_next = "//a[text()='Convert next']"
x_list_len = "(//div[@id='stats']//span)[1]"
x_video = "(//a[@id='video-title'])"

# Needed Lists
list = []
error_vids = []

# Get Playlist's Link
try:
    address = input("Enter Playlist's URL: ")
except:
    print("Input Must Be A String URL")

# Start Updated Chrome Driver
driver = webdriver.Chrome(ChromeDriverManager("latest").install())
driver.get(address)
driver.implicitly_wait(5)

# Get Length Of Playlist
list_len = WebDriverWait(driver, 5).until(ec.presence_of_element_located((By.XPATH, x_list_len))).text
for i in range(int(list_len) + 1):
    if i == int(list_len):
        break
    link = WebDriverWait(driver, 5).until(ec.presence_of_element_located((By.XPATH, x_video + "[" + str(i + 1) + "]"))).get_attribute("href")
    list.append(str(link))

# Go To MP3 Downloader
driver.get("https://ytmp3.cc/")


# Function To Search And Download If Can
def search_and_download(link):
    try:
        input = WebDriverWait(driver, 5).until(ec.presence_of_element_located((By.XPATH, x_input))).send_keys(link)
        convert = WebDriverWait(driver, 5).until(ec.presence_of_element_located((By.XPATH, x_convert))).click()
        download = WebDriverWait(driver, 3).until(ec.presence_of_element_located((By.XPATH, x_download))).click()
        time.sleep(0.5)
        driver.switch_to.window(driver.window_handles[1])
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        next = WebDriverWait(driver, 5).until(ec.presence_of_element_located((By.XPATH, x_next))).click()
        time.sleep(0.5)
        return True
    except:
        error_vids.append(list[i])
        driver.get("https://ytmp3.cc/")
        return False


# Download All Videos From Playlist
i = 0
while i < len(list):
    res = search_and_download(list[i])
    while res == False:
        i += 1
        res = search_and_download(list[i])
    i += 1


# Print Videos That Hasn't Downloaded
print("\n\n\n" + "Videos That Hasn't Been Downloaded: ")
print(error_vids)
print("\n\n\n")