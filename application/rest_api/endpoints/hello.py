from flask_restx import Namespace, Resource
from rest_api.utils import request_parser
from rest_api.utils import representations
import logging
from flask import request
# Get the logger
logger = logging.getLogger('rest_api')

"""
Create a parser object locally
"""
parser = request_parser.parser

"""
The assignment of api changes
"""

api = Namespace('hello', description='Simple API that returns a greeting')

"""
We also need to re-assign the route ans other decorated functions to api
"""

@api.route("/")
class HelloClass(Resource):

    # Add documentation about the parser
    @api.expect(parser, validate=True)
    def get(self):

        # Collect Arguments
        args = parser.parse_args()

        # Overrides the default response route so that the standard HTML URL can return any specified format
        if args['content-type'] == 'application/json':
            logger.debug(f"Returned JSON greeting for {request.remote_addr}")
            return representations.application_json({
                "greeting": "Hello World"
            }, 200, None)
        elif args['content-type'] == 'text/xml':
            logger.debug(f"Returned XML greeting for {request.remote_addr}")
            return representations.xml({
                 "greeting": "Hello World"
            }, 200, None)
        else:
            # Return the api default output
            return {
                 "greeting": "Hello World"
            }
