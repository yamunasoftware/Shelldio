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

# FILE VARIABLES #

# Files List:
files = []

# PATH FUNCTIONS #

# Relative Path Function:
def relativePath():
  # Gets the Relative Path of the Media Files:
  absolute = os.path.abspath(__file__)
  fileDirectory = os.path.dirname(absolute)

  # Sets the Parent Directory and Returns:
  parentDirectory = os.path.dirname(fileDirectory)
  return os.path.join(parentDirectory, 'media')

# Video Path Function:
def videoPath():
  # Gets the Relative Path of the Media Files:
  absolute = os.path.abspath(__file__)
  fileDirectory = os.path.dirname(absolute)

  # Sets the Parent Directory and Returns:
  parentDirectory = os.path.dirname(fileDirectory)
  return os.path.join(parentDirectory, 'video')

# Is Song There Function:
def isSongThere(song: str):
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
  file = video.download(output_path=videoPath())
  extractAudio(file, name)
  deleteAllFiles('video')
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

# Delete All Files Function:
def deleteAllFiles(type: str):
  # Checks the Case:
  if type == 'video':
    # Removes Video Files:
    for file in os.scandir(videoPath()):
      # Removes the File:
      os.remove(file.path)
  
  elif type == 'media':
    # Removes the Audio Files:
    for file in os.scandir(relativePath()):
      # Removes the File:
      os.remove(file.path)

# Delete File Function:
def deleteFile(type: str, name: str):
  # Checks the Case:
  if type == 'video':
    # Removes the Files:
    os.remove(videoPath() + '\\' + name + '.3gpp')
  
  elif type == 'media':
    # Removes the File:
    os.remove(relativePath() + '\\' + name + '.wav')

# MUSIC QUEUE FUNCTIONS #

# Play List Function:
def playList(queue: list):
  # Mixer Event Startup:
  mixer.init()
  end = pygame.USEREVENT+1
  
  # Queue Setup:
  firstTime = True
  index = 0

  # Sets the Event and Runs:
  mixer.music.set_endevent(end)
  musicThread = threading.Thread(target=playMusicQueue, args=(queue, index, end, firstTime,), daemon=True)
  musicThread.start()

# Play Music Queue Function:
def playMusicQueue(queue: list, index: int, end: int, firstTime: bool):
  # Checks the Case:
  if index < len(queue):
    # Sets the Indexes:
    newIndex = index
    first = firstTime

    # Checks the Case;
    if index == 0 and first == True:
      # Plays the Next Track:
      playMusic(queue[index])
      first = False

    else:
      # Loops through Events:
      for event in pygame.event.get():
        # Checks the Case:
        if event.type == end:
          # Sets the Index:
          newIndex+=1

          # Checks the Case:
          if newIndex < len(queue)-1:
            # Plays the Next Track:
            playMusic(queue[index])
    
    # Recurses:
    time.sleep(0.1)
    musicThread = threading.Thread(target=playMusicQueue, args=(queue, newIndex, end, first,), daemon=True)
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