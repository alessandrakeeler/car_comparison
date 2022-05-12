from app import*

import pytest
import requests

api_host = 'localhost'
api_port = '5016'
api_prefix = f'http://{api_host}:{api_port}'


def test_info():
    route = f'{api_prefix}/'
    response = requests.get(route)

    assert response.ok == True
    assert response.status_code == 200
    assert bool(re.search('Try the following routes', response.text)) == True

def test_data_upload():
    route = f'{api_prefix}/data'
    response = requests.get(route)

    assert response.ok == True
    assert response.status_code == 200
    assert response.content == b'Data loaded into redis \n'

def teset_jobs_info():
    route = f'{api_prefix}/jobs'
    response = requests.get(route)

    assert response.ok == True
    assert response.status_code == 200
    assert bool(re.search('To submit a job,', response.text)) == True

load_data()

def test_interact():
    assert isinstance(interact(), str) == True

def test_makes():
    assert isinstance(model_data('a', 'b'), dict) == True

def test_arguments():
    assert isinstance(get_feature('a', 'b', 'c'), str) == True

def test_avg_make_consumption():
    assert isinstance(avg_make_consumption('a', 'b', 'c'), str) == True

def test_avg_feature():
    assert isinstance(avg_feature('a', 'b'), str) == True

