## DIKB Evidence from the evidence base as of 2017 for substrates of 2d6 and 3a4

The evidence about substrates comes from the DIKB evidence base as of 2017. The issue with this is that the FDA has since updated 
their assertions about clinical subsrates and inhibitors. Any final experiments using this evidene needs to consider changes in the newer
FDA information (see the FDA drug interactions for current tables).

This evidence was exported from the DIKB as follows:

- Prerequisites: Python 2 is needed to load the DIKB evidence pickle.

1) the server 130.49.206.139 has an SQL database for the dikb. That database has older data wrt FDA evidence. The script /home/rdb20/ROSKO_Backups/DRIVE_Empirical_Experiment/DIKB-Evidence-analytics/Drive-Experiment/dikb-update.py was ran to update all FDA 2006 data to 2012 data. The results of this run were saved to:

- scripts/dikb-pickles/ev-test-two.pickle

2) the script /home/rdb20/ROSKO_Backups/DRIVE_Empirical_Experiment/DIKB-Evidence-analytics/new-SQL-simple-DIKB-web/createHTML_using_2017_data.py was ran to generated web pages describing evidence 

- html-output

3) the script scripts/dump-2d6-3a4-evidence.py was used to dump the evidence to a TSV file with links to web pages

- cyp2d6-or-cyp3a4-substrates-dikb-2017.tsv

4) The results of inference using the DIKB JTMS engine were copied over 

- DDIPredictions_Lax_2017_evidence.csv

- DDIPredictions_Strict_2017_evidence.csv

5) the script scripts/dump-2d6-3a4-inhibition-evidence.py was used to export inhibitors

- cyp2d6-or-cyp3a4-inhibitors-dikb-2017.tsv

6) the script scripts/dump-interactions-AUC-2-or-more.py was used to export increase auc data

- cyp2d6-or-cyp3a4-increase-auc-evidence-dikb-2017.tsv


