from flask import Flask, render_template, request,flash,redirect, url_for,send_from_directory,send_file
from werkzeug.utils import secure_filename
import cv2
import os
UPLOAD_FOLDER = 'E:\databases'
app = Flask(__name__)


@app.route('/')
def upload_file():
    return render_template('index.html')


@app.route('/uploader', methods=['GET', 'POST'])
def uploader_file():
    if request.method == 'POST':
        f = request.files['file']
        f.save(secure_filename(f.filename))
        img = cv2.imread(f.filename)
        greyimg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        invertimg = cv2.bitwise_not(greyimg)
        blurimg = cv2.GaussianBlur(invertimg, (7, 7), 0)
        inblurimg = cv2.bitwise_not(blurimg)
        sketchimg = cv2.divide(greyimg, inblurimg, scale=256.0)
        cv2.imwrite('s.png', sketchimg)
        #cv2.imshow('shooo','s6.png')
        #filename = secure_filename(file.filename)
        #f2.save(os.path.join(app.config['UPLOAD_FOLDER'],'s6.png' ))
        #name='s6.png'
        #flash(u'Invalid password provided', 'error')
        filename='s6.png'
        return redirect(url_for('download_file'))

@app.route("/download", methods = ['GET'])
def download_file():
    #return send_from_directory(app.config['UPLOAD_FOLDER'], name)
    return render_template('convert.html')
   # return send_file('s6.png',as_attachment=True)
@app.route('/return-files')
def return_files():
    file_path = 's.png'
    return send_file(file_path, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True,port=3001)