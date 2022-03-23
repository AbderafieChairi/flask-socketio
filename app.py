from flask import Flask 
from flask_socketio import SocketIO, send,join_room, leave_room,emit
from models import db,User,Room,Message,Participants
from flask_cors import CORS

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

app = Flask(__name__)
db.init_app(app)
app.config['SECRET_KEY'] = 'mysecret'
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] ="postgres://dmajucpgzfjpef:ed7e7cd83bb95527cb30d83b3bfcebcb749e5fc2effea616b1860311a4adbf6a@ec2-54-73-178-126.eu-west-1.compute.amazonaws.com:5432/dat8693bl607v1"
# app.config['SQLALCHEMY_DATABASE_URI'] ="sqlite:///test.db"
socketio = SocketIO(app, cors_allowed_origins='*')
admin = Admin(app)
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Room, db.session))
admin.add_view(ModelView(Message, db.session))
admin.add_view(ModelView(Participants, db.session))

@socketio.on('message')
def handleMessage(data):
	new_msg = Message(
			user_id=data['user_id'], 
			room_id=data['room_id'], 
			msg=data['msg']
		    )
	Us = [i.user_id for i in Participants.query.filter_by(room_id=data['user_id']).all()]
	print(Us)
	db.session.add(new_msg)
	db.session.commit()
	send({"user1":Us[0],"user2":Us[1]},broadcast=True)

# @socketio.on('message')
# def on_joinoooo(msg):
# 	send(msg,broadcast=True)

# @socketio.on('join')#, namespace='/private')
# def on_join(data):
# 	user = data['username']
# 	print('join room1')
# 	room=data['room']
# 	join_room(room)
# 	send(f'{user} has entered the {room}',room=room)

# @socketio.on('private_message')#, namespace='/private')
# def private_message(payload):
# 	user = payload['username']
# 	message = payload['message']
# 	room=payload['room']

# 	send(f"{room} |{user} :{message} ." ,room=room)


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
	
