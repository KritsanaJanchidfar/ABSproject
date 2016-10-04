# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd

#read data into python
loan_history_ca = pd.read_csv("R:/refm-mfe/absnet1/loan_history_ca.csv")
lhca_col_names = loan_history_ca.columns.values 

# select for desired columns
# respectively 'absnetloanfk' 'histstartdate' 'histenddate', 'histdelqstatusmbarr' 'histdelqstatusotsrr'
lhca_col_names_cleaned = lhca_col_names[[0,6,7, 15,16]]
loan_history_ca_cleaned = loan_history_ca[lhca_col_names_cleaned]

# write to disk
loan_history_ca_cleaned.to_csv("R:/refm-mfe/absnet1/loan_history_ca_cleaned.csv")


