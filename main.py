import opentargets_gql
import pandas as pd
import time

# For usage, add the full name of the csv file of Ensembl_ids to the variable csv_file.
csv_file = "STM2020_NASH_stages_genes.csv"


def annotate_disease_target_association(ensembl_csv, ensembl_header="Ensembl_id", disease="Liver"):
    ensembl_df = pd.read_csv(ensembl_csv)
    rows, columns = ensembl_df.shape

    ensembl_df_annotated = ensembl_df  # Make a copy of the original ensembl_df so as to not overwrite it.

    for i in range(rows):
        ensembl_id = ensembl_df.loc[i, ensembl_header]
        disease_target_association = \
            opentargets_gql.get_target_disease_association(ensembl_id=ensembl_id, disease_name=disease)
        # Get disease target association counts and nested list of disease target associations.
        counts, nested_list = opentargets_gql.extract_association_scores(disease_target_association)
        average_association_score = opentargets_gql.aggregate_association_scores(nested_list)

        time.sleep(1)   # Sleep so as not to flood the GraphQL endpoint with request and get timeout.

        ensembl_df_annotated.loc[i, columns+1] = average_association_score
        ensembl_df_annotated.loc[i, columns+2] = counts

        if len(nested_list) > 0:
            for index, associations in enumerate(nested_list):
                # index starts from 0 and columns+1 is already filled with average_association_score.
                # columns+2 is used for counts.
                # start with columns+3 for first association and columns+3+index for subsequent associations.
                associations_listToStr = ', '.join(map(str, associations))
                ensembl_df_annotated.loc[i, columns+3+index] = associations_listToStr

    return ensembl_df_annotated


result = annotate_disease_target_association(csv_file)

result.to_csv('disease_target_associations.tsv', sep='\t', encoding='utf-8', index=False)
