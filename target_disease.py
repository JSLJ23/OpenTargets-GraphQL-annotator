# Import relevant libraries
import requests
import json


def get_target_disease_association(ensembl_id, disease_name_list, index=0, size=100):
    # Set variables object of arguments to be passed to endpoint
    # ensembl_id taken in as elements of a list for multiple queries

    api_response_as_json_data_list = []

    for diseases in disease_name_list:
        variables = {"ensemblId": ensembl_id,
                     "disease": diseases,
                     "index": index,
                     "size": size}

        # Build query string
        query_string = """
            query target($ensemblId: String!, $disease: String!, $index: Int!, $size: Int!){
                target(ensemblId: $ensemblId){
                    id
                    approvedSymbol
                    approvedName
                    associatedDiseases(BFilter: $disease, page: {
                    index: $index,
                    size: $size
                    }){
                        count
                        rows{
                            disease{
                                name
                                id
                            }
                            score
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
        api_response_as_json_data = api_response_as_json["data"]
        association_score_list = api_response_as_json_data["target"]["associatedDiseases"]["rows"]
        api_response_as_json_data_list.extend(association_score_list)

    api_response_as_json_data_list_unique = \
        list({v['disease']['id']: v for v in api_response_as_json_data_list}.values())

    return api_response_as_json_data_list_unique


def extract_association_scores(disease_list_unique):
    associated_diseases_count = len(disease_list_unique)
    # Using list comprehension to iterate through list of association information, and retrieve disease name,
    # id and score
    association_score_nested_list = \
        [[score["disease"]["name"], score["disease"]["id"], score["score"]] for score in disease_list_unique]

    return associated_diseases_count, association_score_nested_list


def aggregate_association_scores(association_score_nested_list):
    # Index [2] gives position 3, where the disease association score is stored in the nested list
    if len(association_score_nested_list) == 0:
        average_score = 0
    else:
        total_score = sum(disease[2] for disease in association_score_nested_list)
        total_count = len(association_score_nested_list)
        average_score = total_score / total_count

    return average_score
