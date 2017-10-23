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
        for mainmenu in mainmenu_list:
            submenu_list = mainmenu.find_elements_by_xpath(
                ".//div/ul/div")
            for submenu in submenu_list:
                inner_sub_menu_list = submenu.find_elements_by_xpath(
                    ".//li/ul/li")
                for inner_submenu in inner_sub_menu_list:
                    list_page_element = inner_submenu.find_element_by_xpath(
                        ".//a")
                    list_page_link = list_page_element.get_attribute('href')
                    self.listing_links.append(list_page_link)
        print self.listing_links

    def driver_destroy(self):
        self.driver.close()


def to_use():
    from fetchone.begin_scrape import ScrapeIn
    obj = ScrapeIn()
    obj.get_in()
    obj.driver_destroy()
