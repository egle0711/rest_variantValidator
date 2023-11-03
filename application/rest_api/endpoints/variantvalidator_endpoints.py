from flask_restx import Namespace, Resource
from rest_api.utils import request_parser
from rest_api.utils import representations
import requests
from rest_api.utils import exceptions
import logging
from flask import request


# Get the logger
logger = logging.getLogger('rest_api')

"""
Create a parser object locally
"""
parser = request_parser.parser

api = Namespace('VariantValidator', description='VariantValidator API Endpoints')

@api.route("/variantvalidator/<string:genome_build>/<string:variant_description>/<string:select_transcripts>")
@api.param("select_transcripts", "***'all'***\n"
                                 ">   Return all possible transcripts\n"
                                 "\n***Single***\n"
                                 ">   NM_000093.4\n"
                                 "\n***Multiple***\n"
                                 ">   NM_000093.4|NM_001278074.1|NM_000093.3")
@api.param("variant_description", "***HGVS***\n"
                                  ">   NM_000088.3:c.589G>T\n"
                                  ">   NC_000017.10:g.48275363C>A\n"
                                  ">   NG_007400.1:g.8638G>T\n"
                                  ">   LRG_1:g.8638G>T\n"
                                  ">   LRG_1t1:c.589G>T\n"
                                  "\n***Pseudo-VCF***\n"
                                  ">   17-50198002-C-A\n"
                                  ">   17:50198002:C:A\n"
                                  ">   GRCh38-17-50198002-C-A\n"
                                  ">   GRCh38:17:50198002:C:A\n"
                                  "\n***Hybrid***\n"
                                  ">   chr17:50198002C>A\n "
                                  ">   chr17:50198002C>A(GRCh38)\n"
                                  ">   chr17:g.50198002C>A\n"
                                  ">   chr17:g.50198002C>A(GRCh38)")
@api.param("genome_build", "***Accepted:***\n"
                           ">   GRCh37\n"
                           ">   GRCh38\n"
                           ">   hg19\n"
                           ">   hg38")
class VariantValidatorClass(Resource):
    # Add documentation about the parser
    @api.expect(parser, validate=True)
    def get(self, genome_build, variant_description, select_transcripts):

        # Log the request details
        logger.info(f"Received request for Genome Build: {genome_build}, Variant: {variant_description}, Transcripts: {select_transcripts} from IP: {request.remote_addr}")

        # Construct the URL for the VariantValidator rest-API
        url = '/'.join(['https://rest.variantvalidator.org/variantvalidator',
                        genome_build,
                        variant_description,
                        select_transcripts
                        ])
        try:
            validation = requests.get(url)
            # Log success in fetching data from external API
            logger.info(f"Successfully fetched data from {url} for variant: {variant_description}")
        except ConnectionError:
            logger.error(f"Failed to connect to VariantValidator API for variant: {variant_description} from IP: {request.remote_addr}")
            raise exceptions.RemoteConnectionError('https://rest.variantvalidator.org/variantvalidator currently unavailable')
        
        content = validation.json()

        # Log the response details
        logger.debug(f"VariantValidator response for {variant_description}: {content}")

        args = parser.parse_args()
        if args['content-type'] == 'application/json':
            return representations.application_json(content, 200, None)
        elif args['content-type'] == 'text/xml':
            return representations.xml(content, 200, None)
        else:
            return content
