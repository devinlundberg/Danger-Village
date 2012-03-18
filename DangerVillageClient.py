#!/usr/bin/python
# -*- coding: utf-8 -*-

from DangerVillage import Server
from DangerVillageComputer import Computer
from DangerVillage import Game
from Tkinter import *
import socket
import asyncore
import random
import time
import os
import tkMessageBox
import tkSimpleDialog
try:
    import cPickle as pickle
except:
    import pickle


class Client(asyncore.dispatcher_with_send):
    '''Client class for connecting to server as player'''
    
    def __init__(self, host, port, gameView):
	'''sets up client'''
	self.delay=.2
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect((host, port))
        data=pickle.dumps((-1,21))
        self.out_buffer = data
        self.gameView=gameView

    def handle_close(self):
        self.close()

    def handle_read(self):
	'''function that handles recivieng data, analyzes gamestate and calls function update GUI'''
	length=self.recv(4)
	time.sleep(self.delay)
	if length:
	    thelen=int(length)
	    fuckingbug=True
	    while fuckingbug:
		try:
		    data=self.recv(thelen)
		    fuckingbug=False
		except:
		    time.sleep(self.delay)
		    fuckingbug=True
	    if data:
		gamestate=pickle.loads(data)
		print gamestate,'\n'
		self.updateGame(gamestate)
		if gamestate[1]==-2:
		    self.close()
	   
	   
    def setupprocess(self, cardlist):
	'''
	adds the appropriate signal to the out buffer for the setup process
	'''
	self.out_buffer=pickle.dumps(('makeFaceUp',cardlist))

    def pickupprocess(self):
	'''
	adds the appropriate signal to the out buffer for the pickup process
	'''
	self.out_buffer=pickle.dumps(('pickupPile',[]))

    def process(self, cardlist):
	'''
	adds the appropriate signal to the out buffer for the play process
	'''
	self.out_buffer=pickle.dumps(('playCard',cardlist))

	
    def faceDownprocess(self):
	'''
	adds the appropriate signal to the out buffer for the faceDown play process
	'''
	self.out_buffer=pickle.dumps(('playFaceDownCard',[]))
	
	
    def updateGame(self,gamestate):
	'''
	updates GUI with new gamestate information recieved from the server
	'''
	 #(player,currentTurn,hand[player],currentStack,faceUpCards,lastPlay,setup,winners,CRS,getSizeOfFaceDowns,handsizes)
	player=gamestate[0]
	currentTurn=gamestate[1]
	hand=gamestate[2]
	currentStack=gamestate[3]
	faceUpCards=gamestate[4]
	lastPlay=gamestate[5]
	setup=gamestate[6]
	winners=gamestate[7]
	CRS=gamestate[8]
	faceDowns=gamestate[9]
	hands=gamestate[10]
	self.gameView.setCurrentTurn(currentTurn,player)
	self.gameView.setHand(hand,faceUpCards,setup,player,CRS)
	self.gameView.setCurrentStack(currentStack)
	self.gameView.setFaceUpCards(faceUpCards,faceDowns,player)
	self.gameView.setLastPlay(lastPlay, currentStack)
	self.gameView.setHands(hands,player)
	self.gameView.setWinners(winners)
	

