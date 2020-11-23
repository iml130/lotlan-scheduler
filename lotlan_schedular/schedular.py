""" Contains LotlanSchedular class """

# standard libraries
import uuid

# 3rd party packages
import networkx as nx

# local sources
from lotlan_schedular.api.materialflow import MaterialFlow

from lotlan_schedular.task_language_test import test_string

from lotlan_schedular.defines import TEMPLATE_STRING

class LotlanSchedular:
    """ Scheduling class """
    def __init__(self, lotlan_string, test_flag=False):
        self.lotlan_structure = None
        self.test_flag = test_flag
        self.material_flows = []
        self.init(lotlan_string)

    # just validates lotlan string and returns
    # true if valid
    def validate(self, lotlan_string):
        lotlan_structure, error_information, error_list = test_string(lotlan_string,
                                                                      TEMPLATE_STRING, False)
        if (error_information.syntax_error_count == 0 and 
            error_information.semantic_error_count == 0):
            return True
        raise ValueError(error_list)

    def init(self, lotlan_string):
        lotlan_structure, error_information, error_list = test_string(lotlan_string,
                                                                      TEMPLATE_STRING, False)
        self.lotlan_structure = lotlan_structure

        if (error_information.syntax_error_count != 0 or
            error_information.semantic_error_count != 0):
            raise ValueError(error_list)

        graph = self.create_graph(lotlan_structure.tasks)
        self.material_flows = self.find_materialflows(graph, lotlan_structure.tasks)

    def create_graph(self, tasks):
        call_graph = nx.Graph()
        for task in tasks.values():
            call_graph.add_node(task.name)
            for child in task.on_done:
                call_graph.add_edge(task.name, child)
        return call_graph

    def find_materialflows(self, graph, tasks):
        """
            With help of a call graph find all materialflows
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

                materialflow = MaterialFlow(uuid.uuid4(), self.lotlan_structure,
                                            tasks_in_mf, self.test_flag)
                materialflows.append(materialflow)
        return materialflows

    def get_materialflows(self):
        return self.material_flows
