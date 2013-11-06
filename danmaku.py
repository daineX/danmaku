# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
import random, sys, os, math
from particles import Emitter, Particle, SpriteParticle


difficulties = {0: (10, 0.05, 300),
                1: (30, 0.05, 300),
                2: (60, 0.05, 600),
                3: (120, 0.1, 1200)}



class RandomPositioningEmitter(Emitter):

    def perParticleEmission(self):
        self.pos = [random.randint(0, self.w-1), 0]

    def postUpdate(self):
        for p in self.particles:
            if p.pos[1] >= self.h:
                if isinstance(p, pygame.sprite.Sprite):
                    p.kill()
                self.particles.remove(p)
                continue

class Star(Particle):

    def updatePosition(self):
        if self.lifeTime == 0:
            self.velo = [0, max(0.1, random.random()*8)]
        self.pos[0] += self.velo[0]
        self.pos[1] += self.velo[1]

    def updateColor(self):
        if self.lifeTime == 0:
            mag = random.randint(1,255)
            self.color = pygame.Color(mag, mag, mag)


class SpriteStar(SpriteParticle):

    def __init__(self, startPos, startVelo, image):
        SpriteParticle.__init__(self, startPos, startVelo, image)
        self.origImage = self.image

    def updatePosition(self):
        if self.lifeTime == 0:
            self.velo = [0, max(0.1, random.random()*8)]
        self.pos[0] += self.velo[0]
        self.pos[1] += self.velo[1]
        mag = math.sqrt(self.velo[0]**2 + self.velo[1]**2)
        phi = math.degrees(math.acos(self.velo[0] / mag))
        self.image = pygame.transform.rotate(self.origImage, -phi)

    def updateColor(self):
        if self.lifeTime == 0:
            mag = random.randint(1,255)
            self.color = pygame.Color(mag, mag, mag)


class FireworkEmitter(Emitter):

    def postInit(self):
        self.waitTicks = random.randint(10,40)
        self.maxPerFrame = 10

    def preUpdate(self):
        if not self.waitTicks:
            self.perFrame = self.maxPerFrame
            self.waitTicks = random.randint(10,40)
            self.waitTicks = 15
        else:
            self.perFrame = 0
            self.waitTicks -= 1

    def lastParticle(self, p):
        angle = 360. / self.maxPerFrame * (self.bigTick % 360)
        speed = 3
        p.velo = [speed*math.cos(angle), speed*math.sin(angle)]

class FireworkParticle(SpriteParticle):

    def __init__(self, startPos, startVelo, image):
        SpriteParticle.__init__(self, startPos, startVelo, image)
        self.origImage = self.image
        self.diff = 33.0

    def update(self, msecs):
        self.diff = msecs
        SpriteParticle.update(self)

    def updatePosition(self):
        self.pos[0] += self.velo[0] * self.diff / 33.
        self.pos[1] += self.velo[1] * self.diff / 33.
        mag = math.sqrt(self.velo[0]**2 + self.velo[1]**2)
        phi = math.degrees(math.acos(self.velo[0] / mag))
        if self.velo[1] > 0:
            phi = -phi
        self.image = pygame.transform.rotate(self.origImage, phi)

class Shot(SpriteParticle):

    def __init__(self, startPos, startVelo, image):
        SpriteParticle.__init__(self, startPos, startVelo, image)
        self.origImage = self.image
        self.diff = 33.0
        self.radius = self.image.get_width() / 2

    def update(self, msecs):
        self.diff = msecs
        SpriteParticle.update(self)

    def updatePosition(self):
        if self.lifeTime == 0:
            self.velo = [0, -.5]
        self.pos[0] += self.velo[0] * self.diff
        self.pos[1] += self.velo[1] * self.diff
        mag = math.sqrt(self.velo[0]**2 + self.velo[1]**2)
        phi = math.degrees(math.acos(self.velo[0] / mag))
        if self.velo[1] > 0:
            phi = -phi
        self.image = pygame.transform.rotate(self.origImage, phi)

class ShotEmitter(Emitter):

    def postInit(self):
        self.mod = 1
        self.origPos = self.pos
        self.stride = 10

    def perParticleEmission(self):
        self.pos[1] = self.origPos[1]
        self.pos[0] = self.origPos[0] + self.stride * self.mod
        self.mod = -self.mod

class EngineEmitter(ShotEmitter):

    def postInit(self):
        self.mod = 1
        self.origPos = self.pos
        self.stride = 6

    def lastParticle(self, p):
        angle = math.radians(90 + (-0.5+random.random()) * 45)
        speed = (.7 + random.random()*.3)*4
        p.velo = [speed*math.cos(angle), speed*math.sin(angle)] 
        p.color = pygame.Color(255, 200, 128)

class EngineParticle(Particle):

    def updateColor(self):
        self.color = pygame.Color(*map(lambda x:max(0,x-5), (self.color.r, self.color.g, self.color.b)))


