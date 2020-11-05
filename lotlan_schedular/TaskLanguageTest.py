# standard libraries
import sys
sys.path.append('./')

from os import walk
from os.path import splitext, join
from contextlib import contextmanager
import codecs
import errno
import argparse

# 3rd party lib
from antlr4 import InputStream, CommonTokenStream
from tabulate import tabulate

# local sources
from lotlan_schedular.parser.CreateTreeTaskParserVisitor import CreateTreeTaskParserVisitor
from lotlan_schedular.SemanticValidator import SemanticValidator
from lotlan_schedular.ThrowErrorListener import ThrowErrorListener

# globals defines
from lotlan_schedular.defines import TEST_FOLDER_PATH, LOG_PATH, TEMPLATE_STRING, LOTLAN_FILE_ENDING, ANTLR_COMMAND


from lotlan_schedular.parser.LoTLanLexer import LoTLanLexer
from lotlan_schedular.parser.LoTLanParser import LoTLanParser



class ErrorInformation(object):
    '''
        Class for keeping track of syntax and semantic error count
        in a lotlan file
    '''
    def __init__(self, syntax_error_count, semantic_error_count):
        self.syntax_error_count = syntax_error_count
        self.semantic_error_count = semantic_error_count


def get_file_names(path):
    file_names = []

    for root, dirs, files in walk(path):
        for file in files:
            full_path = join(root, file)
            ext = splitext(file)[1]

            if ext == LOTLAN_FILE_ENDING:
                file_names.append(full_path)

    return file_names


# redirects the output(stdout) to a given file
@contextmanager
def stdout_redirection(fileobj):
    old = sys.stdout
    sys.stdout = fileobj
    try:
        yield fileobj
    finally:
        sys.stdout = old


# method for testing: if a valid file got an error or vice versa return 0
def test_all_files():
    valid_file_names = get_file_names(TEST_FOLDER_PATH + "Valid/")
    invalid_file_names = get_file_names(TEST_FOLDER_PATH + "Invalid/")

    failed_tests = 0
    test_results = []

    print("Error messages of tests: \n")
    count = 1
    for valid_file in valid_file_names:
        error_information = test_file(valid_file, TEMPLATE_STRING, False)[1]
        syntax_errors = error_information.syntax_error_count
        semantic_errors = error_information.semantic_error_count
        error_count = syntax_errors + semantic_errors
        if error_count != 0:
            test_results.append((count, valid_file, "0 , 0", str(syntax_errors) + " , " + str(semantic_errors), False))
            failed_tests = failed_tests + 1
        else:
            test_results.append((count, valid_file, "0 , 0", "0 , 0", True))
        count = count + 1

    test_results.append(("------", "-----------------------------------------", "-----", "-----", "-----"))

    for invalid_file in invalid_file_names:
        ErrorInformation = test_file(invalid_file, TEMPLATE_STRING, False)[1]
        syntax_errors = ErrorInformation.syntax_error_count
        semantic_errors = ErrorInformation.semantic_error_count

        expected_errors_string = ""

        if "Semantic" in invalid_file:
            expected_errors_string = "0 , 1"
            if syntax_errors == 0 and semantic_errors == 1:
                test_results.append((count, invalid_file, expected_errors_string, "0 , 1", True))
            else:
                test_results.append((count, invalid_file, expected_errors_string,
                                    str(syntax_errors) + " , " + str(semantic_errors), False))
                failed_tests = failed_tests + 1
        else:
            expected_errors_string = ">0 , 0"
            if syntax_errors > 0:
                test_results.append((count, invalid_file, expected_errors_string, str(syntax_errors) + " , 0", True))
            else:
                test_results.append((count, invalid_file, expected_errors_string, "0 , " + str(semantic_errors), False))
                failed_tests = failed_tests + 1

        print("\n")
        count = count + 1

    test_count = len(valid_file_names) + len(invalid_file_names)
    print(tabulate(test_results, headers=["Test Nr.", "Test Name", "Expected error count (syntax , semantic)",
                                          "Error count", "Has passed"], tablefmt="orgtbl"))
    print("Tests passed: {} of {}".format(test_count - failed_tests, test_count))

    # pre-commit script checks if there was errors (checks for return value 1)
    if failed_tests > 0:
        sys.exit(1)


def test_file(file_path, template_path, used_in_extension):
    try:
        lotlan_file = codecs.open(file_path, "r", encoding='utf8')
        return test_string(lotlan_file.read(), template_path, used_in_extension, file_path)
    except IOError as e:
        if e.errno == errno.EACCES:
            print("File exists, but is not readable")
        elif e.errno == errno.ENOENT:
            print("File does not exist")

        raise Exception("Invalid File")


def test_string(string, template_path, used_in_extension, file_path=""):
    lexer = LoTLanLexer(InputStream(string))
    token_stream = CommonTokenStream(lexer)

    parser = LoTLanParser(token_stream)

    error_listener = ThrowErrorListener(file_path, used_in_extension, token_stream)
    error_list = error_listener.error_strings

    lexer.removeErrorListeners()
    parser.removeErrorListeners()

    lexer._listeners.append(error_listener)
    parser.addErrorListener(error_listener)

    tree = parser.program()

    visitor = CreateTreeTaskParserVisitor(error_listener)
    if error_listener.is_valid() is False:

        return (None, ErrorInformation(error_listener.syntax_error_count, 0), error_list)
    else:
        t = visitor.visit(tree)

        # check for syntax errors detected in visitor
        if error_listener.is_valid() is False:
            return (None, ErrorInformation(error_listener.syntax_error_count, 0), error_list)

        # no syntax errors check for semantic now
        templates = load_templates(template_path)
        semantic_validator = SemanticValidator(file_path, t, templates, used_in_extension, error_listener)
        semantic_validator.validate()

        return (t, ErrorInformation(0, error_listener.semantic_error_count), error_list)


# templates definied in the task language are in a separate file
def load_templates(template_string):
    '''
    if(path.exists(path_to_templates)):
        template_string = ""
        for filename in listdir(path_to_templates):
            if filename.lower().endswith(LOTLAN_FILE_ENDING):
                temp_joined_name = path.join(path_to_templates, filename)
                with open(temp_joined_name, 'r') as file:
                    template_string += file.read()
                    template_string += "\n\r"
            else:
                continue
    '''
    lexer = LoTLanLexer(InputStream(template_string))
    tokenStream = CommonTokenStream(lexer)
    parser = LoTLanParser(tokenStream)
    tree = parser.program()
    visitor = CreateTreeTaskParserVisitor(None)

    return visitor.visit(tree).templates


def main():
    parser = argparse.ArgumentParser(prog="", description="test lotlan grammar and error detection")
    parser.add_argument("--log", help="create a log file and write output there", action="store_true")
    args = parser.parse_args()

    if args.log:
        print("Test Output is printed to file:", LOG_PATH)
        with open(LOG_PATH, 'w') as out:
            with stdout_redirection(out):
                test_all_files()
    else:
        test_all_files()

    # sys exit for pre-commit script
    sys.exit(0)


if __name__ == '__main__':
    main()
