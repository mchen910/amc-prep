import os
import re
import shutil
import termcolor

def remove_file(filename: str):
    os.system(f'rm {filename}')


def run_cleanup(directory: str, file_ext: list = 'default', aux_directory: str = None):

    if file_ext == 'default': 
        file_ext = ['.asy', '.aux', '.log', '.out', '.pre', '.dvi', 'fdb_latexmk', 'fls', '.prc', 'pbsdat']
    if directory[-1] != '/': directory += '/'
    if aux_directory is not None and aux_directory[-1] != '/': aux_directory += '/'
    if not os.path.isdir(directory):
        os.makedirs(directory)

    if aux_directory is not None:
        if not os.path.isdir(aux_directory):
            os.makedirs(aux_directory)
    
    files = os.listdir(directory)
    for file in files:
        for ext in file_ext:
            if file.endswith(ext):
                if aux_directory is None: remove_file(directory + file)
                else:
                    try:
                        shutil.move(os.path.join(directory, file), os.path.join(aux_directory, file))
                    except IOError:
                        print(termcolor.colored('FileNotFound:', 'cyan'), f'{directory + ext} does not exist')


    leftover_files = os.listdir(directory)
    for file in leftover_files:
        if bool(re.search('\-[0-9]+\.pdf', file)):
            if aux_directory is None: remove_file(directory + file)
            else:
                try:
                    shutil.move(os.path.join(directory, file), os.path.join(aux_directory, file))
                except IOError:
                    print(termcolor.colored('FileNotFound:', 'cyan'), f'{directory + ext} does not exist')


def run_asy(filename: str, directory: str, mode: str = 'batchmode', quiet: bool = False):
    if not quiet: print(termcolor.colored('Running asy and moving/deleting auxillary files...', 'cyan'))
    os.system(f'cd {directory}; pdflatex -interaction={mode} {filename};' + 
              f'asy {filename}-*; pdflatex -interaction={mode} {filename}')


def run_pdflatex(filename: str, directory: str, mode: str = 'batchmode'):
    os.system(f'cd {directory}; pdflatex -interaction={mode} {filename}')


def delete_extra_tex_pdf(directory: str):
    """
    Deletes files that have hyphens.

    Parameters:
    ----------
        directory (str): directory to execute `delete_extra_tex_pdf()` in 

    """
    files = [file for file in os.listdir(directory) if os.path.isfile(os.path.join(directory, file))]
    for file in files: 
        if '-' in file:
            remove_file(os.path.join(directory, file))


def check_duplicates(directory: str, *args):
    files = [os.path.splitext(file)[0] for file in os.listdir(directory) 
        if os.path.isfile(os.path.join(directory, file))]
    for f in args:
        if f in files:
            raise ValueError(f'{f} is already used in the directory {directory}.')


def move_ext_files(cur_dir: str, final_dir: str, ext: str = 'pdf'):
    files = [file for file in os.listdir(cur_dir) if os.path.isfile(os.path.join(cur_dir, file))]
    for file in files:
        if file.endswith(ext):
            shutil.move(os.path.join(cur_dir, file), os.path.join(final_dir, file))

