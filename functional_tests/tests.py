

from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import time

MAX_WAIT = 10

class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                        raise e
                time.sleep(0.5)
    def test_can_start_a_list_for_one_user(self):

# Kemarius found out about a new to-do list app. He goes
# to the page
        self.browser.get(self.live_server_url)

# The header mentions to-do in the page title
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)
# He is asked to enter a to-do item right away
        inputbox = self.browser.find_element_by_id('id_new_item')

        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
            )
# He types complete google classroom work
        inputbox.send_keys("Complete google classwork")

# Upon hitting enter, the page updates and now lists
# 1: Finish google classroom assignment
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Complete google classwork')


# A text box exists allowing him to add another item
# He enters complete essay for Civics about the 
# US constitution
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys("Finish US Constitution essay")
        inputbox.send_keys(Keys.ENTER)
# The page updates and now both items are on the list

        self.wait_for_row_in_list_table('1: Complete google classwork')
        self.wait_for_row_in_list_table('2: Finish US Constitution essay')

    def test_multiple_users_can_start_lists_at_different_urls(self):
        #Kemarius starts a new to do list
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Complete google classwork')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Complete google classwork')
# The site generates a unique URL to remember the
# task Kemarius enters
        kemarius_list_url = self.browser.current_url
        self.assertRegex(kemarius_list_url, '/lists/.+')

# Kemarius visits the URL and the list he made is still there

# Now he goes back to playing video games

# Now a new users, Jamia, comes along to the site

## We use a new browser session to make sure that nor information
## of Jamia's is coming through from cookies etc.
        self.browser.quit()
        self.browser = webdriver.Firefox()

# Jamia vists the home page. There is no sign on Kemarius's list
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Complete google classwork', page_text)
        self.assertNotIn('Finish US Constituion essay', page_text)

# Jamia starts a new list by entering a new item
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy flamin hot cheetos')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy flamin hot cheetos')

#Jamia gets her own unique URL
        jamia_list_url = self.browser.current_url
        self.assertRegex(jamia_list_url, '/lists/.+')
        self.assertNotEqual(jamia_list_url, kemarius_list_url)

# Again, there is no trace of Kemarius's list
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assetNotIn('Complete google classwork', page_text)
        self.assertIn("Buy flamin hot cheetos", page_text)

# Satisfied, they both go back to sleep
