import random

from selenium.webdriver.common.by import By

from selenium_ui.base_page import BasePage
from selenium_ui.conftest import print_timing
from selenium_ui.jira.pages.pages import Login
from util.conf import JIRA_SETTINGS

def app_specific_action(webdriver, datasets):
    page = BasePage(webdriver)
    if datasets['custom_issues']:
        issue_key = datasets['custom_issue_key']

    @print_timing("selenium_app_custom_action")
    def measure():
        @print_timing("selenium_app_custom_action:view_issue")
        def sub_measure():
            page.go_to_url(f"{JIRA_SETTINGS.server_url}/browse/{issue_key}")
            page.wait_until_visible((By.ID, "summary-val"))  # Wait for summary field visible
            page.wait_until_visible((By.XPATH, '//*[@id="container-wrap"]/table/tbody/tr/td[1]/a'))  # Wait for you app-specific UI element by ID selector
        sub_measure()

        @print_timing("selenium_app_custom_action:open_detaill")
        def sub_measure():
            page.go_to_url(f"{JIRA_SETTINGS.server_url}/browse/{issue_key}")
            page.wait_until_visible((By.ID, "summary-val"))
            locator = (By.XPATH, "//*[@id='container-wrap']/table/tbody/tr/td/a[contains(@onclick,'SalesforcePropertiesDetails')]")
            table = page.wait_until_visible(locator)
            element = table.get_attribute("onclick")
            #if "SalesforcePropertiesDetails" in element:
            d = element[45:-2]
            page.go_to_url(f"{JIRA_SETTINGS.server_url}"+d)
            page.wait_until_visible((By.XPATH, '//*[@id="details"]/div/div[1]/h2'))
            page.wait_until_visible((By.XPATH, '//*[@id="commentsTab"]')).click()
            page.wait_until_visible((By.XPATH, '//*[@id="attachmentsTab"]')).click()
            page.wait_until_visible((By.XPATH, '//*[@id="feedsTab"]')).click()
            page.wait_until_visible((By.XPATH, '//*[@id="emailsTab"]')).click()

        sub_measure()
    measure()


