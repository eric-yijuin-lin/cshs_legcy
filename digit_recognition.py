import os
from datetime import datetime
from flask import Flask, request, flash, redirect

UPLOAD_FOLDER = './src/imgs'
ALLOWED_EXTENSIONS = set(['jpg', 'jpeg'])
UPLOAD_PARAMETER_NAME = 'imageFile'

def get_image_filename(file):
    date_str = datetime.now().strftime('%Y%m%d%H%M%S')
    file_name, file_extension = os.path.splitext(file.filename)
    return f'{file_name}-{date_str}{file_extension}'
  
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# @app.route('/<int:year>/<int:month>/<title>')
@app.route('/')
@app.route('/hello')
def hello():
    return 'hello world'

@app.route('/img', methods=['POST'])
def upload_file():
    print('received post request')
    if not request.files:
        print('no files in request, request=', request)
        return 'no files in request, request=', 400
    if UPLOAD_PARAMETER_NAME not in request.files:
        return f'uploading file is required and the file name should be "{UPLOAD_PARAMETER_NAME}"', 400
    file = request.files[UPLOAD_PARAMETER_NAME]
    if not file:
        print('file is empty')
        return 'file is empty', 400
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file:
        filename = get_image_filename(file)
        print('saving file')
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return 'OK', 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5123)