class ExplosionParticle(Particle):

    def updatePosition(self):
        self.pos[0] += self.velo[0]
        self.pos[1] += self.velo[1]
        self.velo[0] -= .1
        self.velo[1] -= .1

    def updateColor(self):
        self.color = pygame.Color(*map(lambda x:max(0,x-7), (self.color.r, self.color.g, self.color.b)))

class Explosion(Emitter):

    def postInit(self):
        self.framesToGo = 0

    def postUpdate(self):
        self.framesToGo = max(0, self.framesToGo - 1)

    def lastParticle(self, p):
       angle = math.radians(random.random() * 360)
       speed = (.1 + random.random()*.9)*4
       p.velo = [speed*math.cos(angle), speed*math.sin(angle)]
       r = int(random.random()*55)
       p.color = pygame.Color(200 + r, 128 + int(random.random()*r), 128)

    def emit(self):
        if self.framesToGo:
            Emitter.emit(self)

    def trigger(self, frames):
        self.framesToGo = frames

class Player(pygame.sprite.Sprite):

    def __init__(self, pos, image, shot):
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.pos = pos
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.centerx, self.rect.centery = self.pos
        self.shotEmitter = ShotEmitter(Shot, self.pos, 800, 2, 600, 800, False, shot)
        self.engine = EngineEmitter(EngineParticle, [self.pos[0], self.pos[1]+15], 50, 10, 600, 800, True)
        self.explosion = Explosion(ExplosionParticle, self.pos, 50, 120, 600, 800, True)
        self.lifes = 3
        self.dead = False
        self.radius = 3.0
        self.bombs = 3

        pygame.mouse.set_pos(300, 800)

    def reset(self):
        pygame.mouse.set_pos(300, 800)
        self.pos = [300, 800]

    def emit(self):
        if not self.dead:
            self.shotEmitter.emit()

    def bomb(self):
        if self.bombs:
            self.bombs -= 1
            destroyRect = pygame.Rect(self.pos[0] - 150, 0, 300, self.pos[1])
            return destroyRect
        return None

    def hit(self):
        self.lifes -= 1
        self.explosion.pos = self.pos
        self.explosion.trigger(10)
        if not self.lifes:
            self.dead = True
            self.kill()
            return True
        return False

    def update(self, pos, *args):
        self.shotEmitter.update()
        self.engine.update()
        self.explosion.update()
        self.pos = pos
        self.rect.centerx, self.rect.centery = self.pos
        self.shotEmitter.origPos = self.pos
        self.engine.origPos = [self.pos[0], self.pos[1]+15]
        pygame.sprite.Sprite.update(self, *args)


class Enemy(pygame.sprite.Sprite):

    def __init__(self, pos, difficulty, image, bullet):
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.pos = pos
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.centerx, self.rect.centery = self.pos
        self.radius = self.image.get_width() / 2
        self.shotEmitter = FireworkEmitter(FireworkParticle, self.pos, 1000, 4, 600, 800, True, bullet)
        self.explosion = Explosion(ExplosionParticle, self.pos, 50, 120, 600, 800, True)
        (maxPerFrame, speed, lifes) = difficulties[difficulty]
        self.shotEmitter.maxPerFrame = maxPerFrame
        self.lifes = lifes
        self.dead = False
        self.speed = speed
        self.count = 0

    def emit(self):
        self.shotEmitter.emit()

    def hit(self):
        self.lifes -= 1
        if self.lifes < 1:
            self.explosion.pos = self.pos
            self.explosion.trigger(25)
            self.dead = True
            self.kill()
            return True
        return False

    def update(self, msecs, *args):
        diff = msecs / 33.
        self.count += diff
        self.explosion.update()
        if not self.dead:
            direction = math.sin(self.count*self.speed)*300
            self.pos[0] = 300 + direction
            self.shotEmitter.update()
            self.rect.centerx, self.rect.centery = self.pos
            self.shotEmitter.origPos = self.pos
            pygame.sprite.Sprite.update(self, *args)

def getInput():
    pygame.event.pump()
    key = pygame.key.get_pressed()
    m1, m2, m3 = False, False, False
    m1, _, _ = pygame.mouse.get_pressed()
    for event in pygame.event.get():
        if event.type == QUIT or key[K_ESCAPE]:
            pygame.quit(); sys.exit()
        if event.type == MOUSEBUTTONUP:
            if event.button == 3:
                m3 = True
    if key[K_m]:
        pygame.mixer.music.pause()
    return m1, m2, m3

def main():

    from optparse import OptionParser

    parser = OptionParser()
    parser.add_option("--difficulty", dest="difficulty", default=0)
    parser.add_option("--easy", dest="difficulty", action="store_const", const=0)
    parser.add_option("--normal", dest="difficulty", action="store_const", const=1)
    parser.add_option("--hard", dest="difficulty", action="store_const", const=2)
    parser.add_option("--lunatic", dest="difficulty", action="store_const", const=3)

    (options, arg) = parser.parse_args()

    music = os.path.join("data", "krach.ogg")
    star = pygame.image.load(os.path.join("data", "star.png"))
    bullet = pygame.image.load(os.path.join("data", "bullet.png"))
    bulletPlayer = pygame.image.load(os.path.join("data", "playerBullet.png"))
    playerSprite = pygame.image.load(os.path.join("data", "player.png"))
    enemySprite = pygame.image.load(os.path.join("data", "enemy.png"))

    pygame.init()
    clock = pygame.time.Clock()

    Width = 600
    Height = 800
    Screen = (Width,Height)
    icon = pygame.Surface((1,1)); icon.set_alpha(0); pygame.display.set_icon(icon)
    pygame.display.set_caption("Particles")
    pygame.mixer.music.load(music)
