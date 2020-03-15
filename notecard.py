import pygame
import pygame.midi
import sys
import math
import random
from pygame.locals import *
from enum import IntEnum

WHITE = (255,255,255)
RED = (255,0,0)
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
        self.image = pygame.Surface([100, 100])
        self.image.fill(WHITE)
        self.image.set_colorkey(WHITE)
        WIDTH=24
        HEIGHT=18
        OFFSET=40
        LINEHEIGHT=40
        LINEOFFSET=3
        pygame.draw.ellipse(self.image, color, (OFFSET,OFFSET,WIDTH,HEIGHT))
        pygame.draw.line(self.image, color, (OFFSET+WIDTH+(LINEOFFSET*-1),OFFSET+LINEOFFSET), (OFFSET+WIDTH+(LINEOFFSET*-1),OFFSET-LINEHEIGHT+LINEOFFSET))
        self.rect = self.image.get_rect()
        self.rect.x = 200
        if key.keytype.name == "c" and key.octave == 5:
            y = OFFSET+HEIGHT/2
            x = OFFSET-4
            pygame.draw.line(self.image, color, (x, y), (x+WIDTH+8, y))
            self.rect.y = 150
        elif key.keytype.name == "d" and key.octave == 5:
            self.rect.y = 140
        elif key.keytype.name == "e" and key.octave == 5:
            self.rect.y = 133
        elif key.keytype.name == "f" and key.octave == 5:
            self.rect.y = 122
        elif key.keytype.name == "g" and key.octave == 5:
            self.rect.y = 112
        elif key.keytype.name == "a" and key.octave == 5:
            self.rect.y = 102
        elif key.keytype.name == "b" and key.octave == 5:
            self.rect.y = 92
        elif key.keytype.name == "c" and key.octave == 6:
            self.rect.y = 82
        elif key.keytype.name == "d" and key.octave == 6:
            self.rect.y = 72
        elif key.keytype.name == "e" and key.octave == 6:
            self.rect.y = 62
        elif key.keytype.name == "f" and key.octave == 6:
            self.rect.y = 52
        elif key.keytype.name == "g" and key.octave == 6:
            self.rect.y = 42
        elif key.keytype.name == "a" and key.octave == 6:
            self.rect.y = 32
        elif key.keytype.name == "b" and key.octave == 6:
            self.rect.y = 22
        else:
            self.rect.x = random.randint(0,100)
            self.rect.y = random.randint(0,100)
        

def render_notes(notes, raw_keys):
    for note in notes:
        note.kill()
    keys = [Key(x) for x in raw_keys]
    for key in keys:
        note = Note(BLACK, 10, key)
        notes.add(note)
    print(keys)

def draw_clefs(screen):
    screen.fill(WHITE)
    # treble clef
    pygame.draw.line(screen, BLACK, [100,100], [500,100], 1)
    pygame.draw.line(screen, BLACK, [100,120], [500,120], 1)
    pygame.draw.line(screen, BLACK, [100,140], [500,140], 1)
    pygame.draw.line(screen, BLACK, [100,160], [500,160], 1)
    pygame.draw.line(screen, BLACK, [100,180], [500,180], 1)
    
    # bass clef
    VPOS_BASS = 300
    pygame.draw.line(screen, BLACK, [100,VPOS_BASS + 00], [500,VPOS_BASS + 00], 1)
    pygame.draw.line(screen, BLACK, [100,VPOS_BASS + 20], [500,VPOS_BASS + 20], 1)
    pygame.draw.line(screen, BLACK, [100,VPOS_BASS + 40], [500,VPOS_BASS + 40], 1)
    pygame.draw.line(screen, BLACK, [100,VPOS_BASS + 60], [500,VPOS_BASS + 60], 1)
    pygame.draw.line(screen, BLACK, [100,VPOS_BASS + 80], [500,VPOS_BASS + 80], 1)

pygame.init()
pygame.midi.init()

# List all midi devices
mididevices = pygame.midi.get_count()
if (mididevices == 0):
    print("No MIDI devices found.")
    exit(0)
for x in range(0, mididevices):
    print(pygame.midi.get_device_info(x))
inp = pygame.midi.Input(0)

WIDTH = 800
HEIGHT = 600
TITLE = "Notecard"
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()
refresh_rate = 60

draw_clefs(screen)

pygame.display.flip()
pygame.display.update()

notes = pygame.sprite.Group()

keys_pressed = []

KEY_PRESSED = 144
KEY_RELEASED = 128

done = False
while not done:
    if inp.poll():
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
            pygame.quit()
            exit(0)
    draw_clefs(screen)
    notes.draw(screen)
    pygame.display.update()
    clock.tick(refresh_rate)
pygame.quit()
