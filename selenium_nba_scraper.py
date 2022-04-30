import time
import os
import logging
import time
import os
import traceback

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from PIL import Image
from datetime import datetime
from io import BytesIO

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s : %(name)s : %(lineno)s : %(message)s ', datefmt='%m/%d/%Y %I:%M:%S %p')


class Bot_scraper: 
    
    def __init__(self):
        """
        Initializes an instance of the Bot_scraper class. 
        
            
        Attributes:
            driver (Selenium.webdriver.Chrome): The Chromedriver that is used to automate browser actions
            base_url (str): Base URL to the local site confessions will be typed in.
            actions (ActionsChains): Action chain. I do not believe it's actually used for anything at the moment. Might be used later, 
                                     might as well keep it.
        """ 
        
        
        file_handler = logging.FileHandler('logging.log', mode='w')
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)
        
        
        self.driver = webdriver.Chrome('chromedriver.exe')
        self.url = 'https://www.basketball-reference.com/playoffs/NBA_2020.html' 
        self.driver.get(self.url)      
        self.actions = ActionChains(self.driver) 
        self.loop_counter = 0
        self.playoffs_winners_list = []
        self.playoffs_losers_list = []

        try:
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.ID, self.text_area_id))
            )
            self.text_area = self.driver.find_element(By.ID, self.text_area_id)
            self.block_div = self.driver.find_element(By.ID, self.block_div_id)
            logger.info("Text area captured")
        except Exception as e:
            logger.error(e)
            logger.exception("Text area fail to capture")

        
    def get_winners_and_losers(self):
        container_td_xpath = "//td[contains(text(), 'over')]"
        winner_xpath = container_td_xpath + "/*[1]"
        loser_xpath = container_td_xpath + "/*[2]"

        try:
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.XPATH, container_td_xpath))
            )
            winner_elements = self.driver.find_elements(By.XPATH, winner_xpath )
            loser_elements = self.driver.find_elements(By.XPATH, loser_xpath)
            logger.info("Winners and losers captured")
        except Exception as e:
            logger.error(e)
            logger.exception("Winners and losers fail to capture")

        for index in range(len(winner_elements)):
            self.playoffs_winners_list.append(winner_elements[index].text)
            self.playoffs_losers_list.append(loser_elements[index].text)

        logger.info(self.playoffs_winners_list)
        logger.info(self.playoffs_losers_list)


if __name__ == '__main__':
    web_scraper = Bot_scraper()
    web_scraper.get_winners_and_losers()
