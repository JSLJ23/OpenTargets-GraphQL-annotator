from gql_query_builder import GqlQuery

query_drugs = GqlQuery().fields(['name']).query('hero').operation().generate()
print(query_drugs)
