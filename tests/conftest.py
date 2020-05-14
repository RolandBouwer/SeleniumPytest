"""
This module contains shared fixtures.
"""

import pytest
import json
import os
from datetime import datetime
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver import Firefox, FirefoxOptions

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..', p)
    )

driver = None

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
  global driver
  if config['browser'] == 'Firefox':
    driver = Firefox()
  elif config['browser'] == 'Chrome':
    opts = ChromeOptions()  
    opts.add_experimental_option('useAutomationExtension', False)
    driver = Chrome(options=opts)
  elif config['browser'] == 'Headless Chrome':
    opts = ChromeOptions()
    opts.add_argument('headless')
    opts.add_experimental_option('useAutomationExtension', False)
    driver = Chrome(options=opts)
  elif config['browser'] == 'Headless Firefox':
    opts = FirefoxOptions()
    opts.add_argument('-headless')
    driver = Firefox(options=opts)  
  else:
    raise Exception(f'Browser "{config["browser"]}" is not supported')

  # Make its calls wait for elements to appear
  driver.implicitly_wait(config['implicit_wait'])

  # Return the WebDriver instance for the setup
  yield driver

  # Quit the WebDriver instance for the cleanup
  driver.quit() 

def pytest_html_report_title(report):
   report.title = "Selenium Automation Demo-" +  datetime.now().strftime("%Y-%m-%d_%H.%M.%S")

@pytest.mark.hookwrapper
def pytest_runtest_makereport(item):
    """
    Extends the PyTest Plugin to take and embed screenshot in html report, whenever test fails.
    :param item:
    """
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, 'extra', [])

    if report.when == 'call' or report.when == "setup":
        xfail = hasattr(report, 'wasxfail')
        if (report.skipped and xfail) or (report.failed and not xfail):
            # file_name = report.nodeid.replace("::", "_")+".png"
            ensure_dir('./screenshots' + '/')
            add_name = '{}_{}'.format(report.nodeid.split("::")[1], datetime.now().strftime("%Y-%m-%d_%H.%M.%S"))     
            file_name = PATH('./screenshots' + '/' + add_name + '.png')
            cp_file_name = "./screenshots" + '/' + add_name + ".png"
            driver.get_screenshot_as_file(file_name)
            if file_name:
                html = '<div><img src=' + cp_file_name + ' alt="screenshot" style="width:304px;height:228px;" ' \
                                                         'onclick="window.open(this.src)" align="right"/></div>'
                extra.append(pytest_html.extras.html(html))
        report.extra = extra

def ensure_dir(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

