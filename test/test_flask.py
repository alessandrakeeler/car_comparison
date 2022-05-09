from app import*

import pytest

load_data()

def test_interact():
    assert isinstance(interact(), str) == True

def test_print():
    assert isinstance(print(), dict) == True
