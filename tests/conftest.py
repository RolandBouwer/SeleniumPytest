"""
This module contains shared fixtures.
"""

import pytest
import json
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver import Firefox, FirefoxOptions

@pytest.fixture
def config(scope='session'):

  # Read the file
  with open('config.json') as config_file:
    config = json.load(config_file)
  
  # Assert values are acceptable
  assert config['browser'] in ['Firefox', 'Chrome', 'Headless Chrome','Headless Firefox']
  assert isinstance(config['implicit_wait'], int)
  assert config['implicit_wait'] > 0

  # Return config so it can be used
  return config

@pytest.fixture
def browser(config):

  # Initialize the WebDriver instance
  if config['browser'] == 'Firefox':
    b = Firefox()
  elif config['browser'] == 'Chrome':
    b = Chrome()
  elif config['browser'] == 'Headless Chrome':
    opts = ChromeOptions()
    opts.add_argument('headless')
    b = Chrome(options=opts)
  elif config['browser'] == 'Headless Firefox':
    opts = FirefoxOptions()
    opts.add_argument('-headless')
    b = Firefox(options=opts)  
  else:
    raise Exception(f'Browser "{config["browser"]}" is not supported')

  # Make its calls wait for elements to appear
  b.implicitly_wait(config['implicit_wait'])

  # Return the WebDriver instance for the setup
  yield b

  # Quit the WebDriver instance for the cleanup
  b.quit() 