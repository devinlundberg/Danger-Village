#!/usr/bin/python
# -*- coding: utf-8 -*-
#Danger village unit testing

import unittest
import DangerVillage
import DangerVillageComputer

class DVTests(unittest.TestCase):
    def setUp(self):
	self.a=DangerVillage.Game()
	#player variables
	self.a.hand=([39, 15, 19, 24], [51, 14, 4, 43], [2, 56, 49, 22], [7, 27, 58, 36])
	self.a.faceUpCards=([26, 28, 17, 6], [52, 12, 18, 20], [35, 10, 44, 55], [34, 50, 9, 8])
	self.a.faceDownCards=([13, 32, 38, 53], [42, 41, 0, 48], [54, 29, 23, 47], [59, 40, 57, 25])
	self.a.setup=[True,True,True,True]
	
	#shared game state variables
	self.a.remainingDeck=[33, 5, 21, 3, 11, 37]
	self.a.currentStack=[]
	self.a.lastPlay=(0,0)
	self.a.currentTurn=-1
	self.a.players=[0,1,2,3]
	self.a.winners=[]
    
    def inittest(self):
	b=DangerVillage()
	assert b.CRS == 15 , 'wrong CRS'
	assert b.CARDPILESIZE == 4 , 'wrong pile size'
	assert len(b.hand[0]) == 4 and len(b.hand[1]) == 4 and len(b.hand[3]) ==4, 'bad hand generation'
	assert len(b.faceDownCards[0]) == 4 and len(b.faceDownCards[1]) == 4 and len(b.faceDownCards[3]) ==4, 'bad hand generation'
	assert len(b.faceUpCards[0]) == 4 and len(b.faceUpCards[1]) == 4 and len(b.faceUpCards[3]) ==4, 'bad faceUpCards generation'
	assert b.currentStack==[],'stack size wrong'
	assert len(b.remainingDeck)==6,'incorrect allocation of cards'
	assert a!=b, 'bad randomization'
	
	
    def testconvertToPlayFormat(self):
	'''converts cardlist to format specified in lastplay (card,num) or 0 if invalid'''
	assert self.a.convertToPlayFormat([3,7])==(7,2),'test1'
	assert self.a.convertToPlayFormat([5])==(5,1),'test2'
	assert self.a.convertToPlayFormat([5,6])==0,'test3'
	
	
	
    def testcheckPlay(self):
	'''
	checks to see if a play made by a certain player is valid
	makes sure it is his turn, the play beats the most recently
	played card, cards are all of the same type, and cards are in hand.
	
	player is player number, 
	cardList is the cards from his handList
	
	returns 0 on invalid play, and (card, numberOfCards) if its valid (same format as lastPlay
	'''
	self.a.hand[0].extend([2,17,13,10])
	self.a.currentTurn=0
	assert self.a.checkPlay(0,[2,17])==(2,2),'test0'
	assert self.a.checkPlay(0,[2,13])==0,'test1'
	assert self.a.checkPlay(1,[2])==0,'test2'
	assert self.a.checkPlay(0,[10])==(10,1),'test3'
	self.a.lastPlay=(14,3)
	assert self.a.checkPlay(0,[2])==0,'test4'
	assert self.a.checkPlay(0,[10])==(10,1),'test5'
	
	

	
    def testplayCard(self):
	'''
	plays the list of cards from the player specified
	checks to see if valid play
	then adds cards to stack, changes lastPlay, and performs any special operations(jokers or clears)
	then checks to see if the player has won, then changes the turn if necessary
	'''
	self.a.currentTurn=0
	self.a.playCard(0,[19])
	assert self.a.currentStack==[19],'stack check'
	assert self.a.lastPlay==(4,1)
	
    def testcheckWinner(self):
	''' checks to see if a certain player has won. returns True if they have and False otherwise. '''
	assert self.a.checkWinner(0)==False, 'test0'
	del self.a.hand[0][:]
	del self.a.faceUpCards[0][:]
	del self.a.faceDownCards[0][:]
	assert self.a.checkWinner(0)==True, 'test1'
	
    def testmakeFaceUp(self):
	'''
	takes a input of a card list from the user, makes sure it is valid, and 
	then assigns those cards to be the face up cards and sets the setup flag to True.
	returns True if successful or False if incorrect cards
	'''
	assert self.a.makeFaceUp(1,[51, 14, 4, 42])==False,'t0'
	self.a.setup[1]=False
	assert self.a.makeFaceUp(1,[51, 14, 4, 43]),'t0'
	assert sorted(self.a.faceUpCards[1])==sorted([51, 14, 4, 43]),'t1'
	assert sorted(self.a.hand[1])==sorted([52, 12, 18, 20]),'t1'
	assert self.a.setup[1]==True,'t1'
	assert self.a.currentTurn==0,'t1'
	assert self.a.makeFaceUp(1,[51, 14, 4, 42])==False,'t2'
	
    def testpickupPile(self):
	'''puts current stack into players hand'''
	self.a.currentStack=[1]
	self.a.pickupPile(0)
	assert 1 in self.a.hand[0],'t1'
	assert self.a.currentStack==[],'t2'

    
    def testplayFaceDownCard(self):
	'''plays face down card'''
	self.a.currentTurn=0
	del self.a.hand[0][:]
	del self.a.faceUpCards[0][:]
	self.a.playFaceDownCard(0)
	assert len(self.a.faceDownCards[0])==3,'t1'

	
    def testpickupFaceUpCards(self):
	self.a.currentTurn=0
	del self.a.hand[0][:]
	self.a.pickupFaceUpCards(0)
	assert len(self.a.hand[0])==4, 't1'

    def testGame(self):
        self.a.currentTurn=0
        self.a.playCard(0,[19])
        self.a.playCard(1,[51])
        self.a.playCard(2,[56])
        self.a.playCard(3,[27])
        self.a.playCard(0,[15])
        self.a.playCard(2,[2])
        self.a.playCard(3,[7])
        self.a.playCard(0,[37])
        self.a.playCard(1,[27])
        self.a.playCard(2,[49,3])
        self.a.playCard(3,[21,36])
        self.a.playCard(0,[24,39])
        self.a.playCard(1,[11,56])
        self.a.pickupPile(2)
        self.a.playCard(2,[2])
        self.a.playCard(3,[58])
        assert self.a.currentStack==[2,58]
        
        
        
        
        
        
