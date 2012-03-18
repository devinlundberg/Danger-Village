#!/usr/bin/python
# -*- coding: utf-8 -*-
import random
import asyncore
import socket
try:
    import cPickle as pickle
except:
    import pickle

class Game:
    '''class that keeps track of gamestate and allows players to play cards
    '''
    
    def variables(self):
	'''initializes all of the gamestate variables'''
	self.CRS=15#cards per suite used in constructing the deck and getting values of cards i.e. let x be the numberical representation of a card, x%CRS is the number on the card 11,12,13,14 representing jack queen king ace 0 representing jokers and 1 not existing
	self.CARDPILESIZE=4
	
	#player variables
	self.hand=([],[],[],[])
	self.faceUpCards=([],[],[],[])
	self.faceDownCards=([],[],[],[])
	self.setup=[False,False,False,False]
	
	#shared game state variables
	self.currentStack=[]
	self.lastPlay=(-1,0)
	self.currentTurn=-1
	self.players=[0,1,2,3]
	self.winners=[]
    
    def __init__(self):
	'''shuffles the deck and deals the cards out, initializing all gamestate values'''
	self.variables()
	deck=filter(lambda x: ((x%self.CRS != 0 and x%self.CRS != 1) or x==0 or x==self.CRS),range(0,self.CRS*4))
	random.shuffle(deck)
	for faceDownList,faceUpList,handList in zip(self.faceDownCards,self.faceUpCards,self.hand):
	    for x in range(self.CARDPILESIZE):
		faceDownList.append(deck.pop())
		faceUpList.append(deck.pop())
		handList.append(deck.pop())
	self.remainingDeck=deck
	
	
    def convertToPlayFormat(self, cardList):
	'''converts cardList to format specified in lastplay (card,num) or 0 if invalid'''
	def cardval(card): return card%self.CRS
	newCardList=map(cardval,cardList)
	length=len(newCardList)
	newCardset=set(newCardList)
	try:
	    newCardset.remove(3)
	except KeyError:
	    True
	if(len(newCardset)>=2):
	    return 0
	elif(len(newCardset)==0):
	    return (14,length)
	else:
	    return (newCardset.pop(),len(newCardList))
	
	
	
    def checkPlay(self,player,cardList):
	'''
	checks to see if a play made by a certain player is valid
	makes sure it is his turn, the play beats the most recently
	played card, cards are all of the same type, and cards are in hand.
	
	player is player number, 
	cardList is the cards from his handList
	
	returns 0 on invalid play, and (card, numberOfCards) if its valid (same format as lastPlay
	'''
	if (self.setup[0] and self.setup[1] and self.setup[2] and self.setup[3] and 
	cardList and self.currentTurn==player and set(cardList).issubset(self.hand[player])):
	    play=self.convertToPlayFormat(cardList)
	    if play==0:
		return 0
	    (card,num)=play
	    (pcard,pnum)=self.lastPlay
	    if card==10 or card==0 or num>3:
		return play
	    if num>pnum or (num==pnum and card>=pcard):
		return play
	return 0
	
    def playCard(self,player,cardList):
	'''
	plays the list of cards from the player specified
	checks to see if valid play
	then adds cards to stack, changes lastPlay, and performs any special operations(jokers or clears)
	then checks to see if the player has won, then changes the turn if necessary
	'''
	play=self.checkPlay(player,cardList)
	if play==0:
	    return
	(card,num)=play
	hand=[]
	hand.extend(self.hand[player])
	del self.hand[player][:]
	self.hand[player].extend(list(set(hand)^set(cardList)))
	if card == 10 or num>3:#clears
	    self.currentStack=[]
	    self.lastPlay=(-1,0)
	elif card == 0:#jokers
	    self.currentStack.extend(cardList)
	    self.hand[self.players[(self.players.index(self.currentTurn)+1)%len(self.players)]].extend(self.currentStack)
	    self.currentStack=[]
	    self.lastPlay=(-1,0)
	    self.currentTurn=self.players[(self.players.index(self.currentTurn)+2)%len(self.players)]
	else:#other cards
	    self.lastPlay=(card,num)
	    self.currentStack.extend(cardList)
	    self.currentTurn=self.players[(self.players.index(self.currentTurn)+1)%len(self.players)]
	while self.remainingDeck and len(self.hand[player])<4:
	    self.hand[player].append(self.remainingDeck.pop())
	if not self.hand[player] and self.faceUpCards[player]:
	    self.pickupFaceUpCards(player)
	if self.checkWinner(player):
	    self.winners.append(player)
	    if self.currentTurn==player:
		self.currentTurn=self.players[(self.players.index(self.currentTurn)+1)%len(self.players)]
	    self.players.remove(player)
	    if len(self.winners)==3:
		self.currentTurn=-2
		return self.winners
	    
	return None

	    
	
	
    def checkWinner(self,player):
	''' checks to see if a certain player has won. returns True if they have and False otherwise. '''
	return not (self.hand[player] or self.faceUpCards[player] or self.faceDownCards[player])
	
    def makeFaceUp(self,player,cardList):
	'''
	takes a input of a card list from the user, makes sure it is valid, and 
	then assigns those cards to be the face up cards and sets the setup flag to True.
	returns True if successful or False if incorrect cards
	'''
	if not self.setup[player] and len(cardList)==4:
	    playercards=[]
	    playercards.extend(self.hand[player])
	    playercards.extend(self.faceUpCards[player])
	    if not set(cardList).issubset(playercards):
		return False
	    del self.faceUpCards[player][:]
	    self.faceUpCards[player].extend(cardList)
	    del self.hand[player][:]
	    self.hand[player].extend(list(set(playercards)^set(cardList)))
	    self.setup[player]=True
	    if self.setup[0] and self.setup[1] and self.setup[2] and self.setup[3]:
		self.currentTurn=0
	    return True
	return False
	    
	
    def pickupPile(self,player):
	'''puts current stack into players hand'''
	self.hand[player].extend(self.currentStack)
	self.currentStack=[]
	self.lastPlay=(0,0)
    
    def playFaceDownCard(self,player):
	'''plays face down card'''
	if not self.hand[player] and not self.faceUpCards[player]:
	    randomCard=self.faceDownCards[player].pop()
	    self.hand[player].append(randomCard)
	    self.playCard(player,[randomCard])
	
	    
	
	
	
    def pickupFaceUpCards(self,player):
	'''picks up face up cards'''
	if not self.hand[player]:
	    self.hand[player].extend(self.faceUpCards[player])
	    del self.faceUpCards[player][:]
	    
	    
	    
	    
