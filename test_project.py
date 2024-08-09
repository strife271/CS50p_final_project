import pytest

from project import Routine
from project import Exercise
from project import calc_total
from project import get_plot_data
from project import read_routine_file


def test_calc_total():
    """Tests the total calculation is correct"""
    assert calc_total(10,10, 3) == 300


def test_get_plot_data():
    """Tests that axis data is retrieved correctly"""
    r = Routine()
    ex = Exercise('mike', '07/01/2024', 'legs','squat', 5, 185, 5, 4625)
    r.add_exercise(ex)

    assert get_plot_data(r, 'mike', 'squat') == [['07/01/2024'], [185]]


def test_read_routine_file():
    """Tests that functions reads in and creates a Routine object from a file"""
    obj = read_routine_file("sample_file.csv")
    assert isinstance(obj, Routine)
