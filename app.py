import os
import cv2
from Object2Image import ObjectAndImage
from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/', methods =["GET", "POST"])
def object2Image():
   imageName = 'OTI'
   uploadedString = request.form.get("textInput")

   if request.method == "POST" and uploadedString:
      ObjectAndImage.objectToImage(uploadedString, imageName)
      imageStoreString = os.path.join(os.getcwd(), f'static/{imageName}.png')
      return render_template("img.html", user_image = imageStoreString)

   return render_template("index.html")

@app.route('/upload', methods =["GET", "POST"])
def image2Object():
   uploadedFile = request.files["inputImageName"]
   
   if request.method == "POST" and uploadedFile.filename != '':
      user_obj = ObjectAndImage.imageToObjectWeb(uploadedFile.read())
      return render_template("obj.html", user_output = user_obj )
   
   return render_template("index.html")


if __name__ == '__main__':
   app.run()