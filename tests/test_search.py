"""
These tests cover DuckDuckGo searches.
"""
import pytest
import csv

from pages.result import DuckDuckGoResultPage
from pages.search import DuckDuckGoSearchPage

def getData():
	with open('C:\\Users\\A233842\\PycharmProjects\\SeleniumPytest\\testdata\\testdata.csv') as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		line_count = 0
		stringData = []
		for row in csv_reader:
			if line_count == 0:
				# print(f'Column names are {", ".join(row)}')
				stringData.append(list(row))
				line_count += 1
			else:
				# print(f'\t{row[0]} works in the {row[1]} department, and was born in {row[2]}.')
				line_count += 1
				stringData.append(list(row))
		# print(f'Processed {line_count} lines.')
		return stringData

def open_dataset(file_name='C:\\Users\\A233842\\PycharmProjects\\SeleniumPytest\\testdata\\testdata.csv',header_row=True):
    opened_file = open(file_name)
    from csv import reader
    read_file = reader(opened_file)
    data = list(read_file)
    if header_row:
        return data[1:]
    else:
        return data

apps_data = open_dataset()


@pytest.mark.parametrize('mydata', open_dataset())
def test_basic_duckduckgo_search(browser,mydata):
  search_page = DuckDuckGoSearchPage(browser)
  result_page = DuckDuckGoResultPage(browser)

  # Given the DuckDuckGo home page is displayed
  search_page.load()

  phrase = mydata[0]

  print(phrase)

  # When the user searches for "panda"
  search_page.search(phrase)

  getData()
 
  # Changes made to main branch.
  # And the search result query is "panda"
  assert phrase == result_page.search_input_value()
  
  # And the search result links pertain to "panda"
  #for title in result_page.result_link_titles():
  #  assert phrase.lower() in title.lower()

  # Then the search result title contains "panda"
  assert phrase in result_page.title()