import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import time

import warnings
warnings.filterwarnings("ignore")

import pygame
import threading

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

# MUSIC QUEUE FUNCTIONS #

# Play List Function:
def playList(files: list):
  # Mixer Event Startup:
  mixer.init()
  end = pygame.USEREVENT+1
  
  # Queue Setup:
  firstTime = True
  index = 0

  # Sets the Event and Runs:
  mixer.music.set_endevent(end)
  musicThread = threading.Thread(target=playMusicQueue, args=(files, index, end, firstTime,), daemon=True)
  musicThread.start()

# Play Music Queue Function:
def playMusicQueue(files: list, index: int, end: int, firstTime: bool):
  # Checks the Case:
  if index < len(files):
    # Sets the Indexes:
    newIndex = index
    first = firstTime

    # Checks the Case;
    if index == 0 and first == True:
      # Plays the Next Track:
      playMusic(files[index])
      first = False

    else:
      # Loops through Events:
      for event in pygame.event.get():
        # Checks the Case:
        if event.type == end:
          # Sets the Index:
          newIndex+=1

          # Checks the Case:
          if newIndex < len(files)-1:
            # Plays the Next Track:
            playMusic(files[index])
    
    # Recurses:
    time.sleep(0.1)
    musicThread = threading.Thread(target=playMusicQueue, args=(files, newIndex, end, first,), daemon=True)
    musicThread.start()

# MUSIC INTERFACE FUNCTIONS #

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