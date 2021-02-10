""" Functions defined here set attributes for drawing the petri net """

# standard libraries
import threading

# 3rd party lib
import snakes.plugins

# globals defines
from lotlan_scheduler.defines import DrawConstants, PetriNetConstants

snakes.plugins.load(["labels", "gv"], "snakes.nets", "nets")

draw_lock = threading.Lock()

class PetriNetDrawer:
    """
        Draws image for given petri net.
        Dot attributes for drawing are set here.
    """

    def __init__(self):
        pass

    # dot config methods
    def draw_graph(self, graph, attr):
        attr["nodesep"] = DrawConstants.NODE_SEP_VALUE

    def draw_place(self, place, attr):
        """ Set attributes for drawing places """
        if place.label("placeType") == "input":
            attr["xlabel"] = DrawConstants.INPUT_LABEL
        elif place.label("placeType") == "output":
            attr["xlabel"] = DrawConstants.OUTPUT_LABEL
        elif place.label("placeType") == "connector":
            attr["xlabel"] = DrawConstants.CONNECTOR_LABEL
        elif place.label("placeType") == "or":
            attr["xlabel"] = DrawConstants.OR_LABEL
        elif place.label("placeType") == "and":
            attr["xlabel"] = DrawConstants.AND_LABEL
        elif place.label("placeType") is not None and place.label("placeType") != "":
            attr["xlabel"] = place.label("placeType")
        else:
            attr["xlabel"] = place.name

        if 1 in place:
            attr["label"] = "&bull;"
        else:
            attr["label"] = DrawConstants.PLACE_LABEL
        attr["shape"] = DrawConstants.PLACE_SHAPE

    def draw_transition(self, trans, attr):
        """ Set attributes for drawing transitions """
        if trans.label("transitionType") == "t_s":
            attr["xlabel"] = PetriNetConstants.TASK_FIRST_TRANSITION
        elif trans.label("transitionType") == "t_e":
            attr["xlabel"] = PetriNetConstants.TASK_SECOND_TRANSITION
        elif trans.label("transitionType") == "onDone":
            attr["xlabel"] = DrawConstants.TRANSITION_ON_DONE_LABEL
        elif trans.label("transitionType") == "join":
            attr["xlabel"] = DrawConstants.TRANSITION_JOIN_LABEL

        attr["label"] = DrawConstants.TRANSITION_LABEL
        attr["shape"] = DrawConstants.TRANSITION_SHAPE
        attr["height"] = DrawConstants.TRANSITION_HEIGHT
        attr["width"] = DrawConstants.TRANSITION_WIDTH
        attr["fillcolor"] = DrawConstants.TRANSITION_FILL_COLOR

    def draw_arcs(self, arc, attr):
        if isinstance(arc, snakes.nets.Inhibitor):
            attr["arrowhead"] = DrawConstants.INHIBITOR_ARC_ARROW_HEAD
        attr["label"] = ""

    def draw_image(self, net, filename):
        with draw_lock:
            net.draw(filename, DrawConstants.LAYOUT_METHOD, graph_attr=self.draw_graph,
                     arc_attr=self.draw_arcs, place_attr=self.draw_place,
                     trans_attr=self.draw_transition)
