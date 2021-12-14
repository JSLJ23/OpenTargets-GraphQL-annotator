import main

# For usage, add the full name of the csv file of Ensembl_ids to the variable csv_file.
csv_file = "STM2020_NASH_stages_genes.csv"
csv_file_2 = "test_ensembl_id.csv"

target_disease_association_results = main.annotate_target_disease_association(csv_file, "Ensembl_id",
                                                                              ["liver", "hepato"])
target_disease_association_results.to_csv('target_disease_associations.tsv', sep='\t', encoding='utf-8', index=False)

target_probe_association_results = main.annotate_target_chemical_probe_association(csv_file, "Ensembl_id", "no")
target_probe_association_results.to_csv('target_chem_probe_associations.tsv', sep='\t', encoding='utf-8', index=False)

target_drug_association_results = main.annotate_target_known_drug_association(csv_file, "Ensembl_id")
target_drug_association_results.to_csv('target_drug_associations.tsv', sep='\t', encoding='utf-8', index=False)
