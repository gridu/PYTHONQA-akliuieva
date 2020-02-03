#!/usr/bin/env python3
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
import allure
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


class BasePage(object):
    url = None

    def __init__(self, driver):
        self.driver = driver

    def navigate(self):
        self.driver.get(self.url)


class Homepage(BasePage):
    url = "https://blog.griddynamics.com"

    @allure.step
    def get_first_article_name(self):
        articles = self.driver.find_elements(By.CSS_SELECTOR, '.blog .explor[style="display: block;"]')
        first_article_name = articles[0].find_element(By.CSS_SELECTOR, '.cntt h4').text
        return articles, first_article_name

    @allure.step
    def filter_by_year(self, year):
        action = ActionChains(self.driver)
        year_filter = self.driver.find_element(By.ID, 'filter2')
        action.move_to_element(year_filter).perform()
        self.driver.find_element(By.CSS_SELECTOR, '[data-year=\'' + year + '\']').click()

    @allure.step
    def click_on_filter_button(self):
        wait = WebDriverWait(self.driver, 2)
        wait.until(expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, '.right.explore>a'))).click()

    @allure.step
    def click_on_reset_button(self):
        self.driver.find_element(By.ID, 'reset').click()
