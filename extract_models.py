import tarfile
tar = tarfile.open("./face_recognition_models-0.3.0.tar.gz")
names = tar.getnames()
for name in names:
  tar.extract(name,path="./")
tar.close()