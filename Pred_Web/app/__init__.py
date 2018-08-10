import os
from flask import Flask, request, redirect, url_for, render_template, flash, send_from_directory
from werkzeug.utils import secure_filename
import pandas as pd
import string
from nltk.corpus import stopwords
from nltk import word_tokenize
import pickle
import os

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['csv','xlsx'])

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return filename.split('.')[1] in ALLOWED_EXTENSIONS

@app.route('/')
def upload_file():
    return render_template('home.html')

@app.route('/uploader',methods=['POST','GET'])
def uploader():
    if request.method == 'POST':
        print(request.files)
        #check if post request has a file attached
        if 'file' not in request.files:
            flash('No File Found')
            return 'No file found'
        file = request.files['file']
        #if no file selected
        if file.filename == '':
            flash('No file selected')
            return 'no file selected'
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            #run the prediction
            xl = pd.ExcelFile(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            df = xl.parse('RAW ALL')
            df.columns = df.iloc[0]
            df = df.reindex(df.index.drop(0))
            #Drop unecessary columns
            df['Fault Desc_Rect'] = df['Fault Description'] + df['Fault Rectification']
            #apply word pre-processing
            df['Fault Desc_Rect'] = df['Fault Desc_Rect'].apply(lambda x: str(x).replace('\n'," "))
            table = str.maketrans({key: None for key in string.punctuation})
            df['Fault Desc_Rect'] = df['Fault Desc_Rect'].apply(lambda x: x.translate(table))
            df['Fault Desc_Rect'] = df['Fault Desc_Rect'].apply(lambda x: x.lower())
            stop_words = set(stopwords.words('english'))
            df['Fault Desc_Rect'] = df['Fault Desc_Rect'].apply(lambda x: ' '.join([w for w in word_tokenize(x) if not w in stop_words]))
            #drop rows with Rect/Desc empty
            df = df[df['Fault Desc_Rect']!='nan']
            #filter out FAULT CODE empty
            result = df[df['Fault Code'].isnull()==True]
            #show message if there are no missing fault codes in the raw file
            if result.shape[0]==0:
                return 'No missing Fault Codes'
            df = df[df['Fault Code'].isnull()==False]
            print(df.shape,result.shape)
            print('Done')
            x_predict = pd.Series(result['Fault Desc_Rect'])
            with open('models/linearSVC.pkl','rb') as input:
                SVC_pipeline = pickle.load(input)
            prediction = SVC_pipeline.predict(x_predict)
            #Saves the results into a csv file
            result['Fault Code'] = prediction
            result = result.drop(['Fault Desc_Rect'],axis=1)
            result.to_csv('results.csv')
            rows = pd.read_csv('results.csv').values.tolist()
            return render_template('results.html',rows=rows)

@app.route('/downloader')
def downloader():
    return send_from_directory('','results.csv',as_attachment=True)

@app.route('/downloader2',methods=['POST','GET'])
def downloader2():
    temp = pd.DataFrame.from_dict(request.form,orient='index').values
    data = pd.read_csv('results.csv')
    header = data.columns[1:]
    Fault_Code = []
    Component_Unit = []
    Sub_Level = []
    Type = []
    for i in range(0,temp.shape[0],4):
        print(temp[i])
        Fault_Code.append(temp[i][0])
        Component_Unit.append(temp[i+1][0])
        Type.append(temp[i+2][0])
        Sub_Level.append(temp[i+3][0])
    data['Fault Code'] = Fault_Code
    data['Component Unit'] = Component_Unit
    data['Sub Level'] = Sub_Level
    data['Type'] = Type
    data.to_csv('results.csv',index=False)
    #append the latest info to the historical results
    hist = pd.read_csv('hist_results.csv')
    hist = hist.append(data,ignore_index=True)
    hist.to_csv('hist_results.csv')
    #allow user to download the results file
    return send_from_directory('','results.csv',as_attachment=True)

if __name__=='__main__':
    app.run(debug=True)
