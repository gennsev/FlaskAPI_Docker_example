'''
    Service
    =======

    Provides
      1. Endpoints definitions
      2. Initialization routines

    How to use
    ----------
    If this module is executed, it stars a Flask appliction providing the
    endpoints described below.
'''

import concurrent.futures
import os

import constant_strings as const
import log
from async_routines import post_example, get_example
from flask import Flask, jsonify, make_response, request
from utils import get_hash

application = Flask(__name__)


@application.before_first_request
def initialize():
    ''' Code to run before first request, upon initialization.
    Deals with:
    - multiprocessing pool executor
    - logger initialization routine
    '''

    application.poolExecutor = concurrent.futures.ProcessPoolExecutor(
        max_workers=4)
    log.init_logger()
    log.debug(const.POOL_CREATED)


@application.route('/')
def index():
    ''' Index endpoint
    '''

    log.debug(const.ROOT_ACCESSED)
    return const.ROOT_MESSAGE


@application.route('/health', methods=['GET'])
def health():
    ''' Health-checking endpoint
    '''

    run_hash = get_hash()

    tag = os.environ.get('TAG', None)
    commit = os.environ.get('GIT_COMMIT', None)

    try:
        log.info(
            const.HEALTH_CHECK_SUCCESS, run_hash, service_name=const.SERVICE_NAME,
        )

        response = {
            'message': const.HEALTH_CHECK_SUCCESS,
            'version': tag,
            'commit': commit,
        }

        return make_response(jsonify(response), 200)

    except Exception:
        log.info(
            const.HEALTH_CHECK_ERROR, run_hash, service_name=const.SERVICE_NAME,
        )

        response = {
            'message': const.HEALTH_CHECK_ERROR,
            'version': tag,
            'commit': commit,
        }

        return make_response(jsonify(response), 200)


@application.route('/example_post', methods=['POST'])
def ex_back():
    ''' Runs the process in the background.
    '''

    run_hash = get_hash()

    log.info(
        const.STARTED_REQUEST, run_hash, service_name=const.SERVICE_NAME,
    )

    input_parameters = {
        'string': request.form.get('string', None)
    }

    try:
        application.poolExecutor.submit(post_example, input_parameters,
                                        run_hash)
        log.info(
            const.PROCESS_LAUNCH_SUCCESS, run_hash,
            service_name=const.SERVICE_NAME
        )

    except Exception as e:
        log.error(
            const.PROCESS_LAUNCH_ERROR.format(str(e)),
            run_hash,
            service_name=const.SERVICE_NAME,
        )

        response = {
            'message': const.PROCESS_LAUNCH_ERROR.format(str(e)),
            'run_hash': run_hash
        }

        return make_response(jsonify(response), 500)

    log.info(
        const.ENDED_REQUEST, run_hash, service_name=const.SERVICE_NAME)

    response = {
        'message': const.PROCESS_LAUNCH_SUCCESS,
        'run_hash': run_hash
    }

    return make_response(jsonify(response), 200)


@application.route('/example_get', methods=['GET'])
def ex_get():
    ''' Runs the process.
    '''
    run_hash = get_hash()

    log.info(
        const.STARTED_REQUEST, run_hash, service_name=const.SERVICE_NAME,
    )

    try:
        func_return = get_example()
        log.info(
            const.PROCESS_LAUNCH_SUCCESS, run_hash, service_name=const.SERVICE_NAME,
        )
    except Exception as e:
        log.error(
            const.PROCESS_LAUNCH_ERROR.format(str(e)),
            run_hash,
            service_name=const.SERVICE_NAME,
        )

        response = {
            'message': const.PROCESS_LAUNCH_ERROR.format(str(e)),
            'run_hash': run_hash
        }

        return make_response(jsonify(response), 500)

    log.info(
        const.ENDED_REQUEST, run_hash, service_name=const.SERVICE_NAME,
    )

    return make_response(func_return, 200)


if __name__ == '__main__':
    application.run()
