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
        self.year_dict = {}

        
    def get_winners_and_losers(self):
        logger.info("Getting winners and losers")
        container_td_xpath = "//td[contains(text(), 'over')]"
        winner_xpath = container_td_xpath + "/*[1]"
        loser_xpath = container_td_xpath + "/*[2]"
        playoffs_winners_list = []
        playoffs_losers_list = []
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
            playoffs_winners_list.append(winner_elements[index].text)
            playoffs_losers_list.append(loser_elements[index].text)

        return [playoffs_losers_list, playoffs_winners_list]




    def get_team_stats(self, team, year="2020"):
        logger.info("Getting team stats")
        self.url = 'https://www.basketball-reference.com/playoffs/NBA_' + str(year) + '.html' 
        self.driver.get(self.url)  
        #//div[@id='all_totals_team-opponent']//td/a[contains(text(), 'Dallas')]/../../.
        row_xpath = "//div[@id='all_totals_team-opponent']//td/a[contains(text(), '" + team + "')]/../../*" # This gives all the children in the xpath
        try:
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.XPATH, row_xpath))
            )
            stat_elements = self.driver.find_elements(By.XPATH, row_xpath )
            logger.info("Stats captured")
        except Exception as e:
            logger.error(e)
            logger.exception("Stats fail to capture")
        list_of_stats = []

        for index in range(25): #There are 25 stats we want. The xpath finds the opponent stats too and we don't want that so just manually setting length to 25.
            list_of_stats.append(stat_elements[index].text)

        return list_of_stats

    def get_stats_for_year(self, year):
        logger.info("Getting year stats")
        self.url = 'https://www.basketball-reference.com/playoffs/NBA_' + str(year) + '.html' 
        self.driver.get(self.url) 
        winners_and_losers = self.get_winners_and_losers()
        self.year_dict[year] = {}
        for team in winners_and_losers[0]:
            team_stats = self.get_team_stats(team, year)
            self.year_dict[year][team] = team_stats

if __name__ == '__main__':
    web_scraper = Bot_scraper()
    #for year in range(2017, 2018):
    #    web_scraper.get_stats_for_year(year)
    web_scraper.get_stats_for_year(2020)
    logger.info(web_scraper.year_dict)