from datetime import datetime

__all__ = ['_CURRENT_YEAR', 'EXAMS', 'EXAM_DATES', 'validate_input',
           'generate_url', 'generate_answer_url', 'convert_exam_name']


_CURRENT_YEAR = datetime.now().year


EXAMS = ['AMC_8', 
         'AMC_10A', 'AMC_10B',
         'AMC_12A', 'AMC_12B',
         'AIME_I', 'AIME_II']


EXAM_DATES = {'AMC_8': (2000, _CURRENT_YEAR, 25),
              'AMC_10A': (2002, _CURRENT_YEAR, 25),
              'AMC_10B': (2002, _CURRENT_YEAR, 25),
              'AMC_12A': (2002, _CURRENT_YEAR, 25),
              'AMC_12B': (2002, _CURRENT_YEAR, 25),
              'AIME_I': (2000, _CURRENT_YEAR, 15),
              'AIME_II': (2000, _CURRENT_YEAR, 15)}


def validate_input(exam: str, year: int, problem: int) -> None:
    assert isinstance(exam, str)
    assert isinstance(year, int)
    assert isinstance(problem, int)

    assert exam in EXAM_DATES, f'{exam} is an invalid exam.'
    start_year, end_year, num_problems = EXAM_DATES[exam]
    assert start_year <= year < end_year, f'No {exam} problems found for {year} '
    assert 0 < problem <= num_problems, f'Problem #{problem} not found for the {exam}'


def generate_url(exam: str, year: int, problem: int) -> str:
    validate_input(exam, year, problem)
    head = 'https://artofproblemsolving.com/wiki/index.php/'
    tail = f'{year}_{exam}_Problems/Problem_{problem}'
    return head + tail


def generate_answer_url(exam: str, year: int) -> str:
    validate_input(exam, year, problem=1)
    head = 'https://www.artofproblemsolving.com/wiki/index.php/'
    tail = f'{year}_{exam}_Answer_Key'
    return head + tail


def convert_exam_name(exam_name: str) -> str:
    name_copy = exam_name
    name_copy.replace(' ', '_')
    if name_copy.endswith('1'): name_copy = name_copy[:-1] + 'I'
    elif name_copy.endswith('2'): name_copy = name_copy[:-1] + 'II'

    name_copy = name_copy.upper()

    if name_copy not in EXAMS:
        raise ValueError(f'{exam_name} is not a valid exam name. Valid exams are: {", ".join(EXAMS)}')
    return name_copy