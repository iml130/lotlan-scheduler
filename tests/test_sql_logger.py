""" Contains unit tests for the SQLLogger class """

# standard libraries
import os
import unittest
import hashlib
from pathlib import Path

# 3rd party packages
import xmlrunner
from sqlalchemy import create_engine, MetaData, Table

# local sources
from lotlan_schedular.sql_logger import SQLLogger
from lotlan_schedular.api.location import Location
from lotlan_schedular.api.transportorder import TransportOrder

# globals defines
from lotlan_schedular.defines import SQLCommands

class TestSQLLogger(unittest.TestCase):
    """ Tests SQLLogger methods """

    def setUp(self):
        test_database_path = "test_database.db"
        database_file = Path(test_database_path)

        # check if db file is already there
        if database_file.is_file():
            os.remove(test_database_path)

        self.logger = SQLLogger(test_database_path)
        self.database_engine = create_engine("sqlite:///" + test_database_path, echo=False)
        self.metadata = MetaData(bind=self.database_engine)
        self.con = self.database_engine.connect()

    def test_insert_materialflow_in_sql(self):
        self.logger.insert_materialflow_in_sql("mf_uuid", "test")
        self.logger.insert_materialflow_in_sql("mf_uuid2", "test")

        test_hash = hashlib.md5("test".encode()).hexdigest()

        materialflow_table = Table("materialflow", self.metadata, autoload=True)
        materialflow_instance_table = Table("materialflow_instance", self.metadata, autoload=True)

        query = materialflow_table.count()
        self.assertEqual(self.database_engine.scalar(query), 1)

        result = materialflow_table.select(materialflow_table.c.id==1).execute().first()
        self.assertIsNotNone(result, None)
        self.assertEqual(result.hash, test_hash)
        self.assertEqual(result.lotlan, "test")

        query = materialflow_instance_table.count()
        self.assertEqual(self.database_engine.scalar(query), 2)

        result = materialflow_instance_table.select().execute().fetchall()
        self.assertEqual(result[0].materialflow_id, 1)
        self.assertEqual(result[0].uuid, "mf_uuid")

        self.assertEqual(result[1].materialflow_id, 1)
        self.assertEqual(result[1].uuid, "mf_uuid2")


    def test_insert_transport_order(self):
        self.logger.insert_materialflow_in_sql("mf_uuid", "test")

        pickup = Location("pickup", "pickup_physical", "pickup_type")
        delivery = Location("delivery", "delivery_physical", "delivery_type")

        state_1 = TransportOrder.TransportOrderState.WAIT_FOR_TRIGGERED_BY
        state_2 = TransportOrder.TransportOrderState.WAIT_FOR_FINISHED_BY

        self.logger.insert_transport_order("mf_uuid", "to_uuid", state_1, pickup, delivery)
        self.logger.insert_transport_order("mf_uuid", "to_uuid", state_2, pickup, delivery)
        transport_order_table = Table("transport_order", self.metadata, autoload=True)

        result = transport_order_table.select(transport_order_table.c.materialflow_id==1
                                             ).execute().fetchall()

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].transport_uuid, 1)
        self.assertEqual(result[0].state, state_1)
        self.assertEqual(result[0].pickup_id, 1)
        self.assertEqual(result[0].delivery_id, 2)

        self.assertEqual(result[1].transport_uuid, 1)
        self.assertEqual(result[1].state, state_2)
        self.assertEqual(result[1].pickup_id, 1)
        self.assertEqual(result[1].delivery_id, 2)

    def test_get_transport_uuid(self):
        to_uuid_1 = self.logger.get_transport_uuid("to_uuid")
        to_uuid_2 = self.logger.get_transport_uuid("to_uuid_2")

        self.assertEqual(to_uuid_1, 1)
        self.assertEqual(to_uuid_2, 2)

        transport_order_ids_table = Table("transport_order_ids", self.metadata, autoload=True)
        result = transport_order_ids_table.select().execute().fetchall()

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].uuid, "to_uuid")
        self.assertEqual(result[1].uuid, "to_uuid_2")

    def test_get_location_ids(self):
        location_table = Table("location", self.metadata, autoload=True)
        pickup = Location("pickup", "pickup_physical", "pickup_type")
        delivery = Location("delivery", "delivery_physical", "delivery_type")

        pickup_id, delivery_id = self.logger.get_location_ids(pickup, delivery)
        self.assertEqual(pickup_id, 1)
        self.assertEqual(delivery_id, 2)

        result = location_table.select().execute().fetchall()

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].logical_name, "pickup")
        self.assertEqual(result[0].physical_name, "pickup_physical")
        self.assertEqual(result[0].location_type, "pickup_type")

        self.assertEqual(result[1].logical_name, "delivery")
        self.assertEqual(result[1].physical_name, "delivery_physical")
        self.assertEqual(result[1].location_type, "delivery_type")

if __name__ == "__main__":
    unittest.main(
        testRunner=xmlrunner.XMLTestRunner(output="test-reports"),
        failfast=False, buffer=False, catchbreak=False)
