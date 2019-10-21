import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename

from datetime import datetime

UPLOAD_FOLDER = '/mnt/z/Developer/Flask/uploads'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:12345678@localhost/file_convert'
db = SQLAlchemy(app)


class FileConvert(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    data = db.Column(db.LargeBinary)
    date_created = db.Column(db. DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<FileConvert %r>' % self.id


@app.route("/", methods=['POST', 'GET'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file-upload']
        if file.filename == '':
            return 'No selected file'
        if file:
            filename_input = secure_filename(file.filename)

            file.save(os.path.join(
                app.config['UPLOAD_FOLDER'], filename_input))
            filename_convert = filename_input.split('.')[0] + '.pdf'
            cmd = 'unoconv -f pdf --output=' + \
                'file-convert/' + filename_convert + ' ' + 'uploads/' + filename_input
            os.system(cmd)

            file_convert = open(
                "file-convert/" + filename_convert, "r")
            if file_convert.mode == 'r':
                new_file = FileConvert(
                    name=filename_convert, data=file_convert.read())
                try:
                    db.session.add(new_file)
                    db.session.commit()
                    return 'Upload success'
                except:
                    return 'There was an issue adding to database'
            else:
                return 'There was an issue reading file convert'
    else:
        return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)
