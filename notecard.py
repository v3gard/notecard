import pygame
import pygame.midi
import sys
import math
import random
import os
from pygame.locals import *
from enum import IntEnum

WHITE = (255,255,255)
BLACK = (0,0,0)

class KeyType(IntEnum):
    c = 0
    csh = 1
    d = 2
    dsh = 3
    e = 4
    f = 5
    fsh = 6
    g = 7
    gsh = 8
    a = 9
    ash = 10
    b = 11

class Key(object):
    def __init__(self, raw_key):
        self.raw_key = raw_key
        self.keytype = KeyType(self.raw_key%12)
        self.clef = "treble"
        self.octave = int(math.floor(raw_key/12))
        if self.raw_key < 60:
            self.clef = "bass"
    
    def __repr__(self):
        return f"{self.clef}: {self.keytype.name}{self.octave}"


class Note(pygame.sprite.Sprite):
    def __init__(self, color, radius, key):
        super().__init__()
        self.hidden = False
        self.image = pygame.Surface([100, 100])
        self.image.fill(WHITE)
        self.image.set_colorkey(WHITE)
        self.color = color
        self.WIDTH=24
        self.HEIGHT=18
        self.OFFSET=40
        self.LINEHEIGHT=40
        self.LINEOFFSET=3
        self.sharp = False
        pygame.draw.ellipse(self.image, self.color, (self.OFFSET,self.OFFSET,self.WIDTH,self.HEIGHT))
        self.drawUpline = False
        self.drawDownline = False
        self.linesDrawn = False
        self.rect = self.image.get_rect()
        self.rect.x = 250
        if "sh" in key.keytype.name:
            self.sharp = True
        if key.keytype.name in ("c","csh") and key.octave == 5:
            y = self.OFFSET+self.HEIGHT/2
            x = self.OFFSET-4
            pygame.draw.line(self.image, self.color, (x, y), (x+self.WIDTH+8, y))
            self.drawUpline = True
            self.rect.y = 150
        elif key.keytype.name in ("d","dsh") and key.octave == 5:
            self.rect.y = 140
            self.drawUpline = True
        elif key.keytype.name in ("e") and key.octave == 5:
            self.rect.y = 133
            self.drawUpline = True
        elif key.keytype.name in ("f","fsh") and key.octave == 5:
            self.rect.y = 122
            self.drawUpline = True
        elif key.keytype.name in ("g","gsh") and key.octave == 5:
            self.rect.y = 112
            self.drawUpline = True
        elif key.keytype.name in ("a","ash") and key.octave == 5:
            self.rect.y = 102
            self.drawUpline = True
        elif key.keytype.name in ("b") and key.octave == 5:
            self.rect.y = 92
            self.drawDownline = True
        elif key.keytype.name in ("c","csh") and key.octave == 6:
            self.rect.y = 82
            self.drawDownline = True
        elif key.keytype.name in ("d","dsh") and key.octave == 6:
            self.rect.y = 72
            self.drawDownline = True
        elif key.keytype.name in ("e") and key.octave == 6:
            self.rect.y = 62
            self.drawDownline = True
        elif key.keytype.name in ("f","fsh") and key.octave == 6:
            self.rect.y = 52
            self.drawDownline = True
        elif key.keytype.name in ("g","gsh") and key.octave == 6:
            self.rect.y = 42
            self.drawDownline = True
        elif key.keytype.name in ("a","ash") and key.octave == 6:
            self.rect.y = 32
            self.drawDownline = True
        elif key.keytype.name in ("b") and key.octave == 6:
            self.rect.y = 22
            self.drawDownline = True
        elif key.keytype.name in ("c","csh") and key.octave == 7:
            self.rect.y = 12
            self.drawDownline = True
        elif key.keytype.name in ("b") and key.octave == 4:
            self.rect.y = 242
            self.drawDownline = True
        elif key.keytype.name in ("a","ash") and key.octave == 4:
            self.rect.y = 252
            self.drawDownline = True
        elif key.keytype.name in ("g","gsh") and key.octave == 4:
            self.rect.y = 262
            self.drawDownline = True
        elif key.keytype.name in ("f","fsh") and key.octave == 4:
            self.rect.y = 272
            self.drawDownline = True
        elif key.keytype.name in ("e") and key.octave == 4:
            self.rect.y = 282
            self.drawDownline = True
        elif key.keytype.name in ("d","dsh") and key.octave == 4:
            self.rect.y = 292
            self.drawDownline = True
        elif key.keytype.name in ("c","csh") and key.octave == 4:
            self.rect.y = 302
            self.drawDownline = True
        elif key.keytype.name in ("b") and key.octave == 3:
            self.rect.y = 312
            self.drawDownline = True
        elif key.keytype.name in ("a","ash") and key.octave == 3:
            self.rect.y = 322
            self.drawDownline = True
        elif key.keytype.name in ("g","gsh") and key.octave == 3:
            self.rect.y = 332
            self.drawDownline = True
        elif key.keytype.name in ("f","fsh") and key.octave == 3:
            self.rect.y = 342
            self.drawDownline = True
        elif key.keytype.name in ("e") and key.octave == 3:
            self.rect.y = 352
            self.drawDownline = True
        elif key.keytype.name in ("d","dsh") and key.octave == 3:
            self.rect.y = 362
            self.drawDownline = True
        elif key.keytype.name in ("c","csh") and key.octave == 3:
            self.rect.y = 372
            self.drawDownline = True
        else:
            self.hidden = True

        if self.sharp:
            font = pygame.font.Font('freesansbold.ttf', 32) 
            text = font.render('#', True, self.color, None)
            textRect = text.get_rect() 
            textRect.center = (50+self.WIDTH, 60-(self.HEIGHT)) 
            self.image.blit(text, textRect)
    
    def show_lines(self):
        if self.linesDrawn == False:
            if self.drawUpline:
                 pygame.draw.line(self.image, self.color, (self.OFFSET+self.WIDTH+(self.LINEOFFSET*-1),self.OFFSET+self.LINEOFFSET), (self.OFFSET+self.WIDTH+(self.LINEOFFSET*-1),self.OFFSET-self.LINEHEIGHT+self.LINEOFFSET))
            if self.drawDownline:
                pygame.draw.line(self.image, self.color, (self.OFFSET+(self.LINEOFFSET),self.OFFSET+self.LINEOFFSET), (self.OFFSET+(self.LINEOFFSET),self.OFFSET+self.LINEHEIGHT+self.LINEOFFSET))

