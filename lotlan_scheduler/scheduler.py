""" Contains LotlanScheduler class """

# standard libraries
import uuid

# 3rd party packages
import networkx as nx

# local sources
from lotlan_scheduler.api.materialflow import MaterialFlow
from lotlan_scheduler.validation.task_language_test import test_string
from lotlan_scheduler.defines import TEMPLATE_STRING

class LotlanScheduler:
    """ Scheduling class """
    def __init__(self, lotlan_string, test_flag=False):
        self.lotlan_string = lotlan_string
        self.lotlan_structure = None
        self.test_flag = test_flag
        self.material_flows = []
        self.database_engine = None
        self.init(lotlan_string)

    def validate(self, lotlan_string):
        """ Validates given string and returns true if it is valid """
        lotlan_structure, error_information, error_list = test_string(lotlan_string,
                                                                      TEMPLATE_STRING, False)
        if (error_information.syntax_error_count == 0 and
            error_information.semantic_error_count == 0):
            return True
        raise ValueError(error_list)

    def init(self, lotlan_string):
        """
            Initializes the scheduler:
                - validate test string
                - create call graph
                - find Materialflows
        """
        lotlan_structure, error_information, error_list = test_string(lotlan_string,
                                                                      TEMPLATE_STRING, False)
        self.lotlan_structure = lotlan_structure

        if (error_information.syntax_error_count != 0 or
            error_information.semantic_error_count != 0):
            raise ValueError(error_list)

        graph = self.create_call_graph(lotlan_structure.tasks)
        self.material_flows = self.find_materialflows(graph, lotlan_structure.tasks)

    def create_call_graph(self, tasks):
        """
            Creates a graph where every node is a task
            and a directed edge represents an onDone
        """
        call_graph = nx.Graph()
        for task in tasks.values():
            call_graph.add_node(task.name)
            for child in task.on_done:
                call_graph.add_edge(task.name, child)
        return call_graph

    def find_materialflows(self, graph, tasks):
        """
            With help of a call graph find all Materialflows
        """
        materialflows = []
        tasks_reached = []

        for task in tasks.values():
            if task.name not in tasks_reached:
                tree = nx.bfs_tree(graph, task.name)
                task_names = list(tree.nodes())
                tasks_in_mf = []
                for task_name in task_names:
                    tasks_in_mf.append(self.lotlan_structure.tasks[task_name])
                    tasks_reached.append(task_name)

                materialflow_uuid = uuid.uuid4()
                materialflow = MaterialFlow(materialflow_uuid, self.lotlan_structure,
                                            self.lotlan_string, tasks_in_mf, self.test_flag)
                materialflows.append(materialflow)
        return materialflows

    def get_materialflows(self):
        return self.material_flows
