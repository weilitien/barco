from selenium import webdriver
import pytest


@pytest.fixture()
def lunch_web():
    web = webdriver.Chrome("./chromedriver")
    yield web
    web.close()
