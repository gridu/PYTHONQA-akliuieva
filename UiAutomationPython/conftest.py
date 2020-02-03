#!/usr/bin/env python3
import pytest
from selenium import webdriver
import allure


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
    return rep


@pytest.fixture(scope="function")
def driver(request):
    filename = get_path_to_chrome_driver()
    driver = webdriver.Chrome(filename)
    request.cls.driver = driver

    yield driver

    if request.node.rep_call.failed:
        # Make the screen-shot if test failed:
        try:
            allure.attach(
                driver.get_screenshot_as_png(),
                name=request.function.__name__,
                attachment_type=allure.attachment_type.PNG
            )
        except:
            pass

    driver.close()


def get_path_to_chrome_driver():
    import os
    dir = os.path.dirname(__file__)
    filename = os.path.join(dir, 'chromedriver')
    return filename