def render_notes(notes, raw_keys):
    for note in notes:
        note.kill()
    keys = [Key(x) for x in raw_keys]
    for key in keys:
        note = Note(BLACK, 10, key)
        if not note.hidden:
            if len(keys) == 1:
                note.show_lines()
            notes.add(note)

def draw_clefs(screen, midi, gclef, fclef):
    screen.fill(WHITE)

    pygame.draw.line(screen, BLACK, [100,100], [500,100], 1)
    pygame.draw.line(screen, BLACK, [100,120], [500,120], 1)
    pygame.draw.line(screen, BLACK, [100,140], [500,140], 1)
    pygame.draw.line(screen, BLACK, [100,160], [500,160], 1)
    pygame.draw.line(screen, BLACK, [100,180], [500,180], 1)
    screen.blit(gclef, (90,47))
    
    # bass clef
    VPOS_BASS = 300
    pygame.draw.line(screen, BLACK, [100,VPOS_BASS + 00], [500,VPOS_BASS + 00], 1)
    pygame.draw.line(screen, BLACK, [100,VPOS_BASS + 20], [500,VPOS_BASS + 20], 1)
    pygame.draw.line(screen, BLACK, [100,VPOS_BASS + 40], [500,VPOS_BASS + 40], 1)
    pygame.draw.line(screen, BLACK, [100,VPOS_BASS + 60], [500,VPOS_BASS + 60], 1)
    pygame.draw.line(screen, BLACK, [100,VPOS_BASS + 80], [500,VPOS_BASS + 80], 1)
    screen.blit(fclef, (90,243))

pygame.init()
pygame.midi.init()
pygame.font.init()

# List all midi devices
midi=True
default_input_id = pygame.midi.get_default_input_id()
if (default_input_id == -1):
    print("No MIDI input devices found.")
    midi=False

if midi:
    inp = pygame.midi.Input(default_input_id)

WIDTH = 640
HEIGHT = 480
TITLE = "Notecard"
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()
refresh_rate = 60 

trebleImg = None
bassImg = None
gclef = pygame.image.load(os.path.join('trebleclef.png'))
fclef = pygame.image.load(os.path.join('bassclef.png'))

draw_clefs(screen, midi, gclef, fclef)

pygame.display.flip()
pygame.display.update()

notes = pygame.sprite.Group()

keys_pressed = []

KEY_PRESSED = 144
KEY_RELEASED = 128

done = False
while not done:
    if midi and inp.poll():
        midievent = inp.read(1000)
        for event in midievent:
            state, key, _, _ = event[0]
            if state == KEY_PRESSED:
                if key not in keys_pressed:
                    keys_pressed.append(key)
            elif state == KEY_RELEASED:
                if key in keys_pressed:
                    keys_pressed.remove(key)
        render_notes(notes, keys_pressed)
    for event in pygame.event.get():
        if event.type == QUIT:
            done = True
    draw_clefs(screen, midi, gclef, fclef)
    notes.draw(screen)
    pygame.display.update()
    clock.tick(refresh_rate)
if midi:
    inp.close()
pygame.quit()
