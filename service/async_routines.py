import os
from multiprocessing import get_context
import constant_strings as const
import log
import functions


def post_example(input_parameters, run_hash):

    timeout = 30  #seconds
    input_string = input_parameters['string']

    try:
        p = get_context('spawn').Process(
            target=functions.string_log,
            args=[input_string, run_hash],
        )
        log.info(
            const.START_TEXT, run_hash, service_name=const.SERVICE_NAME,
        )
        p.start()
    except Exception as e:
        log.error(
            const.LAUNCH_ERROR.format(str(e)), run_hash,
            service_name=const.SERVICE_NAME,
        )
    else:
        p.join(timeout)
        if p.is_alive():
            log.error(
                const.TIMEOUT, run_hash, service_name=const.SERVICE_NAME
            )
            try:
                p.terminate()
                p.join()
                log.info(
                    const.KILL_SUCCESS, run_hash,
                    service_name=const.SERVICE_NAME
                )
            except Exception as e:
                log.error(
                    const.KILL_ERROR.format(str(e)), run_hash,
                    service_name=const.SERVICE_NAME
                )


def get_example():
    get_str = functions.hello_world()
    return get_str
