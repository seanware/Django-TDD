

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()
        
    def test_can_start_a_list_and_retrive_it_later(self):

# Kemarius found out about a new to-do list app. He goes
# to the page
        self.browser.get('http://localhost:8000')

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
        time.sleep(1)

        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertTrue(
            any(row.text == '1: Complete google classwork' for row in rows),
            "New to-do item did not appear in table"
            )

# A text box exists allowing him to add another item
# He enters complete essay for Civics about the 
# US constitution
        self.fail('Finish the test!')

# The page updates and now both items are on the list

# The site generates a unique URL to remember the
# task Kemarius enters

# Kemarius visits the URL and the list he made is still there

# Now he goes back to playing video games
if __name__ == '__main__':
        unittest.main()
