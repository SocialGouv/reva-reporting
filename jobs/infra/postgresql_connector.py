import os
from abc import ABC

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine.base import Connection
from sqlalchemy.orm import Session
from structlog import get_logger

load_dotenv()

logging = get_logger()


class PostgreSQLConnector(ABC):
    def __init__(self, db=None, host=None, port=None, user=None, password=None):
        self.db = db
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.connection = self._get_connection()

    def replace_table_data(self, table_name: str, data: pd.DataFrame) -> None:
        session = Session(self.connection)
        with session.begin():
            session.execute(f'TRUNCATE TABLE {table_name}')
            logging.info(f'Truncated Postgresql table: {table_name}')
            data.to_sql(table_name, con=session.connection(), if_exists='append', index=False)

    def append_data_to_existing_table(self, table_name: str, data: pd.DataFrame) -> int:
        data.to_sql(table_name, con=self.connection, if_exists='append', index=False)
        return data.shape[0]

    def _get_connection(self) -> Connection:
        connection_string = f'postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}'
        connector = create_engine(connection_string)
        connection = connector.connect()
        return connection


class ProdPostgreSQLConnector(PostgreSQLConnector):
    def __init__(self):
        db = os.getenv('PGDATABASE_PROD')
        host = os.getenv('PGHOST_PROD')
        port = os.getenv('PGPORT_PROD')
        user = os.getenv('PGUSER_PROD')
        password = os.getenv('PGPASSWORD_PROD')
        super().__init__(db, host, port, user, password)


class DWHPostgreSQLConnector(PostgreSQLConnector):
    def __init__(self):
        db = os.getenv('PGDATABASE_DWH')
        host = os.getenv('PGHOST_DWH')
        port = os.getenv('PGPORT_DWH')
        user = os.getenv('PGUSER_DWH')
        password = os.getenv('PGPASSWORD_DWH')
        super().__init__(db, host, port, user, password)
