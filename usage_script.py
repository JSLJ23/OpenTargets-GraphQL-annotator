import main

# For usage, add the full name of the csv file of Ensembl_ids to the variable csv_file.
csv_file = "STM2020_NASH_stages_genes.csv"

target_disease_association_results = main.annotate_disease_target_association(csv_file, "Ensembl_id", "Liver")
target_disease_association_results.to_csv('disease_target_associations.tsv', sep='\t', encoding='utf-8', index=False)
