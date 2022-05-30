import pandas as pd
from structlog import get_logger

from jobs.utils.monitoring import job_logging
from jobs.infra.postgresql_connector import PostgreSQLConnector

logging = get_logger()


@job_logging
def expose_candidacy_goal() -> int:
    candidacy_goal = read_candidacy_goal()
    nb_of_records = write_candidacy_goal_to_postgres(candidacy_goal)
    return nb_of_records


def read_candidacy_goal() -> pd.DataFrame:
    pg_connector = PostgreSQLConnector.create_prod_connector()
    candidacy_goal = pd.read_sql_query(
        sql='''
            SELECT candidacy_id,
                goal_id,
                additional_information,
                created_at,
                updated_at
            FROM candidacy_goal
        ''',
        con=pg_connector.connection
    )
    logging.info(f'{candidacy_goal.shape[0]} candidacy_goal read from reva')
    return candidacy_goal


def write_candidacy_goal_to_postgres(candidacy_goal: pd.DataFrame) -> int:
    pg_connector = PostgreSQLConnector.create_dwh_connector()
    pg_connector.replace_table_data('candidacy_goal', candidacy_goal)
    logging.info(f'{candidacy_goal.shape[0]} candidacy_goal records written to reva-datawarehouse')
    return candidacy_goal.shape[0]


if __name__ == '__main__':
    expose_candidacy_goal()
