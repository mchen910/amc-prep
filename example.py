import amc

# Total number of problems to include in the test
PROBLEMS = 25

# Directories for the resulting .tex and .pdf files
TEX_DIR = "tex"
PDF_DIR = "pdf"

# Exams to choose problems from, currently AMC 8, AMC 10/12A & B, and AIME I & II are supported
EXAMS = ["AMC 12A", "AMC 10B"]

# Filenames for pdf and tex files
P_FILENAME = "problems_1"
S_FILENAME = "solutions_1"
A_FILENAME = "answers_1"

# Title for each file
P_TITLE = "Problems"
S_TITLE = "Solutions"
A_TITLE = "Answers"

amc.write_practice_test(
    PROBLEMS, TEX_DIR, EXAMS, P_FILENAME, S_FILENAME,
    A_FILENAME, P_TITLE, S_TITLE, A_TITLE, pdf_dir=PDF_DIR
)