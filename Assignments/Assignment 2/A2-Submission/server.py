import socket
import select
import sys
from _thread import *

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

IP_address = '127.0.0.1'
Port = 15000
server.bind((IP_address, Port))
server.listen(100)
user_data = {}

# Checks whether username is valid or not
def valid_username(username):
	if(username.isalnum() and username != 'ALL'):
		return True
	return False

# Parses Registration message
def parse_reg_msg(msg):
	msg = msg.split('\n')
	if(len(msg) != 3 or msg[-1] != '' or msg[-2] != ''):
		return []
	msg = msg[:-2] 
	ans = [msg[0][:15], msg[0][16:]] # Checking length of msg[0]
	if(valid_username(ans[1]) == False):
		return [-1]
	return ans

def parse_recv_msg(msg, username):
	msg = msg.split('\n', 3)
	if(len(msg) != 4):
		return 'ERROR 103'
	line_1 = msg[0].split(' ')
	if(line_1[0] != 'SEND'):
		return 'ERROR 103'
	line_2 = msg[1].split(' ')
	if(line_2[0] != 'Content-length:'):
		return 'ERROR 103'
	if(msg[2] != ''):
		return 'ERROR 103'
	frwd_user = line_1[1]
	try:
		content_length = int(line_2[1])
	except:
		return 'ERROR 103'

	data = msg[3]
	if(content_length != len(data)):
		return 'ERROR 103'
	elif(frwd_user not in user_data and frwd_user != 'ALL'):
		return 'ERROR 102'
	frwd_msg = 'FORWARD ' + username + '\nContent-length: ' + str(content_length) + '\n\n' + data
	return [frwd_user, frwd_msg]

def get_recv_ack(username, conn):
	ack_expected = 'RECEIVED ' + username + '\n\n'
	error_expected = 'ERROR 103 Header Incomplete\n\n'
	while True:
		try:
			ack_msg = conn.recv(2048)
			if ack_msg:
				ack_msg = ack_msg.decode()
				if(ack_msg == ack_expected):
					return True
				elif(ack_msg == error_expected):
					return False
		except:
			continue

def client_thread(conn, addr):

	# Waiting from registration of client
	ack = False
	username = ''
	while(ack == False):
		try:
			reg_msg = conn.recv(2048)
			if reg_msg:
				reg_msg = reg_msg.decode()
				reg_msg = parse_reg_msg(reg_msg)
				# If reg msg is not proper, send error 101
				if(reg_msg == []):
					conn.send('ERROR 101 No user registered\n\n'.encode())

				# If username is Invalid, send error 100
				elif(reg_msg == [-1]):
					conn.send('ERROR 100 Malformed username\n\n'.encode())

				# If reg msg is to recieve, add it to database, close thread
				elif(reg_msg[0] == 'REGISTER TORECV'):
					user_data[reg_msg[1]] = conn
					print('NEW USER: ' + reg_msg[1])
					recieve_ack = 'REGISTERED TORECV ' + reg_msg[1] + '\n\n'
					conn.send(recieve_ack.encode())
					ack = True
					return

				# If reg msg is to send, send ack
				elif(reg_msg[0] == 'REGISTER TOSEND'):
					username = reg_msg[1]
					send_ack = 'REGISTERED TOSEND ' + reg_msg[1] + '\n\n'
					conn.send(send_ack.encode())
					ack = True

				# Anything else, send error 101
				else:
					conn.send('ERROR 101 No user registered\n\n'.encode())

		except:
			continue

	# Waiting For messages from To Send Socket of Client
	while True:
			try:
				msg = conn.recv(2048)
				if msg:
					frwd_data = parse_recv_msg(msg.decode(), username)
					if(frwd_data == 'ERROR 102'):
						conn.send('ERROR 102 Unable to send\n\n'.encode())
						continue
					if(frwd_data == 'ERROR 103'):
						conn.send('ERROR 103 Header Incomplete\n\n'.encode())
						conn.close()
						user_data[username].close()
						user_data.pop(username)
						print('DISCONNECTED: ' + username)
						return

					frwd_user = frwd_data[0]
					frwd_msg = frwd_data[1]

					if(frwd_user == 'ALL'):
						sent = True
						for users in user_data:
							if users != username:
								user_data[users].send(frwd_msg.encode())
								frwd_ack = get_recv_ack(username, user_data[users])
								if(frwd_ack == False):
									sender_ack = 'ERROR 102 Unable to send\n\n'
									conn.send(sender_ack.encode())
									sent = False
									break
						if(sent):
							sender_ack = 'SEND ALL\n\n'
							conn.send(sender_ack.encode())

					else:
						frwd_conn = user_data[frwd_user]
						frwd_conn.send(frwd_msg.encode())      # Unicast
						frwd_ack = get_recv_ack(username, frwd_conn)
						if(frwd_ack == True):
							sender_ack = 'SEND '+ frwd_user + '\n\n'
							conn.send(sender_ack.encode())
						else:
							sender_ack = 'ERROR 102 Unable to send\n\n'
							conn.send(sender_ack.encode())

			except:
				continue

while True:
	conn, addr = server.accept()
	start_new_thread(client_thread,(conn,addr))	

conn.close()
server.close()
