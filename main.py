from colorthief import ColorThief
import os
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from colormap import rgb2hex

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads/'

app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            image = UPLOAD_FOLDER+filename
            palette = colour_pallete(image)
            return render_template('index.html', filename=filename, colours = palette)
        else:
            flash('Allowed file types are png, gif and jpg')
            return redirect(request.url)

@app.route('/display/<filename>')
def display_image(filename):
    #print('display_image filename: ' + filename)
    return redirect(url_for('static', filename='uploads/' + filename), code=301)

def colour_pallete(image):
    color_thief = ColorThief(image)
    # get the dominant color
    dominant_color = color_thief.get_color(quality=1)
    # build a color palette
    palette_rgb = color_thief.get_palette(color_count=6)
    # convert rgb to hex
    palette_hex = [rgb2hex(color[0],color[1],color[2]) for color in palette_rgb]
    return palette_hex


if __name__ == '__main__':
      app.run(host='0.0.0.0', port=80, debug=True)