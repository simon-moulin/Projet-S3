# OUTPUT : nom;img(base64)

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver

url = 'https://worldspinner.com/heraldry/device_editor/'
chrome_options = Options()
chrome_options.add_argument("--headless")  # no window
driver = webdriver.Chrome(options=chrome_options)
driver.get(url)

f = open("blasons.txt", 'a')

while True:
    img_b64 = WebDriverWait(driver, 20).until(
        lambda driver: driver.find_element_by_css_selector('img.device-preview').get_attribute('ng-src'))[22:]
    nom = driver.find_element_by_css_selector('em.ng-binding').get_attribute('innerHTML')[1:-1]
    print(nom)
    f.write(nom + ';' + img_b64 + '\n')
    driver.find_element_by_class_name('brass-button-small').click()
    #  wait end of js function trigged by the click
    WebDriverWait(driver, 20).until(
        lambda driver: driver.find_element_by_css_selector('em.ng-binding').get_attribute('innerHTML')[1:-1] != nom)