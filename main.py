from flask import Flask, request, render_template
import os
import uuid
import json
from coco import *
app = Flask(__name__)

@app.route('/upload_img', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        extension = os.path.splitext(file.filename)[1]
        f_name = str(uuid.uuid4()) + extension
        file.save(os.path.join("", f_name))
        translate(f_name)
        return json.dumps(translate(f_name))

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5001)