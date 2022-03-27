import camelot
import pandas as pd
import numpy as np
import cred as cred

tables = camelot.read_pdf(cred.filename,password=cred.password, pages='all')

temp = {
    'date' : tables[1].df[1][1].split("\n"),
    'txn_details' : tables[1].df[2][1].split("\n"),
    'amt' : tables[1].df[4][1].split("\n"),
    'cb' : tables[1].df[5][1].split("\n")
}

tab1 = pd.DataFrame(temp)
tab1[['amt_value','amt_type']] = tab1['amt'].str.split(expand=True)
tab1[['cb_value','cb_type']] = tab1['cb'].str.split(expand=True)

tab1['amt_cr']=np.where(tab1['amt_type']=='Cr',tab1['amt_value'],0)
tab1['amt_dr']=np.where(tab1['amt_type']=='Dr',tab1['amt_value'],0)
tab1['cb_cr']=np.where(tab1['cb_type']=='Cr',tab1['cb_value'],0)
tab1['cb_dr']=np.where(tab1['cb_type']=='Dr',tab1['cb_value'],0)

tab1['date']= tab1['date'].str.replace(" ","")

tab1['txn_details']= tab1['txn_details'].str.strip()

tab1=tab1.drop(['amt_value','amt_type','cb_value','cb_type'],axis=1)

tab1.columns = ['Date','Summary','Amount','Cashback','Amount Credit','Amount Debit','Cashback Credit','Cashback Debit']

tab1.to_csv('CC_statement.csv')
