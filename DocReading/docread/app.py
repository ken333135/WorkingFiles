from flask import Flask, render_template,request
import pymongo
import pandas as pd
#must install dnspython


app = Flask(__name__)

#declarations for connecting to database
client = pymongo.MongoClient('mongodb+srv://ken_test:Password1@kentest-82ly3.gcp.mongodb.net/test?retryWrites=true')
db = client.test
#define a database called 'contdatabase'
mydb = client['contdatabase']
#define a collection called 'documents'
mycol = mydb['documents']

@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        myquery = { "container": {"$regex": "."},
                         "date": {"$regex": "."},
                    "shippedon": {"$regex": "."},
                "products.name": {"$regex": "."},
             "products.cartons": {"$regex": "."},
              "products.weight": {"$regex": "."},
            "products.pdtndate": {"$regex": "."}
                  }
        myquery['container']['$regex'] = '[a-z0-9]?'+str(request.form['container'])+'[a-z0-9]?'
        myquery['date']['$regex'] = '[.]?'+str(request.form['date'])+'[.]?'
        myquery['shippedon']['$regex'] = '[.]?'+str(request.form['shippedon'])+'[.]?'
        #query for products
        myquery['products.name']['$regex'] = '[a-z0-9]?'+str(request.form['name'])+'[a-z0-9]?'
        myquery['products.cartons']['$regex'] = '[a-z0-9]?'+str(request.form['cartons'])+'[a-z0-9]?'
        myquery['products.weight']['$regex'] = '[a-z0-9.]?'+str(request.form['weight'])+'[a-z0-9.]?'
        myquery['products.pdtndate']['$regex'] = '[.]?'+str(request.form['pdtndate'])+'[.]?'
        print(myquery)
        mydoc = mycol.find(myquery,{'_id': 0,'doc': 1,'date': 1,'container': 1,'shippedon' :1, 'products':1})
        data = [i for i in mydoc]
        print(data)
        return render_template('index2.html',data=data)
    return render_template('index2.html')

if __name__=='__main__':
    app.run(debug=True)
