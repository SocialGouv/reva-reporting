import time
from structlog import configure, get_logger, processors

configure(processors=[processors.JSONRenderer()])

logging = get_logger()


def job_logging(func):
    def wrapper():
        start_time = time.time()
        try:
            nb_of_records = func()
            logging.info('Success', message='Job report', report={'jobName': func.__name__,
                                                                  'success': True,
                                                                  'executionTimeInSeconds': time.time() - start_time,
                                                                  'numberOfRecords': nb_of_records})
            return nb_of_records
        except Exception as error:
            logging.error('Failure', message='Job report', report={'jobName': func.__name__,
                                                                   'success': False,
                                                                   'executionTimeInSeconds': time.time() - start_time})
            raise error

    return wrapper
