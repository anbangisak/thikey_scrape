# from os.path import abspath, dirname
from selenium import webdriver
# from selenium.webdriver.common.keys import Keys

# driver = webdriver.Firefox()
# chrome_driver_path = abspath(dirname(dirname(__file__))) + "/chromedriver"


class ScrapeIn(object):
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        chrome_driver_path = (
            "/home/malar/Documents/projects/python/"
            "govgroup_scrap/thikey_scrape/govgroup_scrape/chromedriver")
        self.driver = webdriver.Chrome(
            chrome_driver_path, chrome_options=options)
        self.listing_links = []

    def get_in(self):
        self.driver.get("http://www.govgroup.com/")
        mainmenu_list = self.driver.find_elements_by_xpath(
            "//ul[@class='pseudoct']/li")
        submenu_list = mainmenu_list[0].find_elements_by_xpath(
            ".//div/ul/div")
        inner_sub_menu_list = submenu_list[0].find_elements_by_xpath(
            ".//li/ul/li")
        list_page_element = inner_sub_menu_list[0].find_element_by_xpath(
            ".//a")
        list_page_link = list_page_element.get_attribute('href')
        self.listing_links.append(list_page_link)

    def driver_destroy(self):
        self.driver.close()
