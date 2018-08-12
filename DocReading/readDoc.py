# -*- coding: utf-8 -*-
"""
Created on Sat Jun 23 10:15:56 2018

@author: Ken
"""
'''
Page is a collection of blocks, plus meta-information about the page: sizes, resolutions (X resolution and Y resolution may differ).

Block represents one "logical" element of the page—for example, an area covered by text, or a picture or separator between columns. The text and table blocks contain the main information needed to extract the text.

Paragraph is a structural unit of text representing an ordered sequence of words. By default, words are considered to be separated by word breaks.

Word is the smallest unit of text. It is represented as an array of Symbols.

Symbol represents a character or a punctuation mark.
'''
import argparse
from enum import Enum
import io

#pip install google-cloud
from google.cloud import vision
from google.cloud.vision import types
from PIL import Image, ImageDraw

#%%
class FeatureType(Enum):
    PAGE = 1
    BLOCK = 2
    PARA = 3
    WORD = 4
    SYMBOL = 5

def draw_boxes(image, bounds, color):
    #Draw a border around the image using the hints in the vector list
    draw = ImageDraw.Draw(image)

    for bound in bounds:
        draw.polygon([
            bound.vertices[0].x, bound.vertices[0].y,
            bound.vertices[1].x, bound.vertices[1].y,
            bound.vertices[2].x, bound.vertices[2].y,
            bound.vertices[3].x, bound.vertices[3].y], None, color)
    return image

def get_document_bounds(image_file, feature):
    #Returns document bounds given an image.
    client = vision.ImageAnnotatorClient()

    bounds = []

    with io.open(image_file, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    response = client.document_text_detection(image=image)
    document = response.full_text_annotation

    # Collect specified feature bounds by enumerating all document features
    for page in document.pages:
        for block in page.blocks:
            for paragraph in block.paragraphs:
                for word in paragraph.words:
                    for symbol in word.symbols:
                        if (feature == FeatureType.SYMBOL):
                            bounds.append(symbol.bounding_box)

                    if (feature == FeatureType.WORD):
                        bounds.append(word.bounding_box)

                if (feature == FeatureType.PARA):
                    bounds.append(paragraph.bounding_box)

            if (feature == FeatureType.BLOCK):
                bounds.append(block.bounding_box)

        if (feature == FeatureType.PAGE):
            bounds.append(block.bounding_box)

    # The list `bounds` contains the coordinates of the bounding boxes.
    return bounds

def render_doc_text(filein, fileout):
    image = Image.open(filein)
    bounds = get_document_bounds(filein, FeatureType.PAGE)
    draw_boxes(image, bounds, 'blue')
    bounds = get_document_bounds(filein, FeatureType.PARA)
    draw_boxes(image, bounds, 'red')
    bounds = get_document_bounds(filein, FeatureType.WORD)
    draw_boxes(image, bounds, 'yellow')

    if fileout is not 0:
        image.save(fileout)
    else:
        image.show()

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument(r'C:\Users\Ken\Documents\Ken\Random\20150816_121309.jpg', help='The image for text detection.')
    parser.add_argument(r'-C:\Users\Ken\Documents\Ken\Random\testing.jpg', help='Optional output file', default=0)
    args = parser.parse_args()

    parser = argparse.ArgumentParser()
    
    render_doc_text(r'C:\Users\Ken\Documents\Ken\Random\20150816_121309.jpg', r'C:\Users\Ken\Documents\Ken\Random\testing.jpg')
    
#%%
key = 'AIzaSyCAB76WKrDESogX-JRbv4loMF-OsvIhta4'

{
  "requests": [
    {
       #stored locally
        "content":"/9j/7QBEUGhvdG9...image contents...eYxxxzj/Coa6Bax//Z"
            #can be a google cloud storage file location
        "source":{
          "imageUri":
            "gs://bucket_name/path_to_image_object"
      },
      "features": [
        {
          "type": "TEXT_DETECTION"
        }
      ]
    }
  ]
}
      
'C:\Users\Ken\Documents\Ken\Random\20150816_121309.jpg'
'C:\Users\Ken\Documents\Ken\WorkingFiles\DocReading\TestFolder\0611701E18A.pdf'
'C:\Users\Ken\Documents\Ken\WorkingFiles\DocReading\temp\temp-0.jpg'
#%%
import os

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
            print(block_text)
            #print('Block Bounds: {}'.format(block.bounding_box))
#%%
from wand.image import Image
# Converting first page into JPG
#need to install GhostScript, ImageMagick
os.chdir(r'C:/Users/Ken/Documents/Ken/WorkingFiles/DocReading')
with Image(filename="C:/Users/Ken/Documents/Ken/WorkingFiles/DocReading/0611701E18A.pdf",resolution=300) as img:
     img.save(filename="temp.jpg")
# Resizing this image
with Image(filename="temp.jpg") as img:
     #img.resize(200, 150)
     img.save(filename="thumbnail_resize.jpg")
#%%
from tika import parser

raw = parser.from_file('0611701E18A.pdf')
print(raw['content'])
#%% FOR PDF
from PIL import Image as Img
from wand.image import Image
import uuid
import numpy as np
import glob
import os
import sys

def detect_document(path):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r'C:\Users\Ken\Documents\Ken\WorkingFiles\DocReading\readDoc_apikey.json'
    #credentials = 'AIzaSyCk1qxd616poOgdwJcJq473GVTurYotUW8'
    client = vision.ImageAnnotatorClient()
    
    with io.open(path,'rb') as image_file:
        content = image_file.read()
    
    mime_type = 'application/pdf'
    feature = vision.types.Feature(type=vision.enums.Feature.Type.DOCUMENT_TEXT_DETECTION)
    input_config = vision.types.InputConfig(gcs_source=gcs_source, mime_type=mime_type)
    image = types.Image(content=content,mime_type=mime_type)
    
    async_request = vision.types.AsyncAnnotateFileRequest(
        features=[feature], input_config=input_config,
        output_config=output_config)

    operation = client.async_batch_annotate_files(
        requests=[async_request])
    
    response = client.document_text_detection(image=image)
    document = response.full_text_annotation
    
    for page in document.pages:
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
            
            print('Block Content: {}'.format(block_text))
            #print('Block Bounds: {}'.format(block.bounding_box))


def convert_pdf(filepdf):
    temp_name = 'temp_' + filepdf
    try:
        with Image(filename=filepdf,resolution=200) as img:
            img.compression_quality = 80
            img.save(filename='temp/'+ temp_name)
    except Exception:
        return 'failed first step'
    else:
        pathsave=[]
        try:
            list_im = glob.glob(r'C:\Users\Ken\Documents\Ken\WorkingFiles\DocReading\temp')
            list_im.sort()
            imgs = [Img.open(i) for i in list_m]
            min_shape = sorted([(np.sum(i.size),i.size) for i in imgs])[0][1]
            imgs_comb = np.vstack((np.asarray(i.resize(min_shape)) for i in imgs))
            imgs_comb = Img.fromarray(imgs_comb)
            pathsave = "test.jpg"
            imgs_comb.save(pathsave)
        except Exception:
            return False
        return pathsave