# standard libraries
from pathlib import Path
import hashlib
import datetime

# 3rd party packages
from sqlalchemy import create_engine, MetaData, Table 


# local sources

# globals defines
from lotlan_schedular.defines import SQLCommands

class SQLLogger():
    """
        Establishes a SQLite connection and inserts logging data 
    """
    def __init__(self):
        database_file = Path(SQLCommands.DATABASE_PATH)
        create_tables = True
         # check if db file is already there
        if database_file.is_file():
            create_tables = False
        self.database_engine = create_engine("sqlite:///" + SQLCommands.DATABASE_PATH, echo=False)

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
        metadata = MetaData(bind=self.database_engine)
        con = self.database_engine.connect()

        materialflow_table = Table("materialflow", metadata, autoload=True)
        lotlan_hash = hashlib.md5(lotlan_string.encode()).hexdigest()

        result = materialflow_table.select(materialflow_table.c.hash==lotlan_hash).execute().first()
        materialflow_id = None

        if result is None:
            result = con.execute(materialflow_table.insert(), lotlan=lotlan_string, hash=lotlan_hash)
            materialflow_id = result.lastrowid
        else:
            materialflow_id = result.id

        if materialflow_id is not None:
            now = datetime.datetime.now()
            materialflow_instance_table = Table("materialflow_instance", metadata, autoload=True)
            result = con.execute(materialflow_instance_table.insert(),
                                 materialflow_id=materialflow_id,
                                 uuid=str(mf_uuid),
                                 timestamp=now)
            materialflow_instance_id = result.lastrowid

            return materialflow_instance_id

        return None