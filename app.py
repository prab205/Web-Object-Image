from Object2Image import ObjectAndImage
from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/', methods =["GET", "POST"])
def object2Image():
   uploadedString = request.form.get("textInput")

   if request.method == "POST" and uploadedString:
      baseString = ObjectAndImage.objectToBase64(uploadedString)
      return render_template("img.html", image_string = baseString)

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