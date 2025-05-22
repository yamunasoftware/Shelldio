import random
import backend
import sys

# APP UTILITY FUNCTIONS #

# List Songs Function:
def listSongs():
  # Get the Files in Directory:
  files = backend.os.listdir(backend.relativePath())
  newFiles = []

  # Loop Variables:
  counts = 0
  turns = 0

  # Loops through List:
  while counts < len(files):
    # Checks the Case:
    if files[counts].find('.mp3') != -1:
      # Appends the Value:
      newFiles.append(files[counts])

    counts+=1

  # Loops through List:
  while turns < len(newFiles):
    # Prints the Songs:
    print(newFiles[turns].replace('.mp3', ''))
    
    turns+=1

  # Sets the Files:
  backend.files = newFiles

# Handle Commands Function:
def handleCommands(command: str):
  # Checks the Case:
  if command == 'help':
    # Lists the Commands:
    help()

  elif command == 'play':
    # Plays the Music:
    play()

  elif command == 'loop':
    # Loops through Tracks:
    loop()

  elif command == 'pause':
    # Pauses Music:
    pause()

  elif command == 'unpause':
    # Unpauses Music:
    unpause()

  elif command == 'rewind':
    # Rewinds Music:
    rewind()

  elif command == 'timeline':
    # Scrubs through Timeline:
    timeline()

  elif command == 'add':
    # Adds New Music:
    add(False)

  elif command == 'add -d':
    # Adds Music With Delete:
    add(True)

  elif command == 'shuffle':
    # Error Handling:
    try:
      # Gets the Input:
      rawSongs = input('Queue: ')

      # Checks the Case:
      if rawSongs == 'back':
        # Restarts:
        mainApp()

      else:
        # Sets the Songs:
        songs = int(rawSongs)

        # Checks the Case:
        if songs < 0:
          # Restarts Command:
          print('Invalid Queue Number\n')
          handleCommands(command)

        # Shuffles the Music:
        shuffle(songs, current=[])
    
    except BaseException as e:
      # Restarts Command:
      print('Invalid Queue Number\n')
      handleCommands(command)
  
  elif command == 'delete':
    # Deletes File:
    delete()

  elif command == 'delete -a':
    # Deletes All Files:
    deleteAll()

  elif command == 'exit':
    # Ends the Application:
    end()

  # Goes Back to Main Menu:
  print('\n')
  mainApp()

# Main Application Function:
def mainApp():
  # Prints the Songs:
  print('\n')
  listSongs()

  # Starts the Commands:
  command = input('Shelldio >> ')
  handleCommands(command)

# APP CONTROL FUNCTIONS #

# Help Function:
def help():
  # Prints the Commands:
  print('\nhelp\nplay\nloop\npause\nunpause\nrewind\ntimeline\nadd (-d for delete)\nshuffle\ndelete (-a for all)\nexit\nback (inside of command)')

# Play Function:
def play():
  # Error Handling:
  try:
    # Gets the Song Input:
    songInput = input('Track: ')
    rawSongs = input('Queue: ')

    # Checks the Case:
    if songInput == 'back' or rawSongs == 'back':
      # Restarts:
      mainApp()

    else:
      # Sets the Songs:
      songs = int(rawSongs)

      # Checks the Case:
      if songs < 0:
        # Restarts Play:
        print('Invalid Queue Number\n')
        play()

      # Checks the Case:
      if songInput.find('.mp3') != -1:
        # Restarts Play:
        print('Invalid Track\n')
        play()

      else:
        # Checks the Case:
        if backend.isSongThere(songInput):
          # Shuffles:
          shuffle(songs-1, current=[songInput + '.mp3'])

        else:
          # Restarts Play:
          print('Invalid Track\n')
  
  except BaseException as e:
    # Restarts Play:
    print('Invalid Queue Number\n')
    play()

