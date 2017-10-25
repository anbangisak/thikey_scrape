import time

# from os.path import abspath, dirname
from selenium import webdriver
from fetchone.models import GovDetail, DetailLink, ListinLink
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
        self.detail_links = []

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
                    listin_lk, created = ListinLink.objects.get_or_create(
                        url=list_page_link)
        print self.listing_links

    def detail_pg_list(self):
        for lt_lks in ListinLink.objects.filter(crawled=False):
            self.driver.get(lt_lks.url)
            time.sleep(1)
            options = self.driver.find_elements_by_xpath(
                '//select[@name="navInfo[itemsPerPage]"]/option')
            self.driver.find_element_by_xpath(
                "//select[@name='navInfo[itemsPerPage]']/option[text()='{0}']".format(
                    options[len(options) - 1].text)).click()
            time.sleep(5)
            print "-- sleep complete --"
            pages = self.driver.find_elements_by_xpath(
                "//a[@class='navigator_products_link']")
            # for page in range(len(pages)):
            while True:
                boxes = self.driver.find_elements_by_xpath(
                    "//div[@class='brief_box']")
                for box in boxes:
                    dtl_lnk = box.find_element_by_xpath(
                        ".//div[@class='brief_name']/a").get_attribute("href")
                    self.detail_links.append(dtl_lnk)
                    de_lk, created = DetailLink.objects.get_or_create(
                        url=dtl_lnk)
                pages = self.driver.find_elements_by_xpath(
                    "//a[@class='navigator_products_link']")
                if len(pages):
                    [pg.click() for pg in pages if pg.text == ">"]
                else:
                    break
                # if len(pages) and pages[len(pages) - 1].text == ">>":
                    # pages[len(pages) - 2].click()
                # elif len(pages) and pages[len(pages) - 1].text == ">":
                #     pages[len(pages) - 1].click()
                # else:
                #     break
                time.sleep(5)
            lt_lks.crawled = True
            lt_lks.save()
        print self.detail_links

    def get_detail_data(self):
        for dtl_lks in DetailLink.objects.filter(crawled=False):
            self.driver.get(dtl_lks.url)
            gov, created = GovDetail.objects.get_or_create(url=dtl_lks.url)
            time.sleep(1)
            if gov:
                gov.name = self.driver.find_element_by_xpath(
                    '//*[@id="dt_name"]/h1').text
                gov.img = self.driver.find_element_by_xpath(
                    '//*[@id="dt_imagebox"]/div[@class="mainbigimage"]/img'
                ).get_attribute('src')
                gov.large_img = self.driver.find_element_by_xpath(
                    '//*[@id="dt_imagebox"]/div[@class="mainbigimage"]/img'
                ).get_attribute('largeimagefullname')
                prop_str = self.driver.find_element_by_xpath(
                    '//*[@id="dt_propertyinfo"]').text
                gov.desc = self.driver.find_element_by_xpath(
                    '//*[@id="dt_disc"]/div[@class="dt_spec_content"]').text
                props = prop_str.split("\n")
                prop_dict = {}
                [prop_dict.update(
                    {"condition": s.replace("Condition: ", "")}
                ) for s in props if "Condition: " in s]
                [prop_dict.update(
                    {"upc": s.replace("UPC: ", "")}
                ) for s in props if "UPC: " in s]
                [prop_dict.update(
                    {"sku": s.replace("SKU: ", "")}
                ) for s in props if "SKU: " in s]
                cats = self.driver.find_elements_by_xpath(
                    "//span[@class='breadcrumbsItem']")
                gov.category = cats[len(cats) - 1].find_element_by_xpath(
                    ".//a").text
                gov.crawled = True
                gov.sku = prop_dict.get("sku", None)
                gov.upc = prop_dict.get("upc", None)
                gov.condition = prop_dict.get("condition", None)
                gov.save()
            dtl_lks.crawled = True
            dtl_lks.save()

    def driver_destroy(self):
        self.driver.close()


def to_use():
    from fetchone.begin_scrape import ScrapeIn
    obj = ScrapeIn()
    obj.get_in()
    obj.driver_destroy()
