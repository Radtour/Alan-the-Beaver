from selenium import webdriver
from selenium.webdriver.common.keys import Keys

url = 'https://www.epicbundle.com/category/article/for-free/'

browser = webdriver.Firefox()
browser.get(url)

posts_element = browser.find_elements_by_xpath('/html/body/div/div[1]/section[1]/main/div/div')

for element in posts_element:
    title_element = element.find_element_by_class_name('entry-title')
    title_element.send_keys(Keys.CONTROL + 'T')
