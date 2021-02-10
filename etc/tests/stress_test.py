# standard libraries
import sys
import os
from os import walk
from os.path import splitext, join
import threading
import unittest
import time

# 3rd party packages
import xmlrunner
from snakes.nets import Marking, MultiSet

sys.path.append(os.path.abspath("../lotlan_schedular"))

# local sources
import lotlan_schedular.helpers as helpers
from lotlan_schedular.api.event import Event
from lotlan_schedular.schedular import LotlanSchedular
from lotlan_schedular.api.location import Location
from lotlan_schedular.logger.sqlite_logger import SQLiteLogger
from lotlan_schedular.defines import SQLCommands

# uninstall possible old lotlan_schedular packages
# so current code is used not old one
os.system("pip3 uninstall lotlan_schedular")

def test_simple_task():
    f = open("etc/examples/Scheduling/001_simple_task.tl")
    lotlan_logic = LotlanSchedular(f.read(), True)
    material_flows = lotlan_logic.get_materialflows()

    material_flow = material_flows[0]
    material_flow.start()

    material_flow.fire_event("0",Event("task_finished", "", "Boolean", value=True))  # should not be allowed

    material_flow.fire_event("0", Event("to_done", "", "Boolean", value=True))
    material_flow.fire_event("0", Event("moved_to_location", "", "Boolean", value=True))

    material_flow.fire_event("0", Event("moved_to_location", "", "Boolean", value=True))

    f.close()

def main():
    threads=[]

    num_threads = 500
    for i in range(num_threads):
        threads.append(threading.Thread(target=test_simple_task))

    start = time.time()
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    end = time.time()
    print("Runtime with {} threads: {} seconds".format(num_threads, end-start))

if __name__ == "__main__":
    main()
