""" """
# standard libraries
import argparse

# local sources
from lotlan_scheduler.task_language_test import test_file, test_string

# globals defines
from lotlan_scheduler.defines import TEMPLATES_PATH


def main():
    parser = argparse.ArgumentParser(prog="", description="Process Lotlan input")
    parser_2 = parser.add_mutually_exclusive_group()  # user can only give one type of input

    parser_2.add_argument("--file", help="lotlan file", type=str)
    parser_2.add_argument("--string", help="", type=str)
    parser.add_argument("--ext",
                        help="output of test is used in extension for error highlighting",
                        type=str)

    args = parser.parse_args()
    arg_dict = {"file": args.file, "string": args.string}

    templates_path = TEMPLATES_PATH

    if args.ext and args.ext != "":
        templates_path = args.ext
    if arg_dict["file"] is not None:
        test_file(arg_dict["file"], templates_path, args.ext is not None)
    elif arg_dict["string"] is not None:
        test_string(arg_dict["string"], templates_path, args.ext is not None)


if __name__ == "__main__":
    main()
