from app import*

import pytest

load_data()

def test_interact():
    assert isinstance(interact(), str) == True

def test_print():
    assert isinstance(print_data(), str) == True

def test_makes():
    assert isinstance(model_data('a', 'b'), dict) == True

def test_arguments():
    assert isinstance(get_feature('a', 'b', 'c'), str) == True

def test_avg_make_consumption():
    assert isinstance(avg_make_consumption('a', 'b', 'c'), str) == True

def test_avg_feature():
    assert isinstance(avg_feature('a', 'b'), str) == True
