from flask_sqlalchemy import SQLAlchemy
db=SQLAlchemy()



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    email = db.Column(db.String(50),nullable=False,unique=True)
    particpants = db.relationship('Participants', backref='user', lazy=True)
    msgs = db.relationship('Message', backref='user', lazy=True)

    def __repr__(self):
        return 'Utilisateur %r' % self.email


class Participants(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'),nullable=False)

class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    particpants = db.relationship('Participants', backref='room', lazy=True)
    msgs = db.relationship('Message', backref='room', lazy=True)
    room=db.Column(db.Integer,nullable=False,unique=True)


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'),nullable=False)
    msg = db.Column(db.Text)
    