# Loop Tracks Function:
def loop():
  # Error Handling:
  try:
    # Gets the Song Input:
    songInput = input('Track: ')
    rawSongs = input('Queue: ')

    # Checks the Case:
    if songInput == 'back' or rawSongs == 'back':
      # Restarts:
      mainApp()

    else:
      # Sets the Songs:
      songs = int(rawSongs)

      # Checks the Case:
      if songs < 0:
        # Restarts Play:
        print('Invalid Queue Number\n')
        loop()

      # Checks the Case:
      if songInput.find('.mp3') != -1:
        # Restarts Play:
        print('Invalid Track\n')
        loop()

      else:
        # Checks the Case:
        if backend.isSongThere(songInput):
          # Song List:
          musicList = []
          turns = 0

          # Populates Song List:
          while turns < songs:
            # Appends:
            musicList.append(songInput + '.mp3')
            
            turns+=1

          # Plays Music List:
          backend.playListPause(musicList)

        else:
          # Restarts Play:
          print('Invalid Track\n')
  
  except BaseException as e:
    # Restarts Play:
    print('Invalid Queue Number\n')
    loop()

# Pause Function:
def pause():
  # Pauses:
  backend.pauseMusic()

# Unpause Function:
def unpause():
  # Unpauses:
  backend.unpauseMusic()

# Rewind Function:
def rewind():
  # Rewinds:
  backend.unpauseMusic()
  backend.rewindMusic()

# Timeline Function:
def timeline():
  # Error Handling:
  try:
    # Checks the Case:
    if backend.soundObject != None:
      # Prompts User for Number:
      length = backend.getTrackLength()
      number = input('Length: ' + str(round(length)) + '\nSeconds: ')

      # Checks the Case:
      if number == 'back':
        # Restarts:
        mainApp()

      else:
        # Sets the Position:
        position = float(number)

        # Checks the Case:
        if position < 0 or position > length:
          # Restarts Timeline:
          print('Invalid Timeline Number')
          timeline()

        else:
          # Scrubs to Position:
          backend.scrub(position)

  except BaseException as e:
    # Restarts Timeline:
    print('Invalid Timeline Number')
    timeline()  

# Add Function:
def add(delete: bool):
  # Error Handling:
  try:
    # Gets the URL and Name:
    url = input('URL: ')
    name = input('Name: ')

    # Checks the Case:
    if url == 'back' or name == 'back':
      # Restarts:
      mainApp()

    else:
      # Checks the Case:
      if name.find('.mp3') != -1:
        # Restarts Add:
        print('Invalid Name\n')
        add() 

      else:
        # Adds Music:
        backend.downloadMusic(url, name, delete)

  except BaseException as e:
    # Restarts Add:
    print('Invalid YouTube URL\n')
    add()

# Shuffle Function:
def shuffle(songs: int, current: list):
  # Loop Variables:
  musicList = current
  turns = 0

  # Loops through Times:
  while turns < songs:
    # Generates Random Start:
    start = random.randint(0, len(backend.files)-1)
    musicList.append(backend.files[start])

    turns+=1

  # Plays the List of Music:
  backend.playListPause(musicList)

# Delete Function:
def delete():
  # Error Handling:
  try:
    # Folder and File Input:
    type = input('Folder: ')
    name = input('File: ')

    # Checks the Case:
    if type == 'back' or name == 'back':
      # Restarts:
      mainApp()

    else:
      # Runs Deletion:
      backend.deleteFile(type, name)
  
  except BaseException as e:
    # Restarts Delete:
    print('Invalid Inputs\n')
    delete()

# Delete All Function:
def deleteAll():
  # Error Handling:
  try:
    # Folder Input:
    type = input('Folder: ')

    # Checks the Case:
    if type == 'back':
      # Restarts:
      mainApp()

    else:
      # Runs Deletion:
      backend.deleteAllFiles(type)
  
  except BaseException as e:
    # Restarts Delete:
    print('Invalid Folder\n')
    deleteAll()

# End Function:
def end():
  # Exits:
  sys.exit()

# APP RUNNING FUNCTION CALLS #

# App Running Calls:
mainApp()