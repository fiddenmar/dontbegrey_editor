from tkinter import *
from tkinter import filedialog
import math
import re

class App(Tk):
	def __init__(self, *args, **kwargs):
		Tk.__init__(self, *args, **kwargs)

		self.size = 20
		self.tileSize = 40

		self.menubar = Menu(self)
		self.menubar.add_command(label="configure", command = self.configure)
		self.menubar.add_command(label="load", command = self.load)
		self.menubar.add_command(label="save", command = self.save)
		self.config(menu=self.menubar)

		self.frame = Frame(self, width = 800, height = 800)
		self.frame.grid(row = 0, column = 2, columnspan = 5, rowspan = 5)
		self.canvas = Canvas(self.frame, bg = '#FFFFFF', width = 800, height = 800, scrollregion = (0,0,self.size * self.tileSize,self.size * self.tileSize))
		self.hbar = Scrollbar(self.frame, orient = HORIZONTAL)
		self.hbar.pack(side = BOTTOM, fill = X)
		self.hbar.config(command = self.canvas.xview)
		self.vbar = Scrollbar(self.frame, orient = VERTICAL)
		self.vbar.pack(side = RIGHT, fill = Y)
		self.vbar.config(command = self.canvas.yview)
		self.canvas.config(width = 800, height = 800)
		self.canvas.config(xscrollcommand = self.hbar.set, yscrollcommand = self.vbar.set)
		self.frame.bind('<Enter>', self._bound_to_mousewheel)
		self.frame.bind('<Leave>', self._unbound_to_mousewheel)
		self.canvas.bind("<ButtonPress-1>", self.press)
		self.canvas.bind("<ButtonRelease-1>", self.release)
		self.canvas.bind("<B1-Motion>", self.paint)
		self.canvas.pack(side = LEFT, fill = BOTH, expand = TRUE)

		self.checked = 0

		self.background = Listbox(self)
		for item in ["red", "green", "blue", "black", "grey"]:
			self.background.insert(END, item)
		self.background.select_set(0)
		self.background.event_generate("<<ListboxSelect>>")
		self.background.bind("<ButtonPress-1>", self.background_mode)
		self.background.grid(row = 0, column = 0)

		self.objects = Listbox(self)
		for item in ["start", "finish", "text"]:
			self.objects.insert(END, item)
		self.objects.bind("<ButtonPress-1>", self.object_mode)
		self.objects.grid(row = 0, column = 1)

		self.state = False

		self.rows = 100
		self.columns = 100
		self.cellwidth = self.tileSize
		self.cellheight = self.tileSize

		self.map = {}
		for column in range(self.size):
			for row in range(self.size):
				x1 = column * self.cellwidth
				y1 = row * self.cellheight
				x2 = x1 + self.cellwidth
				y2 = y1 + self.cellheight
				self.map[row,column] = self.canvas.create_rectangle(x1,y1,x2,y2, fill="black", outline="white", tags="map")
		self.start = {}
		self.finish = {}
		self.text = {}

		self.messagelabel = Label(self, text = "Text: ")
		self.messagelabel.grid(row = 1, column = 0)
		self.message = Entry(self, width = 40)
		self.message.grid(row = 1, column = 1)

		self.authorlabel = Label(self, text = "Extra: ")
		self.authorlabel.grid(row = 2, column = 0)
		self.author = Entry(self, width = 40)
		self.author.grid(row = 2, column = 1)

	def press(self, event):
		if self.checked == 0:
			self.state = True
			pos = self.map[math.floor(event.y / self.tileSize), math.floor(event.x / self.tileSize)]
			color = self.toColor(self.background.get(self.background.curselection()))
			self.canvas.itemconfig(pos, fill = color)
		else:
			column = math.floor(event.x / self.tileSize)
			row = math.floor(event.y / self.tileSize)
			x1 = column * self.cellwidth
			y1 = row * self.cellheight
			x2 = x1 + self.cellwidth
			y2 = y1 + self.cellheight
			color = self.toColor(self.objects.get(self.objects.curselection()))
			if color == "#FDFD96":
				self.canvas.delete(self.start);
				del self.start
				self.start = self.canvas.create_rectangle(x1,y1,x2,y2, fill=color, tags="start")
			if color == "#FFB347":
				self.canvas.delete(self.finish);
				del self.finish
				self.finish = self.canvas.create_rectangle(x1,y1,x2,y2, fill=color, tags="finish")
			if color == "#AB33C6":
				self.canvas.delete(self.text);
				del self.text
				self.text = self.canvas.create_rectangle(x1,y1,x2,y2, fill=color, tags="text")

	def release(self, event):
		self.state = False

	def paint(self, event):
		if self.state:
			pos = self.map[math.floor(event.y / self.tileSize), math.floor(event.x / self.tileSize)]
			color = self.toColor(self.background.get(self.background.curselection()))
			self.canvas.itemconfig(pos, fill = color)

	def _bound_to_mousewheel(self, event):
		self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)   

	def _unbound_to_mousewheel(self, event):
		self.canvas.unbind_all("<MouseWheel>") 

	def _on_mousewheel(self, event):
		self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

	def toColor(self, color):
		if color == "red":
			return "#FFA8A8"
		elif color == "green":
			return "#A8FFA8"
		elif color == "blue":
			return "#A8A8FF"
		elif color == "black":
			return "#000000"
		elif color == "start":
			return "#FDFD96"
		elif color == "finish":
			return "#FFB347"
		elif color == "text":
			return "#AB33C6"
		elif color == "grey":
			return "#AAAAAA"
		else:
			return "#FFFFFF"

	def toSaveColor(self, color):
		if color == "#FFA8A8":
			return "1"
		elif color == "#A8FFA8":
			return "2"
		elif color == "#A8A8FF":
			return "3"
		elif color == "#AAAAAA":
			return "4"
		elif color == "#FDFD96":
			return "1"
		elif color == "#FFB347":
			return "2"
		else:
			return "0"

	def fromSaveColor(self, number):
		if number == "0":
			return "#000000"
		elif number == "1":
			return "#FFA8A8"
		elif number == "2":
			return "#A8FFA8"
		elif number == "3":
			return "#A8A8FF"
		elif number == "4":
			return "#AAAAAA"

	def background_mode(self, e):
		self.checked = 0

	def object_mode(self, e):
		self.checked = 1

	def save(self):
		f = filedialog.asksaveasfile(mode='w', defaultextension=".dbgmap")
		if f is None:
			return
		f.write("Tilesize:\n")
		f.write(str(self.tileSize)+"\n")
		f.write("Map:\n")
		for row in range(self.size):
			for column in range(self.size):
				saveColor = self.toSaveColor(self.canvas.itemcget(self.map[row,column], "fill"))
				f.write(saveColor+" ")
			f.write("\n")

		try:
			c = self.canvas.coords(self.start)
			msg = str(round(c[0]/self.tileSize))+" "+str(round(c[1]/self.tileSize))
			f.write("Start:\n")
			f.write(msg)
			f.write("\n")
		except:
			print("No start")
		try:
			c = self.canvas.coords(self.finish)
			msg = str(round(c[0]/self.tileSize))+" "+str(round(c[1]/self.tileSize))
			f.write("Finish:\n")
			f.write(msg)
			f.write("\n")
		except:
			print("No finish")
		try:
			c = self.canvas.coords(self.text)
			msg = str(round(c[0]/self.tileSize))+" "+str(round(c[1]/self.tileSize))
			f.write("Message:\n")
			f.write(msg)
			f.write("\n")
			f.write(self.message.get())
			f.write("\n")
			f.write(self.author.get())
			f.write("\n")
		except:
			print("No message")
		f.close()

	def load(self):
		f = filedialog.askopenfile(mode='r', defaultextension=".dbgmap")
		if f is None:
			return
		content = f.read()
		res = re.split("Tilesize:\n|Map:\n|Start:\n|Finish:\n|Message:\n", content, flags=re.M)
		self.tileSize = int(res[1])
		mmap = res[2]
		lines = mmap.split("\n")
		i = 0
		for line in lines:
			cells = line.split(" ")
			j = 0
			for cell in cells:
				color = self.fromSaveColor(cell)
				x1 = j * self.tileSize
				y1 = i * self.tileSize
				self.map[i, j] = self.canvas.create_rectangle(x1, y1, x1 + self.tileSize, y1 + self.tileSize, fill=color, tags="map")
				j = j + 1
			i = i + 1

		start = res[3]
		x1 = int(start.split(" ")[0]) * self.tileSize
		y1 = int(start.split(" ")[1]) * self.tileSize
		self.start = self.canvas.create_rectangle(x1, y1, x1 + self.tileSize, y1 + self.tileSize, fill="#FDFD96", tags="start")
		finish = res[4]
		x1 = int(finish.split(" ")[0]) * self.tileSize
		y1 = int(finish.split(" ")[1]) * self.tileSize
		self.finish = self.canvas.create_rectangle(x1, y1, x1 + self.tileSize, y1 + self.tileSize, fill="#FFB347", tags="finish")
		messageinfo = res[5]
		messageinfo = messageinfo.split("\n")
		x1 = int(messageinfo[0].split(" ")[0]) * self.tileSize
		y1 = int(messageinfo[0].split(" ")[1]) * self.tileSize
		self.message.delete(0, END)
		self.message.insert(0, messageinfo[1])
		self.author.delete(0, END)
		self.author.insert(0, messageinfo[2])
		self.text = self.canvas.create_rectangle(x1, y1, x1 + self.tileSize, y1 + self.tileSize, fill="#AB33C6", tags="text")

	def configure(self):
		pass


if __name__ == "__main__":
	app = App()
	app.mainloop()