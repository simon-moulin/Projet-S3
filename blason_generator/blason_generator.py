"""
Generation of blazons and saving them in the file blazons.txt
Output format :
one blazon per line : name_of_the_blazon;image_in_base64_format

Genere des blasons et les sauvegardes dans le fichier blasons.txt
Format de sortie :
un blason par ligne : nom_du_blason;image_en_base64
"""

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver

OUTPUT_FILE = 'blasons.txt'

url = 'https://worldspinner.com/heraldry/device_editor/'
chrome_options = Options()
chrome_options.add_argument("--headless")  # no window
driver = webdriver.Chrome(options=chrome_options)
driver.get(url)

f = open(OUTPUT_FILE, 'a')

while True:
    # waiting for the image load
    img_b64 = WebDriverWait(driver, 20).until(
        lambda driver: driver.find_element_by_css_selector('img.device-preview').get_attribute('ng-src'))[22:]
    nom = driver.find_element_by_css_selector('em.ng-binding').get_attribute('innerHTML')[1:-1]
    print(nom)
    f.write(nom + ';' + img_b64 + '\n')
    driver.find_element_by_class_name('brass-button-small').click()
    #  wait for the new image loaded by the click on the Respin button
    WebDriverWait(driver, 20).until(
        lambda driver: driver.find_element_by_css_selector('em.ng-binding').get_attribute('innerHTML')[1:-1] != nom)
