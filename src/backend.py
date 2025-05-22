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

# BACKEND VARIABLES #

# Playback Variables:
files = []
soundObject = None

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
    if files[turns] == (song + '.mp3'):
      # Breaks Loop:
      returnValue = True
      break

    turns+=1
  
  # Returns the Value:
  return returnValue

# MUSIC DOWNLOAD FUNCTIONS #

# Download Music Function:
def downloadMusic(url: str, name: str, delete: bool):
  # Gets Audio from Downloaded Video:
  specifyDownload(url, name)
  extractAudio(getDefaultDownload(name), name)

  # Checks the Case:
  if delete == True:
    # Deletes the Files:
    deleteFile('video', name)

  # Success Notification:
  print('Download Successful\n')

# Specify Download Function:
def specifyDownload(url: str, name: str):
  # Downloads the Video with Filename:
  YouTube(url).streams.first().download(filename=getDefaultDownload(name))

# Extract Audio Function:
def extractAudio(file: str, name: str):
  # Extracts the Audio:
  videoClip = VideoFileClip(file)
  audioClip = videoClip.audio
  audioClip.write_audiofile(relativePath() + '\\' + name + '.mp3')

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
    os.remove(relativePath() + '\\' + name + '.mp3')

# MUSIC QUEUE FUNCTIONS #

# Play List Pause Function:
def playListPause(queue: list):
  # Plays the List:
  pauseMusic()
  playList(queue)

# Play List Function:
def playList(queue: list):
  # Mixer Event Startup:
  mixer.init()
  end = pygame.USEREVENT+1
  mixer.music.set_endevent(end)

  # Queue Execution:
  threading.Thread(target=playMusicQueue, args=(queue, end,), daemon=True).start()
  threading.excepthook = exit

# Play Music Queue Function:
def playMusicQueue(queue: list, end: int):
  # Loop Setup:
  turns = 0
  playMusic(queue[turns])
  
  # Loops through Queue:
  while turns < len(queue):
    # Loops through Events:
    for event in pygame.event.get():
      # Checks the Case:
      if event.type == end:
        # Plays the Music:
        turns+=1
        playMusic(queue[turns])
    
    # Waits:
    time.sleep(2)
          
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

  # Sets the Sound Object:
  global soundObject
  soundObject = mixer.Sound(filename)

  # Loads and Plays Music:
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

# Rewind Music Function:
def rewindMusic():
  # Rewinds:
  mixer.init()
  mixer.music.rewind()

# MUSIC SCRUBBING FUNCTIONS #

# Scrub Function:
def scrub(timestamp: float):
  # Sets the Position:
  mixer.init()
  mixer.music.play(start=timestamp)

# Get Track Length Function:
def getTrackLength():
  # Checks the Case:
  if soundObject != None:
    # Returns the Length:
    return soundObject.get_length()
  
  else:
    # Returns the Default:
    return -1