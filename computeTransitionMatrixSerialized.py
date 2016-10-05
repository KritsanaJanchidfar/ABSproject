# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
import numpy as np
from multiprocessing import Pool

os.system("taskset -p 0xff %d" % os.getpid())

data = pd.read_csv('R:/refm-mfe/absnet1/loan_history_ca_cleaned.csv ')

# Testing with smaller data frame
test_df = data[0:100][:]

#define fuction to get the delinq
''''
"Lewtan's Delinquency Loan Status history flag for Roll Rates for the life of the loan on ABSNET Loan
0 = Prepay, 1 = Current, 2 = 30 Days Delq, 3 = 60 Days Delq, 4 = 90 Days Delq, 
5 = 120 Days Delq, 6 = 150+ Days Delq, 7 = Foreclosure, 8 = REO, 9 = Liquidated, X = Not available"

''''
def datediff(date1, date2):
    # date is a string in this format: 'yyyy-mm'
    # return pd dataframe date1- date2 in month
    y1 = int(date1[0:4])
    m1 = int(date1[5:7])
    y2 = int(date2[0:4])
    m2 = int(date2[5:7])
    return 12*y1+m1-12*y2-m2

def getOccurenceMatrix(data,dliq,startdate,enddate):
    # date is a string in this format: 'yyyy-mm'
    # startdate -> begin date  enddate-> end date
    # startdate < enddate
    # dliq = string -> 'histdelqstatusmbarr' or 'histdelqstatusotsrr'
    occur = np.zeros((10,10),dtype=np.int)
    data['diff_cstart_startdate'] = data['histstartdate'].apply(datediff,args=(startdate,))
    data['diff_cstart_enddate'] = data['histstartdate'].apply(datediff,args=(enddate,))
    data['diff_cend_startdate'] = data['histenddate'].apply(datediff,args=(startdate,))
    data['diff_cend_enddate'] = data['histenddate'].apply(datediff,args=(enddate,))
    # list to colect the string
    l = []
    for i in range(data.shape[0]):
        cstart_enddate = data['diff_cstart_enddate'][i]
        cend_startdate = data['diff_cend_startdate'][i]
        cstart_startdate = data['diff_cstart_startdate'][i]
        cend_enddate =  data['diff_cend_enddate'][i]
        s = data[dliq][i]
        if  cstart_enddate >= 0 or  cend_startdate <= 0:
            continue
        elif cstart_startdate >= 0 and  cend_enddate >0:
            # append the string from cstart to enddate
            l.append(s[:-cend_enddate])
        elif cstart_startdate < 0 and cend_enddate >0:
            # append the string from startdate to enddate
            l.append(s[-cstart_startdate:-cend_enddate])
        elif cstart_startdate < 0 and cend_enddate <=0:
            # append the string from startdate to cend
            l.append(s[-cstart_startdate:])
        else:
            # append the string
            l.append(s)
    # Counting the occurence in the strings
    for i in range(len(l)):
        # for each string calculate the occurance
        # we skip when we see X
        if len(l[i]) <= 1:
            continue
        prev = int(l[i][0])
        for j in range(1,len(l[i])-1):
            if l[i][j] == 'X':
                continue
            else:
                curr = int(l[i][j])
                occur[prev][curr] = occur[prev][curr]+1
                prev = curr
    return occur
            
data['histdelqstatusmbarr'] = data['histdelqstatusmbarr'].str[0:7]
data['histdelqstatusotsrr'] = data['histdelqstatusotsrr'].str[0:7]
