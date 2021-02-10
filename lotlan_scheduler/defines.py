""" Global defines """

TEST_FOLDER_PATH = "etc/tests/"
LOG_PATH = "logs/log.txt"
TEMPLATES_PATH = "lotlan_scheduler/templates"

LOTLAN_FILE_ENDING = ".tl"

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
    """ Constants that are used in PetriNetGeneration """
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
    TASK_DONE_PLACE = "task_done"

    TOS_STARTED_PLACE = "tos_started"
    TOS_MOVED_TO_LOCATION_PLACE = "moved_to_location"
    TOS_WAIT_FOR_ACTION_PLACE = "wait_for_action"
    TOS_FINISHED_PLACE = "tos_finished"
    TOS_FIRST_TRANSITION = "tos_first"
    TOS_SECOND_TRANSITION = "tos_second"
    TOS_TRIGGERED_BY_TRANSITION = "tos_triggered_by_t"


class DrawConstants:
    """ Constants that are used in PetriNetDrawing """
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
    """ Constants that are used in the control logic of the scheduler """
    TRIGGERED_BY_PASSED_MSG = "tb_by"
    TOS_TB_PASSED_MSG = "tos_tb_by"
    TOS_WAIT_FOR_ACTION = "tos_wait_for_action"
    TOS_FINISHED_MSG = "tos_finished"
    TO_DONE_MSG = "to_done"
    TASK_FINISHED_MSG = "t_finished"

class SQLCommands:
    DATABASE_PATH = "transport_order_logger.db"

    """ SQL Commands to create SQL tables for TransportOrder logger """
    CREATE_MATERIALFLOW_TABLE = """
    CREATE TABLE "materialflow" (
        "id"	INTEGER NOT NULL UNIQUE,
        "lotlan"	TEXT UNIQUE,
        "hash"	TEXT UNIQUE,
        PRIMARY KEY("id")
    )
    """

    CREATE_MATERIALFLOW_INSTANCE_TABLE = """
    CREATE TABLE "materialflow_instance" (
        "id"	INTEGER NOT NULL UNIQUE,
        "materialflow_id"	INTEGER,
        "uuid"	TEXT,
        "timestamp"	INTEGER,
        PRIMARY KEY("id" AUTOINCREMENT),
        FOREIGN KEY("materialflow_id") REFERENCES "materialflow"("id")
    )
    """

    CREATE_TRANSPORT_ORDER_TABLE = """
    CREATE TABLE "transport_order" (
        "id"	INTEGER NOT NULL UNIQUE,
        "materialflow_id"	INTEGER,
        "timestamp"	INTEGER,
        "transport_uuid" INTEGER,
        "state"	INTEGER,
        "location_id_pickup"	INTEGER,
        "location_id_delivery"	INTEGER,
        FOREIGN KEY("materialflow_id") REFERENCES "materialflow_instance"("id"),
        FOREIGN KEY("transport_uuid") REFERENCES "transport_order_ids"("id"),
        FOREIGN KEY("location_id_delivery") REFERENCES "location"("id"),
        PRIMARY KEY("id" AUTOINCREMENT),
        FOREIGN KEY("location_id_pickup") REFERENCES "location"("id")
    )
    """

    CREATE_TRANSPORT_ORDER_IDS_TABLE = """
    CREATE TABLE "transport_order_ids" (
        "id"	INTEGER NOT NULL UNIQUE,
        "uuid"	TEXT UNIQUE,
        PRIMARY KEY("id" AUTOINCREMENT)
    )
    """

    CREATE_LOCATION_TABLE = """
    CREATE TABLE "location" (
        "id"	INTEGER NOT NULL UNIQUE,
        "logical_name"	TEXT UNIQUE,
        "physical_name"	TEXT,
        "location_type"	TEXT,
        PRIMARY KEY("id" AUTOINCREMENT)
    )
    """