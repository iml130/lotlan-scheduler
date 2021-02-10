# 3rd party packages
from antlr4.error.Errors import InputMismatchException
from antlr4.error.Errors import LexerNoViableAltException
from antlr4.error.Errors import NoViableAltException
from antlr4.error.ErrorListener import ErrorListener

# globals defines
from lotlan_scheduler.defines import SYMBOLIC_NAMES


class SyntaxErrorListener(ErrorListener):
    '''
        Catches errors from generated lexer and parser.
        Can print all kinds of errors with detailed descriptions.
    '''

    def __init__(self, file_path, used_in_extension, token_stream):
        super()
        self.lines = []
        self.file_path = file_path
        self.used_in_extension = used_in_extension
        self.token_stream = token_stream
        self.syntax_error_count = 0
        self.semantic_error_count = 0
        self.error_strings = []

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        # current input does not match with the expected token
        if isinstance(e, InputMismatchException):
            missing_symbol = e.getExpectedTokens().toString(recognizer.symbolicNames,
                                                            recognizer.literalNames)

            symbol_description = parse_expected_symbols(missing_symbol)

            msg = "expected " + symbol_description

            offending_symbol_length = len(offendingSymbol.text)

            hidden_token = self.token_stream.getHiddenTokensToLeft(offendingSymbol.tokenIndex)
            if hidden_token is not None:
                last_token = hidden_token.pop()
                comment_length = len(last_token.text)
                column = column - comment_length

            self.print_error(msg, line, column, offending_symbol_length)

        # the lexer could not decide which path to take so the input doesnt match with anything
        elif isinstance(e, LexerNoViableAltException):
            # if we get a LexerNoViableAltException in one line ignore the other
            # exceptions that will occur due to the first one
            if line not in self.lines:
                self.lines.append(line)
                invalid_char = msg[msg.find("'") + 1: msg.rfind("'")]
                msg = "Invalid Character '" + invalid_char + "'"
                offending_symbol_length = 1  # the first char that doesnt match so length is 1

                self.print_error(msg, line, column, offending_symbol_length)
        # a valid symbol by the lexer but there is no parser rule to match it in the current ctx
        elif isinstance(e, NoViableAltException):
            msg = "Symbol '" + offendingSymbol.text + "' cant be used here"
            offending_symbol_length = len(offendingSymbol.text)

            self.print_error(msg, line, column, offending_symbol_length)

        # those errors dont throw an exception so check it like this
        elif msg.startswith("extraneous input"):
            offendingSymbol = msg.split("'")[1]
            start_index = msg.find("expecting") + len("expecting") + 1
            end_index = len(msg)
            expected_symbol = msg[start_index: end_index]

            symbol_description = parse_expected_symbols(expected_symbol)
            msg = "Wrong symbol '" + offendingSymbol + "' used. Expected " + symbol_description

            self.print_error(msg, line, column, len(offendingSymbol))
        elif msg.startswith("missing"):
            missing_symbol = msg.split(" ")[1]
            symbol_description = parse_expected_symbols(missing_symbol)
            msg = "Missing " + symbol_description
            self.print_error(msg, line, column, 1)
        else:
            offending_symbol_length = len(offendingSymbol.text)

            hidden_token = self.token_stream.getHidden_tokensToLeft(offendingSymbol.tokenIndex)
            if hidden_token is not None:
                last_token = hidden_token.pop()
                comment_length = len(last_token.text)
                column = column - comment_length

            self.print_error(msg, line, column, offending_symbol_length)

    def reportAmbiguity(self, recognizer, dfa, start_index, stopIndex, exact, ambigAlts, configs):
        raise Exception("Task-Language could not be parsed")

    def reportAttemptingFullContext(self, recognizer, dfa, startIndcex, stopIndex, conflictingAlts, configs):
        raise Exception("Task-Language could not be parsed")

    def reportContextSensitivity(self, recognizer, dfa, start_index, stopIndex, prediction, configs):
        raise Exception("Task-Language could not be parsed")

    def is_valid(self):
        return self.syntax_error_count == 0 and self.semantic_error_count == 0

    def print_error(self, msg, line, column, off_symbol_length, syntax_error=True):
        """ Prints an error message with line, column and file path info """
        err_string = msg + "\nFile '" + self.file_path + "', line " + str(line) + ":" + str(column)
        self.error_strings.append(err_string)

        # python shell in extension parses print statements of python
        if self.used_in_extension is True:
            print(msg)
            print(line)
            print(column)  # for ext: antlr starts at column 0, vs code at column 1
            print(off_symbol_length)
        else:
            print(msg)
            print("File '" + self.file_path + "', line " + str(line) + ":" + str(column))

        if syntax_error is True:
            self.syntax_error_count = self.syntax_error_count + 1
        else:
            self.semantic_error_count = self.semantic_error_count + 1

def parse_expected_symbols(symbol_string):
    """ Extracts the symbol names from an antlr generated error string """

    # if there are more than one possible symbol that can be used
    # antlr produces a string in the format: {token1, token2, ..}
    if symbol_string.startswith("{") and symbol_string.endswith("}"):
        tokens = symbol_string.split(",")

        output_string = ""
        for token in tokens:
            token = token.replace(" ", "").replace("{", "").replace("}", "")
            symbol = SYMBOLIC_NAMES.get(token)
            if symbol:
                output_string += symbol + " or "
            else:
                output_string += token + " or "
        output_string = output_string[:-4]  # remove last or
        return output_string

    symbol = SYMBOLIC_NAMES.get(symbol_string)
    if symbol:
        return symbol
    return symbol_string
