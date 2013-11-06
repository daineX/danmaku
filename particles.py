# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *

class Particle(object):

    def __init__(self, startPos, startVelo, color=None):
        self.pos = startPos
        self.lifeTime = 0
        if color:
            self.color = color
        else:
            self.color = pygame.Color(0,0,0)
        self.velo = startVelo

    def tick(self):
        if self.lifeTime >= 0:
            self.updatePosition()
            self.updateColor()
            self.lifeTime += 1

    def updatePosition(self):
        self.pos[0] += self.velo[0]
        self.pos[1] += self.velo[1]

    def updateColor(self):
        self.color = pygame.Color(255, 255, 255)

    def draw(self, arr):
        if (0 <= self.pos[0] < Width and 0 <= self.pos[1] < Height):
            arr[self.pos[0] % Width, self.pos[1] % Height] = self.color

    def surfaceDraw(self, Surface, Width, Height):
        #print self.pos
        if (0 <= self.pos[0] < Width and 0 <= self.pos[1] < Height):
            Surface.set_at((int(self.pos[0]), int(self.pos[1])), self.color)


    def __str__(self):
        return 'Particle %s %s %s %s' % (self.pos, self.velo, self.lifeTime, self.color)

class SpriteParticle(pygame.sprite.Sprite):

    def __init__(self, startPos, startVelo, image):
        pygame.sprite.Sprite.__init__(self, self.groups )
        self.pos = startPos
        self.lifeTime = 0
        self.image = image
        self.rect = self.image.get_rect()
        if color:
            self.color = color
        else:
            self.color = pygame.Color(0,0,0)
        self.velo = startVelo

    def tick(self):
        if self.lifeTime >= 0:
            self.updatePosition()
            self.updateColor()
            self.lifeTime += 1

    def update(self, *args):
        pygame.sprite.Sprite.update(self, *args)
        self.tick()
        self.rect.centerx = round(self.pos[0],0)
        self.rect.centery = round(self.pos[1],0)

    def updatePosition(self):
        self.pos[0] += self.velo[0]
        self.pos[1] += self.velo[1]

    def updateColor(self):
        self.color = pygame.Color(255, 255, 255)

    def draw(self, arr):
        pass

    def surfaceDraw(self, Surface, Width, Height):
        pass

    def __str__(self):
        return 'Particle %s %s %s %s' % (self.pos, self.velo, self.lifeTime, self.color)


class Emitter(object):

    def __init__(self, particleCls, pos, maxLifeTime, perFrame, w, h, autoEmit = True, *args):
        self.particleCls = particleCls
        self.pos = pos
        self.maxLifeTime = maxLifeTime
        self.perFrame = perFrame
        self.particles = []
        self.autoEmit = autoEmit
        self.w = w
        self.h = h
        self.bigTick = 0
        self.extraArgs = args
        self.postInit()

    def postInit(self):
        pass

    def preUpdate(self):
        pass

    def postUpdate(self):
        pass

    def update(self):
        self.preUpdate()
        if self.autoEmit:
            self.emit()
        for p in self.particles:
            p.tick()
            if p.lifeTime >= self.maxLifeTime or p.lifeTime < 0:
                if isinstance(p, pygame.sprite.Sprite):
                    p.kill()
                self.particles.remove(p)
                continue
        self.postUpdate()

    def perParticleEmission(self):
        pass

    def lastParticle(self, particle):
        pass

    def emit(self):
        if len(self.particles) < self.maxLifeTime * self.perFrame:
            for i in range(self.perFrame):
                self.perParticleEmission()
                self.particles.append(self.particleCls(self.pos[:], [0,0], *self.extraArgs))
                self.lastParticle(self.particles[-1])
                self.bigTick += 1


    def draw(self, Surface):
        for p in self.particles:
            p.surfaceDraw(Surface, self.w, self.h)