class DVCTests(unittest.TestCase):
    def setUp(self):
	self.a=DangerVillageComputer.Client('localhost',42)

	
    def testgetHand(self):
	'''
	tests function that does the following:
	
	takes card data from gamestate and returns processable card 
	information by mapping cards to their values
	
	returns a tuple of 
	a list of tuples with values, unique card number
	and a list of values with the number of cards of that value
	'''
	assert self.a.getHand([2,4,53],15)==([(2, 2), (4, 4), (8, 53)], [(1, 2), (1, 4), (1, 8)])

	


    def testgetCards(self):
	'''
	tests function that does the following:
	takes a play in the format value,card and tuples of value,card number
	returns a list of cardnums
	'''
	x,y=self.a.getHand([2,4,53],15)
	assert self.a.getPlay(y,(5,1))==(8,1)

    def testsetupprocess(self):
	'''
	tests that it
	setups cards by simply retruning, can add more logic later
	returns (0,list of cards to be faceup)
	
	does not check the logic only checks that it returns correct types
	'''
	assert len(self.a.setupprocess((1, 1, [0, 33, 3, 44, 14, 15, 18, 59], [50], ([], [], [], []), (5, 1), [True, True, True, True], [2, 0], 15, (0, 1, 0, 0), (0, 8, 0, 9)) ))==2
	

    def testprocess(self):
	'''
	test that function takes raw gamestate data and processes them until it decides output
	does not check the logic only checks that it returns correct types
	'''
	assert len(self.a.process((1, 1, [0, 33, 3, 44, 14, 15, 18, 59], [50], ([], [], [], []), (5, 1), [True, True, True, True], [2, 0], 15, (0, 1, 0, 0), (0, 8, 0, 9)) ))==2
	
	
	
if __name__ == '__main__':
    unittest.main()
    