import random
import backend

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
    if files[counts].find('.wav') != -1:
      # Appends the Value:
      newFiles.append(files[counts])

    counts+=1

  # Loops through List:
  while turns < len(newFiles):
    # Prints the Songs:
    print(newFiles[turns].replace('.wav', ''))
    
    turns+=1

  # Returns the Files:
  return newFiles

# Handle Commands Function:
def handleCommands(files: list, command: str):
  # Checks the Case:
  if command == 'help':
    # Lists the Commands:
    help()

  elif command == 'play':
    # Plays the Music:
    play(files)

  elif command == 'pause':
    # Pauses Music:
    pause()

  elif command == 'unpause':
    # Unpauses Music:
    unpause()

  elif command == 'add':
    # Adds New Music:
    add()

  elif command == 'shuffle':
    # Error Handling:
    try:
      # Gets the Input:
      songs = int(input('Queue: '))

      # Checks the Case:
      if songs < 0:
        # Restarts Command:
        print('Invalid Queue Number\n')
        handleCommands(files, command)

      # Shuffles the Music:
      shuffle(files, songs, current=[])
    
    except Exception:
      # Restarts Command:
      print('Invalid Queue Number\n')
      handleCommands(files, command)

  elif command == 'exit':
    # Ends the Application:
    quit()

  # Goes Back to Main Menu:
  print('\n')
  mainApp()

# Main Application Function:
def mainApp():
  # Start the App:
  localFiles = listSongs()
  command = input('Shelldio >> ')
  handleCommands(localFiles, command)

# APP CONTROL FUNCTIONS #

# Help Function:
def help():
  # Prints the Commands:
  print('\nhelp\nplay\npause\nunpause\nadd\nshuffle\nexit\n')

# Play Function:
def play(files: list):
  # Error Handling:
  try:
    # Gets the Song Input:
    songInput = input('Track: ')
    songs = int(input('Queue: '))

    # Checks the Case:
    if songs < 0:
      # Restarts Play:
      print('Invalid Queue Number\n')
      play(files)

    # Checks the Case:
    if songInput.find('.wav') != -1:
      # Restarts Play:
      print('Invalid Song\n')
      play(files)

    else:
      # Checks the Case:
      if backend.isSongThere(files, songInput):
        # Shuffles:
        shuffle(files, songs, current=[songInput + '.wav'])

      else:
        # Restarts Play:
        print('Invalid Song\n')
  
  except Exception:
    # Restarts Play:
    print('Invalid Queue Number\n')
    play(files)

# Pause Function:
def pause():
  # Pauses:
  backend.pauseMusic()

# Unpause Function:
def unpause():
  # Unpauses:
  backend.unpauseMusic()

# Add Function:
def add():
  # Error Handling:
  try:
    # Gets the URL and Name:
    url = input('URL: ')
    name = input('Name: ')

    # Checks the Case:
    if name.find('.wav') != -1:
      # Restarts Add:
      print('Invalid Name\n')
      add() 

    else:
      # Adds Music:
      backend.downloadMusic(url, name)

  except Exception:
    # Restarts Add:
    print('Invalid YouTube URL\n')
    add()

# Shuffle Function:
def shuffle(files: list, songs: int, current: list):
  # Loop Variables:
  musicList = current
  turns = 0

  # Loops through Times:
  while turns < songs:
    # Generates Random Start:
    start = random.randint(0, len(files)-1)
    musicList.append(files[start])

    turns+=1

  # Plays the List of Music:
  backend.playList(musicList)

# APP RUNNING FUNCTION CALLS #

# App Running Calls:
mainApp()