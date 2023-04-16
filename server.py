from flask import Flask, render_template, request
from Object2Image import ObjectAndImage
app = Flask(__name__)

@app.route('/', methods =["GET", "POST"])
def object2Image():
   imageName = 'webTest'
   if request.method == "POST":
      inputString = request.form.get("inputString")
      ObjectAndImage.objectToImage(inputString, imageName)
      return render_template("img.html", user_image = f'../static/{imageName}.png' )
      #return render_template("img.html", user_image = f'D:/VSStudio/WebImage/static/{imageName}' )

   return render_template("index.html")

@app.route('/upload', methods =["GET", "POST"])
def image2Object():
   if request.method == "POST" and request.files:
      return ObjectAndImage.imageToObjectWeb(request.files["inputImageName"].read())
      #img = cv2.imdecode(numpy.fromstring(request.files['file'].read(), numpy.uint8), cv2.IMREAD_UNCHANGED)
      
      object = ObjectAndImage.imageToObject(inputImage)
      return 'the object is' + object
      return render_template("img.html", user_image = f'../static/{imageName}.png' )
      #return render_template("img.html", user_image = f'D:/VSStudio/WebImage/static/{imageName}' )

   return render_template("index.html")


if __name__ == '__main__':
   app.run()