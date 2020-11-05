TEST_FOLDER_PATH = "etc/test/"
LOG_PATH = "logs/log.txt"
TEMPLATES_PATH = "lotlan_schedular/templates"

LOTLAN_FILE_ENDING = ".tl"

ANTLR_COMMAND = "java -jar antlr-4.7.2-complete.jar -Dlanguage=Python3 -visitor TaskLexer.g4 TaskParser.g4"

SYMBOLIC_NAMES = {
    "TEMPLATE": "a template",
    "TASK": "a task",
    "TRANSPORT_ORDER_STEP": "a transportOrderStep",
    "INSTANCE:": "an instance",
    "WHITESPACE": "a whitespace",
    "NEW_LINE": "a new line",
    "INDENTATION": "an indentation",
    "EQUAL": "an '=' literal",
    "END_IN_BLOCK": "end in block",
    "LOCATION": " a location statement",
    "REPEAT": " a repeat statement",
    "REPEAT_TIMES": " repeat times",
    "TRANSPORT": " a transport statement",
    "FROM": "a 'from'",
    "TO": "a 'to'",
    "ON_DONE": "an ondone statement",
    "TRIGGERED_BY": "a triggered by",
    "FINISHED_BY": "a finished by",
    "COMMA": " a ',' literal",
    "STARTS_WITH_LOWER_C_STR": "a String that starts with a lowercase char",
    "STARTS_WITH_UPPER_C_STR": "a String that starts with an uppercase char",
    "STRING_VALUE": "a string value",
    "NUMERIC_VALUE": "a number value",
    "EMPTY_VALUE": "an empty value",
    "E_LEFT_PARENTHESIS": "a '{' literal",
    "E_RIGHT_PARENTHESIS": "a '}' literal",
    "E_LESS_THAN": "a '<' literal",
    "E_LESS_THAN_OR_EQUAL": "a '<=' literal",
    "E_GREATER_THAN": "a '>' literal",
    "E_GREATER_THAN_OR_EQUAL": "a '>=' literal",
    "E_EQUAL": "a '= literal",
    "E_NOT_EQUAL": "a '!=' literal",
    "E_BOOLEAN_AND": "a '&&' literal",
    "E_BOOLEAN_OR": "a '||' literal",
    "E_BOOLEAN_NOT": "a '!' literal",
    "E_ATTRIBUTE": "an attribute",
    "E_TRUE": "a 'True' expression",
    "E_FALSE": "a 'False' expression",
    "E_INTEGER": "an integer value",
    "E_FLOAT": "a float value",
}

TEMPLATE_STRING = """
Template Constraint
    type = ""
End

Template Event
    name = ""
    type = ""
End

Template Location
    name = ""
    type = ""
End

Template Time
    timing = ""
End
"""


TRIGGERED_BY_KEY = "TriggeredBy"
FINISHED_BY_KEY = "FinishedBy"
ON_DONE_KEY = "OnDone"
REPEAT_KEY = "Repeat"
TRANSPORT_ORDER_KEY = "TransportOrder"
PARAMETER_KEY = "Parameter"
LOCATION_KEY = "Location"

# Petri Net Generation


class PetriNetConstants:
    PETRI_NET_NAME = "Petri_Net"
    IMAGE_ENDING = ".png"
    TRIGGERED_BY = "triggered_by"
    TRIGGERED_BY_TRANSITION = "triggered_by_t"
    FINISHED_BY = "finished_by"
    FINISHED_BY_TRANSITION = "finished_by_t"
    SELF_LOOP = "self_loop"
    ON_DONE_ENDING = "_fork"
    INPUT_PLACE_ENDING = "_i"
    OUTPUT_PLACE_ENDING = "_o"
    TASK_FIRST_TRANSITION = "finish_task"
    TASK_SECOND_TRANSITION = "exec_on_done"
    TASK_STARTED_PLACE = "task_started"
    TO_DONE_PLACE = "task_done"


class DrawConstants:
    NODE_SEP_VALUE = 3

    PLACE_SHAPE = "circle"
    PLACE_LABEL = ""

    TRANSITION_SHAPE = "rect"
    TRANSITION_FILL_COLOR = "black"
    TRANSITION_WIDTH = 1
    TRANSITION_HEIGHT = 0.1
    TRANSITION_LABEL = ""

    INHIBITOR_ARC_ARROW_HEAD = "odot"

    LAYOUT_METHOD = "dot"

    INPUT_LABEL = "in"
    OUTPUT_LABEL = "out"
    CONNECTOR_LABEL = "connect"
    OR_LABEL = "or"
    AND_LABEL = "and"

    TRANSITION_ON_DONE_LABEL = "OnDone"
    TRANSITION_JOIN_LABEL = "Join"


class LogicConstants:
    TRIGGERED_BY_PASSED_MSG = "t_by"
    TO_DONE_MSG = "t_done"
    TASK_FINISHED_MSG = "t_finished"
