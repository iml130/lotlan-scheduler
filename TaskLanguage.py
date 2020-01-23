__author__ = "Maximilian Hörstrup"
__version__ = "0.0.1"
__maintainer__ = "Maximilian Hörstrup"

# globals defines
from defines import TEMPLATES_PATH

import TaskLanguageTest
import sys

def main():
    # command line arguments: 
    # [file or string]
    # [template_path]:  (optional) 
    # [--ext]:          (optional, can only be used if template_path is provided) 

    if len(sys.argv) == 2:
            TaskLanguageTest.testFile(sys.argv[1], TEMPLATES_PATH)
    elif len(sys.argv) == 3:
        if sys.argv[2] == "--ext":
            print("provide a template path if you want to use it in the extension")
        else:
            TaskLanguageTest.testFile(sys.argv[1], sys.argv[2])
    elif len(sys.argv) == 4 :
        if sys.argv[3] != "--ext":
            print("Argument " + sys.argv[3] + " has to be --ext or nothing")
        else:
            TaskLanguageTest.testFile(sys.argv[1], sys.argv[2], True)
    else:
        print("Invalid Input")

if __name__ == '__main__':
    main()