# Notecard

This is a pygame app to help learn read sheet music.

Connect a midi capable device, and start playing. The notes should
then appear on the staff.

Sample screenshots are provided below.

![C Chord Treble](/gfx/c_chord_treble.png)

![C](/gfx/c.png)

![C Chord Bass](/gfx/c_chord_bass.png)

## Build and run instructions

Attached setup.py file uses py2app to create a Mac OS capable application.

On other platforms:

1. Create virtual environment (``python -m venv venv``)
2. Activate virtual environment (``source venv/bin/activate``)
3. Install packages: ``pip install -r requirements.txt``
4. Run notecard.py: ``python notecard.py``
