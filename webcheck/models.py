from webcheck import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
	return Pengguna.query.get(int(user_id))

class Pengguna(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)
	password = db.Column(db.String(60), nullable=False)

	def __repr__(self):
		return '{} {}'.format(self.username, self.email)

class Instansi(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	nama = db.Column(db.String(200), unique=True, nullable=False)
	website = db.relationship('Web', backref='author', lazy=True)

	def __repr__(self):
		return '{}'.format(self.nama)

class Web(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	url = db.Column(db.String(200), unique=True, nullable=False)
	status = db.Column(db.Boolean, default=True, nullable=False)
	id_instansi = db.Column(db.Integer, db.ForeignKey('instansi.id'), nullable=False)

	def __repr__(self):
		return '{} {}'.format(self.url, self.id_instansi)