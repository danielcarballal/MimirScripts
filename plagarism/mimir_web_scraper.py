from bs4 import BeautifulSoup
import chromedriver_binary
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import InvalidCookieDomainException
from sys import maxint


USER_SESSION_ID_VALUE = "Zmt5Q0VON0YrcjlBMnM1RkF4RlluZW4wc3k0NVQ3enVtclY2b3hKY0"
"Z0Ymd1cTc4ak5sV0F6K2RPdTNHd29iTS0tTkk3ckZTZDRsek9WcE9kVGFQSUZ5Zz09--5752c0dd53"
"feb0bc669e8de183729edc6184cbb9" #  
USER_SESSION_TOKEN_VALUE = "aE1rVWsyMVpiaUFVSFFBRjJTcjNubGNtc09qSVVqaURWdmZMZy81K0taaHlKdlRnb0wvWWFnbnpFbmd2MVVTbG00WVFLcWxXL0lEaXBvN3R6d09tSmc9PS0tSUdQSS9MNlFsN0UzZVgxWGd3NnBmdz09--f46bff5ae991b193acd56011ac363c56aec6db51"

INSTRUCTION_STAFF = ["Daniel Carballal","Chijioke Kamanu","Mikayla Orange"]
FILES_TO_IGNORE = ["functions_caller.py"]

PAGE_SELECTOR_ID = ("frontend-shared-components-Paginate-___Paginate"
					"__paginate___1ZVkH")
TEXT_FILE_OUTPUT = "student_records_lab8.txt"

url = ("https://class.mimir.io/projects/196037bb-3126-495f-9812-"
		"32f0239a79a4/plagiarism")

"""
Loads Mimir URL and adds tokens.
"""
def navigate_to_mimir_with_coookies(
	driver, url, user_session_id_value, user_session_token_value):
	if "class.mimir.io" not in url:
		raise ValueException("Must navigate to a valid class.mimir.io domain")
	# The WebDriver spec requires we have landed on the page before setting
	# cookies.
	driver.get(url)
	try:
		driver.add_cookie({
			"name": "user_session_id",
			"value": USER_SESSION_ID_VALUE,
			"domain": "class.mimir.io",
			"path": "/",
			"secure": True
		})
		driver.add_cookie({
			"name": "user_session_token",
			"value": USER_SESSION_TOKEN_VALUE,
			"domain": "class.mimir.io",
			"path": "/",
			"secure": True
		})
	except InvalidCookieDomainException:
		print("InvalidCookieDomainException")
	driver.get(url)


"""
Sign in with user credidentials.
"""
def sign_in_to_chrome_browser():
	# Must have $PATH pointing to a chrome version between 70 and 73
	driver = webdriver.Chrome()
	# Wait three seconds for the log in to occur.
	driver.implicitly_wait(3)
	navigate_to_mimir_with_coookies(
		driver, url, USER_SESSION_ID_VALUE, USER_SESSION_TOKEN_VALUE)
	driver.implicitly_wait(3)
	return driver


"""
Write a text version of a table row to the output file.
"""
def write_web_element_text_to_output(output_file, we_text):
	# Split on new line. Expected entries have 6 fields
	we_array = [a for a in we_text.split("\n") if a]
	print(we_array)
	if (len(we_array) != 6):
		return
	skip = False
	for instructor in INSTRUCTION_STAFF:
		if instructor in we_array:
			skip = True
	for file_to_ignore in FILES_TO_IGNORE:
		if file_to_ignore in we_array:
			skip = True
	if not skip:
		output_file.write(",".join(we_array) + "\n")


"""
Parse the plagarism table and write results to driver.
"""
def parse_table(driver, output_file):
	table_rows = driver.find_elements_by_css_selector("tr")
	if not table_rows:
		raise Exception("Did not find any table rows.")
	for element_tr in table_rows:
		row_text = ""
		for web_element_td in element_tr.find_elements_by_css_selector("td"):
			row_text += web_element_td.text + "\n"
		write_web_element_text_to_output(output_file, row_text)
	# Whatever the last tr is, assume it's parent's next sibling is our button 
	parent = element_tr.find_element_by_xpath("./../../../..")
	page_selector_el = parent.find_element_by_class_name(PAGE_SELECTOR_ID)
	found_new = False
	for button_we in page_selector_el.find_elements_by_css_selector("button"):
		b_text = str(button_we.text)
		if not found_new and b_text.isdigit() and int(b_text) > page_num:
			button_we.click()
			page_num = int(b_text)
			found_new = True
	return found_new



def traverse_plagarism_counts(driver, output_file, max_page_count):
	found_new = True
	page_num = 1
	while found_new and page_num < max_page_count:
		found_new = parse_table(driver, output_file)

if __name__ == "__main__":
	driver = sign_in_to_chrome_browser()
	output_file = open(TEXT_FILE_OUTPUT, "w")
	traverse_plagarism_counts(driver, output_file, maxint)
