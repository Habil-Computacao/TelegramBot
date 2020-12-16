import time

from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait

# options.addArguments("--auto-open-devtools-for-tabs");


class WebDriver:
    def __init__(self):
        self.driver = Chrome()

    def setUrl(self, url: str):
        self.driver.get(url)


class BetwayApi(WebDriver):
    def __init__(self):
        super().__init__()
        self.baseUrl = 'https://sports.betway.com/pt/sports'
        self.setUrl(self.baseUrl)

    def changeCatergory(self, name: str):
        WebDriverWait(self.driver, timeout=20).until(lambda d: d.find_elements_by_xpath(xpath="//*[@class='categoryListItemWrapper contentSelectorItemButton']") is not None or [])
        categories = self.driver.find_elements_by_xpath(xpath="//*[@class='categoryListItemWrapper contentSelectorItemButton']")
        categoriesText = []
        # for category in categories

    def getGameList(self):
        WebDriverWait(self.driver, timeout=20).until(lambda d: d.find_element_by_xpath(xpath="//*[@class='layout premiumLayout collection vertical']") is not None or [])
        time.sleep(3)
        container = self.driver.find_element_by_xpath(xpath="//*[@class='layout premiumLayout collection vertical']")
        anchors = container.find_elements(By.CLASS_NAME, 'scoreboardInfoNames')
        for anchor in anchors:
            # anchor.find_element(By.TAG_NAME, '')
            print(anchor)
            print(anchor.text)
            print(anchor.get_attribute('href'))

    def getGameInfo(self):
        pass

    def takeScreenShot(self):
        self.driver.save_screenshot('screen.png')

    def run(self):  # , url=None):
        # if url is None:
        #     url = self.baseUrl
        # self.setUrl(url)
        self.getGameList()
