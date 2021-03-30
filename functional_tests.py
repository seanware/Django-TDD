

from selenium import webdriver
import unittest

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
# Kemarius found out about a new to-do list app. He goes
# to the page
    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        self.browser.get('http://localhost:8000')

# The header mentions to-do in the page title
        self.assertIn('To-Do', self.browser.title)
        self.fail("Finish the test!")
# He is asked to enter a to-do item right away

# He types complete google classroom work

# Upon hitting enter, the page updates and now lists
# 1: Finish google classroom assignment

# A text box exists allowing him to add another item
# He enters complete essay for Civics about the 
# US constitution

# The page updates and now both items are on the list

# The site generates a unique URL to remember the
# task Kemarius enters

# Kemarius visits the URL and the list he made is still there

# Now he goes back to playing video games
if __name__ == '__main__':
        unittest.main()
