import socket
import select
import sys
from _thread import *
import os

def valid_username(recipent):
	if(len(recipent) < 2):
		return False
	if(recipent[0] != '@'):
		return False
	return True

def parse_send_msg(data_msg):
	splitted = data_msg.split(' ', 1)
	if(len(splitted) != 2):
		return False
	recipent = splitted[0]
	data = splitted[1]
	data = data[:-1]
	if(valid_username(recipent) == False):
		return False
	recipent = recipent[1:]
	content_length = len(data)
	send_msg = 'SEND ' + recipent + '\nContent-length: ' + str(content_length) + '\n\n' + data #
	return [recipent, send_msg]

def parse_recv_msg(message):
	splitted = message.split('\n', 3)
	if(len(splitted) != 4):
		return 'ERROR 103'
	if(splitted[0][:7] != 'FORWARD'):
		return 'ERROR 103'
	if(splitted[1][:15] != 'Content-length:'):
		return 'ERROR 103'
	if(splitted[2] != ''):
		return 'ERROR 103'
	sender = splitted[0][8:]
	try:
		content_length = int(splitted[1][16:])
	except:
		return 'ERROR 103'
	data = splitted[3]
	if(content_length != len(data)):
		return 'ERROR 103'
	display_msg = data
	return [sender, display_msg]

def get_recv_ack(send_socket, recipent):
	ack_expected = 'SEND ' + recipent + '\n\n'
	error1_expected = 'ERROR 103 Header Incomplete\n\n'
	error2_expected = 'ERROR 102 Unable to send\n\n'
	while True:
		try:
			ack_msg = send_socket.recv(2048)
			if ack_msg:
				ack_msg = ack_msg.decode()
				if(ack_msg == ack_expected):
					return True
				elif(ack_msg == error1_expected):
					return 'ERROR 103'
				elif(ack_msg == error2_expected):
					return 'ERROR 102'
		except:
			continue

def recieve_thread(recieve_socket, username):

	# After acknowledgement is recieved, then wait for message from server
	while True:
		try:
			msg = recieve_socket.recv(2048)
			if msg:
				display = parse_recv_msg(msg.decode())
				if(display == 'ERROR 103'):
					# print('here')
					recieve_socket.send('ERROR 103 Header Incomplete\n\n'.encode())
				else:
					print ("Message from " + display[0] + ": " + display[1])
					ack_msg = 'RECEIVED ' + display[0] + '\n\n'
					recieve_socket.send(ack_msg.encode())
		except:
			continue

def send_thread(send_socket, username):

	# After acknowledgement, wait for client to enter input
	while True:
		try:
			data_msg = sys.stdin.readline()
			if data_msg:
				send_msg = parse_send_msg(data_msg)
				if(send_msg == False):
					print('---Invalid message, Type Again; Correct Format: @[recipient name] [message]')
				else:
					send_socket.send(send_msg[1].encode())
					# print('hi')
					recv_ack = get_recv_ack(send_socket, send_msg[0])
					if(recv_ack == True):
						print('---Successfully delivered message to ' + send_msg[0])
					elif(recv_ack == 'ERROR 102'):
						print('---ERROR 102: Unable to send message to ' + send_msg[0])
					else:
						print('---ERROR 103: Unable to send message to ' + send_msg[0])
						print('Disconnected From server')
						os._exit(1)
		except:
			continue


send_socket = socket.socket()
recieve_socket = socket.socket()
IP_address = str(input("Enter IP Address: "))
Port = int(15000)
recieve_socket.connect((IP_address, Port))
send_socket.connect((IP_address, Port))
username = str(input("Enter User Name: "))

# Registering to Recieve message from server
reg_msg = 'REGISTER TORECV ' + username + '\n\n'
ack_expected = 'REGISTERED TORECV ' + username + '\n\n'
error_100 = 'ERROR 100 Malformed username\n\n'
error_101 = 'ERROR 101 No user registered\n\n'
recieve_socket.send(reg_msg.encode())
ack = False

# Waiting For Acknowledgement from Server
# If recieved message is not correct acknowledgement, client is disconnected
while(ack == False):
	try:
		message = recieve_socket.recv(2048)
		if message:
			ack_msg = message.decode()
			if(ack_msg == ack_expected):
				print('---Successfully registered to Revieve messages!')
				ack = True
			elif(ack_msg == error_100):
				username = str(input("ERROR 100: Invalid Username\nEnter New User Name: "))
				reg_msg = 'REGISTER TORECV ' + username + '\n\n'
				recieve_socket.send(reg_msg.encode())
				ack_expected = 'REGISTERED TORECV ' + username + '\n\n'
			elif(ack_msg == error_101):
				print('ERROR 101: No User Registered')
				reg_msg = 'REGISTER TORECV ' + username + '\n\n'
				recieve_socket.send(reg_msg.encode())

	except:
		continue

# Registering to send messages to server
reg_msg = 'REGISTER TOSEND ' + username + '\n\n'
send_socket.send(reg_msg.encode())
ack_expected = 'REGISTERED TOSEND ' + username + '\n\n'
ack = False

# Waiting For Acknowledgement from Server
# If recieved message is not correct acknowledgement, client is disconnected
while(ack == False):
	try:
		message = send_socket.recv(2048)
		if message:
			ack_msg = message.decode()
			if(ack_msg == ack_expected):
				print('---Successfully registered to Send messages!')
				ack = True
			elif(ack_msg == error_100):
				username = str(input("ERROR 100: Invalid Username\nEnter New User Name: "))
				reg_msg = 'REGISTER TOSEND ' + username + '\n\n'
				send_socket.send(reg_msg.encode())
				ack_expected = 'REGISTERED TOSEND ' + username + '\n\n'
			elif(ack_msg == error_101):
				print('ERROR 101: No User Registered')
				reg_msg = 'REGISTER TOSEND ' + username + '\n\n'
				send_socket.send(reg_msg.encode())
	except:
		continue

start_new_thread(recieve_thread,(recieve_socket,username))	
start_new_thread(send_thread,(send_socket,username))

while True:
		continue
