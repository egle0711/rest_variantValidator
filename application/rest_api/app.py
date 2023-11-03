import sys
sys.path.append('/home/egleg/PycharmProjects/rest_variantValidator/application')

"""
Simple rest interface for VariantValidator built using Flask Flask-RESTX and Swagger UI
"""

# Import modules
from flask import Flask, request
from endpoints import api
from rest_api.utils import representations, exceptions, request_parser
import logging
from logging import handlers
import time

"""
Logging Configuration for Debugging/Development Environment
"""
# Setup logger
logger = logging.getLogger('rest_api')
logger.setLevel(logging.DEBUG)

# Console log handler for real-time log streaming during development
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(console_format)
logger.addHandler(console_handler)

# Absolute path for the rotating file log handler to ensure consistent log file location
log_file_path = '/home/egleg/PycharmProjects/rest_variantValidator/application/rest_api.log'
logHandler = handlers.RotatingFileHandler(log_file_path, maxBytes=500000, backupCount=2)
logHandler.setLevel(logging.DEBUG)
file_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logHandler.setFormatter(file_format)
logger.addHandler(logHandler)

# Log the initialization for testing
logger.debug("Logging system initialized")

"""
Create a parser object locally
"""
parser = request_parser.parser

# Define the application as a Flask app with the name defined by __name__ (i.e. the name of the current module)
# Most tutorials define application as "app", but I have had issues with this when it comes to deployment,
# so application is recommended
application = Flask(__name__)

api.init_app(application)

# By default, show all endpoints (collapsed)
application.config.SWAGGER_UI_DOC_EXPANSION = 'list'

"""
Representations
 - Adds a response-type into the "Response content type" drop-down menu displayed in Swagger
 - When selected, the APP will return the correct response-header and content type
 - The default for flask-RESTX is application/json
 
Note 
 - The decorators are assigned to the functions
"""
@api.representation('text/xml')
def application_xml(data, code, headers):
    resp = representations.xml(data, code, headers)
    return resp

@api.representation('application/json')
def application_json(data, code, headers):
    resp = representations.application_json(data, code, headers)
    return resp

"""
Error handlers
    - exceptions has now been imported from utils!
"""
def log_exception(exception_type):
    params = dict(request.args)
    params['path'] = request.path
    message = '%s occurred at %s with params=%s' % (exception_type, time.ctime(), params)
    logger.exception(message, exc_info=True)

@application.errorhandler(exceptions.RemoteConnectionError)
def remote_connection_error_handler(e):
    log_exception('RemoteConnectionError')
    args = parser.parse_args()
    if args['content-type'] != 'text/xml':
        return application_json({'message': str(e)}, 504, None)
    else:
        return application_xml({'message': str(e)}, 504, None)

@application.errorhandler(404)
def not_found_error_handler():
    args = parser.parse_args()
    if args['content-type'] != 'text/xml':
        return application_json({'message': 'Requested Endpoint not found'}, 404, None)
    else:
        return application_xml({'message': 'Requested Endpoint not found'}, 404, None)

@application.errorhandler(500)
def default_error_handler():
    log_exception('RemoteConnectionError')
    args = parser.parse_args()
    if args['content-type'] != 'text/xml':
        return application_json({'message': 'unhandled error: contact https://variantvalidator.org/contact_admin/'}, 500, None)
    else:
        return application_xml({'message': 'unhandled error: contact https://variantvalidator.org/contact_admin/'}, 500, None)

# Allows app to be run in debug mode
if __name__ == '__main__':
    application.debug = True  # Enable debugging mode
    application.run(host="127.0.0.1", port=5000)
