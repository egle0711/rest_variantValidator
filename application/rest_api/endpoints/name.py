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

api = Namespace('name', description='Return a name provided by the user')

"""
We also need to re-assign the route and other decorated functions to api
"""

@api.route("/<string:name>")
@api.param("name", "Enter name")
class NameClass(Resource):

    # Add documentation about the parser
    @api.expect(parser, validate=True)
    def get(self, name):

        # Log the request
        logger.debug(f"Name request received: {name} from {request.remote_addr}")

        # Collect Arguments
        args = parser.parse_args()

        # Overrides the default response route so that the standard HTML URL can return any specified format
        if args['content-type'] == 'application/json':
            logger.debug(f"Returned JSON name response for {name} to {request.remote_addr}")
            return representations.application_json({
                "My name is": name
            },
                200, None)
        # example: http://127.0.0.1:5000/name/name/bob?content-type=text/xml
        elif args['content-type'] == 'text/xml':
            logger.debug(f"Returned XML name response for {name} to {request.remote_addr}")
            return representations.xml({
                "My name is": name
            },
                200, None)
        else:
            # Return the api default output
            return {
                "My name is": name
            }
