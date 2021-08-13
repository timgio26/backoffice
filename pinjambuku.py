from flask import Flask,render_template,redirect,url_for,session,flash
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
from flask_wtf import FlaskForm
from wtforms import *
from wtforms.fields.html5 import *
import os

app = Flask(__name__)
basedir=os.path.abspath(os.path.dirname(__file__))
app.config['SECRET_KEY']='bumimarinaemas'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
Migrate(app,db)
bootstrap = Bootstrap(app)

class user_tbl(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    nama=db.Column(db.Text)
    email=db.Column(db.Text,unique=True)
    password=db.Column(db.String)

    def __repr__(self):
        return f"{self.id} {self.nama} {self.email}"



class Listbuku(db.Model):
    __tablename__='listbuku'
    id=db.Column(db.Integer,primary_key=True)
    judul_buku=db.Column(db.Text)
    penulis=db.Column(db.Text)
    penerbit=db.Column(db.Text)
    tahun=db.Column(db.Integer)
    id_pemilik=db.Column(db.Integer,db.ForeignKey('user_tbl.id'))
    id_peminjam=db.Column(db.Integer,db.ForeignKey('user_tbl.id'))


    pemilik=db.relationship(user_tbl,foreign_keys=[id_pemilik])
    peminjam=db.relationship(user_tbl,foreign_keys=[id_peminjam])



    def __repr__(self):
        if self.peminjam:
            return f"{self.id} {self.judul_buku} milik {self.pemilik.nama} sdh dipinjam {self.peminjam.nama}"
        else:
            return f"{self.id} {self.judul_buku} milik {self.pemilik.nama} available"
# class Peminjam(db.Model):
#     __tablename__='peminjam'
#     id=db.Column(db.Integer,primary_key=True)
#     nama=db.Column(db.Text)
#     buku_id=db.Column(db.Integer,db.ForeignKey('listbuku.id'))
#
#     def __init__(self,nama,buku_id):
#         self.nama=nama
#         self.buku_id=buku_id
#
#     def __repr__(self):
#         return f"{self.nama} meminjam {self.buku_id}"

class tambahbuku(FlaskForm):
    judul=StringField('Judul Buku:')
    penulis=StringField('Penulis Buku:')
    penerbit=StringField('Penerbit Buku:')
    tahun=IntegerField('Tahun Terbit:')
    submit=SubmitField('Tambah')

class pinjambuku(FlaskForm):
    # nama=StringField('Nama Peminjam:')
    id_buku=IntegerField('ID Buku dipinjam:')
    submit=SubmitField('Pinjam')
#
class hapusbuku(FlaskForm):
    id_buku=IntegerField('ID Buku Hapus:')
    submit=SubmitField('Hapus')

class signupform(FlaskForm):
    nama=StringField    ('Nama:     ')
    email=EmailField    ('Email:    ')
    pwd=PasswordField   ('Password: ')
    submit=SubmitField  ('Daftar')

class loginform(FlaskForm):
    email=EmailField    ('Email:    ')
    pwd=PasswordField   ('Password: ')
    submit=SubmitField  ('Masuk')

@app.route('/')
def index():
    # print(user_tbl.query.all())
    # print(Listbuku.query.all())
    print(session.get('nama_online_user',None),session.get('id_online_user',None))
    return redirect(url_for('semua'))

@app.route('/tambah',methods=['GET','POST'])
def tambah_buku():
    form=tambahbuku()
    if form.validate_on_submit():
        if session.get('id_online_user',None):
            user=user_tbl.query.get(session.get('id_online_user',None))
            print(user)
            buku=Listbuku(judul_buku=form.judul.data,penulis=form.penulis.data,penerbit=form.penerbit.data,tahun=form.tahun.data,pemilik=user)
            db.session.add(buku)
            db.session.commit()
            return redirect(url_for('semua'))
        else:
            return redirect(url_for('masuk'))
    return render_template('add.html',form=form)

# @app.route('/hapus',methods=['GET','POST'])
# def hapus_buku():
#     form=hapusbuku()
#     if form.validate_on_submit():
#         id=form.id_buku.data
#         buku=Listbuku.query.get(id)
#         if session.get('id_online_user',None)==buku.pemilik.id:
#             db.session.delete(buku)
#             db.session.commit()
#             return redirect(url_for('semua'))
#         else:
#             return render_template('delete.html',form=form,msg='hapus buku sendiri ya')
#     return render_template('delete.html',form=form)

@app.route('/hapus/<id>',methods=['GET','POST'])
def hapus_buku_2(id):

    buku=Listbuku.query.get(id)
    if session.get('id_online_user',None)==buku.pemilik.id:
        db.session.delete(buku)
        db.session.commit()

        return redirect(url_for('semua'))
    else:

        return redirect(url_for('semua'))


@app.route('/Home')
def semua():
    allbuku=Listbuku.query.filter_by(id_peminjam=None)
    return render_template('semua.html',allbuku=allbuku,msg=session.get('msg'))

@app.route('/profile')
def profile():
    bukuku=Listbuku.query.filter_by(id_pemilik=session.get('id_online_user',None))
    bukukupinjam=Listbuku.query.filter_by(id_peminjam=session.get('id_online_user',None))
    return render_template('profile.html.',bukuku=bukuku,bukukupinjam=bukukupinjam)

# @app.route('/pinjam', methods=['GET','POST'])
# def pinjam():
#     form=pinjambuku()
#     if form.validate_on_submit():
#         if session.get('id_online_user',None):
#             id=form.id_buku.data
#             buku=Listbuku.query.get(id)
#             if buku.id_pemilik==session.get('id_online_user',None):
#                 return render_template('pinjam.html',form=form,msg='pinjam punya org lain ya')
#             else:
#                 buku.id_peminjam=session.get('id_online_user',None)
#                 db.session.add(buku)
#                 db.session.commit()
#                 return redirect(url_for('semua'))
#         else:
#             return redirect(url_for('masuk'))
#
#     return render_template('pinjam.html',form=form)

@app.route('/pinjam/<id>', methods=['GET','POST'])
def pinjam_2(id):
    if session.get('id_online_user',None):
        # id=form.id_buku.data
        buku=Listbuku.query.get(id)
        if buku.id_pemilik==session.get('id_online_user',None):
            return redirect(url_for('semua'))
        else:
            buku.id_peminjam=session.get('id_online_user',None)
            db.session.add(buku)
            db.session.commit()
            return redirect(url_for('semua'))
    else:
        return redirect(url_for('masuk'))

@app.route('/kembali/<id>', methods=['GET','POST'])
def kembali(id):
    buku=Listbuku.query.get(id)
    if buku.id_peminjam==session.get('id_online_user',None):
        buku.id_peminjam=None
        db.session.add(buku)
        db.session.commit()
        return redirect(url_for('profile'))
    else:
        return redirect(url_for('profile'))



@app.route('/daftar',methods=['GET','POST'])
def daftar():
    form=signupform()
    if form.validate_on_submit():
        user_baru=user_tbl(nama=form.nama.data,email=form.email.data,password=form.pwd.data)
        db.session.add(user_baru)
        db.session.commit()
        return redirect(url_for('masuk'))
    return render_template('signup.html',form=form)

@app.route('/msk',methods=['GET','POST'])
def masuk():
    form=loginform()
    if form.validate_on_submit():
        emailmsk=form.email.data
        password=form.pwd.data
        ygmaumasuk=user_tbl.query.filter_by(email=emailmsk).first()

        if ygmaumasuk is not None:
            if ygmaumasuk.password==password:
                session['id_online_user']=ygmaumasuk.id
                session['nama_online_user']=ygmaumasuk.nama
                return redirect(url_for('index'))
            else:
                print(ygmaumasuk.password)
                return render_template('login.html',form=form,msg="email atau password salah")
        else:
            return render_template('login.html',form=form,msg="email atau password salah")
    return render_template('login.html',form=form,msg="")

@app.route('/keluar')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
