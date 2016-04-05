import pygame
import random
import numpy as np
import math

def cos(n):
	return math.cos(math.radians(n))
	
def sin(n):
	return math.sin(math.radians(n))

def levelGen(size):
	world = np.chararray((size,size))
	world[:]='.'
	world[0,]='|'
	world[-1,]='|'
	world[:,0]='|'
	world[:,-1]='|'
	def r(): return random.randint(1,size-2)
	
	area = size**2
	density = float(world.count('|').sum()-size*4)/float(area)
	'''
	while density <0.15:
		x,y=r(),r()
		for i in range(random.randint(1,7)):
			world[x%size,y%size]='|'
			next = random.choice([-1,1])
			if random.randint(0,1):
				x+=next
			else: 
				y+=next
			density = float(world.count('|').sum()-size*4)/float(area)
	'''
	#sets spawnpoint
	world[r(),r()]=random.choice(['N','E','S','W'])

	world=  '\n'.join(map(''.join,world.tolist()))
	return  world
	
class LEVEL:
	def __init__(self, mapSize):
		self.readMaP(mapSize)
		self.mapSize = mapSize
		self.characters = []
	
	def readMaP(self,mapSize):
		
		f = levelGen(mapSize)
		f=f.split('\n')
		self.MAP={}
		
		directions = {'N':0,'E':90,'S':180,'W':270}
		#print ' ',''.join(map(str,range(9)))
		#print len(f)
		for y in range(len(f)):
		
			#print f[y],len(f[y])
			for x in range(len(f[y])):
				if f[y][x] in directions: 
					self.angle = directions[f[y][x]]
					self.pos	= (y,x) 
				#print f[y][x],
				self.MAP[x,y]=f[y][x]
		#print self.angle,self.pos
	def add_hero(self,hero):
		self.characters.append(hero)
		
	def __str__(self):
		toprint =self.MAP.copy() 
		for i in self.characters:
			x,y = i.location
			x,y = int(x),int(y)
			toprint[x,y]='X'
		width = (max(map(lambda x: x[0],self.MAP.keys())))
		height= (max(map(lambda x: x[1],self.MAP.keys())))
		#print height,width
		#print width,height
		out = []
		map(lambda x: out.append([' ']*(width+1)),range(height+1))#
		for a,b in toprint.iteritems():
			i,j = a
			out[j][i]=b
		out  = map(''.join, out)
		return '\n'.join(out)
	
	def moveNom(self):
		def r(): return random.randint(1,self.mapSize -2)
		while True:
			x,y = r(),r()
			if self.MAP[x,y] in ['N','E','S','W','|']:continue
			self.MAP[x,y]='O'
			break
	
	
class Character:
	def __init__(self,location,direction, world):
		self.angle = direction 
		self.location= map(float,location)
		x,y = self.location
		self.location=y,x
		self.world = world
		world.add_hero(self)
		self.collidables = ['|','O']
		
		self.steps= pygame.mixer.Sound('resources/steps.wav')
		


		
	def loc(self):
		return self.location,self.angle

	def rotate(self,angle):
		self.angle+=angle
		self.angle = self.angle%360

	def move(self,forward=0,right=0, colisions='|', colide=True):
		curr = self.location
		X = forward*cos(self.angle)
		Y = forward*sin(self.angle)		
		X -= right*sin(self.angle)
		Y += right*cos(self.angle)	
		x,y = self.location
		self.location = x+X,y+Y
		standing_on = self.inTile()
		if colide:self.steps.play(1)
		if standing_on in colisions:
			if colide:self.location =curr
			return ('Collision',standing_on)
		return ('StandingOn',standing_on)

	def cast_view(self):
		original_coords= self.location
		original_angle = self.angle
		scan = []
		#print map(lambda x: (original_angle+fov*float(x)/W)%360,range(-W/2,W/2))
		for angle in range(-W/2,W/2):
			angle = float(angle)/(W/2)* fov/2.0
			self.angle +=angle
			n=0
			#self.rotate(angle)
			#print 'ANGLE cast:',angle,
			out = False
			castSpeed = 0.25
			fineSpeed = -0.01
			changeCol=True
			while n<drawDist:
				standing_on = self.move(forward=castSpeed,
										colisions='|O',
										colide = False)
				n+=castSpeed
				while 'Collision'== standing_on[0]:
					X,Y = self.location	
					if 'O' == standing_on[1]:
						changeCol=False
						color=(255,255,255)
					standing_on = self.move(forward=fineSpeed,
											colisions='|O',
											colide = False)
					n+=fineSpeed
					if not 'Collision'== standing_on[0]:
						if changeCol:
							X,Y = int(X), int(Y)
							color = ((100+Y+X**Y) %255,(200+X+Y**X)%255,X*Y%255)
						#print n,standing_on, self.location
						scan.append((n,color))
						out = True
						break
						
				if out:break
			#print  self.angle
			if n>= drawDist: scan.append(drawDist,(0,0,0))
			#print angle,self.angle,n

			self.location=original_coords
			self.angle=original_angle
		#print original_angle
		return scan
	
	def inTile(self):
		x,y = self.location
		return self.world.MAP[int(x),int(y)]
	
	def intLoc(self):
		x,y = self.location
		return int(x),int(y)
	
