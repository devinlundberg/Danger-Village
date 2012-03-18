#!/usr/bin/python
# -*- coding: utf-8 -*-
import socket
import asyncore
import time
try:
    import cPickle as pickle
except:
    import pickle


class Computer(asyncore.dispatcher_with_send):
    '''Computer class for connecting to server as player'''
    
    def __init__(self, host, port):
	'''sets up client'''
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect((host, port))
        data=pickle.dumps((-1,21))
        self.out_buffer = data

    def handle_close(self):
        self.close()

    def handle_read(self):
	'''function that handles recivieng data, analyzes gamestate and calls functions to find return'''
	length=self.recv(4)
	time.sleep(.05)
	if length:
	    thelen=int(length)
	    data=self.recv(thelen)
        #(player,currentTurn,hand[player],currentStack,faceUpCards,lastPlay,setup,winners,CRS,getSizeOfFaceDowns,handsizes)
	    if data:
		gamestate=pickle.loads(data)
		print gamestate,'\n'
		if not gamestate[6][gamestate[0]]:#checks to see if game is setup
		    output=self.setupprocess(gamestate)
		    self.out_buffer=pickle.dumps(output)
		if gamestate[1]==gamestate[0]:#checks to see if it is currently your turn
		    output=self.process(gamestate)
		    self.out_buffer=pickle.dumps(output)
		if gamestate[1]==-2:
		    self.close()
	   
	   
    def setupprocess(self,gamestate):
	'''
	setups cards by simply retruning, can add more logic later
	returns (0,list of cards to be faceup)
	'''
        cards=[]
        cards.extend(gamestate[2])
        cards.extend(gamestate[4][gamestate[0]])
        CRS=gamestate[8]
        valuemap,values=self.getHand(cards,CRS)

        faceupcards=self.getSetup(values)
	if faceupcards!=0:
            return ('makeFaceUp',self.getCards(valuemap,faceupcards)[1])
        return ('makeFaceUp',gamestate[2])
	
    def getSetup(self,values):
        '''
        uses logic to determine the best cards to put face up
        '''
        threes=0
        for count, card in values:
	    if card == 3:
                threes=count
        for count, card in values:
	    if card != 3 and card != 10 and card !=0:
		if count+threes>=4:
		    return card,4
	retlist=[]
        return 0
		

    def process(self,gamestate):
	'''takes raw gamestate data and processes them until it decides output'''
	hand=gamestate[2]
	CRS=gamestate[8]
	lastPlay=gamestate[5]
	if not hand:
	    return ('playFaceDownCard',[])
	valuehand,values=self.getHand(hand,CRS)
	play=self.getPlay(values,lastPlay)
	return self.getCards(valuehand,play)

	
    def getHand(self,hand,CRS):
	'''
	takes card data from gamestate and returns processable card 
	information by mapping cards to their values
	
	returns a tuple of 
	a list of tuples with values, unique card number
	and a list of values with the number of cards of that value
	'''
	def cardval(card): return card%CRS
	handval=map(cardval,hand)
	ret= zip(handval,hand)
	ret.sort()
	cardcount=[]
	for i in set(handval):
	    cardcount.append((handval.count(i),i))
	cardcount.sort()
	return ret,cardcount
	
    def getPlay(self, values,lastPlay):
	'''
	the logic that decides what card will be played
	takes values in format of list of value, count
	
	accounts for logic of computer and thus can be imporved
	
	returns play in value,count format
	'''
	lastCard, lastCount=lastPlay
	#checks for a 3 and something else as the only cards in hand
	if len(values)==2:
            for count, card in values:
                if card == 3:
                    for othercount, othercard in values:
                        if othercard != 3 and othercard != 10 and othercard !=0:
                            if othercount+count>lastCount or (othercount+count==lastCount and othercard>=lastCard):
                                return othercard,othercount+count
	#play lowest non-3,10,or joker
	for count, card in values:
	    if card != 3 and card != 10 and card !=0:
		if count>lastCount or (count==lastCount and card>=lastCard):
		    return card,count
	#see if combining a 3 with something would yield a better play
	for count, card in values:
	    if card == 3:
		for othercount, othercard in values:
		    if othercard != 3 and othercard != 10 and othercard !=0:
			if othercount+count>lastCount or (othercount+count==lastCount and othercard>=lastCard):
			    return othercard,othercount+count
		if lastCount<=count:
		    return 14,count
	#play joker or 10
	for count, card in values:
	    if card==0 or card==10:
		return card, 1

	return 0
	

    def getCards(self,valuehand,play):
	'''
	takes a play in the format value,card and tuples of value,card number
	returns a list of cardnums
	'''
	if play==0:
	    return ('pickupPile',[])
	cardList=[]
	count=play[1]
	for card in valuehand:
	    if card[0]==play[0]:
		cardList.append(card[1])
		count=count-1
	    if count==0:
		return ('playCard',cardList)
	for card in valuehand:
	    if card[0]==3:
		cardList.append(card[1])
		count=count-1
	    if count==0:
		return ('playCard',cardList)
	

#test code
if __name__ == '__main__':
    client = Computer('localhost', 8081)
    asyncore.loop()

