import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import time

import warnings
warnings.filterwarnings("ignore")

import pygame
import threading

from pygame.locals import *
from pygame import mixer

from youtube_dl import YoutubeDL
from moviepy.editor import *

# BACKEND VARIABLES #

# List Variables:
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
  # Gets Audio from Downloaded Video:
  specifyDownload(url, name)
  extractAudio(getDefaultDownload(name), name)

  # Resets the Folder:
  deleteAllFiles('video')
  print('Download Successful\n')

# Specify Download Function:
def specifyDownload(url: str, name: str, **options):
  # Downloads the Video with Filename:
  options['outtmpl'] = getDefaultDownload(name)
  with YoutubeDL(options) as video:
    video.download([url])

# Extract Audio Function:
def extractAudio(file: str, name: str):
  # Extracts the Audio:
  videoClip = VideoFileClip(file)
  audioClip = videoClip.audio
  audioClip.write_audiofile(relativePath() + '\\' + name + '.wav')

  # Closes the Clip Managers:
  audioClip.close()
  videoClip.close()

# Get Default Download Function:
def getDefaultDownload(name: str):
  # Returns the Default:
  return videoPath() + '\\' + name + '.mp4'

# DELETION FUNCTIONS #

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
    os.remove(videoPath() + '\\' + name + '.mp4')
  
  elif type == 'media':
    # Removes the File:
    os.remove(relativePath() + '\\' + name + '.wav')

# MUSIC QUEUE FUNCTIONS #

# Play List Function:
def playList(queue: list):
  # Mixer Event Startup:
  mixer.init()
  end = pygame.USEREVENT+1
  mixer.music.set_endevent(end)
  
  # Queue Setup:
  index = 0
  firstTime = True

  # Queue Execution:
  threading.Thread(target=playMusicQueue, args=(queue, index, end, firstTime,), daemon=True).start()
  threading.excepthook = exit

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
    playMusicQueue(queue, newIndex, end, first)

# Exit Function: 
def exit(args):
  # Exits:
  sys.exit()

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