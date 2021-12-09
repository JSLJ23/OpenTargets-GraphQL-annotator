# Import relevant libraries
import requests
import json


def get_target_chemical_probe_association(ensembl_id):
    # Set variables object of arguments to be passed to endpoint
    variables = {"ensemblId": ensembl_id}

    # Build query string
    query_string = """
        query target($ensemblId: String!){
            target(ensemblId: $ensemblId){
                id
                approvedSymbol
                approvedName
                    chemicalProbes{
              id
              drugId
              inchiKey
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


def extract_associations(json_response, drug_id_filter):

    associated_chemical_probes = json_response["target"]["chemicalProbes"]

    if len(associated_chemical_probes) >= 0:

        if drug_id_filter == "yes":
            filtered_chemical_probes = [probe for probe in associated_chemical_probes if probe["drugId"] is not None]

        else:
            filtered_chemical_probes = associated_chemical_probes

        associated_chemical_probe_count = len(filtered_chemical_probes)

        # Using list comprehension to iterate through list of association information, and retrieve disease name,
        # id and score
        filtered_chemical_probes_nested_list = \
            [[probe["id"], probe["drugId"], probe["inchiKey"]] for probe in filtered_chemical_probes]

    else:
        associated_chemical_probe_count = 0
        filtered_chemical_probes_nested_list = []

    return associated_chemical_probe_count, filtered_chemical_probes_nested_list
