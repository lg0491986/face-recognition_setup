#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
# 这是一个非常简单的使用Web服务上传图片运行人脸识别的案例，后端服务器会识别这张图片是不是奥巴马，并把识别结果以json键值对输出
# 比如：运行以下代码
# $ curl -XPOST -F "file=@obama2.jpg" http://127.0.0.1:5001
# 会返回：
# {
#  "face_found_in_image": true,
#  "is_picture_of_obama": true
# }
#
# 本项目基于Flask框架的案例 http://flask.pocoo.org/docs/0.12/patterns/fileuploads/

# 提示：运行本案例需要安装Flask，你可以用下面的代码安装Flask
# $ pip3 install flask
'''

import face_recognition.api as face_recognition
from flask import Flask, jsonify, request, redirect
import json
import numpy as np

# You can change this to any folder on your system
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/detection', methods=['GET', 'POST'])
def detection_image():
    # 检测图片是否上传成功
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)

        file = request.files['file']

        if file.filename == '':
            return redirect(request.url)

        if file and allowed_file(file.filename):
            # 图片上传成功，检测图片中的人脸
            return detect_faces_in_image(file)

    # 图片上传失败，输出以下html代码
    return '''
    <!doctype html>
    <title>detect the picture features</title>
    <h1>Upload a picture and output the features</h1>
    <form method="POST" enctype="multipart/form-data">
      <input type="file" name="file">
      <input type="submit" value="Upload">
    </form>
    '''


def detect_faces_in_image(file_stream):
    # 载入用户上传的图片
    img = face_recognition.load_image_file(file_stream)
    # 为用户上传的图片中的人脸编码
    face_encodings = face_recognition.face_encodings(img)

    encodings = []
    for face_encoding in face_encodings:
        encodings.append(face_encoding.tolist())
    
    face_locations = face_recognition.face_locations(img, number_of_times_to_upsample=0, model="hog")
    
    # face_landmarks = face_recognition.face_landmarks(img, face_locations=face_locations, model='large')

    # 讲识别结果以json键值对的数据结构输出
    result = {
        "encodings": encodings,
        "locations": face_locations
    }
    return jsonify(result)


@app.route('/recognition', methods=['GET', 'POST'])
def recognition_image():
    # 检测图片是否上传成功
    if request.method == 'POST':
        if 'detectfile' not in request.files \
            or 'knownfile' not in request.files:
            return redirect(request.url)

        detectfile = request.files['detectfile']
        knownfile = request.files['knownfile']

        if knownfile.filename == '' or detectfile.filename == '':
            return redirect(request.url)

        if detectfile and allowed_file(detectfile.filename) \
            and knownfile and allowed_file(knownfile.filename):
            # 图片上传成功，检测图片中的人脸
            return recognition_faces_in_image(knownfile, detectfile)

    # 图片上传失败，输出以下html代码
    return '''
    <!doctype html>
    <title>compare two picture?</title>
    <h1>Upload two picture and see if they have the same persion!</h1>
    <form method="POST" enctype="multipart/form-data">
      <input type="file" name="knownfile">
      <input type="file" name="detectfile">
      <input type="submit" value="Upload">
    </form>
    '''


def recognition_faces_in_image(knownfile_stream, detectfile_stream):
    # 载入用户上传的图片
    knownimg = face_recognition.load_image_file(knownfile_stream)
    detectimg = face_recognition.load_image_file(detectfile_stream)
    
    # 为用户上传的图片中的人脸编码
    knownface_encodings = face_recognition.face_encodings(knownimg)
    detectface_encodings = face_recognition.face_encodings(detectimg)
    
    if len(knownface_encodings) > 1:
        result = {
            "ret": 1,
            "msg": "knownface has more than one face"
        }
        return jsonify(result)
    
    if not knownface_encodings or not detectface_encodings:
        result = {
            "ret": 2,
            "msg": "knownface or detectface has no face"
        }
        return jsonify(result)
    

    checked_results = []
    for detectface_encoding in detectface_encodings:
        distances = face_recognition.face_distance(knownface_encodings, detectface_encoding)
        checked_result = list(distances <= 0.6)
        checked_results.append(distances.tolist())
        
        
    # 讲识别结果以json键值对的数据结构输出
    result = {
        "ret": 0,
        "results": checked_results
    }
    return jsonify(result)


@app.route('/compare', methods=['POST'])
def compare_image():
    data = request.get_data()
    if not data:
        result =  {
            "ret": 3,
            "msg": "format error"
        }
        return jsonify(result)
    j_data = json.loads(data)
	
    if "knownface" not in j_data or "detectface" not in j_data:
        result =  {
            "ret": 3,
            "msg": "format error"
        }
        return jsonify(result)
    
    knownface = j_data['knownface']
    detectface = j_data['detectface']
	
    return compare_faces_in_image(knownface, detectface)


def compare_faces_in_image(knownface, detectface):
    knownface_encodings = []
    detectface_encodings = []
	
    knownface_encodings.append(np.array(knownface))
    detectface_encodings.append(np.array(detectface))
    if len(knownface_encodings) > 1:
        result = {
            "ret": 1,
            "msg": "knownface has more than one face"
        }
        return jsonify(result)
    
    if not knownface_encodings or not detectface_encodings:
        result = {
            "ret": 2,
            "msg": "knownface or detectface has no face"
        }
        return jsonify(result)
    

    checked_results = []
    for detectface_encoding in detectface_encodings:
        distances = face_recognition.face_distance(knownface_encodings, detectface_encoding)
        checked_result = list(distances <= 0.6)
        checked_results.append(distances.tolist())
        
        
    # 讲识别结果以json键值对的数据结构输出
    result = {
        "ret": 0,
        "results": checked_results
    }
    return jsonify(result)


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5001, debug=True)
	