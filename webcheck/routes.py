from flask import render_template, url_for, flash, redirect, request, json
from webcheck import app, bcrypt, db, scheduler
from webcheck.forms import SignupForm, SigninForm, PostUrl, PostInstansi
from webcheck.models import Pengguna, Instansi, Web
from flask_login import login_user, current_user, logout_user, login_required
from flask_session import Session
import urllib.request


@app.route("/")
@app.route("/dashboard")
def dashboard():
	jumlah_instansi = db.session.query(Instansi.id).count()
	jumlah_website = db.session.query(Web.id).count()
	website_active = (Web.query.filter_by(status=True).count())
	website_down = (Web.query.filter_by(status=False).count())
	data = [website_down,website_active] 
	labels = ['Down','Active']
	print(data)
	return render_template('dashboard.html', jumlah_instansi=jumlah_instansi, jumlah_website=jumlah_website,
			data=data, website_down=website_down, website_active=website_active, labels=labels)


@app.route("/instansi")
def datainstansi():
	form = PostInstansi()
	instansi = Instansi.query.all()
	return render_template('instansi.html', ndi=instansi, title='Instansi', form=form)


@app.route("/instansi", methods=['POST'])
@login_required
def postinstansi():
	form = PostInstansi()
	if form.validate_on_submit:
		if Instansi.query.filter_by(nama=form.instansi.data).first():
			flash(f'Instansi sudah terdaftar!','danger')
			return redirect(request.referrer)
		else:
			post_instansi = Instansi(nama=form.instansi.data)
			db.session.add(post_instansi)
			db.session.commit()
			flash(f'Instansi berhasil dibuat!','success')
			return redirect(request.referrer)
	return render_template('instansi.html', title='Instansi', form=form)


@app.route("/deleteinstansi/<id_instansi>", methods=['POST'])
@login_required
def deleteinstansi(id_instansi):
	data_instansi = Instansi.query.get(id_instansi)
	db.session.delete(data_instansi)
	db.session.commit()
	flash(f'Instansi berhasil dihapus!','success')
	return redirect(request.referrer)


@app.route("/instansi/<id_inst>")
def dataweb(id_inst):
	form = PostInstansi()
	firm = PostUrl()
	instansi = Instansi.query.all()
	website = Web.query.filter_by(id_instansi=id_inst).all()
	return render_template('website.html', ndw=website, ndi=instansi, title='Instansi', form=form, firm=firm)


@app.route("/instansi/<id_inst>", methods=['POST'])
@login_required
def postwebsite(id_inst):
	form = PostInstansi()
	firm = PostUrl()
	if form.validate_on_submit:
		if Web.query.filter_by(url=firm.url.data).first():
			flash(f'Website sudah terdaftar!','danger')
			return redirect(request.referrer)
		else:
			post_web = Web(url=firm.url.data, id_instansi=id_inst)
			db.session.add(post_web)
			db.session.commit()
			flash(f'Website berhasil dibuat!','success')
			return redirect(request.referrer)
	return render_template('website.html', title='Instansi', form=form, firm=firm)


@app.route("/deleteweb/<id_web>", methods=['POST'])
@login_required
def deletewebsite(id_web):
	data_web = Web.query.get(id_web)
	db.session.delete(data_web)
	db.session.commit()
	flash(f'URL berhasil dihapus!','success')
	return redirect(request.referrer)


@app.route("/register", methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('dashboard'))
	form = SignupForm()
	token = 'donpablo'
	if form.validate_on_submit():
		if Pengguna.query.filter_by(username=form.username.data).first():
			flash(f'Username sudah dipakai. Coba yang lain!','danger')
			return redirect(url_for('register'))
		elif Pengguna.query.filter_by(email=form.email.data).first():
			flash(f'Email sudah dipakai. Coba yang lain!','danger')
			return redirect(url_for('register'))
		elif token != form.token.data:
			flash(f'Token yang anda masukan salah!','danger')
			return redirect(request.referrer)
		else:
			hash_pass = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
			user = Pengguna(username=form.username.data, email=form.email.data, password=hash_pass)
			db.session.add(user)
			db.session.commit()
			flash(f'Akun anda berhasil dibuat. Silakan login!', 'success')
			return redirect(url_for('login'))
	return render_template('signup.html', title='Sign Up', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = SigninForm()
	if form.validate_on_submit():
		user = Pengguna.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember=form.remember.data)
			return redirect(url_for('dashboard'))
		else:
			flash('Login tidak berhasil. Silakan cek email dan username!', 'danger')
	return render_template('signin.html', title='Sign In', form=form)


@app.route("/logout")
def logout():
	logout_user()
	return redirect(url_for('dashboard'))

def getallurl():
	for url, id in db.session.query(Web.url, Web.id):
		try:
			isActive = urllib.request.urlopen(url).getcode()
			Web.query.filter_by(id=id).update({Web.status:True})
			db.session.commit()
		except:
			Web.query.filter_by(id=id).update({Web.status:False})
			db.session.commit()
	return (print("success"))

scheduler.add_job(func=getallurl, trigger="interval", seconds=60)
scheduler.start()