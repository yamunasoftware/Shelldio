import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

from pygame.locals import *
from pygame import mixer

# Relative Path Function:
def relativePath():
  # Gets the Relative Path of the Media Files:
  absolute = os.path.abspath(__file__)
  fileDirectory = os.path.dirname(absolute)
  parentDirectory = os.path.dirname(fileDirectory)
  return os.path.join(parentDirectory, 'media')

# Is Song There Function:
def isSongThere(files: list, song: str):
  # Loop Variable:
  returnValue = False
  turns = 0

  # Loops through List:
  while turns < len(files):
    # Checks the Case:
    if files[turns] == (song + '.wav'):
      # Breaks Loop:
      returnValue = True
      break

    turns+=1
  
  # Returns the Value:
  return returnValue

# Play List Function:
def playList(files: list):
  # Loop Variable and Setup:
  mixer.init()
  turns = 0

  # Loops Through List:
  while turns < len(files):
    # Checks the Case:
    if mixer.music.get_busy() == False:
      # Plays the Files:
      playMusic(files[turns])

    turns+=1

# Play Music Function:
def playMusic(file: str):
  # Plays the Music:
  filename = relativePath() + '\\' + file
  mixer.init()
  mixer.music.load(filename)
  mixer.music.play()

# Pause Music Function:
def pauseMusic():
  mixer.init()
  mixer.music.pause()

# Unpause Music Function:
def unpauseMusic():
  mixer.init()
  mixer.music.unpause()