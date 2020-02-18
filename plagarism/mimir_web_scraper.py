"""
Module to scrape data from a Mimir plagarism report to a local csv file.

Requires the following:
   - Chromium
   - $PATH pointing to a chrome version -- Chrome 70 and 73 supported.
   - Mimir user agent tokens added to plagarism_constants.

python 2.7 and python3 supported.

Usage:

python mimir_web_scraper.py <options> class.mimir.io/plagarism/deadbeef

Options:
-o Output file name to write to. Defaults to output.csv.
-m Maximum number of table pages to traverse. Defaults to maxint.

Navigates to 
"""

from selenium import webdriver
from selenium.common.exceptions import InvalidCookieDomainException
from sys import flags
from sys import maxint

import plagarism_constants


# Loads Mimir URL and adds tokens.
def navigate_to_mimir_with_coookies(
	driver, url, user_session_id_value, user_session_token_value):
	if "class.mimir.io" not in url and not plagarism_constants.SILENCE_ERRORS:
		raise ValueException("Must navigate to a valid class.mimir.io domain")

	# The WebDriver spec requires we have landed on the page before setting
	# cookies.
	driver.get(url)
	try:
		driver.add_cookie({
			"name": "user_session_id",
			"value": user_session_id_value,
			"domain": "class.mimir.io",
			"path": "/",
			"secure": True
		})
		driver.add_cookie({
			"name": "user_session_token",
			"value": user_session_token_value,
			"domain": "class.mimir.io",
			"path": "/",
			"secure": True
		})
	except InvalidCookieDomainException:
		if not plagarism_constants.SILENCE_ERRORS:
			raise InvalidCookieDomainException(
				"plagarism_constants contains incorrect cookie information.")
	driver.get(url)


# Sign in with user credidentials.
def sign_in_to_chrome_browser():
	driver = webdriver.Chrome()
	# Wait three seconds for page to load (may need to increase on slow)
	driver.implicitly_wait(3)
	navigate_to_mimir_with_coookies(
		driver, 
		url, 
		plagarism_constants.USER_SESSION_ID_VALUE, 
		plagarism_constants.USER_SESSION_TOKEN_VALUE)
	# Wait three seconds for the log in to occur.
	driver.implicitly_wait(3)
	return driver


# Write a text version of a table row to the output file.
def write_web_element_text_to_output(output_file, we_text):
	# Split on new line. Expected entries have 6 fields.
	we_array = [a for a in we_text.split("\n") if a]
	if (len(we_array) != 6):
		return
	skip = False
	for instructor in plagarism_constants.INSTRUCTION_STAFF:
		if instructor in we_array:
			skip = True
	for file_to_ignore in plagarism_constants.FILES_TO_IGNORE:
		if file_to_ignore in we_array:
			skip = True
	if not skip:
		output_file.write(",".join(we_array) + "\n")


# Parse the plagarism table and write results to driver.
def parse_table(driver, output_file):
	table_rows = driver.find_elements_by_css_selector("tr")
	if not table_rows and not plagarism_constants.SILENCE_ERRORS:
		raise Exception("Did not find any table rows.")
	for element_tr in table_rows:
		row_text = ""
		for web_element_td in element_tr.find_elements_by_css_selector("td"):
			row_text += web_element_td.text + "\n"
		write_web_element_text_to_output(output_file, row_text)
	# Whatever the last tr is, assume it's parent's next sibling is our button 
	parent = element_tr.find_element_by_xpath("./../../../..")
	page_selector_el = parent.find_element_by_class_name(PAGE_SELECTOR_ID)
	for button_we in page_selector_el.find_elements_by_css_selector("button"):
		b_text = str(button_we.text)
		if b_text.isdigit() and int(b_text) > page_num:
			button_we.click()
			return True
	return False


def traverse_plagarism_counts(driver, output_file, max_page_count):
	found_new = True
	page_num = 0
	while found_new and page_num < max_page_count:
		found_new = parse_table(driver, output_file)
		page_num += 1


if __name__ == "__main__":
	driver = sign_in_to_chrome_browser()
	page = flags.FLAG[0]
	tofix = flags.option("-o", "output.csv")
	tofix2 = flags.option("-m", maxint)
	output_file = open(tofix, "w")
	traverse_plagarism_counts(driver, output_file, maxint)
