"""
amc-prep
========

A tool to prepare for the AMC and AIME competitions.
To create a practice test, run (as an example): 

>>> PROBLEMS = 25
>>> TEX_DIR = "tex"
>>> PDF_DIR = "pdf"
>>> EXAMS = ["AMC 12A", "AMC 10B"]
>>> P_FILENAME = "problems_1"
>>> S_FILENAME = "solutions_1"
>>> A_FILENAME = "answers_1"
>>> P_TITLE = "Problems"
>>> S_TITLE = "Solutions"
>>> A_TITLE = "Answers"
>>> write_practice_test(
        PROBLEMS, TEX_DIR, EXAMS, P_FILENAME, S_FILENAME, 
        A_FILENAME, P_TITLE, S_TITLE, A_TITLE, pdf_dir=PDF_DIR
    )

"""

__version__ = "1.0.0"

from src.write import write_practice_test, write_default_test, get_problem, get_solution
from src.randomizer import calculate_difficulties, set_difficulties
from src.generate import convert_exam_name

