import os
import os.path

WIKI_DATA_DIR = 'wiki_text_data'

WIKI_FILE_PREFIX = 'english'

VALID_LINE_LEN_THRESHOLD = 13

CLEANED_FILE_TEMP_EXT = '.temp'

FINAL_REDUCED_WIKI_FILE_NAME = 'wikipedia.data'

def begin_work():
    """Top level function.
    Note: call this function to begin all the dirty work."""

    file_path_list = get_absolute_file_paths_list(WIKI_DATA_DIR)
    create_cleaned_files_for_dirty_files(file_path_list)
    concat_all_clean_temp_files_into_final_file()
    delete_all_clean_temp_files()

def get_absolute_file_paths_list(wiki_data_dir):
    """Return a list containing all the absolute file path for the given\
    wiki_data_dir.
    - Input: wiki_data_dir -string dir where all the wiki data is stored.
    - Return: file_list -list"""

    file_list = []
    for root, dirs, files in os.walk(wiki_data_dir):
        for name in files:
            if not name.startswith(WIKI_FILE_PREFIX):
                continue
            file_list.append(root + '/' + name)

    return file_list

def concat_all_clean_temp_files_into_final_file():
    """Concatinate all the cleaned temp file, which has an extension '.temp'\
    into one final file."""

    os.system('cat ' + '*' + CLEANED_FILE_TEMP_EXT + ' > ' + FINAL_REDUCED_WIKI_FILE_NAME)
    print 'wikipedia.data has been created.'

def delete_all_clean_temp_files():
    """Delete all the temp cleaned files."""

    os.system('rm ' + '*' + CLEANED_FILE_TEMP_EXT)
    print 'All the cleaned temp files have been deleted.'

def create_cleaned_files_for_dirty_files(file_path_list):
    """Create temp cleaned files for the given path list.
    - Input: file_path_list -list containing all the dirty raw file path.
    - Return: void, but create all the cleaned files."""

    print 'Starting to create temp files. Please wait.'
    for file_path in file_path_list:
        create_cleaned_file_for_single_dirty_file(file_path)
    print 'All the cleaned temp files have been created.'

def create_cleaned_file_for_single_dirty_file(file_path):
    """Create a cleaned file for a given dirty file.
    - Input: file_path string path to the given dirty file.
    - Return: void, but create a cleaned version of the dirty file."""

    clean_file_name = gen_cleaned_file_name_from_dirty_file(file_path)
    qualified_lines = get_qualified_lines_from_single_file(file_path)
    try:
        with open(clean_file_name, 'w') as f:
            f.write('\n'.join(qualified_lines))
    except IOError:
        raise Exception('Something is wrong!!')

def gen_cleaned_file_name_from_dirty_file(file_path):
    """Generate the name for clean version file given the dirty file.
    Input: file_path -string path to dirty file.
    Return: name for cleaned file."""

    return file_path.split('/')[-1] + CLEANED_FILE_TEMP_EXT

def get_qualified_lines_from_single_file(file_path):
    """Return a list of qualified lines for the given file.
    - Input: file_path -string single file path
    - Return: a list of qualified lines."""

    qualified_lines = []
    try:
        with open(file_path, 'r') as f:
            for line in f:
                qualified_line = select_qualified_line(line)
                if qualified_line:
                    qualified_lines.append(qualified_line)
    except IOError:
        raise Exception('Something is wrong!!')

    return qualified_lines

def select_qualified_line(line):
    """Return the line if it is satisfied with the defined criterias.
    - Input: line -string
    - Return: qualified line."""

    qualified_line = ''
    stripped_line = line.strip()
    if stripped_line and meets_generial_criterias(stripped_line):
        qualified_line = stripped_line

    return qualified_line

def meets_generial_criterias(line):
    """Determine if the line meets the generial criterias.
    - Input: line -string
    - Return qualified -bool"""

    return not_starts_with_doc(line) and not_starts_with_slash_doc(line)\
    and is_line_long_enough(line)

def not_starts_with_doc(line):
    """Determine if the line does not start with '<doc'
    - Input: line -string
    - Return true if not start with '<doc', false otherwise"""

    return not line.startswith('<doc')

def not_starts_with_slash_doc(line):
    """Determine if the line does not start with '</doc>'
    - Input: line -string
    - Return true if line not start with '</doc>', false otherwise."""

    return not line.startswith('</doc>')

def is_line_long_enough(line):
    """Determine if the line is long enough.
    - Note: valid line length threshold is defined.
    - Input: line -string
    - Return: true if line length is >= threshold, false otherwise."""

    return len(line.split()) >= VALID_LINE_LEN_THRESHOLD

if __name__ == '__main__':
    begin_work()