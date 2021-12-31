from pylatex import Document, Section, Command, Enumerate, NoEscape, Package

class FileWriter:
    
    UNSUPPORTED_COMMANDS = {r'\tfrac': r'\frac', '•': r'$\cdot$', r'$$':  r'$\$'}
   
    @classmethod
    def detect_imports(cls, text: str, imports: list) -> str:
        """
        Detect the packages needed to imported.

        Parameters:
            text (str): text to be analyzed
            imports (list): list of imports to be checked for. 
        
        Returns:
            `res` (str): Formatted string with imports not detected in the text
        """
        res = ''
        for i in imports:
            if i not in text:
                res += f'import {i}; '
        return res


    def __init__(self, tex_filename: str) -> None:
        self.doc = Document(tex_filename)
        self.problems = []

    
    def add_problem_to_section(self, problem: str) -> None:
        _imports = ['olympiad', 'cse5']
        problem = problem.lstrip()

        for unsupported, supported in FileWriter.UNSUPPORTED_COMMANDS.items():
            problem = problem.replace(unsupported, supported)

            if problem.find('[asy]') != -1:
                if problem.find('size') == -1:
                    problem = problem.replace('[asy]', '\n\\begin{center}\n\\begin{asy}\n\t' +
                                                f'{FileWriter.detect_imports(problem, _imports)}size(6cm);')
                    problem = problem.replace('[/asy]', '\n\\end{asy}\n\end{center}')
                
                else:
                    problem = problem.replace('[asy]', '\n\\begin{center}\n\\begin{asy}\n\t' +
                                                f'{FileWriter.detect_imports(problem, _imports)} ')
                    problem = problem.replace('[/asy]', '\n\\end{asy}\n\end{center}')

        self.problems.append(problem)

    
    def initialize_doc(self, title: str, author: str, with_date: bool = True) -> None:
        self.doc.packages.append(Package('amsmath'))
        self.doc.packages.append(Package('amssymb'))
        self.doc.packages.append(Package('hyperref'))
        self.doc.packages.append(Package('geometry'))
        self.doc.packages.append(Package('asymptote'))

        self.doc.preamble.append(Command('title', title))
        self.doc.preamble.append(Command('author', author))
        self.doc.preamble.append(Command('geometry', 'margin=1in'))

        if with_date:
            self.doc.preamble.append(Command('date', NoEscape(r'\today')))
        self.doc.append(NoEscape(r'\maketitle'))

        with self.doc.create(Section('Acknowledgement', numbering=False)):
            self.doc.append(NoEscape(r"All the following problems are copyrighted by the " + 
                                     r"\href{https://www.maa.org/}{Mathematical Association " + 
                                     r"of America}'s \href{https://www.maa.org/math-competitions}" + 
                                     r"{American Mathematics Competitions}."))
        
        self.doc.append(NoEscape(r'\clearpage'))

    
    def add_section(self, section_name: str, description: list = None) -> None:
        if description is None:
            with self.doc.create(Section(section_name, numbering=False)):
                with self.doc.create(Enumerate()) as enum:
                    for problem in self.problems:
                        enum.add_item(NoEscape(problem))
            self.problems = []

        else:
            # with self.doc.create(Section(section_name, numbering=False)):
            #     with self.doc.create(Description()) as desc:
            #         i = 0
            #         for problem in self.problems:
            #             desc.add_item(description[i], problem)
            raise NotImplementedError


    def write_tex(self):
        self.doc.generate_tex()

