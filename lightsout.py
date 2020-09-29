#!/usr/bin/env python

from Tkinter import *
from itertools import *
from random import randint

class Window(Tk):
    def __init__(self,parent,game):
        Tk.__init__(self,parent)
        self.parent = parent
        self.game = game
        self.title("Lights Out!")
        self.geometry("500x500")
        self.create_widgets()
        self.focus_set()        
        
    def create_widgets(self):
        # self.grid()
        self.update()
        
        square_size = self.winfo_width() / self.game.size
                
        self.boxes = {}
        for (i,j) in product(xrange(self.game.size),xrange(self.game.size)):
            self.boxes[(i,j)] = Frame(width=square_size,height=square_size)
            self.boxes[(i,j)]["bg"] = "white"
            self.boxes[(i,j)].grid(row=i+1,column=j,sticky=(N,E,S,W))
            self.boxes[(i,j)].bind("<Button-1>",lambda event,row=i,col=j: self.press_light(event,row,col))
            # self.boxes[(i,j)].bind("<Button>", lambda event: self.press_light(event,i,j))
        
        for i in xrange(self.game.size):
            self.grid_rowconfigure(i+1,weight=1)
            self.grid_columnconfigure(i,weight=1)
        
        # self.menubar = Menu()
        # self.menubar.add_command(label="Quit",command=exit)
        # self.config(menu=self.menubar)
        
        self.game_mode = StringVar()
        self.game_mode.set("Play")
        self.game_mode_menu = OptionMenu(self,self.game_mode,"Play","Draw")
        self.game_mode_menu.grid(row=0,column=0,columnspan=2,sticky=(N,W))
        
        self.message_box = Label(font=("Arial",24,"bold"))
        self.message_box.grid(row=0,column=1,columnspan=self.game.size-2)
        self.message_box["text"] = "Moves: 0"

        self.randomise_button = Button(text="Randomise",command=self.randomise)
        self.randomise_button.grid(row=0,column=2,columnspan=self.game.size-2,sticky=(N,E))
        
        # self.quit_button = Button(text="Quit",command=exit)
        # self.quit_button.grid(row=0,column=2,columnspan=self.game.size-2,sticky=(N,E))
        
    def press_light(self,event,row,col):
        self.game.mode = self.game_mode.get()
        self.game.lights[(row,col)].press()
        self.update_boxes()
        if self.game.mode == "Play":
            if [ light for light in self.game.lights.values() if light.on ] == []:
                self.message_box["text"] = "You win!"
                self.game.moves = 0
            else:
                self.message_box["text"] = "Moves: " + str(self.game.moves)

    def update_boxes(self):
        for (i,j) in product(xrange(self.game.size),xrange(self.game.size)):
            if self.game.lights[(i,j)].on:
                box_colour = "DodgerBlue3"
            else:
                box_colour = "white"
            self.boxes[(i,j)]["bg"] = box_colour
        if self.game.mode == "Draw":
            self.message_box["text"] = "Draw mode"
        self.update()
        
    def randomise(self):
        for (i,j) in product(xrange(self.game.size),xrange(self.game.size)):
            if randint(0,1) == 1:
                self.game.lights[(i,j)].on = True
            else:
                self.game.lights[(i,j)].on = False
        self.update_boxes()
        self.game.moves = 0
        self.message_box["text"] = "Moves: 0"


class LightsOutGame:
    def __init__(self,size=5):
        self.size = size
        self.mode = "Play"
        self.lights = {}
        self.moves = 0
        for (i,j) in product(xrange(self.size),xrange(self.size)):
            self.lights[(i,j)] = Light(i,j,self)
            

class Light:
    def __init__(self,row,col,game,on=False):
        self.coords = (row,col)
        self.on = on
        self.game = game
        
    def neighbours(self):
        row = self.coords[0]
        col = self.coords[1]
        neighbours = []
        if row > 0:
            neighbours.append(self.game.lights[(row-1,col)])
        if row < self.game.size-1:
            neighbours.append(self.game.lights[(row+1,col)])
        if col > 0:
            neighbours.append(self.game.lights[(row,col-1)])
        if col < self.game.size-1:
            neighbours.append(self.game.lights[(row,col+1)])
        return neighbours

    def flip(self):
        self.on = not self.on

    def press(self):
        self.flip()
        if self.game.mode == "Play":
            self.game.moves += 1
            for light in self.neighbours():
                light.flip()

        
if __name__ == "__main__":
    g = LightsOutGame()
    game_window = Window(None,g)
    game_window.mainloop()
