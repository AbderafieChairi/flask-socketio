from flask import Flask 
from flask_socketio import SocketIO, send,join_room, leave_room,emit
# from models import db,User,Room,Message,Participants
from flask_cors import CORS

# from flask_admin import Admin
# from flask_admin.contrib.sqla import ModelView

app = Flask(__name__)
# db.init_app(app)
app.config['SECRET_KEY'] = 'mysecret'
CORS(app)

# app.config['SQLALCHEMY_DATABASE_URI'] ="postgresql://sqfchhvcywmegt:1e4f30c9447087c90170fe999bdbd7cdf542f57f61dbe368baaeb2e358a62329@ec2-176-34-105-15.eu-west-1.compute.amazonaws.com:5432/d3e165le2np51u"
# "sqlite:///test.db"
socketio = SocketIO(app, cors_allowed_origins='*')
# admin = Admin(app)
# admin.add_view(ModelView(User, db.session))
# admin.add_view(ModelView(Room, db.session))
# admin.add_view(ModelView(Message, db.session))
# admin.add_view(ModelView(Participants, db.session))


@socketio.on('message')
def on_joinoooo(msg):
	send(msg,broadcast=True)

@socketio.on('join')#, namespace='/private')
def on_join(data):
	user = data['username']
	print('join room1')
	room=data['room']
	join_room(room)
	send(f'{user} has entered the {room}',room=room)

@socketio.on('private_message')#, namespace='/private')
def private_message(payload):
	user = payload['username']
	message = payload['message']
	room=payload['room']

	send(f"{room} |{user} :{message} ." ,room=room)


# @socketio.on('join')
# def on_join(data):
# 	print('join handling')
# 	p1=[i.room_id for i in Participants.query.filter_by(user_id=data['sender_id']).all()]
# 	p2=[i.room_id for i in Participants.query.filter_by(user_id=data['receiver_id']).all()]
# 	room = "room :"+str([i for i in p1 if i in p2][0])
# 	username=User.query.filter_by(id=data['sender_id']).first().email
# 	join_room(room)
# 	send(username + ' has entered the room.', broadcast=True, room=room)

# @socketio.on('leave')
# def on_leave(data):
# 	print('leave handling')
# 	p1=[i.room_id for i in Participants.query.filter_by(user_id=data['sender_id']).all()]
# 	p2=[i.room_id for i in Participants.query.filter_by(user_id=data['receiver_id']).all()]
# 	room = "room :"+str([i for i in p1 if i in p2][0])
# 	username=User.query.filter_by(id=data['sender_id']).first().email
# 	leave_room(room)
# 	send(username + ' has leaved the room.', broadcast=True, room=room)

# @socketio.on('leave')
# def on_leave(data):
# 	room=Room.query.filter_by(sender_id=data['sender_id'],receiver_id=data['receiver_id']).first().id
# 	if not room:
# 		room=Room.query.filter_by(sender_id=data['receiver_id'],receiver_id=data['sender_id']).first().id
# 	username=User.query.filter_by(id=data['sender_id']).first().email
# 	leave_room(room)
# 	send(username + ' has left the room.', to=room)

# @socketio.on('private_message')
# def on_private_message(data):
# 	p1=[i.room_id for i in Participants.query.filter_by(user_id=data['sender_id']).all()]
# 	p2=[i.room_id for i in Participants.query.filter_by(user_id=data['receiver_id']).all()]
# 	room = [i for i in p1 if i in p2][0]
# 	R=Room.query.filter_by(id=room).first()
# 	user=User.query.filter_by(id=data['sender_id']).first()
# 	message = data["message"]
# 	room = "room :"+str(room)
# 	R.msgs.append(Message(room_id=room,user_id=user.id,msg=message))
# 	db.session.commit()
# 	# send(username.email + ': '+message, to=room)
# 	send(user.email + ': '+message, broadcast=True, room=room)


# @socketio.on('Alert')
# def handleMessage(msg):
# 	print('Message: ' + msg)
# 	send(msg, broadcast=True)

# @socketio.on('message')
# def handleMessage(msg):
# 	print('Message: ' + msg)
# 	send(msg, broadcast=True)

if __name__ == '__main__':
	socketio.run(app,debug=True)


# web: gunicorn -k geventwebsocket.gunicorn.workers.GeventWebSocketWorker -w 1 app:app
	
