import sys
import os
import numpy as np
import copy
import cv2
import arabic_reshaper
from bidi.algorithm import get_display
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
import tensorflow as tf 
model = tf.keras.models.load_model('C:\\Users\\nengd\\OneDrive\\Documents\\Semester 6\\Prak. Sistem Multimedia\\Arabic-Sign-Language\\models\\asl_model.h5', compile=False)

def process_image(img):
    img = cv2.resize(img, (64, 64))
    img = np.array(img, dtype=np.float32)
    img = np.reshape(img, (-1, 64 , 64 , 3))
    img = img.astype('float32') / 255.
    return img

cap = cv2.VideoCapture(0)

# Get video properties
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(cap.get(cv2.CAP_PROP_FPS))

# Creates a VideoWriter object to store compressed video
output_path = 'video/compressed_videos.mp4'
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
output = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

frame_counter = 0

sequence = ''
fontFile = "C:\\Users\\nengd\\OneDrive\\Documents\\Semester 6\\Prak. Sistem Multimedia\\Arabic-Sign-Language\\fonts\\Sahel.ttf"
font_size = 70
font = ImageFont.truetype(fontFile, font_size, encoding='unic')

categories=[
["ain",'ع'],
["al","ال"],
["aleff",'أ'],
["bb",'ب'],
["dal",'د'],
["dha",'ط'],
["dhad","ض"],
["fa","ف"],
["gaaf",'جف'],
["ghain",'غ'],
["ha",'ه'],
["haa",'ه'],
["jeem",'ج'],
["kaaf",'ك'],
["la",'لا'],
["laam",'ل'],
["meem",'م'],
["nun","ن"],
["ra",'ر'],
["saad",'ص'],
["seen",'س'],
["sheen","ش"],
["ta",'ت'],
["taa",'ط'],
["thaa","ث"],
["thal","ذ"],
["toot",' ت'],
["waw",'و'],
["ya","ى"],
["yaa","ي"],
["zay",'ز']]
while True:
    ret, img = cap.read()
    img = cv2.flip(img, 1)
    
    if ret:
        x1, y1, x2, y2 = 150, 150, 500, 400
        img_cropped = img[y1:y2, x1:x2]

        image_data = cv2.imencode('.jpg', img_cropped)[1].tostring()
        
        a = cv2.waitKey(1)
        if frame_counter % 5 == 0:
            score = 0
            res = ''
            try:
                proba = model.predict(process_image(img_cropped))[0]
                mx = np.argmax(proba)

                score = proba[mx] * 100
                res = categories[mx][0]
                sequence = categories[mx][1]
            except:
                continue 

        reshaped_text = arabic_reshaper.reshape(sequence)   
        bidi_text = get_display(reshaped_text)    

        frame_counter += 1
        img_pil = Image.fromarray(img)
        draw = ImageDraw.Draw(img_pil)
        draw.text((100, 300), bidi_text, (255,255,255), font=font)
        img = np.array(img_pil)
        # cv2.putText(img, '%s' % res, (100,400), cv2.FONT_HERSHEY_SIMPLEX, 4, (255,255,255), 4)
        cv2.putText(img, '(score = %.5f)' % (float(score)), (100,450), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255))
        cv2.rectangle(img, (x1, y1), (x2, y2), (255,0,0), 2)
        cv2.imshow("img", img)

        
        if a == 27: # when `esc` is pressed
            break

# Following line should... <-- This should work fine now
cap.release()
output.release()
cv2.destroyAllWindows()