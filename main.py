import camelot as cm
import pandas as pd
import numpy as np
import cred
import os

#Function 
def exract_table(filename,passwrd):
    # Extracting table from page 1
    pdf = cm.read_pdf(filename,password=passwrd,flavor='stream',table_areas=['0,670,600,475'],pages='1')
    table1 = pdf[0].df
    if (table1[-1:][2]=='**** End of Statement ****').bool():
        table1 = table1[0:-1]
        table1.columns = ['date','summary','category','amount','cashback']
#         print('returning table 1')
        return table1
    
    # Extracting table from page 2 if "End of Statement" not found
    pdf = cm.read_pdf(filename,password=passwrd,flavor='stream',table_areas=['0,915,600,0'],pages='2')
    table2 = pdf[0].df
    if (table2[-1:][2]=='**** End of Statement ****').bool():
        table2 = table2[0:-1]
        table0 = pd.concat([table1,table2])
        table0.columns = ['date','summary','category','amount','cashback']
#         print('returning table 2')
        return table0
    
    # Extracting table from page 3 if "End of Stat"
    pdf = cm.read_pdf(filename,password=passwrd,flavor='stream',table_areas=['0,915,600,0'],pages='3')
    table3 = pdf[0].df
    table3 = table3[0:-1]
    table0 = pd.concat([table1,table2,table3])
    table0.columns = ['date','summary','category','amount','cashback']
#     print('returning table 3')
    return table0

def normalise_table(table):
    # Removing whitespace withing the string (only for req. columns)
    table.date = table.date.str.replace(" ","")
    table.category = table.category.str.replace(" ","")
    table.amount = table.amount.str.replace(" ","")
    table.cashback = table.cashback.str.replace(" ","")
    
    # Splitting the value and type of amount
    table['amt_value'] = table['amount'].str.slice(stop=-2)
    table['amt_type'] = table['amount'].str.slice(start=-2)
    table['cb_value'] = table['cashback'].str.slice(stop=-2)
    table['cb_type'] = table['cashback'].str.slice(start=-2)
    
    # Seggreating amount based on Cr/Dr
    table['amt_cr']=np.where(table['amt_type']=='Cr',table['amt_value'],0)
    table['amt_dr']=np.where(table['amt_type']=='Dr',table['amt_value'],0)
    table['cb_cr']=np.where(table['cb_type']=='Cr',table['cb_value'],0)
    table['cb_dr']=np.where(table['cb_type']=='Dr',table['cb_value'],0)

    # Removing trailing whitespaces
    table['summary']= table['summary'].str.strip()
    
    # Deleting un-required columns
    table=table.drop(['amt_value','amt_type','cb_value','cb_type'],axis=1)
    
    # Renaming the columns
    table.columns = ['Date','Summary','Category','Amount','Cashback','Amount Credit','Amount Debit','Cashback Credit','Cashback Debit']
    
    return table

filenames = os.listdir('./pdf')[1:]

for fname in filenames:
    result = exract_table(filename='./pdf/'+fname,passwrd=cred.password)
    result = normalise_table(result)
    result['Year-Month'] = '20'+ fname[-9:-4]
    result.to_csv('./csv/'+fname[:-4]+'.csv')