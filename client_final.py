from tkinter import *
import socket
import threading

HEADER = 1024
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


class PROG:
	''' so all functions are related '''
	def __init__(self):
		
		#creating chatroom window and hiding it for now
		self.root = Tk()
		self.root.withdraw()

		#Creating login window in Tkinter
		self.login=Toplevel()
		self.login.title("Login")
		#Creating a Label widget
		self.Title= Label(self.login, text="Please enter your name to continue:")
		#Putting Label onto the screen
		self.Title.grid(row = 1)
		#Creating an input field
		self.Nameinput= Entry(self.login)
		self.Nameinput.grid(row=2)
		#automatically focus to type
		self.Nameinput.focus()
		
		#Creating a Button
		self.Button1= Button(self.login, text="Login", bg="white", fg="black", command = lambda: self.Start(self.Nameinput.get())).grid(row=3)
		
		self.root.mainloop()


	def Start(self, name):
		''' close the login window , get name and start '''
		self.login.destroy()
		self.interface(name)
		
		rec = threading.Thread(target = self.receive)
		rec.start() 

	def interface(self, name):
		''' main interface for the user '''
		self.name = name
		#showing the chatroom window
		self.root.deiconify()
		self.root.title("CHATROOM")

		#won't work 3shan msh nafs el directory 3and kolo (we'll try to make it work)
		#root.iconbitmap('C:/Users/yousef/Desktop/python/tkinter/bubble-chat.ico')

		#configuring window size w tb2a fixed
		self.root.resizable(width = False, height = False)
		self.root.configure(width = 500, height = 600, bg = "grey8")

		#creating head
		self.root.head = Label(self.root, bg = "grey8", fg = "white", pady = 5, text = self.name)
		self.root.head.place(relwidth = 1)

		#line ka design
		self.root.line = Label(self.root, width = 480, bg = "grey")
		self.root.line.place(relwidth = 1, rely = 0.05, relheight = 0.005)

		#creating chat area
		self.root.chat = Text(self.root, width = 25, height = 2, bg = "grey8", fg = "white", padx = 5, pady = 5)
		self.root.chat.place(relheight = 0.7, relwidth = 1, rely = 0.08)

		#creating bottom area
		self.root.bottom = Label(self.root, bg = "grey", height = 100)
		self.root.bottom.place(relwidth = 1, rely = 0.8)

		#creating area for user to type msgs (placing it in bottom area)
		self.root.entry = Entry(self.root.bottom, bg = "white", fg = "black")
		self.root.entry.place(relwidth = 0.75, relheight = 0.06, rely = 0.008, relx = 0.011)
		#to automatically focus on typing lama nefta7
		self.root.entry.focus()

		#creating send button (placing it in bottom area)
		self.root.button = Button(self.root.bottom, bg = "white", fg = "black", width = 20, text = "Send", command = lambda: self.sendButton(self.root.entry.get()))
		self.root.button.place(relx= 0.77, rely = 0.008, relheight = 0.06, relwidth = 0.22)

		#creating scrollbar (placing it in chat area)
		self.scrollbar = Scrollbar(self.root.chat)
		self.scrollbar.place(relheight = 1, relx = 0.98)
		self.scrollbar.config(command = self.root.chat.yview)

		#so you cannot type into the chat area
		self.root.chat.config(state = DISABLED)
		
	def sendButton(self, msg):
		'''used to send message using the send button '''
		self.root.chat.config(state = DISABLED)
		self.msg = msg
		self.root.entry.delete(0, END)
		s = threading.Thread(target = self.sendMsg)
		s.start()
		
	def receive(self):
		'''decode and save the input'''
		while True:
			try:
				message = client.recv(HEADER).decode(FORMAT)
				self.root.chat.config(state = NORMAL)
				self.root.chat.insert(END, message + '\n')
				self.root.chat.config(state = DISABLED)
				self.root.chat.see(END)
			except:
				print("ERROR")
				break
		
	def sendMsg(self):
		'''display messages to users '''
		self.root.chat.config(state = DISABLED)
		while True:
			message = (f"{self.name}: {self.msg}")
			client.send(message.encode(FORMAT))
			break

begin = PROG()

