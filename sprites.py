# Sprites

import pygame
from settings import *
import random
import numpy as np



class Agent(pygame.sprite.Sprite):
    def __init__(self, identifier, health, pos, layout, risk):
        pygame.sprite.Sprite.__init__(self)
        self.id = identifier
        self.hp = health
        self.risk = risk
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect()

        self.layout = layout
        self.plan   = []
        self.dest   = [ [index, row.index('E')] for index, row in enumerate(self.layout) if 'E' in row][0]

        self.x = random.randrange(0, len(self.layout))
        self.y = random.randrange(0, len(self.layout[0]))

        while(self.layout[self.x][self.y] == 'W'):
            self.x = random.randrange(0, len(self.layout))
            self.y = random.randrange(0, len(self.layout[0]))
        
        
    def move(self, dx=0, dy=0):
        self.x += dx
        self.y += dy
    
    def update(self):
        self.move(dx = (self.plan[0] - self.x), dy = (self.plan[1] - self.y))
        self.rect.x = self.x * TILESIZE 
        self.rect.y = self.y * TILESIZE
        
        #if i < len(self.plan): self.move(dx = (self.plan[i][0] - self.x), dy = (self.plan[i][1] - self.y))

    #update my vision of the layout only in the range of (self.x +- RANGE, self.y +- RANGE)
    def percept(self, layout):
    	x0 = self.x-RANGE
    	y0 = self.y-RANGE 
    	x1 = self.x+RANGE
    	y1 = self.y+RANGE
    	if (x0 < 0):
    		x0 = 0
    	if (y0 < 0):
    		y0 = 0
    	if (x1 > len(layout)-1):
    		x1 = len(layout)-1
    	if (y1 > len(layout[0])-1):
    		y1 = len(layout[0])-1
    	for i in range(x0, x1+1):
    		for j in range(y0, y1+1):
    			self.layout[i][j] = layout[i][j]

    def plan_(self):
    	self.plan = self.bfs()

    def panic(self):
    	return [self.x, self.y]

    def bfs(self):
        source  = [self.x, self.y]
        dest    = self.dest
       	visited = [[0 for _ in range(len(self.layout))] for _ in range(len(self.layout))]
        queue   = []
        path    = []
        prev    = []

        if (source == dest):
        	return source

        queue.append(source)
        visited[source[0]][source[1]] = 1
        
        row = [-1, 0, 0, 1]
        col = [0, -1, 1, 0]
        
        while (len(queue) > 0):
            cur = queue.pop(0)
            if(cur == dest): break

            for i in range(len(row)):
                x = cur[0] + row[i]
                y = cur[1] + col[i]

                if (x < 0 or y < 0 or x > len(self.layout) or y > len(self.layout[0])): continue
                if(self.layout[x][y] != 'W' and self.layout[x][y] != 'F' and visited[x][y] == 0):
                    visited[x][y] = 1
                    l = [x, y]
                    queue.append(l)
                    prev.append([l, cur])       # prev = [ [no, predecessor] ]

        if (not visited[dest[0]][dest[1]]):
        	return self.panic()

        at = dest
        while at != source:
            path.append(at)
            for i in range(len(prev)):
                if(at == prev[i][0]): 
                	at = prev[i][1]
        path.append(source)
        path.reverse()
        #return path

        return path[1] #onde é q quero estar a seguir


class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = self.x * TILESIZE 
        self.rect.y = self.y * TILESIZE

class Fire(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.image.fill(ORANGE)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = self.x * TILESIZE 
        self.rect.y = self.y * TILESIZE