H=720
W=1280
#1280x720
H,W = 400,600
fov = 45
screenSize = W,H
fps = 20
speed = 5.0
speed = speed/fps
FineSpeed= -0.01
drawDist = 100
fontSize = 30
ylim=H/3
black = (50  ,50  ,50  )
white = (255,255,255)
red	= (255,0  ,0  )
sky	= (0, 255, 255)
def grey(value,max=20):
	return (255-255*value/max,
			255-255*value/max,
			255-255*value/max)

			
			
pygame.init()
bite = pygame.mixer.Sound('resources/bite.wav')
gameDisplay = pygame.display.set_mode(screenSize, pygame.FULLSCREEN)
END = False
while not END:
	pygame.display.set_caption('the castle of py')
	clock = pygame.time.Clock()
	font = pygame.font.SysFont("monospace", fontSize)
	pygame.mouse.set_visible(False)
	recordUser, highScore = open('record.txt','r').read().split('\t')

	level = LEVEL(20)
	hero  = Character(level.pos,level.angle,level)

	prev = hero.intLoc()
	level.moveNom()
	hist=[(0,0)]*3
	score = 0
	#hero.cast_view()
	showGUI = True
	yAngle = 0
	restart=False
	while not restart:
		#END = True
		for event in pygame.event.get():
			if event.type == pygame.QUIT: 
				END=True
			if event.type==4:
				posX,posY = event.pos
				posX,posY = posX-W/2,posY-H/2
			
				hero.rotate(posX)
				yAngle+=posY
				if yAngle< -ylim:yAngle=-ylim
				if yAngle> ylim:yAngle=ylim
				pygame.mouse.set_pos((W/2,H/2))
			if event.type ==pygame.KEYDOWN:
				keyPress = event.unicode
				#print repr(keyPress)
				if keyPress=='\x1b':END = True
				
				#WASD movements

				if keyPress=='m':
					if showGUI==False:showGUI=True
					elif showGUI==True:showGUI=False
				if keyPress=='r':
					restart = True
			if event.type ==pygame.KEYUP:
				pass
				#print event
				#keyPress = event.unicode
				#print repr(keyPress)
		if END:break

		for keys ,pressed in enumerate(pygame.key.get_pressed()):
			if pressed:
				
				keyPress = pygame.key.name(keys)
				if keyPress=='w': 
					hero.move(forward=speed)
				if keyPress=='s': 
					hero.move(forward=-speed)
				if keyPress=='a': 
					hero.move(right=-speed)
				if keyPress=='d': 
					hero.move(right=speed)
				if keyPress=='q': 
					hero.rotate(-5)
				if keyPress=='e': 
					hero.rotate(5)
		
		
		#monitors positions
		now = hero.intLoc()
		
		if now != prev :
			hist.append(now)
			level.MAP[random.choice(hist[:-2])]='|'
			prev = now
			
		if hero.inTile()=='O':
			bite.play()

			level.moveNom()
			level.MAP[hero.intLoc()]='_'
			score+=len(hist)
		
		
		#raycasts the map
		# import matplotlib.pyplot as plt
		# plt.plot(map(lambda x: x[0],hero.cast_view()))
		# plt.show()
		# break
		for x,distcol in enumerate(hero.cast_view()):
			dist ,col = distcol
			if dist<0:dist=0.001
			wallFraction = 1/dist
			if wallFraction>1:wallFraction=1
			spacer = int((H-H*wallFraction)/2)
			wall = int(H*wallFraction)
			gameDisplay.fill(sky,((x,0),(1,spacer+yAngle)))
			gameDisplay.fill(col,((x,spacer+yAngle),(1,wall)))
			gameDisplay.fill((100,100,100),((x,spacer+wall+yAngle),(1,spacer-yAngle)))

		pygame.display.set_caption(str(map(lambda x: round(x,3),hero.location))+' '+str(hero.angle)+' '+hero.inTile())

		if showGUI:
			linePos = 0
			#for i in str(level).split('\n'):
			#	text = font.render(i, True, (0, 0, 0))
			#	gameDisplay.blit(text,(0,linePos))
			#	linePos+=fontSize
			#a,b = hero.loc()
			#a = map(int,a)
			
			#text = font.render(str(a)+' '+str(b),True, (0, 0, 0))
			#gameDisplay.blit(text,(10,linePos))
			text = font.render('High score: '+highScore+' by '+recordUser,True, (0, 0, 0))
			gameDisplay.blit(text,(10,linePos))
		
			text = font.render('Score: '+str(score),True, (0, 0, 0))
			gameDisplay.blit(text,(10,linePos+fontSize))
		
		pygame.display.update()
		clock.tick(fps)

	if score > int(highScore): 

		name = ""
		#font = pygame.font.Font(None, 50)
		doneName=False
		while not doneName:
			for evt in pygame.event.get():
					if evt.type == pygame.KEYDOWN:
						if evt.unicode.isalpha():
							name += evt.unicode
						elif evt.key == pygame.K_BACKSPACE:
							name = name[:-1]
						elif evt.key == pygame.K_RETURN:
							doneName = True
							
			gameDisplay.fill((0, 0, 0))
			text = font.render('You`ve made a new record: '+str(score),True, (255,255,255))
			gameDisplay.blit(text,(10,10))
			text = font.render('What shall we remember you by?',True,  (255, 255, 255))
			gameDisplay.blit(text,(10,10+fontSize))
			block = font.render(name, True, (255, 255, 255))
			rect = block.get_rect()
			rect.center = gameDisplay.get_rect().center
			gameDisplay.blit(block, rect)
			pygame.display.flip()
		open('record.txt','w').write(name+'\t'+str(score))
		doneName=False
pygame.quit()
					


