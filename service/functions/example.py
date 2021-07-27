import constant_strings
import log


def hello_world():
    return "Hello World"


def string_log(string="Hello World", run_hash=None):
    """
    Logs a string.
    """
    try:
        log.info(constant_strings.PROCESS_SUCCESS.format(string), run_hash, 
                 service_name=constant_strings.SERVICE_NAME)
    except Exception as e:
        log.error(constant_strings.PROCESS_EXCEPTION, run_hash,
                  service_name=constant_strings.SER)

    return True
