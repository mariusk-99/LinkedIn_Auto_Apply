from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains

from confidential import password_file
import json
import time
import random

class EasyApplyLinkedIn:

    def __init__(self, data):
        """Parameter initialisation"""

        self.email = data['email']
        self.password = data['password']
        self.keywords = data['keywords']
        self.location = data['location']
        self.filter_experience = data['filter_experience']
        self.filter_date_posted = data['filter_date_posted']

        # Options() keeps the chrome tab open
        self.chrome_options = Options()
        self.chrome_options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(data['driver_path'], chrome_options=self.chrome_options)

        # Opening tab in fullscreen to overcome error with finding the keyword and location fields

        # Method 1: Starting in fullscreen (simulating F11 control):
        # self.chrome_options.add_argument("--start-fullscreen")
        
        # Method 2: Maximising the tab

        self.driver.maximize_window()


    def login_linkedin(self):
        """ This function logs into your personal LinkedIn profile"""

        # make driver go to the LinkedIn login url
        self.driver.get("https://www.linkedin.com/jobs/search")

        sign_in = self.driver.find_element(By.LINK_TEXT, "Sign in")
        sign_in.click()

        time.sleep(round(random.uniform(1,2),1))

        # introduce our email and password and hit enter
        login_email = self.driver.find_element(By.NAME, "session_key")
        login_email.clear()
        login_email.send_keys(self.email)

        login_password = self.driver.find_element(By.NAME, "session_password")
        login_password.clear()
        login_password.send_keys(self.password)
        login_password.send_keys(Keys.RETURN)


    def job_search(self):

        # introduce keyword and location and hit enter

        search_location = self.driver.find_element(By.XPATH, "//input[starts-with(@id, 'jobs-search-box-location')]")
        search_location.clear()
        search_location.send_keys(self.location)

        time.sleep(round(random.uniform(1,2),1))

        search_keyword = self.driver.find_element(By.XPATH, "//input[starts-with(@id, 'jobs-search-box-keyword')]")
        search_keyword.clear()
        search_keyword.send_keys(self.keywords)
        search_location.send_keys(Keys.RETURN)

    def filter(self):
        """ This function filters all the job results by '' """

        easy_apply_button = self.driver.find_element(By.XPATH, "//button[starts-with(@aria-label, 'Easy Apply filter.')]")
        easy_apply_button.click()
        time.sleep(round(random.uniform(1,2),1))

        all_filters_button = self.driver.find_element(By.XPATH, "//button[starts-with(@aria-label, 'Show all filters. ')]")
        all_filters_button.click()
        time.sleep(round(random.uniform(1,2),1))

        if "intern" in self.filter_experience:
            intern_level = self.driver.find_element(By.XPATH, "//label[@for='advanced-filter-experience-1']")
            intern_level.click()
            time.sleep(round(random.uniform(1,2),1))

        if "entry" in self.filter_experience:
            entry_level = self.driver.find_element(By.XPATH, "//label[@for='advanced-filter-experience-2']")
            entry_level.click()
            time.sleep(1)

        if "associate" in self.filter_experience:
            associate_level = self.driver.find_element(By.XPATH, "//label[@for='advanced-filter-experience-3']")
            associate_level.click()
            time.sleep(1)

        if "midsenior" in self.filter_experience:
            midsenior_level = self.driver.find_element(By.XPATH, "//label[@for='advanced-filter-experience-4']")
            midsenior_level.click()
            time.sleep(1)

        if "director" in self.filter_experience:
            director_level = self.driver.find_element(By.XPATH, "//label[@for='advanced-filter-experience-5']")
            director_level.click()
            time.sleep(1)

        if "executive" in self.filter_experience:
            executive_level = self.driver.find_element(By.XPATH, "//label[@for='advanced-filter-experience-6']")
            executive_level.click()
            time.sleep(1)

        """ This filters based on date posted"""
        """
        Any time      = //label[@for='advanced-filter-timePostedRange-']
        Past 24 hours = //label[@for='advanced-filter-timePostedRange-r86400']
        Past week     = //label[@for='advanced-filter-timePostedRange-r604800']
        Past month    = //label[@for='advanced-filter-timePostedRange-r2592000']
        """

        if "any time" == self.filter_date_posted:
            filter_date_button = self.driver.find_element(By.XPATH, "//label[@for='advanced-filter-timePostedRange-']")
            filter_date_button.click()
        elif "past 24 hours" == self.filter_date_posted:
            filter_date_button = self.driver.find_element(By.XPATH, "//label[@for='advanced-filter-timePostedRange-r86400']")
            filter_date_button.click()
        elif "past week" == self.filter_date_posted:
            filter_date_button = self.driver.find_element(By.XPATH, "//label[@for='advanced-filter-timePostedRange-r604800']")
            filter_date_button.click()
        elif "past month" == self.filter_date_posted:
            filter_date_button = self.driver.find_element(By.XPATH, "//label[@for='advanced-filter-timePostedRange-r2592000']")
            filter_date_button.click()

        time.sleep(1)

        #time.sleep(1.5)
        #reset_filter = self.driver.find_element(By.XPATH, "//span[@class='artdeco-button__text' and text() = 'Reset']")
        #reset_filter.click()
        
        #easy_apply_button = self.driver.find_element(By.XPATH, "//input[@id='adToggle_ember599')]")
        #easy_apply_button.click()
        #time.sleep(1)

        apply_filters_button = self.driver.find_element(By.XPATH, "//button[@data-test-reusables-filters-modal-show-results-button='true']")
        apply_filters_button.click()


    def find_offers(self):
        """This function finds all the"""
        
        # find the total number of results (in case there are more than 24 of them)

        total_results = self.driver.find_element(By.XPATH, "//div[starts-with(@class, 'jobs-search-results-list__subtitle')]")
        total_results_int = int(total_results.text.split(' ', 1)[0].replace(",",""))
        print(total_results_int)

        time.sleep(2)

        current_page = self.driver.current_url
        job_listings = self.driver.find_element(By.XPATH, "//li[starts-with(@class, 'ember-view   jobs-search-results__list-item occludable-update p0 relative scaffold-layout__list-item')]")

        # for each job add, submits and application if no questions are asked

        for job_listing in job_listings:
            hover = ActionChains(self.driver).move_to_element(job_listing)
            hover.perform()
        
    def submit_application(self,job_ad):
        """This function submits the application for the job ad found"""

        print('You are applying to the position of: ', job_ad.text)
        job_ad.click()
        time.sleep(2)

        # click on the easy apply button, skip if already applied to the position
        try:
            in_apply = self.driver.find_element("//button[starts-with(@class, 'jobs-apply-button artdeco-button artdeco-button--3 artdeco-button--primary ember-view')]")
            in_apply.click()

        except NoSuchElementException:
            print('You already applied to this job, go to the next one ...')
        
        time.sleep(1)

        # try to submit application if the application is available
        #try:
            #submit = self.driver.find_element(By.XPATH, "")




if __name__ == "__main__":

    with open("config.json") as config_file:
        data = json.load(config_file)
    
    bot = EasyApplyLinkedIn(data)
    bot.login_linkedin()
    time.sleep(round(random.uniform(2,3),1))
    bot.job_search()
    time.sleep(round(random.uniform(2,3),1))
    bot.filter()
    time.sleep(round(random.uniform(2,3),1))
    bot.find_offers()
