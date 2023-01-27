#Author: Ruckapark
#Date: 27/01/2023 14:09

import psycopg2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import cv2


if __name__ == "__main__":
    
    #pw = #define password for db
    
    #connect to database - my db is at port 5433
    conn = psycopg2.connect(dbname = "pythontest", user = "postgres", password = pw, port=5433)
    
    #create cursur and readtable
    #cur = conn.cursor()
    #cur.execute("SELECT * FROM photoinfo")
    #cur.close()
    
    #simple method with open connection
    photoinfo_df = pd.read_sql_query('SELECT * FROM "photoinfo"', conn)
    
    conn.close()
    
    #%%
    output_df = pd.DataFrame(index = photoinfo_df.index,columns = ['id','photos'])
    for i in range(photoinfo_df.shape[0]):
        
        #read file grayscale
        img = cv2.imread(photoinfo_df['pathfile'].iloc[i],0)
        
        #if not square extract top of image resized
        dim = np.min(img.shape)
        img = cv2.resize(img[:dim,:dim],(64,64))
        
        #write to string
        output_df.iloc[i] = [i+1,np.array2string(img.flatten(),separator = ',',threshold = 50000).strip('[]').replace('\n', '').replace(' ', '')]
        
    #write to .sql file to input into table