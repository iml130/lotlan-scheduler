# standard libraries
import sys
import os
import threading

sys.path.append(os.path.abspath("../lotlan_scheduler"))

# local sources
from lotlan_scheduler.api.location import Location
from lotlan_scheduler.sql_logger import SQLLogger
from lotlan_scheduler.defines import SQLCommands

def test_sqlite_connection(mf_uuid, lotlan_string, to_uuid, state, pickup, delivery):
    logger = SQLLogger(SQLCommands.DATABASE_PATH)
    logger.insert_materialflow_in_sql(mf_uuid, lotlan_string)
    logger.insert_transport_order(mf_uuid, to_uuid, state, pickup, delivery)

def main():
    threads=[]

    pickup_1 = Location("pickup_lname_1", "pickup_pname_1", "pickuploc_type_1")
    pickup_2 = Location("pickup_lname_2", "pickup_pname_2", "pickuploc_type_2")
    delivery_1 = Location("delivery_lname_1", "delivery_pname_1", "deliveryloc_type_1")
    delivery_2 = Location("delivery_lname_2", "delivery_pname_2", "deliveryloc_type_2")

    threads.append(threading.Thread(target=test_sqlite_connection, args=[0, "test", "uuid_1", 1, pickup_1, delivery_1]))
    threads.append(threading.Thread(target=test_sqlite_connection, args=[0, "test", "uuid_2", 1, pickup_1, delivery_2]))
    threads.append(threading.Thread(target=test_sqlite_connection, args=[1, "test2", "uuid_3", 0, delivery_2, pickup_1]))
    threads.append(threading.Thread(target=test_sqlite_connection, args=[2, "test3", "uuid_4", 1, pickup_2, delivery_2]))
    threads.append(threading.Thread(target=test_sqlite_connection, args=[3, "test", "uuid_5", 2, pickup_1, delivery_1]))
    threads.append(threading.Thread(target=test_sqlite_connection, args=[3, "test4", "uuid_6", 1, pickup_1, delivery_1]))
    threads.append(threading.Thread(target=test_sqlite_connection, args=[4, "test", "uuid_7", 3, pickup_1, delivery_1]))
    threads.append(threading.Thread(target=test_sqlite_connection, args=[5, "test3", "uuid_8", 4, pickup_1, delivery_1]))

    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()
