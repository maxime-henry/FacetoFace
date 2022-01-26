import streamlit as st
from pymongo import MongoClient
import pandas as pd
import random 

rand = random.randint(1,2)



st.set_page_config(
     page_title="Face to face",
     page_icon="🧊",
     layout="wide",
     initial_sidebar_state="expanded",
     menu_items={
         'Get Help': 'https://www.extremelycoolapp.com/help',
         'Report a bug': "https://www.extremelycoolapp.com/bug",
         'About': "# This is a header. This is an *extremely* cool app!"
     }
 )
user = st.secrets.db_connection.user
pwd = st.secrets.db_connection.password
host = "cluster0.vdgze"
databaseName = "Faces"
collectionName = "googleface"


CONNECTION_STRING = f"mongodb+srv://{user}:{pwd}@{host}.mongodb.net/{databaseName}"

client = MongoClient(CONNECTION_STRING)

mydb = client["Faces"]
mycol = mydb["BSAface"]


st.cache(max_entries=2)
def first_loading():
    mydoc =list(mycol.find().sort('rep').limit(3))
    data = pd.DataFrame(mydoc)
    image1 = data.iloc[0][1]
    image2 = data.iloc[rand][1]
    try:
        score1= data.iloc[0]['note']
    except:
        score1= 400
        ### REP 1 ###  
    try:
        rep1= data.iloc[0]['rep']
    except:
        rep1= 0

    
        ### Note ###
    try:
        score2= data.iloc[0]['note']
    except:
        score2= 400
        ### REP ###  
    try:
        rep2= data.iloc[0]['rep']
    except:
        rep2= 0
    return (image1,image2, score1, score2, rep1,rep2)



image1, image2, score1 , score2, rep1,rep2 = first_loading()

#########################################

st.cache(max_entries=2)
def get_image(image1,image2, score1, score2, rep1,rep2, win):
    if win ==1 :
        #Faire le calcul des points
        expected1 = 1/(1+    pow(10,((score2-score1)/400) ))
        newscore1 = score1 + 32*(1-expected1)
        expected2 = 1/(1+    pow(10,((score1-score2)/400) ))
        newscore2 = score2 + 32*(0-expected2)

#########################################################################
    if win ==2:
        #Faire le calcul des points
        expected1 = 1/(1+    pow(10,((score2-score1)/400) ))
        newscore1 = score1 + 32*(0-expected1)
        expected2 = 1/(1+    pow(10,((score1-score2)/400) ))
        newscore2 = score2 + 32*(1-expected2)

    print(expected1,expected2,newscore1,newscore2)
    newrep1 = rep1 + 1
    newrep2 = rep2 +1
    # Enregistrer les données 
    print(newscore2, image2)
    # mycol.update_one({"X1":image1}, {"$set":{'note':newscore1,'rep':int(newrep1)}})
    # mycol.update_one({"X1":image2}, {"$set":{'note':newscore2,'rep':int(newrep2)}})
    print("Updated")
    # Rechercher de nouvelles images

    mydoc = list(mycol.find().sort('rep').limit(3))
    data = pd.DataFrame(mydoc)
    image1 = data.iloc[0][1]
    try:
        score1= data.iloc[0]['note']
    except:
        score1= 400
        ### REP 1 ###  
    try:
        rep1= data.iloc[0]['rep']
    except:
        rep1= 0

    image2 = data.iloc[rand][1]
        ### Note ###
    try:
        score2= data.iloc[0]['note']
    except:
        score2= 400
        ### REP ###  
    try:
        rep2= data.iloc[0]['rep']
    except:
        rep2= 0
    print(image1, image2)
    return (image1,image2, score1, score2, rep1,rep2)


st.title("Hey ! Tu préfères qui ?")


col1, col2 = st.columns(2)

with col1 :
    col1.subheader("Image 1")
    # picture = st.camera_input("Take a picture")

    # if picture:
    #     st.image(picture)
    # st.write(score1)
    # st.write("rep",rep1)
    if st.button("This", 'click1'):
        image1, image2, score1 , score2, rep1,rep2= get_image(image1, image2, score1 , score2, rep1,rep2,win =1)
    st.image(image1)
    


with col2:
    col2.subheader("Image 2")
    # st.write(score2)
    # st.write('rep',rep2)
    if st.button("This", 'click2'):
        image1, image2,score1, score2,rep1,rep2 = get_image(image1, image2, score1 , score2, rep1,rep2,win =2)
    st.image(image2)



