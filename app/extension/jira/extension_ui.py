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

    # To run action as specific user uncomment code bellow.
    # NOTE: If app_specific_action is running as specific user, make sure that app_specific_action is running
    # just before test_2_selenium_z_log_out action
    #
    # @print_timing("selenium_app_specific_user_login")
    # def measure():
    #     def app_specific_user_login(username='admin', password='admin'):
    #         login_page = Login(webdriver)
    #         login_page.delete_all_cookies()
    #         login_page.go_to()
    #         login_page.set_credentials(username=username, password=password)
    #         if login_page.is_first_login():
    #             login_page.first_login_setup()
    #         if login_page.is_first_login_second_page():
    #             login_page.first_login_second_page_setup()
    #         login_page.wait_for_page_loaded()
    #     app_specific_user_login(username='admin', password='admin')
    # measure()

    @print_timing("selenium_app_custom_action")
    def measure():
        @print_timing("selenium_app_custom_action:view_issue")
        def sub_measure():
            page.go_to_url(f"{JIRA_SETTINGS.server_url}/browse/{issue_key}")
            page.wait_until_visible((By.ID, "summary-val"))  # Wait for summary field visible
            page.wait_until_visible((By.XPATH,
                                     '//*[@id="container-wrap"]/table[contains(@class,"sf-properties-panel")]'))  # Wait for you app-specific UI element by ID selector
        sub_measure()

        @print_timing("selenium_app_custom_action:open_detail")
        def sub_measure():
            page.go_to_url(f"{JIRA_SETTINGS.server_url}/browse/{issue_key}")
            page.wait_until_visible((By.ID, "summary-val"))
            locator = (
            By.XPATH, "//*[@id='container-wrap']/table/tbody/tr/td/a[contains(@onclick,'SalesforcePropertiesDetails')]")
            table = page.wait_until_visible(locator)
            element = table.get_attribute("onclick")
            start = element.find('"') + 1
            url = element[start:-2]
            page.go_to_url(url)
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
            existElement = page.element_exists((By.XPATH,
                                                '//*[@id="container-wrap"]/table/tbody/tr/td/a[contains(@onclick,"displaySendAttachmentsDialog")]'))
            if existElement == True:
                page.get_element((By.XPATH,
                                  '//*[@id="container-wrap"]/table/tbody/tr/td/a[contains(@onclick,"displaySendAttachmentsDialog")]')).click()
                page.wait_until_any_element_visible((By.XPATH, '//*[@id="send-attachments-dialog"]'))
                page.get_element((By.XPATH,
                                  '//*[@id="send-attachments-dialog"]/div/div[1]/div/table/tbody/tr[1]/td[1]/input')).click()
                page.get_element((By.XPATH, '//*[@id="send-attachments-dialog"]/div/div[2]/button')).click()
                page.wait_until_visible((By.XPATH,
                                         '//*[@id="send-attachments-dialog"]/div/div[1]/div/table/tbody/tr[1]/td[1]/img[contains(@id,"success")]'))
                page.get_element((By.XPATH, '//*[@id="send-attachments-dialog"]/div/div[2]/a')).click()
        sub_measure()
    measure()
