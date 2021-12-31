"""
amc-prep
========

A tool to prepare for the AMC and AIME competitions.
To create a practice test, run: 

>>> from amc import *
>>> PROBLEMS = 25
>>> TEX_DIR = "tex"; PDF_DIR = "pdf"
>>> EXAMS = ["AMC 10"]

"""

from src.write import write_practice_test, write_default_test, get_problem, get_solution
from src.randomizer import calculate_difficulties, set_difficulties
from src.generate import convert_exam_name

