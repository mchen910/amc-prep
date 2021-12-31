# amc-prep

`amc-prep` is a Python program used to generate random problems to prepare for the AMC 8, AMC 10/12, and the AIME. It uses past problems on the [AoPS](https://artofproblemsolving.com/) website, and generates 3 pdfs and 3 latex files (problem, answer, solutions).


## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the neccesary packages first.

```bash
pip3 install -r requirements.txt
```

This will install `beautifulsoup4`, `requests`, `termcolor`, and `pylatex`.

You also need a `LaTeX` installation as well, capable of running `pdflatex`.


## Asymptote

Many AoPS problems require the use of a package called `Asymptote` to draw figures. This comes standard with LaTeX installations, but many figures require the use of two other packages, called `olympiad` and `cse5`. To install on MacOS:

```bash
cd ~
cd .asy
nano olympiad.asy
```

Then copy-paste the contents of [this](https://math.berkeley.edu/~monks/images/olympiad.asy) file into `olympiad.asy`, and press `Ctrl+o` to save. 

After that, run: 
```bash
nano cse5.asy
```
And copy paste the contents of [this](https://github.com/vEnhance/dotfiles/blob/main/asy/cse5.asy) file into `cse5.asy` and press `Ctrl+o` to save.

Now you will be able to use the `olympiad` and `cse5` packages in `Asymptote` commands.

## Usage

Go to the `main.py` file in the `src` directory, and customize the problems depending on what you want. As a brief overview: 

| Parameters   |   Usage     |
| ------------ | ----------- |
| `EXAMS`      | List of exams to include in the practice test. The AMC 8, AMC 10/12, and the AIME I/II are all supported.
| `PROBLEMS`   | Total number of problems to include the the practice test. It should use the estimated difficulties of each problem to make the problems as hard as they would be in the real AMC/AIME. Currently these are capped at the test with the least number of questions included.
| `OUTPUT_DIR` | The output directory, where the files will be created. 
| `TEST_DIR`   | An optional directory, where the pdfs will be moved to after being created.
| `P_FILENAME` | The filename of the generated problem pdf and tex file.
| `S_FILENAME` | The filename of the generated solutions pdf and tex file.
| `A_FILENAME` | The filename of the generated answer key pdf and tex file.

Problems that have been generated before are stored in a `.used` file, which includes exam name, year, and problem number.