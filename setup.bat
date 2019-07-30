pip install ./dlib-19.7.0-cp36-cp36m-win_amd64.whl
pip install ./numpy-1.17.0-cp36-cp36m-win_amd64.whl
pip install ./Click-7.0-py2.py3-none-any.whl
pip install ./Pillow-6.1.0-cp36-cp36m-win_amd64.whl
python extract_models.py
cd face_recognition_models-0.3.0
python setup.py build
python setup.py install
cd ..
rd /s /q ./face_recognition_models-0.3.0
pip install ./face_recognition-1.2.3-py2.py3-none-any.whl
pip install ./opencv_python-4.1.0.25-cp36-cp36m-win_amd64.whl
pip install face-recognition
pip install opencv-python
