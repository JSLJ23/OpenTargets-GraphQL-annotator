# Import relevant libraries
import requests
import json


def get_target_drugs_association(ensembl_id):
    # Set variables object of arguments to be passed to endpoint
    variables = {"ensemblId": ensembl_id}

    # Build query string
    query_string = """
        query target($ensemblId: String!){
                target(ensemblId: $ensemblId){
                    id
                    approvedSymbol
                    approvedName
                            knownDrugs(size: 500){
                      uniqueDrugs
                      count
                      rows{
                        drug{
                          name
                        }
                        drugId
                        phase
                        mechanismOfAction
                    }
                }
            }
        }
    """

    # Set base URL of GraphQL API endpoint
    base_url = "https://api.platform.opentargets.org/api/v4/graphql"

    # Perform POST requests and check status code of response
    json_query = {"query": query_string,
                  "variables": variables}
    r = requests.post(base_url, json=json_query)

    # Transform API response into JSON format
    api_response_as_json = json.loads(r.text)

    return api_response_as_json["data"]


def extract_associations(json_response_data):

    if json_response_data["target"]["knownDrugs"] is not None:
        associated_known_drugs = json_response_data["target"]["knownDrugs"]["rows"]

        if len(associated_known_drugs) >= 0:
            unique_drugs_count = json_response_data["target"]["knownDrugs"]["uniqueDrugs"]
            all_drugs_count = json_response_data["target"]["knownDrugs"]["count"]

    else:
        unique_drugs_count = 0
        all_drugs_count = 0

    return unique_drugs_count, all_drugs_count
