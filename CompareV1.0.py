# -*- coding: utf-8 -*-
"""
Created on Thu Jul 16 20:42:53 2020

@author: https://github.com/JustasBud/CSV-Compare
"""

import pandas as pd
#pd.set_option('float_format', '{:f}'.format) #convert scientific to whole numbers
import numpy as np


############################################################################
import os

import glob
#newest = max(glob.iglob('C:/Users/Justas/Downloads/*.csv'), key=os.path.getctime)






#set path for csv:
path = r'C:\Users\Justas\Downloads\*.csv'

list_of_files=glob.glob(path)

#getctime for creation or getmtime for modified
sorted_files = sorted(list_of_files, key=os.path.getmtime) 
#last modified
print ('Last modified file: ' + sorted_files[-1])
#2nd last modified
print ('2nd Last modified file: ' + sorted_files[-2])

lastmodifiedDF1=sorted_files[-1]
secondlastmodifiedDF2=sorted_files[-2]
###########################################################################
lastmodifiedDF1=lastmodifiedDF1[lastmodifiedDF1.rindex('\\')+1:] #strip path
secondlastmodifiedDF2=secondlastmodifiedDF2[secondlastmodifiedDF2.rindex('\\')+1:] #strip path

df1 = pd.read_csv(sorted_files[-1]) 
df2 = pd.read_csv(sorted_files[-2]) 


#Define files manually:
#df1 = pd.read_csv(r"C:\Users\Justas\Downloads\ABC.csv") 
#df2 = pd.read_csv(r"C:\Users\Justas\Downloads\DEF.csv") 


#Step 1: checking if the same number of columns:
df1length=len(df1.columns)
df2length=len(df2.columns)

df1l=list(df1) 
df2l=list(df2) 

x = set(df1l)
y = set(df2l)


if df1length==df2length:
    print('PASS (1): Number of columns are the same')
    step0Fail='False'
else:
    step0Fail='True'
    print('FAIL (1): Number of columns are NOT the same')
    print (lastmodifiedDF1 + ' Columns: ' + str(df1length))
    print (secondlastmodifiedDF2 + ' Columns: ' +  str(df2length))
    print ('Different/Missing column: ' + str(x^y))



#Step 2:
##Checking if the same number of columns and if the column headers are the same
#Checking if column headers are the same (also checks if the same number of headers)
#Does NOT check for if in the same order, done in Step 2
df1l=list(df1) 
df2l=list(df2) 

x = set(df1l)
y = set(df2l)

if step0Fail=='False':
    if x == y:
        print('PASS (2): Column headers are the same')
        step1Fail='False'
    #    print("First and Second list are Equal")
    else:
        step1Fail='True'
        print("FAIL (2): Column headers are NOT the same")
#        print(lastmodifiedDF1 + ' Columns: ' + str(x)+'\n')
#        print(secondlastmodifiedDF2 + ' Columns: ' + str(y)+'\n')
        print('Different columns between files:' + '\n'+str(x^y))
    
    
#Step 3:
#Checking if columns are in the same order
if step0Fail=='False' and step1Fail=='False':
    if df1l==df2l:
        print('PASS (3): Columns in the same order')
        
        step2Fail='False'
    else:
        step2Fail='True'
        print('FAIL (3): Columns NOT in the Same Order')

    
#Step 4:
#Checking number of rows

lendf1=len(df1.index)+1
lendf2=len(df2.index)+1



if step0Fail=='False' and step1Fail=='False' and step2Fail=='False':
    
    if lendf1==lendf2:
        print('PASS (4): Same number of rows: ' + str(lendf1))
        
        step3Fail='False'
    else:
        print('FAIL (4): NOT same number of rows')
        print('FAIL (4): Number of rows for: ' + str(lastmodifiedDF1) + '\n' + str(lendf1))
        print('FAIL (4): Number of rows for: ' + str(secondlastmodifiedDF2) + '\n' + str(lendf2))
        step3Fail='True'


#Step 5:

#does not work for str with float, splitting into num vs obj
    
#NOT NEEDED as objects will include dates and dates are not formatted in the same way
#objects = ['object']

#df1_obj = df1.select_dtypes(include=objects)    
#df1_objstr=df1_obj.astype(str)

numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']    

#df1_num = df1.select_dtypes(include=[np.number])   #not using, np not needed
df1_num = df1.select_dtypes(include=numerics)    
#filling blanks with 0 in order to convert to int
df1_num = df1_num.fillna(0)
#convert to int because of different rounding Orbit v Polaris
df1_int=df1_num.astype(int)


#NOT NEEDED as objects will include dates and dates are not formatted in the same way
#df2_obj = df2.select_dtypes(include=objects)    
#df2_objstr=df2_obj.astype(str)

#df2_num = df2.select_dtypes(include=[np.number])    #not using, np not needed
df2_num = df2.select_dtypes(include=numerics)   
#filling blanks with 0 in order to convert to int
df2_num = df2_num.fillna(0)
#convert to int because of different rounding Orbit v Polaris
df2_int=df2_num.astype(int)



#sumdf1=df1.sum(axis=0)
#sumdf2=df2.sum(axis=0)
#Step 4.1 sorting all columns low->high




#NOT NEEDED as objects will include dates and dates are not formatted in the same way
#df1o = pd.DataFrame(np.sort(df1_objstr.values, axis=0), index=df1_objstr.index, columns=df1_objstr.columns)
#df2o = pd.DataFrame(np.sort(df2_objstr.values, axis=0), index=df2_objstr.index, columns=df2_objstr.columns)


#ExportForDebug
#df1o.to_csv(r'C:\Users\Justas\Downloads\test1.csv', index = False)
#df2o.to_csv(r'C:\Users\Justas\Downloads\test2.csv', index = False)


#Step 5 - does not work for str with float: 
df1n = pd.DataFrame(np.sort(df1_int.values, axis=0), index=df1_int.index, columns=df1_int.columns)
df2n = pd.DataFrame(np.sort(df2_int.values, axis=0), index=df2_int.index, columns=df2_int.columns)


#NOT NEEDED as objects will include dates and dates are not formatted in the same way
#df1compareO=df1o.values.tolist()
#df2compareO=df2o.values.tolist()

#compare numeric values only (not comparing strings due to different date formatting from 2 systems)
df1compare=df1n.values.tolist()
df2compare=df2n.values.tolist()

#if df1compareO==df2compareO:
#    print('Same object values')
#else:
#    print('NOT Same object values')
if step0Fail=='False' and step1Fail=='False' and step2Fail=='False' and step3Fail=='False':
    if df1compare==df2compare:
        
        print('PASS (5): Same numeric values')
        step4Fail='False'
    else:
        print('FAIL (5): NOT Same numeric values')
        step4Fail='True'

if step0Fail=='False' and step1Fail=='False' and step2Fail=='False' and step3Fail=='False' and step4Fail=='False':
    print ('OVERALL: PASS')
else:
    print ('OVERALL: FAIL')
#df2s = pd.DataFrame(np.sort(df2.values, axis=0), index=df2.index, columns=df2.columns)

#from pandas.util.testing import assert_frame_equal
#print (assert_frame_equal(df1, df2))


