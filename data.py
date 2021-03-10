from pymongo import MongoClient
import  os
import pandas as pd
from flask import send_from_directory,Flask
from decouple import config
from flask_pymongo import PyMongo

app=Flask(__name__)

app.config["MONGO_URI"]=config("MONGO_URI")
mongo=PyMongo(app)
doc=mongo.db.MLG


mlglist = list(doc.find({'Topic': { '$exists': 'true' } },{'Topic':1})) #list(doc.find({'movie': { '$exists': 'true' } },{'.':1,'_id':0}))

mlglist  = [i['Topic'] for i in mlglist]
mlglist = list( set( mlglist ) )
size = len(mlglist)


def page(pg , index):
    
    if pg == 'next':
        if size-1 > index:
            return mlglist[index+1]
        elif size-1 == index:
            return mlglist[0]
    elif pg == 'pre':
        if index == 0 :
            return mlglist[size-1]
        else:
            return mlglist[index-1]

def write(**kwargs):
    app.config["MONGO_URI"]=config("MONGO_URI")
    mongo=PyMongo(app)
    doc=mongo.db.MLG
    doc.update({'Topic':kwargs['topic']},{ '$set':{'content':kwargs['content'],'tags':kwargs['tags'],'levels':kwargs['levels']} })
    
    
    
def get_csv(a):
       
    app.config["MONGO_URI"]=config("MONGO_URI")
    mongo=PyMongo(app)
    doc=mongo.db.MLG
    df = list(doc.find({}))
    df = pd.DataFrame(df)
    
    df = df.to_csv('Ml_Glossary.csv',index=False)
    path = os.path.abspath('Ml_Glossary.csv')
    print(path)
    client.close()
   
    #path = path[:-8] or path.replace('data.csv','')
    path = path.replace('Ml_Glossary.csv','')
    a.config["CLIENT_CSV"] = path
    return(send_from_directory(a.config["CLIENT_CSV"],filename='Ml_Glossary.csv',as_attachment=True) )

def writes(resp):
    app.config["MONGO_URI"]=config("MONGO_URI")
    mongo=PyMongo(app)
    doc=mongo.db.login
    doc.insert(resp)
    