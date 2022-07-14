from amc.generate import *
from amc.extract import *
from amc.filewriter import FileWriter
from amc.utils import *
from amc.randomizer import randomize

# TODO: add threading: from concurrent.futures import ThreadPoolExecutor


def get_description(exam: str, year: int, problem: int, description: str) -> str:
    if description == 'full':
        return '[\\textbf{{{} {} P{}}}] '.format(year, exam.replace('_', ' '), problem)
    if description == 'number':
        return '[\\textbf{{Problem {}}}]'.format(problem)
    return ''


def get_problem(webpage: list, exam: str, year: int, problem: int, description: str = '') -> str:
    return get_description(exam, year, problem, description) + webpage[0]


def get_solution(webpage: str, exam: str, year: int, problem: int, description: str = '') -> str:
    return get_description(exam, year, problem, description) + webpage
    

def write_default_test(exam_name: str, exam_year: int, tex_dir: str, p_filename: str, 
        s_filename: str, a_filename: str, aux_dir: str = None, pdf_dir: str = None, quiet: bool = False) -> None:
    
    if any(['-' in name for name in [p_filename, s_filename, a_filename]]):
        raise ValueError('Filenames cannot contain hyphens.')

    # Must create tex_dir first; if it doesn't exist pylatex will throw errors
    if not os.path.isdir(tex_dir): os.makedirs(tex_dir)

    formatted_exam = convert_exam_name(exam_name)
    num_of_problems = EXAM_DATES[formatted_exam][2]

    p_filewriter = FileWriter(os.path.join(tex_dir, p_filename))
    s_filewriter = FileWriter(os.path.join(tex_dir, s_filename))
    a_filewriter = FileWriter(os.path.join(tex_dir, a_filename))
    
    p_filewriter.initialize_doc(f'{exam_name} {exam_name} Problems', 'MAA')
    s_filewriter.initialize_doc(f'{exam_year} {exam_name} Solutions', 'MAA')
    a_filewriter.initialize_doc(f'{exam_year} {exam_name} Answers', 'MAA')

    _ANSWER_URL = generate_answer_url(formatted_exam, exam_year)

    for i in range(num_of_problems):
        _url = generate_url(formatted_exam, exam_year, i + 1)
        webpage = scrape_aops_webpage(_url, extract_content_num(_url))

        p_filewriter.add_problem_to_section(get_problem(webpage, exam_name, exam_year, i + 1, description=''))
        if not quiet: print(f'Problem {i + 1} successfully added to .tex file')

        solutions = webpage[1:]
        for sol in solutions:
            s_filewriter.add_problem_to_section(get_solution(sol, exam_name, exam_year, i+1, description=''))
        s_filewriter.add_section(f'Problem {i+1}', None)

        if not quiet: print(f'Solution {i+1} successfully added to .tex file')

        answers = extract_answer_key(_ANSWER_URL)
        a_filewriter.add_problem_to_section(answers.get(i+1))
        if not quiet: print(f'Answer {i+1} successfully added to .tex file')

    p_filewriter.add_section('Problems')
    p_filewriter.write_tex()
    s_filewriter.write_tex()
    a_filewriter.add_section('Answers')
    a_filewriter.write_tex()

    run_asy(p_filename, tex_dir)
    run_asy(s_filename, tex_dir)
    run_pdflatex(a_filename, tex_dir)
    run_cleanup(tex_dir, file_ext='default', aux_directory=aux_dir)
    delete_extra_tex_pdf(tex_dir)

    if pdf_dir is not None: 
        if not os.path.isdir(pdf_dir): os.makedirs(pdf_dir)
        move_ext_files(tex_dir, pdf_dir)


def write_practice_test(problems: int, tex_dir: str, exams: list, p_filename: str, s_filename: str, 
        a_filename: str, p_exam_name: str, s_exam_name: str, a_exam_name: str, aux_dir: str = None, 
        pdf_dir: str = None, quiet: bool = False) -> None:

    if any(['-' in name for name in [p_filename, s_filename, a_filename]]):
        raise ValueError('Filenames cannot contain hyphens.')

    if not os.path.isdir(tex_dir): os.makedirs(tex_dir)
    check_duplicates(tex_dir, p_filename, s_filename, a_filename)
    
    exams = [convert_exam_name(exam) for exam in exams]
    _PROBLEM_DICT = randomize(problems, exams)

    p_filewriter = FileWriter(os.path.join(tex_dir, p_filename))
    s_filewriter = FileWriter(os.path.join(tex_dir, s_filename))
    a_filewriter = FileWriter(os.path.join(tex_dir, a_filename))
    
    p_filewriter.initialize_doc(p_exam_name, 'MAA')
    s_filewriter.initialize_doc(s_exam_name, 'MAA')
    a_filewriter.initialize_doc(a_exam_name, 'MAA')

    for i in range(problems):
        _exam, _year, _problem = _PROBLEM_DICT.get(i+1)
        _problem_url = generate_url(_exam, _year, _problem)
        _answer_url = generate_answer_url(_exam, _year)

        webpage = scrape_aops_webpage(_problem_url, extract_content_num(_problem_url))

        p_filewriter.add_problem_to_section(get_problem(webpage, _exam, _year, i + 1, description=''))
        if not quiet: print(termcolor.colored(f'Problem {i + 1}', color='green'), 'successfully added to .tex file')

        solutions = webpage[1:]
        for sol in solutions:
            s_filewriter.add_problem_to_section(get_solution(sol, _exam, _year, i+1, description=''))
        s_filewriter.add_section(f'Problem {i+1}', None)

        if not quiet: print(termcolor.colored(f'Solution {i + 1}', color='green'), 'successfully added to .tex file')

        answers = extract_answer_key(_answer_url)
        a_filewriter.add_problem_to_section(answers[_problem])
        if not quiet: print(termcolor.colored(f'Answer {i + 1}', color='green'), 'successfully added to .tex file')

    p_filewriter.add_section('Problems')
    p_filewriter.write_tex()
    s_filewriter.write_tex()
    a_filewriter.add_section('Answers')
    a_filewriter.write_tex()

    run_asy(p_filename, tex_dir, quiet = quiet)
    run_asy(s_filename, tex_dir, quiet = quiet)
    run_pdflatex(a_filename, tex_dir)
    run_cleanup(tex_dir, file_ext='default', aux_directory=aux_dir)
    delete_extra_tex_pdf(tex_dir)
    
    if pdf_dir is not None: 
        if not os.path.isdir(pdf_dir): os.makedirs(pdf_dir)
        move_ext_files(tex_dir, pdf_dir)
