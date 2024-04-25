from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
import hashlib
import os
from datetime import datetime

app = Flask(__name__)


db_uri = 'mysql+pymysql://takita:takita@172.21.0.2/protecter?charset=utf8'
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
db = SQLAlchemy(app)


class Item(db.Model):
    __tablename__ = 'metadata'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user = db.Column(db.Text())
    filename = db.Column(db.Text())
    hash_value = db.Column(db.Text())
    timestamp = db.Column(db.DateTime())


@app.route('/')
def list():

    message = 'Hello protecter'
    items = Item.query.all()

    return render_template('view_list.html', message = message, items = items)


@app.route('/show/<int:id>')
def show_post(id):
    item = Item.query.get(id)
    message = "ファイルの詳細"

    return render_template('view_item.html', message = message, item = item)

@app.route('/new')
def new_item():

    return render_template('new_item.html')

@app.route('/create', methods = ['POST'])
def create_item():

    new_item = Item()
    new_item.user = request.form['user']
    #new_item.filename = request.form['filename']

    file = request.files["filename"]
    new_item.filename = file.filename
    fileData = file.read()
    hash_sha3_256 = hashlib.sha3_256(fileData).hexdigest()

    new_item.hash_value = hash_sha3_256

    new_item.timestamp = datetime.now()

    db.session.add(new_item, id)
    db.session.commit()

    item = Item.query.get(new_item.id)

    message = "新規登録しました。"

    return render_template('view_item.html', message = message, item = item)

@app.route('/check/<int:id>', methods = ['POST'])
def check_item(id):


    # データベース上
    check_item = Item.query.get(id)
    original_filename = check_item.filename
    original_hash_value = check_item.hash_value

    # 監査したいファイル
    file = request.files["filename"]
    target_filename = file.filename
    fileData = file.read()
    hash_sha3_256 = hashlib.sha3_256(fileData).hexdigest()

    target_hash_value = hash_sha3_256

    if original_filename != target_filename:
        return render_template('view_message.html', message = "ファイル名が違います。")
    
    if original_hash_value != target_hash_value:
        return render_template('view_message.html', message = target_filename+"は変更されています。")
    
    return render_template('view_message.html', message = target_filename+"は変更されていません。")

@app.route('/destroy/<int:id>')
def destroy_item(id):

    destroy_item = Item.query.get(id)
    db.session.delete(destroy_item)
    db.session.commit()

    message = destroy_item.filename + "を削除しました。"

    return render_template('view_message.html', message = message)

