# amc-prep

`amc-prep` is a Python program used to generate random problems to prepare for the AMC 8, AMC 10/12, and the AIME. It uses past problems on the [AoPS](https://artofproblemsolving.com/) website, and generates 3 pdfs and 3 latex files (problem, answer, solutions).


## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the neccesary packages first. After, run the following: 

```bash
pip3 install -r requirements.txt
```

This will install the `beautifulsoup4`, `requests`, `termcolor`, and `pylatex` packages needed to use this tool.

You also need a `LaTeX` installation as well, capable of running `pdflatex`. Install it from the official [LaTeX website](https://www.latex-project.org/get/#tex-distributions) and ensure that `pdflatex` is installed by running 

```bash
pdflatex --version
```
in a new terminal.


## Asymptote

Many AoPS problems require the use of a package called `Asymptote` to draw figures. This comes standard with LaTeX installations, but many figures require the use of two other packages, called `olympiad` and `cse5`. To install on MacOS and Linux:

```bash
cd ~
mkdir .asy && cd .asy
nano olympiad.asy
```

Then copy-paste the contents of [this](https://math.berkeley.edu/~monks/images/olympiad.asy) file into `olympiad.asy`, and press `Ctrl + O` to save. Enter and press `Ctrl + X` to exit.

Next, run: 
```bash
nano cse5.asy
```
And copy paste the contents of [this](https://github.com/vEnhance/dotfiles/blob/main/asy/cse5.asy) file into `cse5.asy` and press `Ctrl + O` to save. Likewise, enter, and press `Ctrl + X` to exit.

Now you will be able to use the `olympiad` and `cse5` packages in `Asymptote` commands.

## Usage

Create a new file, and import everything from `amc`. Run `write_practice_test` using these parameters: 

| Parameters   |   Usage     |
| ------------ | ----------- |
| `exams`      | List of exams to include in the practice test. The AMC 8, AMC 10/12, and the AIME I/II are all supported.
| `problems`   | Total number of problems to include the the practice test. It should use the estimated difficulties of each problem to make the problems as hard as they would be in the real AMC/AIME. Currently these are capped at the test with the least number of questions included.
| `tex_dir`    | The LaTeX directory, where the files will be created. 
| `pdf_dir`    | An optional directory, where the pdfs will be moved to after being created.
| `aux_dir`    | An optional directory to move the auxillary files created by `pdflatex` to. If this directory is not specified, all auxillary files will be deleted.
| `p_filename` | The filename of the generated problem pdf and tex file.
| `s_filename` | The filename of the generated solutions pdf and tex file.
| `a_filename` | The filename of the generated answer key pdf and tex file.
| `p_exam_name`| The exam name of the created problem file.
| `s_exam_name`| The exam name of the created solution file.
| `a_exam_name`| The exam name of the created answer file.
| `quiet`      | An optional parameter to pass to silence all extra messages

Problems that have been generated before are stored in a `.used` file, which includes exam name, year, and problem number. Refer to `example.py` for a demonstration of these differnt parameters.

Do not use AIME problems if you plan on putting more than 15 problems in a file, otherwise the program will break.