#    pygame.mixer.music.play(-1)
    Surface = pygame.display.set_mode(Screen)

    bullet = bullet.convert_alpha()
    bulletPlayer = bulletPlayer.convert_alpha()
    playerSprite = playerSprite.convert_alpha()
    enemySprite = enemySprite.convert_alpha()

    starGroup = pygame.sprite.Group()
    SpriteStar.groups = starGroup
    starField = RandomPositioningEmitter(Star, [0,0], Height*8, 3, Width, Height, True)

    bulletGroup = pygame.sprite.Group()
    bulletPlayerGroup = pygame.sprite.Group()
    FireworkParticle.groups = bulletGroup
    Shot.groups = bulletPlayerGroup

    enemyGroup = pygame.sprite.Group()
    Enemy.groups = enemyGroup
    enemy = Enemy([300,300], options.difficulty, enemySprite, bullet)

    font = pygame.font.SysFont("Arial", 60)
    pointsFont = pygame.font.SysFont("Arial", 20)
    points = 0
    fontren = font.render("BULLET HELL!!", True, pygame.Color(255,255,255))

    playerGroup = pygame.sprite.Group()
    Player.groups = playerGroup
    player = Player([300, 800], playerSprite, bulletPlayer)
    pygame.mouse.set_visible(False)
    player.reset()

    gameOver = False
    win = False
    graze = 0
    enemyLifes = difficulties[options.difficulty][2]
    
    while True:
        (m1, m2, m3) = getInput()
        Surface.fill(Color(0,0,0))
        for b in bulletGroup.sprites():
            if not Surface.get_rect().contains(b.rect):
                b.kill()
                enemy.shotEmitter.particles.remove(b)

        msecs = clock.tick(30)
        starField.update()
        starField.draw(Surface)
        enemy.update(msecs)
        enemy.explosion.draw(Surface)
        mousePos = pygame.mouse.get_pos()
        player.update(list(mousePos))
        player.explosion.draw(Surface)

        if not win and not gameOver:
            enemyGroup.draw(Surface)
            if m1:
                player.emit()
            if m3:
                destroyRect = player.bomb()
                if destroyRect:
                    for b in bulletGroup:
                        if destroyRect.contains(b.rect):
                            b.kill()
                            continue
            bulletPlayerGroup.update(msecs)
            bulletPlayerGroup.draw(Surface)
            player.engine.draw(Surface)
            playerGroup.draw(Surface)
            bulletGroup.update(msecs)
            bulletGroup.draw(Surface)

            enemyHits = pygame.sprite.groupcollide(enemyGroup, bulletPlayerGroup, False, False)
            for enemy in enemyHits:
                for bullet in enemyHits[enemy]:
                    if pygame.sprite.collide_circle(enemy, bullet):
                        win = enemy.hit()
                        points += (options.difficulty + 1)*(graze+1)
                        bullet.kill()
                        continue

            playerHits = pygame.sprite.groupcollide(playerGroup, bulletGroup, False, False)
            hits = False
            for player in playerHits:
                for bullet in playerHits[player]:
                    if pygame.sprite.collide_circle(player, bullet):
                        gameOver = player.hit()
                        player.reset()
                        bulletPlayerGroup.empty()
                        bulletGroup.empty()
                        hits = True
                        break
                    else:
                        graze += 1
                if hits:
                    break
            if options.difficulty == 3:
                r = random.randint(0,360)
                rotatedFont = pygame.transform.rotate(fontren, r)
                Surface.blit(rotatedFont, (random.randint(0,Width),random.randint(0,Height)))

        else:
            if win:
                player.engine.draw(Surface)

                playerGroup.draw(Surface)
                f = font.render("You WIN!", True, pygame.Color(255,255,255))
                w = f.get_width()
                Surface.blit(f, ((Width - w) / 2, Height / 2 - 100))

            if gameOver:
                enemyGroup.draw(Surface)
                bulletGroup.update(msecs)
                bulletGroup.draw(Surface)                
                f = font.render("You LOSE!", True, pygame.Color(255,255,255))
                w = f.get_width()
                Surface.blit(f, ((Width - w) / 2, Height / 2 - 100))

        f = pointsFont.render("Points: %s" % points, True, pygame.Color(255, 255, 255))
        Surface.blit(f, (0,0))
        pygame.display.flip()
        pygame.display.set_caption("You: %d, Enemy: %.1f%%, Graze: %d, Bombs: %d, FPS: %.2f" % (player.lifes, float(enemy.lifes) / enemyLifes * 100, graze, player.bombs, clock.get_fps()))


if __name__ == "__main__":
    main()
