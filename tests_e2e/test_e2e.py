import os
from threading import Thread
import pytest
from selenium import webdriver
from dotenv import load_dotenv
import requests

from todo_app.app_config import Config
from todo_app.app import create_app

def create_trello_board():
    config = Config()
    response = requests.post(
        url=f'{config.TRELLO_BASE_URL}/boards',
        params={
            'key': config.TRELLO_API_KEY,
            'token': config.TRELLO_API_SECRET,
            'name': 'Selenium Test Board'
        }
    )
    return response.json()['id']


def delete_trello_board(board_id):
    config = Config()
    requests.delete(
        url=f'{config.TRELLO_BASE_URL}/boards/{board_id}',
        params={
            'key': config.TRELLO_API_KEY,
            'token': config.TRELLO_API_SECRET,
        }
    )


@pytest.fixture(scope='module')
def app_with_temp_board():
    load_dotenv(override=True)
    board_id = create_trello_board()
    os.environ['TRELLO_BOARD_ID'] = board_id

    app = create_app()
    thread = Thread(target=lambda: app.run(use_reloader=False))
    thread.daemon = True
    thread.start()
    yield app

    # Tear Down
    thread.join(1)
    delete_trello_board(board_id)


@pytest.fixture(scope='module')
def driver():
    opts = webdriver.ChromeOptions()
    opts.add_argument('--headless')
    opts.add_argument('--no-sandbox')
    opts.add_argument('--disable-dev-shm-usage')
    with webdriver.Chrome(options=opts) as driver:
        yield driver


def test_task_journey(driver, app_with_temp_board):
    driver.get('http://127.0.0.1:5000/')

    assert driver.title == 'To-Do App'

    add_new_task(driver)
    start_task(driver)
    complete_task(driver)
    mark_test_as_incomplete(driver)


def add_new_task(driver):
    new_task_input = driver.find_element_by_xpath("//*[@data-test-id='name-input']")
    new_task_input.send_keys('Test Task')

    driver.find_element_by_xpath("//button[contains(text(), 'Add Item')]").click()

    assert find_task_in_section('to-do-section', driver) is not None


def start_task(driver):
    task = find_task_in_section('to-do-section', driver)
    task.find_element_by_link_text('Start').click()

    assert find_task_in_section('doing-section', driver) is not None


def complete_task(driver):
    task = find_task_in_section('doing-section', driver)
    task.find_element_by_link_text('Complete').click()

    assert find_task_in_section('done-section', driver) is not None


def mark_test_as_incomplete(driver):
    task = find_task_in_section('done-section', driver)
    task.find_element_by_link_text('Mark as Incomplete').click()

    assert find_task_in_section('to-do-section', driver) is not None


def find_task_in_section(section_name, driver):
    section = driver.find_element_by_xpath(f"//*[@data-test-id='{section_name}']")
    tasks = section.find_elements_by_xpath("//*[@data-test-class='task']")
    return next(task for task in tasks if task.find_element_by_xpath("//*[contains(text(), 'Test Task')]") is not None)
