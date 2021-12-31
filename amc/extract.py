import requests
from bs4 import BeautifulSoup
from bs4.element import NavigableString, Tag 
import termcolor

__all__ = ['extract_content_num', 'extract_answer_key', 'scrape_aops_webpage']


URL_FLAG = False


def extract_text_from_tag(tag: Tag, warn: bool = False) -> str:
    assert isinstance(tag, Tag), 'extract_text_from_tag can only be used with Tag objects'
    if tag.name == 'i':
        return ''
    if tag.name == 'img':
        return tag['alt']
    if tag.name == 'a':
        global URL_FLAG
        URL_FLAG = True
        try:
            title = tag['title'] # Just for detecting non wiki links
            name = tag.get_text()
            return '\href{{{0}}}{{{1}}}'.format(tag['href'], name.replace('_', '\\_').replace('%', '\\%'))

        except KeyError:
            return '\href{{{0}}}{{{1}}}'.format(tag['href'], tag['href'].replace('_', '\\_').replace('%', '\\%'))


    if warn: print(termcolor.colored('Warning:', 'red'), 'Extracting text from unknown type tags')
    return ''
    

def extract_content_num(url: str) -> int:
    num_of_sols = 0
    soup = BeautifulSoup(requests.get(url).content, 'html.parser')
    for li in soup.find_all('li'):
        if li.has_attr('class'):
            num_of_sols += 1
    
    return num_of_sols if num_of_sols > 3 else 3


def extract_contents(url: str) -> list:
    #TODO
    raise NotImplementedError


def extract_answer_key(url: str) -> dict:
    """
    Scrapes the answer key from the AOPS answer key website.

        Parameters: 
            url (str): URL of the answer key website. Should be of the form 
            https://artofproblemsolving.com/wiki/index.php/{year}_{exam}_Answer_Key
        
        Returns:
            answers (dict): Dictionary of problem number - answer pairs for all 
            problems of the exam
        
    >>> URL = r'https://artofproblemsolving.com/wiki/index.php/2015_AMC_10A_Answer_Key'
    >>> extract_answer_key(URL)
    {1: 'C', 2: 'D', 3: 'D', 4: 'B', 5: 'E', 6: 'B', 7: 'B', 8: 'B', 9: 'D', 10: 'C', 11: 'C',
     12: 'C', 13: 'C', 14: 'C', 15: 'B', 16: 'B', 17: 'D', 18: 'E', 19: 'D', 20: 'B', 21: 'C', 
     22: 'A', 23: 'C', 24: 'B', 25: 'A'}

    """

    answers = []
    soup = BeautifulSoup(requests.get(url).content, 'html.parser')

    for li in soup.find_all('li'):
        for descendant in li:
            answers.append(descendant)

    indices = [i for i in range(1, len(answers) + 1)]

    return dict(zip(indices, answers))


def scrape_aops_webpage(url: str, content_num: int, warn: bool = False) -> list:
    r"""
    Scrapes an AOPS Problem/Solution website.

    Parameters:
        url (str): url of AOPS website to scrape. Should be in the form 
        https://artofproblemsolving.com/wiki/index.php/{year}_{exam}_Problems/Problem_{problem_num}.

        content_num (int): Number of solutions as provided by the table of contents, 
        including any diagrams but not including the original problem statement or the See Also 
        section. Refer to `extract_content_num(url)` to scrape the contents of the website.

        warn (bool) : Set to False, and warns user when extracting text from unknown tags. If set to 
        true, a message will be printed out to warn the user.

    Returns:
        contents (list): Problem and Solutions from the website, in a list. The first element is the 
        problem statement, and all others are diagrams/solutions.

    Raises:
        ValueError: Raises this error if sol_num is less than 1.
        ExtractionError: Raises this error if no solutions are scraped.

    >>> URL = 'https://artofproblemsolving.com/wiki/index.php/2017_AMC_10B_Problems/Problem_24'
    >>> extract_content_num(URL)
    5
    >>> scrape_aops_webpage(URL, 5)
    ['The vertices of an equilateral triangle lie on the hyperbola $xy=1$, and a vertex of this ...']
    """

    # Must include Problem statement, See Also section, and one solution
    if content_num < 3: raise ValueError('Number of solutions must be greater than zero.')

    contents = []
    counter = difference = 0
    soup = BeautifulSoup(requests.get(url).content, 'html.parser')

    for div in soup.find_all('div'):
        if div.has_attr('class') and div['class'][0] == 'mw-parser-output':
            res = ''
            for child in div.children:
                if child.name == 'h1' or child.name == 'h2':
                    counter += 1
                    if difference != counter:
                        contents.append(res); res = ''
                        difference += 1
                        if (counter > content_num): break
                
                elif child.name == 'p':
                    for descendant in child.descendants:
                        if isinstance(descendant, NavigableString):
                            global URL_FLAG
                            if URL_FLAG: URL_FLAG = False; pass
                            else: res += descendant.replace('_', '\\_').replace('$', '\\$')
                        else:
                            res += extract_text_from_tag(descendant)

                    res += '\n'

    if len(contents) < 2: raise ExtractionError('No solutions extracted.')

    return contents[1:] # Discard first element


class ExtractionError(Exception):
    pass
