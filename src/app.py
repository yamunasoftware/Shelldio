import random
import backend

# List Songs Function:
def listSongs():
  # Get the Files in Directory:
  files = backend.os.listdir(backend.relativePath())
  turns = 0

  # Loops through List:
  while turns < len(files):
    # Prints the Songs:
    print(files[turns].replace('.wav', ''))
    
    turns+=1

  # Returns the Files:
  return files

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

  elif command == 'shuffle':
    # Error Handling:
    try:
      # Shuffles the Music:
      songs = int(input('Queue: '))
      shuffle(files, songs)
    
    except ValueError:
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

# APP CONTROLS #

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
    if backend.isSongThere(files, songInput):
      # Queues the Song:
      backend.playMusic(songInput + '.wav')

    # Shuffles the Music:
    shuffle(files, songs)
  
  except ValueError:
    # Restarts Shuffle:
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

# Shuffle Function:
def shuffle(files: list, songs: int):
  # Loop Variables:
  musicList = []
  turns = 0

  # Loops through Times:
  while turns < songs:
    # Generates Random Start:
    start = random.randint(0, len(files)-1)
    musicList.append(files[start])

    turns+=1

  # Plays a List of Music:
  backend.playList(musicList)

# APP RUNNING #

# App Running Calls:
mainApp()