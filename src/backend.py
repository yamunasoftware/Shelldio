import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import warnings
warnings.filterwarnings("ignore")

from pygame.locals import *
from pygame import mixer

from pytube import YouTube
from moviepy.editor import *

# PATH FUNCTIONS #

# Relative Path Function:
def relativePath():
  # Gets the Relative Path of the Media Files:
  absolute = os.path.abspath(__file__)
  fileDirectory = os.path.dirname(absolute)

  # Sets the Parent Directory and Returns:
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

# MUSIC DOWNLOAD FUNCTIONS #

# Download Music Function:
def downloadMusic(url: str, name: str):
  # Sets the URL and Downloads:
  tube = YouTube(url)
  video = tube.streams.filter().first()

  # Downloads File and Converts:
  file = video.download(output_path=relativePath())
  extractAudio(file, name)
  print('Download Successful\n')

# Extract Audio Function:
def extractAudio(file: str, name: str):
  # Extracts the Audio:
  videoClip = VideoFileClip(file)
  audioClip = videoClip.audio
  audioClip.write_audiofile(relativePath() + '\\' + name + '.wav')

  # Closes the Clip Managers:
  audioClip.close()
  videoClip.close()

# MUSIC INTERFACE FUNCTIONS #

# Play List Function:
def playList(files: list):
  # Loop Variable and Setup:
  mixer.init()
  turns = 0

  # Loops Through List:
  while turns < len(files):
    # Checks the Case;
    if turns == 0:
      # Plays the Files:
      playMusic(files[turns])

    else:
      # Checks the Case:
      if mixer.music.get_busy() == False:
        # Plays the Files:
        playMusic(files[turns])

    turns+=1

# Play Music Function:
def playMusic(file: str):
  # Sets the Path:
  filename = relativePath() + '\\' + file
  mixer.init()

  # Loads and PLays Music:
  mixer.music.load(filename)
  mixer.music.play()

# Pause Music Function:
def pauseMusic():
  # Pauses Music:
  mixer.init()
  mixer.music.pause()

# Unpause Music Function:
def unpauseMusic():
  # Unpauses Music:
  mixer.init()
  mixer.music.unpause()