#Author: Ruckapark
#Date: 27/01/2023 14:09

import psycopg2
import numpy as np
import pandas as pd
from sqlalchemy import create_engine

import cv2

def plot_grayscale_psql(df,index):
    
    image = np.array(df.loc[df['id'] == index,'photos'].iloc[0].split(','))
    image = np.array(np.reshape(image,(int(len(image)**0.5),)*2),dtype=np.uint8)
    cv2.imshow('image',image)


if __name__ == "__main__":
    
    pw = input('Password:') #input postgres db
    
    #connect to database - my db is at port 5433
    conn = psycopg2.connect(dbname = "pythontest", user = "postgres", password = pw, port=5433)
    
    #create cursur and readtable
    #cur = conn.cursor()
    #cur.execute("SELECT * FROM photoinfo")
    #cur.close()
    
    #Simple read with open db connection
    photoinfo_df = pd.read_sql_query('SELECT * FROM "photoinfo"', conn)
    
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
    
    #reopen connection with sqlalchemy
    db = create_engine("postgresql+psycopg2://postgres:{}@localhost:5433/pythontest".format(pw))
    
    #write to .sql file to input into table: photos_grayscale_64
    output_df.to_sql('photos_grayscale_64',db,if_exists='replace',index=False)
    
    #%%
    #Check written table and plot images
    photos_gs = pd.read_sql_query('SELECT * FROM "photos_grayscale_64"', conn)
    conn.close()
    
    #Plot image using grayscale for check
    plot_grayscale_psql(photos_gs,1)    