class DangerVillageApp:
    '''
    '''
    def __init__(self, parent):
	
	self.currenthand=[]
	self.selectedcards=[]
	self.gifsdict = {}
	dirpath = './images/'
	for suite in zip(['s','c','d','h'],range(0,4)):
	    for card in range(2,15):
		gifname=suite[0]+str(card)+'.gif'
		gifpath = os.path.join(dirpath, gifname)
		gif = PhotoImage(file=gifpath)
		self.gifsdict[suite[1]*15+card] = gif
	for suite in [('j',0)]:
	    for card in range(1,3):
		gifname=suite[0]+str(card)+'.gif'
		gifpath = os.path.join(dirpath, gifname)
		gif = PhotoImage(file=gifpath)
		self.gifsdict[card*15-15] = gif
	gifpath = os.path.join(dirpath, 'b1fv.gif')
	gif = PhotoImage(file=gifpath)
	self.gifsdict[-1] = gif
	

	
	#sets window size
	self.myParent = parent 
	self.myParent.geometry("640x575")
	parent.title('Danger Village')
	
	
	#set up menu bar
	menubar = Menu(parent)
	filemenu = Menu(menubar, tearoff=0)
	filemenu.add_command(label="New Game", command=self.newServer)
	filemenu.add_command(label="Add Computer", command=self.addComputer)
	filemenu.add_command(label="Connect to Computer", command=self.connectToServer)
	filemenu.add_separator()
	filemenu.add_command(label="Exit", command=parent.quit)
	menubar.add_cascade(label="File", menu=filemenu)
	
	helpmenu = Menu(menubar, tearoff=0)
	helpmenu.add_command(label="Rules", command=self.help)
	menubar.add_cascade(label="Help", menu=helpmenu)
	parent.config(menu=menubar)
	
	# the window frame
	self.window = Frame(parent) ###
	self.window.pack(expand=YES, fill=BOTH)
	
	
	
	# sets up the hand frame
	self.hand_frame=Frame(self.window)
	self.hand_frame.pack(side=BOTTOM, expand=NO, fill=X, anchor=S)
	
	#set up display frames
	
	
	
	
	
	
	self.leftcardframe=Frame(self.window)
	self.leftcardframe.pack(side=LEFT, expand=NO, fill=X, anchor=E)
	
	self.rightcardframe=Frame(self.window)
	self.rightcardframe.pack(side=RIGHT, expand=NO, fill=X, anchor=W)
	
	self.bottomcardframe=Frame(self.window)
	self.bottomcardframe.pack(side=BOTTOM, expand=NO, fill=Y, anchor=S)
	
	self.topcardframe=Frame(self.window)
	self.topcardframe.pack(side=TOP, expand=NO, fill=Y, anchor=N)
	
	self.lefts=[]
	self.rights=[]
	self.bottoms=[]
	self.tops=[]
	
	self.leftinfoframe=Frame(self.leftcardframe)
	self.leftinfoframe.pack(side=LEFT, expand=NO, fill=X, anchor=E)
	
	self.rightinfoframe=Frame(self.rightcardframe)
	self.rightinfoframe.pack(side=RIGHT, expand=NO, fill=X, anchor=W)
	
	self.bottominfoframe=Frame(self.bottomcardframe)
	self.bottominfoframe.pack(side=BOTTOM, expand=NO, fill=Y, anchor=S)
	
	self.topinfoframe=Frame(self.topcardframe)
	self.topinfoframe.pack(side=TOP, expand=NO, fill=Y, anchor=N)
	
	
	self.leftplayer=Label(self.leftinfoframe,text='')
	self.leftplayer.pack(side=TOP)
	
	self.rightplayer=Label(self.rightinfoframe,text='')
	self.rightplayer.pack(side=TOP)
	
	self.topplayer=Label(self.topinfoframe,text='')
	self.topplayer.pack(side=LEFT)
	
	self.bottomplayer=Label(self.bottominfoframe,text='')
	self.bottomplayer.pack(side=LEFT)
	
	self.leftcards=Label(self.leftinfoframe,text='')
	self.leftcards.pack(side=TOP)
	
	self.rightcards=Label(self.rightinfoframe,text='')
	self.rightcards.pack(side=TOP)
	
	self.topcards=Label(self.topinfoframe,text='')
	self.topcards.pack(side=LEFT)
	
	self.bottomcards=Label(self.bottominfoframe,text='')
	self.bottomcards.pack(side=LEFT)
	
	# control frame - basically everything except the demo frame
	self.control_frame = Frame(self.window) ###
	self.control_frame.pack(side=TOP, expand=Y, pady=0,  padx=10, ipadx=1)  	
	
	#sets up (temporary) gamestate displays
	self.playertext=Label(self.control_frame, text='', justify=LEFT)
	self.playertext.pack(side=TOP, anchor=S)
	
	self.currentTurntext=Label(self.control_frame, text='', justify=LEFT)
	self.currentTurntext.pack(side=TOP, anchor=S)
	
	self.currentStacktext=Label(self.control_frame, text='', justify=LEFT)
	self.currentStacktext.pack(side=TOP, anchor=S)
	
	self.lastPlaytext=Label(self.control_frame, text='', justify=LEFT)
	self.lastPlaytext.pack(side=TOP, anchor=S)
	
	self.lastPlaypic=Label(self.control_frame, text='', justify=LEFT)
	self.lastPlaypic.pack(side=TOP, anchor=S)
	
	self.winnerstext=Label(self.control_frame, text='', justify=LEFT)
	self.winnerstext.pack(side=TOP, anchor=S)
	
	
	self.serverrunning=False
	
	# set up for buttons
	self.buttons_frame = Frame(self.hand_frame) ###
	self.buttons_frame.pack(side=TOP, expand=NO, fill=Y, ipadx=5)    
	
	
	self.playButton = Button(self.buttons_frame)
	self.playButton.configure(text="Play Card")
	self.playButton.pack(side=RIGHT)
	self.playButton.focus_force()         
	self.playButton.bind("<Button-1>", self.playClick)  
	self.playButton.bind("<Return>", self.playClick) 
	
	self.setupButton = Button(self.buttons_frame)
	self.setupButton.configure(text="Setup")   
	self.setupButton.pack(side=RIGHT)
	self.setupButton.bind("<Button-1>", self.setupClick)   
	self.setupButton.bind("<Return>", self.setupClick)
	
	self.faceDownButton = Button(self.buttons_frame)
	self.faceDownButton.configure(text="Play FaceDown")   
	self.faceDownButton.pack(side=RIGHT)
	self.faceDownButton.bind("<Button-1>", self.playFaceDownClick)   
	self.faceDownButton.bind("<Return>", self.playFaceDownClick)
	
	self.pickupButton = Button(self.buttons_frame)
	self.pickupButton.configure(text="Pick up pile")   
	self.pickupButton.pack(side=RIGHT)
	self.pickupButton.bind("<Button-1>", self.pickupClick)   
	self.pickupButton.bind("<Return>", self.pickupClick)
	
	
	scrollbar = Scrollbar(self.hand_frame, orient=HORIZONTAL)
	self.handcanvas = Canvas(self.hand_frame)
	
	self.handcanvas.config(height=100,scrollregion=self.handcanvas.bbox(ALL), xscrollcommand=scrollbar.set)
	scrollbar.config(command=self.handcanvas.xview)
	scrollbar.pack(side=BOTTOM, fill=X)
	self.handcanvas.pack(side=LEFT, fill=BOTH, expand=1)
	
	#starts polling the server
	self.asynpoll()

    def help(self):
	tkMessageBox.showinfo('Rules','The point of the game is to play your cards before the other players\nThis game is a four player card game using a 54 card deck of cards (includes jokers). The game starts by shuffling the deck of cards and dealing 4 cards facedown to each player. Then 4 more cards are dealt face up so all players can see them. Then another 4 cards are dealt facedown to each player. The other cards are put aside.\nThen each player picks up the second set of facedown cards and the face up cards and chooses 4 to put face up in front of him and 4 to keep in his hand.\nThen play begins. The first player to play is decided and they play a card from their hand onto the stack. Play continues to the left. Players draw from the remaining deck of cards after they play so they have four cards until the remaining cards are gone. When a player empties his hand, he picks up his 4 face up cards. When his hand is emptied again, he plays one of his face down cards randomly. When he has played all of his face down cards and emptied his hand, that player has won.')
	tkMessageBox.showinfo('Rules for Play','A player can choose to pick up the current cards in play or play a card or combination of cards in their hand higher than the last card played. Cards are ordered from 2 to aces with aces being the highest card. Pairs of cards can be played and are worth more than all single cards and ordered from 2 to ace. Three of a kinds can also be played and similarly are worth more than all pairs and single cards. Four of a kinds will clear the pile; it will be set aside and ignored for the rest of the game.\nThere are several special cards in the game. 10s will clear the pile similar to four of a kinds. 3s are wild and can be considered any card for pairing with other cards. Jokers cause the next player to pick up the cards and skips their turn.')


    def connectToServer(self):
	output=tkSimpleDialog.askstring('Server Location','Ip Address')
	if output:
	    if self.serverrunning:
		self.server.close()
	    self.client=Client(output,8081,self)

    def newServer(self):
	if self.serverrunning:
	    self.server.close()
	self.server=Server('',8081)
	self.client= Client('localhost', 8081,self)
	self.serverrunning=True

    def addComputer(self):
	Computer('localhost',8081)


    def playFaceDownClick(self,event):
	'''
	tells the server to play a facedown card 
	'''
	try:
	    self.client.faceDownprocess()
	except:
	    print "The connection to the server has been lost. Please start a new game."
	    
    def pickupClick(self,event):
	'''
	tells the server to pick up cards
	'''
	try:
	    self.client.pickupprocess()
	except:
	    print "The connection to the server has been lost. Please start a new game."


    def playClick(self,event):
	'''
	takes selected list box cards and sends them to the server to be played
	'''
	selected= self.selectedcards
	try:
	    self.client.process(selected)
	except:
	    print "The connection to the server has been lost. Please start a new game."

    def setupClick(self,event):
	'''
	takes selected list box cards and sends them to the server to be made face up
	'''
	selected= self.selectedcards
	try:
	    self.client.setupprocess(selected)
	except:
	    print "The connection to the server has been lost. Please start a new game."
	
	
	
    def setCurrentTurn(self,currentTurn,player):
	'''
	takes current Turn and reconfigures the gui features that incorporate it
	'''
	
	self.leftplayer['text']=(player+3)%4
	self.leftplayer.pack(side=TOP)
	
	self.rightplayer['text']=(player+1)%4
	self.rightplayer.pack(side=TOP)
	
	self.topplayer['text']=(player+2)%4
	self.topplayer.pack(side=LEFT)
	
	self.bottomplayer['text']=player
	self.bottomplayer.pack(side=LEFT)
	
	if currentTurn==-1:
	    self.currentTurntext['text']='Setting up Game...'
	elif currentTurn==-2:
	    self.currentTurntext['text']='Game Over'
	else:
	    self.currentTurntext['text']='Player '+ str(currentTurn) + '\'s Turn'
	    if currentTurn==player:
		self.playButton.configure(state=NORMAL)
		self.pickupButton.configure(state=NORMAL)
	    else:
		self.playButton.configure(state=DISABLED)
		self.pickupButton.configure(state=DISABLED)
	
	self.currentTurntext.pack(side=TOP, anchor=W)
	
    def imgclick(self,event):
	cardnum=int(event.widget.cget('text'))
	if cardnum in self.selectedcards:
	    defbg=Label().cget('bg')
	    self.selectedcards.remove(cardnum)
	    event.widget.config(bg=defbg)
	else:
	    self.selectedcards.append(cardnum)
	    event.widget.config(bg='blue')

    def setHand(self,hand,faceUpCards,setup,player,CRS):
	'''
	takes hand and reconfigures the gui features that incorporate it
	'''
	if not setup[player]:
	    hand.extend(faceUpCards[player])
	    self.setupButton.configure(state=NORMAL)
	    self.playButton.configure(state=DISABLED)
	    self.pickupButton.configure(state=DISABLED)
	else:
	    self.setupButton.configure(state=DISABLED)
	hand=sorted(hand,key=lambda card:card%CRS)
	if hand:
	    self.faceDownButton.configure(state=DISABLED)
	else:
	    self.faceDownButton.configure(state=NORMAL)
	if self.currenthand !=hand:
	    self.selectedcards=[]
	    self.currenthand=hand
	    self.handcanvas.delete(ALL)
	    handframe=Frame()
	    for card in hand:
		img = Label(handframe)
		img.bind('<Button-1>',self.imgclick)
		img.pack(side=LEFT)
		img.config(text=str(card),image=self.gifsdict[card], takefocus=1)
	    self.handcanvas.create_window(75*len(hand)/2,50,window=handframe)
	    self.myParent.lift()
	

	
    def setCurrentStack(self,currentStack):
	'''
	takes the CurrentStack and reconfigures the gui features that incorporate it
	'''
	displayStack=map(lambda x:x%15,currentStack)
	displayStack=map(lambda x: 'A' if x==14 else 'K' if x==13 else 'Q' if x==12 else 'J' if x==11 else str(x),displayStack)
	 
	self.currentStacktext['text']=displayStack
	self.currentStacktext.pack(side=BOTTOM, anchor=S)
	
    def setFaceUpCards(self,faceUpCards,faceDowns,player):
	'''
	takes faceupcards and the number of facedown cards and reconfigures the gui features that incorporate it
	'''
	self.setupRightCards(faceUpCards[(player+1)%4],faceDowns[(player+1)%4])
	self.setupLeftCards(faceUpCards[(player+3)%4],faceDowns[(player+3)%4])
	self.setupBottomCards(faceUpCards[player],faceDowns[player])
	self.setupTopCards(faceUpCards[(player+2)%4],faceDowns[(player+2)%4])
	
    def setupLeftCards(self, cards, facedown):
	for card in self.lefts:
	    card.pack_forget()
	if not cards:
	    cards=[-1]*facedown
	for card in cards:
	    img = Label(self.leftcardframe)
	    img.pack(side=TOP)
	    img.config(text=str(card),image=self.gifsdict[card], takefocus=1)
	    self.lefts.append(img)


    def setupRightCards(self, cards, facedown):
	for card in self.rights:
	    card.pack_forget()
	if not cards:
	    cards=[-1]*facedown
	for card in cards:
	    img = Label(self.rightcardframe)
	    img.pack(side=TOP)
	    img.config(text=str(card),image=self.gifsdict[card], takefocus=1)
	    self.rights.append(img)


    def setupTopCards(self, cards, facedown):
	for card in self.tops:
	    card.pack_forget()
	if not cards:
	    cards=[-1]*facedown
	for card in cards:
	    img = Label(self.topcardframe)
	    img.pack(side=RIGHT)
	    img.config(text=str(card),image=self.gifsdict[card], takefocus=1)
	    self.tops.append(img)

    def setupBottomCards(self, cards, facedown):
	for card in self.bottoms:
	    card.pack_forget()
	if not cards:
	    cards=[-1]*facedown
	for card in cards:
	    img = Label(self.bottomcardframe)
	    img.pack(side=LEFT)
	    img.config(text=str(card),image=self.gifsdict[card], takefocus=1)
	    self.bottoms.append(img)


    def setLastPlay(self,lastPlay,currentStack):
	'''
	takes lastPlay and reconfigures the gui features that incorporate it
	'''
	self.lastPlaytext['text']=lastPlay[1]
	self.lastPlaytext.pack(side=BOTTOM, anchor=S)
	if currentStack:
	    self.lastPlaypic['image']=self.gifsdict[currentStack[-1]]
	else:
	    self.lastPlaypic['image']=self.gifsdict[-1]
	self.lastPlaypic.pack(side=BOTTOM, anchor=S)
	
    def setHands(self,hands,player):
	'''
	takes hand sizes and reconfigures the gui features that incorporate it
	'''
	self.leftcards['text']='Hand:'+str(hands[(player+3)%4])
	self.leftcards.pack(side=TOP)
	
	self.rightcards['text']='Hand:'+str(hands[(player+1)%4])
	self.rightcards.pack(side=TOP)
	
	self.topcards['text']='Hand:'+str(hands[(player+2)%4])
	self.topcards.pack(side=LEFT)
	
	self.bottomcards['text']='Hand:'+str(hands[player])
	self.bottomcards.pack(side=LEFT)
	
    def setWinners(self,winners):
	'''
	takes winners and reconfigures the gui features that incorporate it
	'''
	self.winnerstext['text']='Winners:'+str(winners)
	self.winnerstext.pack(side=BOTTOM, anchor=S)
	
	
    def asynpoll(self):
	'''
	function that polls the network and then sets a timer to call itself again
	'''
	asyncore.poll()
	self.myParent.after(50,self.asynpoll)





#test code
if __name__ == '__main__': 
    root = Tk()
    myapp = DangerVillageApp(root)
    root.mainloop()
