from amc.generate import *
import random

DIFFICULTIES = {
    'AMC_8': [(1, 5), (6, 10), (11, 15), (16, 20), (21, 23), (24, 25)],
    'AMC_10A': [(1, 5), (6, 10), (11, 15), (16, 20), (21, 23), (24, 25)],
    'AMC_10B': [(1, 5), (6, 10), (11, 15), (16, 20), (21, 23), (24, 25)],
    'AMC_12A': [(1, 5), (6, 10), (11, 15), (16, 20), (21, 23), (24, 25)],
    'AMC_12B': [(1, 5), (6, 10), (11, 15), (16, 20), (21, 23), (24, 25)],
    'AIME_I': [(1, 5), (6, 8), (9, 11), (12, 13), (14, 15)],
    'AIME_II': [(1, 5), (6, 8), (9, 11), (12, 13), (14, 15)]
}

def randomize(problems: int, exams: list) -> dict:
    """
    Creates a dictionary of problem number - exam pairs.

    Parameters: 
        problems (int): total number of problems to include in dictionary
        difficulties (list): list of problem numbers grouped by difficulty, e.g. 
            `[(1, 5), (6, 10), (11, 15), (16, 20), (21, 23), (24, 25)]`
        exams (list): Exams to pull problems from. Valid exams are: 
            `AMC_8, AMC_10, AMC_10A, AMC_10B, AMC_12, AMC_12A, AMC_12B,  
            AIME_I`, and `AIME_II`

    Returns:
        problem_dict (dict): Dictionary of problem number - (exam, year, problem) pairs.

    Raises:
        ValueError: If `exams` contains invalid exams
    """

    for exam in exams:
        if exam not in EXAMS:
            raise ValueError(f'{exam} does not exist or has not been implemented yet')
    
    _used = []
    problem_dict = {}

    _used_file = open('.used', 'a+')
    _used_file.seek(0)
    u = _used_file.read().splitlines()

    for triple in u:
        exam, year, problem = triple.split()
        year, problem = int(year), int(problem)
        _used.append((exam, year, problem))

    for i in range(1, problems + 1):
        exam = random.choice(exams)
        for j in calculate_difficulties(exam):
            if j[0] <= i <= j[1]:
                EXAM, YEAR, PROBLEM = exam, random_year(exam), random.randint(j[0], j[1])
                while (EXAM, YEAR, PROBLEM) in _used:
                    EXAM, YEAR, PROBLEM = exam, random_year(exam), random.randint(j[0], j[1])
                
                _used.append((EXAM, YEAR, PROBLEM))
                problem_dict[i] = (EXAM, YEAR, PROBLEM)
    
        _used_file.write(' '.join([EXAM, str(YEAR), str(PROBLEM)]) + '\n')
    _used_file.close()

    return problem_dict
    

def calculate_difficulties(exam_name: str) -> list:
    try:
        return DIFFICULTIES[exam_name]
    except KeyError: 
        raise NotImplementedError(f'{exam_name} is currently not a supported exam.')
    

def random_year(exam_name: str) -> int:
    try:
        start, end = EXAM_DATES[exam_name][0], EXAM_DATES[exam_name][1]
    except KeyError:
        raise ValueError(f'{exam_name} does not exist or has not been implemented yet')
    return random.randint(start, end - 1)


def _parse_used(exams: list, _used: list) -> dict:
    # Find a better way to get new problems based on the .used file instead 
    # of randomly choosing until all possibilities are exhausted
    #TODO
    pass


def set_difficulties(exam_name: str, difficulties: list) -> None:
    #TODO
    pass