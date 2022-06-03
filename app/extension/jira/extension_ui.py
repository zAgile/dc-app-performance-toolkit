import random
from selenium.webdriver.common.keys import Keys
from datetime import datetime
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
            d = element[45:-2]
            page.go_to_url(f"{JIRA_SETTINGS.server_url}"+d)
            page.get_element((By.XPATH, '//*[@id="details"]/div/div[1]/h2'))
            page.get_element((By.XPATH, '//*[@id="commentsTab"]')).click()
            page.get_element((By.XPATH, '//*[@id="attachmentsTab"]')).click()
            page.get_element((By.XPATH, '//*[@id="feedsTab"]')).click()
            page.get_element((By.XPATH, '//*[@id="emailsTab"]')).click()
        sub_measure()

        @print_timing("selenium_app_custom_action:send attachment to SF")
        def sub_measure():
            page.go_to_url(f"{JIRA_SETTINGS.server_url}/browse/{issue_key}")
            page.wait_until_visible((By.ID, "summary-val"))
            page.get_element((By.XPATH, '//*[@id="container-wrap"]/table/tbody/tr/td/a[contains(@onclick,"displaySendAttachmentsDialog")]')).click()
            page.wait_until_any_element_visible((By.XPATH, '//*[@id="send-attachments-dialog"]'))
            page.get_element((By.XPATH, '//*[@id="send-attachments-dialog"]/div/div[1]/div/table/tbody/tr[1]/td[1]/input')).click()
            page.get_element((By.XPATH, '//*[@id="send-attachments-dialog"]/div/div[2]/button')).click()
            page.wait_until_visible((By.XPATH,'//*[@id="send-attachments-dialog"]/div/div[1]/div/table/tbody/tr[1]/td[1]/img[contains(@id,"success")]'))
            page.get_element((By.XPATH, '//*[@id="send-attachments-dialog"]/div/div[2]/a')).click()
        sub_measure()

        #@print_timing("selenium_app_custom_action:send comment using share to SF")
        """def sub_measure():
            page.go_to_url(f"{JIRA_SETTINGS.server_url}/browse/{issue_key}")
            page.wait_until_visible((By.ID, "summary-val"))
            page.get_element((By.XPATH, '//div[@id="issue-content"]//div[@id="addcomment"]//a[@id="footer-comment-button"]')).click()
            page.wait_until_available_to_switch((By.XPATH, '//iframe[contains(@id,"mce")]'))
            body = page.get_element((By.XPATH, '//*[@id="tinymce"]'))
            comment = datetime.today()
            hashtag = ' #salesforce'
            body.send_keys(str(comment) + hashtag)
            page.return_to_parent_frame()
            button = page.get_element((By.XPATH, '//*[@id="issue-comment-add-submit"]'))
            button.click()
        sub_measure()"""

    measure()