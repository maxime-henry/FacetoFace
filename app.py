from cmath import nan
import streamlit as st
from pymongo import MongoClient
import pandas as pd
import random 

rand = random.randint(1,2)



st.set_page_config(
     page_title="Face to face",
     page_icon="🧊",
     layout="wide",
     initial_sidebar_state="expanded"
 )

user = st.secrets.db_connection.user
pwd = st.secrets.db_connection.password
host = "cluster0.vdgze"
databaseName = "Faces"


CONNECTION_STRING = f"mongodb+srv://{user}:{pwd}@{host}.mongodb.net/{databaseName}"

client = MongoClient(CONNECTION_STRING)

mydb = client["Faces"]
mycol = mydb["BSAface"]


st.cache()
def images():
    mydoc =list(mycol.find().sort('rep').limit(4))
    data = pd.DataFrame(mydoc)
    image1 = data.iloc[0][1]

    

    score1= data.iloc[0]['note']

 
    rep1= data.iloc[0]['rep']

    image2 = data.iloc[rand][1]
    score2= data.iloc[rand]['note']

    rep2= data.iloc[rand]['rep']


    return (image1,image2, score1, score2, rep1,rep2)

st.cache()
def get_results():
    mydoc =list(mycol.find())
    data = pd.DataFrame(mydoc)
    data.sort_values(by ='note', inplace=True, ascending=False)
    return(data)




#########################################

st.cache()
def scoring(image1,image2, score1, score2, rep1,rep2, win):
    if win ==1 :
        #Faire le calcul des points
        expected1 = 1/(1+    pow(10,((int(score2)-int(score1))/400) ))
        newscore1 = int(score1) + 32*(1-expected1)
        expected2 = 1/(1+    pow(10,((int(score1)-int(score2))/400) ))
        newscore2 = int(score2) + 32*(0-expected2)

#########################################################################
    if win ==2:
        #Faire le calcul des points
        expected1 = 1/(1+    pow(10,((int(score2)-int(score1))/400) ))
        newscore1 = int(score1) + 10*(0-expected1)
        expected2 = 1/(1+    pow(10,((int(score1)-int(score2))/400) ))
        newscore2 = int(score2) + 10*(1-expected2)

    print(expected1,expected2,newscore1,newscore2)
    newrep1 = rep1 + 1
    newrep2 = rep2 +1
    # Enregistrer les données 
    print(newscore2, image2)
    mycol.update_one({"X1":image1}, {"$set":{'note':newscore1,'rep':int(newrep1)}})
    mycol.update_one({"X1":image2}, {"$set":{'note':newscore2,'rep':int(newrep2)}})
    print("Updated" , image1, "with ", newscore1)
    return ()



image1, image2, score1 , score2, rep1,rep2 = images()

# Create a page dropdown 
page = st.sidebar.selectbox("Tu veux faire quoi ?", ["Je classe", "Je juge"]) 

if page == "Je classe":

    st.title("Hey ! Tu préfères qui ?")
    col1, col2 = st.columns(2)

    with col1 :
        col1.subheader("Image 1")

        if st.button("This", 'click1'):
            scoring(image1, image2, score1 , score2, rep1,rep2,win =1)
  
        st.image(image1)
        


    with col2:
        col2.subheader("Image 2")

        if st.button("This", 'click2'):
            scoring(image1, image2, score1 , score2, rep1,rep2,win =2)
        print(image1, image2)

        st.image(image2)

if  page == "Je juge":


    data = get_results()



    # st.table(data[['X1','note']]) 
    st.title("Les gagnants")
    col1, col2, col3 = st.columns(3)



    with col1:
        st.header("Deuxième")
        st.header("")
        st.image(data.iloc[1][1])

    with col2:
        st.header("Premier")
        st.image(data.iloc[0][1])
        

    with col3:
        st.header("Troisième")
        st.header("")
        st.header("")
        st.image(data.iloc[2][1])

    st.title("Les nullos")

    # data = data.sort_values(by ='note', inplace=True, ascending=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Deuxième nullos")
        st.header("")
        st.image(data.iloc[-2][1])

    with col2:
        st.header("Premier nullos")
        st.image(data.iloc[-1][1])
        

    with col3:
        st.header("Troisième nullos")
        st.header("")
        st.header("")
        st.image(data.iloc[-3][1])


