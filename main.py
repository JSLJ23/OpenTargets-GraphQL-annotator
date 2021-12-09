import target_disease
import target_chem_probe
import pandas as pd


def annotate_target_disease_association(ensembl_csv, ensembl_header, disease):
    ensembl_df = pd.read_csv(ensembl_csv)
    rows, columns = ensembl_df.shape

    ensembl_df_annotated = ensembl_df  # Make a copy of the original ensembl_df so as to not overwrite it.

    for i in range(rows):
        ensembl_id = ensembl_df.loc[i, ensembl_header]
        target_disease_association = \
            target_disease.get_target_disease_association(ensembl_id=ensembl_id, disease_name=disease)
        # Get disease target association counts and nested list of disease target associations.
        counts, nested_list = target_disease.extract_association_scores(target_disease_association)
        average_association_score = target_disease.aggregate_association_scores(nested_list)

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


def annotate_target_chemical_probe_association(ensembl_csv, ensembl_header, drug_id_filter="yes"):
    ensembl_df = pd.read_csv(ensembl_csv)
    rows, columns = ensembl_df.shape

    ensembl_df_annotated = ensembl_df  # Make a copy of the original ensembl_df so as to not overwrite it.

    for i in range(rows):
        ensembl_id = ensembl_df.loc[i, ensembl_header]
        target_probe_association = target_chem_probe.get_target_chemical_probe_association(ensembl_id=ensembl_id)
        counts, nested_list = target_chem_probe.extract_associations(target_probe_association, drug_id_filter)

        ensembl_df_annotated.loc[i, columns+1] = counts

        if len(nested_list) > 0:
            for index, associations in enumerate(nested_list):
                chem_probes_listToStr = ', '.join(map(str, associations))
                ensembl_df_annotated.loc[i, columns + 2 + index] = chem_probes_listToStr

    return ensembl_df_annotated

