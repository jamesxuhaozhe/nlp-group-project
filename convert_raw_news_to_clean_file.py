import os
import os.path
import language_detector as ld

RAW_NEWS_TEXT_DIR = 'raw_text_data_from_news'

CLEANED_TEMP_FILE_EXT = '.newstemp'

FINAL_NEWS_FILE_NAME = 'news.data'

LONG_LINE_THRESHOLD = 20

def begin_work():
    """Top level caller."""
    file_path_list = get_file_path_list(RAW_NEWS_TEXT_DIR)
    create_temp_clean_files(file_path_list)
    concat_temp_files_into_final_file()
    delete_all_temp_files()

def get_file_path_list(dir_path):
    """Get a list absolute file paths within the given directory.
    - Input: dir_path -string directory path
    - Return list containing all the absolute file paths for the given dir."""

    file_path_list = []
    for root, dirs, files in os.walk(dir_path):
        for name in files:
            if not name.endswith('.txt'):
                continue
            file_path_list.append(root + '/' + name)

    return file_path_list

def concat_temp_files_into_final_file():
    """Concatineate all the temp files into one final file.
    - Input: void
    - Return: void"""

    os.system('cat ' + '*' + CLEANED_TEMP_FILE_EXT + ' > ' + FINAL_NEWS_FILE_NAME)
    print 'Final file has been created.'

def delete_all_temp_files():
    """Delete all the temp files.
    - Input: void
    - Return: void"""

    os.system('rm ' + '*' + CLEANED_TEMP_FILE_EXT)
    print 'All the temp files have been deleted.'

def create_temp_clean_files(file_path_list):
    """Create temp cleaned files for the given file path list.
    - Input: file_path_list -list containing all the abso file paths.
    - Return: void, but create temp clean files."""

    print 'Starting to create temp clean files.'
    for file_path in file_path_list:
        create_temp_clean_for_single_file(file_path)
    print 'Temp clean files have been created.'

def create_temp_clean_for_single_file(file_path):
    """Create temp cleaned file for single file.
    - Input: file_path -string path to file.
    - Return: void, but create single."""

    temp_file_name = get_temp_clean_file_name(file_path)
    qualified_lines_to_write = get_qualified_lines_from_file(file_path)
    try:
        with open(temp_file_name, 'w') as f:
            f.write('\n'.join(qualified_lines_to_write))
    except IOError:
        raise Exception('Something is wrong!!')
    print '%s has been created.' % temp_file_name


def get_temp_clean_file_name(file_path):
    """Return a valid temp clean file name for the given file path.
    - Input: file_path -string path to file.
    - Return: temp clean name."""

    return file_path.split('/')[-1] + CLEANED_TEMP_FILE_EXT

def get_qualified_lines_from_file(file_path):
    """Return a list of qualified lines from a given file.
    - Input: file_path -string path to file.
    - Return: a list of qualified lines -list."""

    qualified_lines = []
    try:
        with open(file_path, 'r') as f:
            for line in f:
                qualified_line = select_qualified_line(line)
                if qualified_line:
                    qualified_lines.append(qualified_line)
    except IOError:
        print 'Something is goring wrong.'
        pass

    return qualified_lines

def select_qualified_line(line):
    """Select the qualified line.
    - Input: line -string given line to be checked.
    - Return: original line if qualified, '' otherwise."""

    qualified_line = ''
    stripped_line = line.strip()
    if stripped_line and meets_generial_criterias(stripped_line):
        qualified_line = stripped_line

    return qualified_line

def meets_generial_criterias(line):

    """Return if the line meets the generial criterias.
    - Input: line -string
    - Return: true if it meets, false otherwise."""

    return is_line_long_enought(line) and is_line_in_english(line)

def is_line_long_enought(line):
    """Check if the line is long enough.
    - Input: line -string
    - Return: true if it is long enough, false otherwise."""

    return len(line.split()) >= LONG_LINE_THRESHOLD

def is_line_in_english(line):
    """Check if the line is in english.
    - Input: line -string.
    - Return: true if line is in english ,false otherwise."""

    return ld.detect_language(line) == 'english'

if __name__ == '__main__':
    begin_work()
