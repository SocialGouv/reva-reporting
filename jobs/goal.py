import pandas as pd
from structlog import get_logger

from jobs.utils.monitoring import job_logging
from jobs.infra.postgresql_connector import PostgreSQLConnector

logging = get_logger()


@job_logging
def expose_goal() -> int:
    goal = read_goal()
    nb_of_records = write_goal_to_postgres(goal)
    return nb_of_records


def read_goal() -> pd.DataFrame:
    pg_connector = PostgreSQLConnector.create_prod_connector()
    goal = pd.read_sql_query(
        sql='''
            SELECT id,
                label,
                is_active,
                created_at,
                updated_at,
                needs_additional_information,
                "order"
            FROM goal
        ''',
        con=pg_connector.connection
    )
    logging.info(f'{goal.shape[0]} goal read from reva')
    return goal


def write_goal_to_postgres(goal: pd.DataFrame) -> int:
    pg_connector = PostgreSQLConnector.create_dwh_connector()
    pg_connector.replace_table_data('goal', goal)
    logging.info(f'{goal.shape[0]} goal records written to reva-datawarehouse')
    return goal.shape[0]


if __name__ == '__main__':
    expose_goal()
