# -*- coding: utf-8 -*-
"""
Created on Mon Jun 25 22:17:31 2018

@author: Ken
"""
import io
import os
import glob
import re
#pip install google-cloud
from google.cloud import vision
from google.cloud.vision import types
from wand.image import Image
from datetime import datetime
import shutil

os.chdir(r'C:/Users/Ken/Documents/Ken/WorkingFiles/DocReading')

def detect_document(path):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r'C:\Users\Ken\Documents\Ken\WorkingFiles\DocReading\readDoc_apikey.json'
    #credentials = 'AIzaSyCk1qxd616poOgdwJcJq473GVTurYotUW8'
    client = vision.ImageAnnotatorClient()
    
    with io.open(path,'rb') as image_file:
        content = image_file.read()
    
    image = types.Image(content=content)
    
    response = client.document_text_detection(image=image)
    document = response.full_text_annotation
    
    for page in document.pages:
        whole_doc = []
        for block in page.blocks:
            block_words = []
            for paragraph in block.paragraphs:
                block_words.extend(paragraph.words)
                
            block_symbols = []
            for word in block_words:
                block_symbols.extend(word.symbols)
                
            block_text = ''
            for symbol in block_symbols:
                block_text = block_text + symbol.text
            
            #print('Block Content: {}'.format(block_text))
            whole_doc.append(block_text)
            #print('Block Bounds: {}'.format(block.bounding_box))
        whole_doc = ''.join(str(x) for x in whole_doc)
        return(whole_doc)

#converts each page in pdf to a jpg file
def convert_image(path):
    #need to install GhostScript, ImageMagick
    #check if temp folder exists, if yes, delete all inside, if no create it
    time_start = datetime.now()
    total_time = datetime(2018,1,1)
    if os.path.exists(os.path.join(os.path.dirname(path),'temp')):
        shutil.rmtree(os.path.join(os.path.dirname(path),'temp'))
    os.mkdir(os.path.join(os.path.dirname(path),'temp'))
    print('dir created!')
    with Image(filename=path,resolution=300) as img:
         img.save(filename=os.path.join(os.path.dirname(path),'temp','temp.jpg'))
    time_end = datetime.now()
    total_time += (time_end-time_start)
    print('total time:',total_time)
    #total time: 2018-01-01 00:00:40.268347
    # Resizing this image
    #with Image(filename="temp.jpg") as img:
         #img.resize(200, 150)
         #img.save(filename="/tempthumbnail_resize.jpg")
      
#sends jpg file to google OCR for conversion
def get_all_pages(path):
    os.chdir(path)
    files = glob.glob('temp*.jpg')
    #create empty string
    contents = ''
    #time the process
    total_time = datetime(2018,1,1)
    for file in files:
        time_start = datetime.now()
        if not detect_document(file)==None:
            contents += str(detect_document(file))
        time_end = datetime.now()
        print('file',file,'time taken:',time_end-time_start)
        total_time += (time_end-time_start)
    print('total time:',total_time)
    os.chdir(os.path.dirname(path))
    shutil.rmtree(path)
    return contents

#runs process for all pdf files in a folder
def convert_folder(path):
    os.chdir(path)
    pdf_files = glob.glob('*.pdf')
    doc_data = []
    for pdf_file in pdf_files:
        #convert each pdf to jpg
        convert_image(pdf_file)
        #convert each jpg to text
        text = get_all_pages(path+'/temp')
        #adds file and text to final list
        doc_data.append([pdf_file,text])
    return doc_data

def find_cont(text):
    pattern = re.compile('[A-Z]{4}[0-9]{7}')
    return pattern.search(text)[0]

def find_shipped(text):
    shipped = re.compile('Shippedon:.{11}')
    return shipped.search(text)[0][-11:]

def find_health(text):
    #to get all the health certificates
    health = re.compile('Natureofcuts:.*?Shippingmark:')
    #to get the individual health certificate
    info = re.compile('Natureofcuts:(.*)Typeofpackaging:CARTONSNumberofcutsorpackages:(.*)Netweight:(.*)Dateorperiodofproduction:(.*)Productbrand:(.*)Shippingmark:')
    health = health.findall(text)
    compiled = [info.findall(x) for x in health]
    return compiled

def run(folder_path):
    doc_data = convert_folder(folder_path)
    data = [] #container to store 1.doc_data 2.container num 3.shippedon 4.Healthcert info
    keys = ['doc','data','date','container','shippedon','products']
    today = datetime.strftime(datetime.now(),'%d/%m/%y')
    for i in doc_data:
        temp = [i[0],i[1]] #stores docname, doc_data
        temp.append(today) #stores date doc inserted
        temp.append(find_cont(i[1])) #stores container num 
        temp.append(find_shipped(i[1])) #stores shippedon
        temp.append(find_health(i[1])) #stores healthcert info
        my_dict = dict(zip(keys,temp))
        data.append(my_dict)
    return data
    