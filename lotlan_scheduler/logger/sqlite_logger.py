""" Contains SQLLogger class """

# standard libraries
from pathlib import Path
import hashlib
import time
import threading

# 3rd party packages
from sqlalchemy import create_engine, MetaData, Table

# globals defines
from lotlan_scheduler.defines import SQLCommands

init_lock = threading.Lock()
mf_lock = threading.Lock()
to_lock = threading.Lock()
location_lock = threading.Lock()

class SQLiteLogger():
    """
        Establishes a SQLite connection and inserts logging data
    """
    def __init__(self, dabase_path = SQLCommands.DATABASE_PATH):
        with init_lock:
            database_file = Path(dabase_path)
            create_tables = True

            # check if db file is already there
            if database_file.is_file():
                create_tables = False
            self.database_engine = create_engine("sqlite:///" + dabase_path, echo=False)
            self.metadata = MetaData(bind=self.database_engine)
            self.con = self.database_engine.connect()
            self.mf_uuid_to_mf_instance_id = {}

            if create_tables:
                self.database_engine.execute(SQLCommands.CREATE_MATERIALFLOW_TABLE)
                self.database_engine.execute(SQLCommands.CREATE_MATERIALFLOW_INSTANCE_TABLE)
                self.database_engine.execute(SQLCommands.CREATE_TRANSPORT_ORDER_TABLE)
                self.database_engine.execute(SQLCommands.CREATE_TRANSPORT_ORDER_IDS_TABLE)
                self.database_engine.execute(SQLCommands.CREATE_LOCATION_TABLE)

    def insert_materialflow_in_sql(self, mf_uuid, lotlan_string):
        """
            Inserts materialflow information into the tables
            'materialflow' and 'materialflow_instance'
            Returns materailflow_instance id if no error occured
        """

        materialflow_table = Table("materialflow", self.metadata, autoload=True)
        lotlan_hash = hashlib.md5(lotlan_string.encode()).hexdigest()

        mf_uuid = str(mf_uuid)
        materialflow_id = None

        with mf_lock:
            select_stmt = materialflow_table.select(materialflow_table.c.hash==lotlan_hash)
            result = select_stmt.execute().first()

            if result is None:
                result = self.con.execute(materialflow_table.insert(),
                                        lotlan=lotlan_string, hash=lotlan_hash)
                materialflow_id = result.lastrowid
            else:
                materialflow_id = result.id

        if materialflow_id is not None:
            now = int(time.time()) # time in utc
            materialflow_instance_table = Table("materialflow_instance",
                                                self.metadata, autoload=True)
            result = self.con.execute(materialflow_instance_table.insert(),
                                      materialflow_id=materialflow_id,
                                      uuid=str(mf_uuid),
                                      timestamp=now)
            materialflow_instance_id = result.lastrowid

            self.mf_uuid_to_mf_instance_id[mf_uuid] = materialflow_instance_id

    def insert_transport_order(self, mf_uuid, to_uuid, state, pickup, delivery):
        """
            Inserts a TransportOrder state into the database
            pickup and delivery have to be Location objects
        """
        now = int(time.time()) # time in utc
        mf_uuid = str(mf_uuid)

        # Get foreign keys in transport_order table
        transport_uuid = self.get_transport_uuid(to_uuid)
        pickup_id = self.get_location_id(pickup)
        delivery_id = self.get_location_id(delivery)

        mf_instance_id = self.mf_uuid_to_mf_instance_id[mf_uuid]

        transport_order_table = Table("transport_order", self.metadata, autoload=True)
        self.con.execute(transport_order_table.insert(),
                         materialflow_id=mf_instance_id,
                         timestamp=now,
                         transport_uuid=transport_uuid,
                         state=state,
                         location_id_pickup=pickup_id,
                         location_id_delivery =delivery_id)

    def get_transport_uuid(self, to_uuid):
        """
            Searches for foreign key of given TransportOrder.
            If no entry is found a new one is inserted.
        """
        transport_order_ids_table = Table("transport_order_ids", self.metadata, autoload=True)
        transport_uuid = None

        to_uuid = str(to_uuid)

        with to_lock:
            select_stmt = transport_order_ids_table.select(transport_order_ids_table.c.uuid==to_uuid)
            result = select_stmt.execute().first()

            if result is None:
                result = self.con.execute(transport_order_ids_table.insert(), uuid=to_uuid)
                transport_uuid = result.lastrowid
            else:
                transport_uuid = result.id

        return transport_uuid

    def get_location_id(self, location):
        """
            Searches for foreign key for given location
            If no entry is found a new one is inserted.

            Returns the foreign key if no error occured and location object is defined
            Returns None otherwise
        """
        location_id = None
        if location:
            location_table = Table("location", self.metadata, autoload=True)

            with location_lock:
                select_stmt = location_table.select(location_table.c.logical_name==location.logical_name)
                result = select_stmt.execute().first()

                if result is None:
                    insert_result = self.con.execute(location_table.insert(),
                                                    logical_name=location.logical_name,
                                                    physical_name=location.physical_name,
                                                    location_type=location.location_type)
                    location_id = insert_result.lastrowid
                else:
                    location_id = result.id

        return location_id