#Querying Functions-----------------------------------------------
    def getHand(self,player):
	'''returns hand'''
	def cardval(card): return card%self.CRS
	handval=map(cardval,self.hand[player])
	ret= zip(handval,self.hand[player])
	ret.sort()
	return ret
	
    def getFaceups(self):
	'''returns faceup cards of all players'''
	def cardval(card): return card%self.CRS
	retlist=[]
	for player in self.players:
	    handval=map(cardval,self.faceUpCards[player])
	    ret= zip(handval,self.faceUpCards[player])
	    ret.sort()
	    retlist.append(ret)
	return ret
	
    def getStack(self):
	def cardval(card): return card%self.CRS
	handval=map(cardval,self.currentStack)
	ret= zip(handval,self.currentStack)
	return ret
	
    def getLastPlay(self):
	return self.lastPlay
	
    def getSizeOfFaceDowns(self):
	'''returns number of cards in each facedown stack'''
	return (len(self.faceDownCards[0]),len(self.faceDownCards[1]),len(self.faceDownCards[2]),len(self.faceDownCards[3]))
	
    def getSizeOfHands(self):
	'''returns number of cards in each facedown stack'''
	return (len(self.hand[0]),len(self.hand[1]),len(self.hand[2]),len(self.hand[3]))
	
    def getGameState(self,player):
	'''returns gamestate information for use in sockets'''
	return (player,self.currentTurn,self.hand[player],self.currentStack,self.faceUpCards,self.lastPlay,self.setup,self.winners,self.CRS,self.getSizeOfFaceDowns(),self.getSizeOfHands())



class Handler(asyncore.dispatcher):

    def __init__(self, host, socket,num):
	'''creates dispatcher object to handle socket connection with one player'''
        asyncore.dispatcher.__init__(self, socket)
        self.host = host
        self.num=num
        self.outbox=[]
        print num
        
    def handle_read(self):
	'''reads in data, calls user function on gamestate, and sends new gamestate to all players'''
        data = self.recv(8192)
        if data:
	    userinput=pickle.loads(data)
	    print userinput,self.num
	    if userinput[0]=='makeFaceUp':
		self.host.game.makeFaceUp(self.num,userinput[1])
	    elif userinput[0]=='playCard':
		if not self.host.game.playCard(self.num,userinput[1]) is None:
		    self.host.handle_close()
	    elif userinput[0]=='pickupPile':
		self.host.game.pickupPile(self.num)
	    elif userinput[0]=='playFaceDownCard':
		self.host.game.playFaceDownCard(self.num)
            self.host.broadcast()
        
    def handle_close(self):
	if self.outbox:
	    message=self.outbox.pop()
	    self.send('%04d'%len(message))
	    self.send(message)
	self.close()
	

    def say(self):
	'''adds an instance of the gamestate to the outbox stack'''
	gamestate=self.host.game.getGameState(self.num)
	data=pickle.dumps(gamestate)
	self.outbox.append(data)

    def handle_write(self):
	'''sends messages in the outbox to the player'''
	if not self.outbox:
	    return
	message=self.outbox.pop()
	self.send('%04d'%len(message))
	self.send(message)

class Server(asyncore.dispatcher):

    def __init__(self, host, port):
	'''sets up server and game with the host being the server host and the port being the server port'''
	asyncore.dispatcher.__init__(self)
	self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
	self.set_reuse_addr()
	self.bind((host, port))
	self.listen(5)
	self.players=[]
	self.game=Game()
	
    def broadcast(self):
	'''sends gamestate to all players'''
	for player in self.players:
	    player.say()

    def handle_close(self):
	self.broadcast()
	for player in self.players:
	    player.handle_close()
	self.close()

    def handle_accept(self):
	'''handles someone trying to connect to game if there are less than 4 players it lets them in otherwise no'''
	pair = self.accept()
	if not (pair is None):
            sock, addr = pair
            print 'Incoming connection from %s' % repr(addr)
            if len(self.players)<4:
		self.players.append(Handler(self,sock,len(self.players)))

#test code
if __name__ == '__main__':
    server = Server('localhost', 8081)
    asyncore.loop()

