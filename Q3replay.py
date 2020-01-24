# CMPT 145:
#Name: Muhammad Usman Ahmed
#ID 11275853
#NSID mua942
#Assigment: 2 Q3
##Lab L02
import flavourSW as flavour
import sys as sys

def create_room():
    '''
    Purpose:
        to create a dict representing one room in the dungeon
    Pre:
        None
    Post:
        None
    :return: a dict containg keys with NONE as value
    '''
    room = {}
    room['contents'] = None
    room['N'] = None
    room['E'] = None
    room['S'] = None
    room['W'] = None
    return room


def connect(room1, axis, room2):
    '''
    Purpose:
    To set the NSWE of a room to the dict of another room in the corresponding direction
    pre:
        :param room1: a dict containing the information of a room
        :param axis: a string defining which direction to work in NS or WE
        :param room2: a dict containing the information of a room
    Post:
        effects the original room entry in the 'dungeon' list of lists of dicts in 'create_dungeon()' function
    :return:
        None
    '''
    if axis == 'row':
      room1['E'] = room2
      room2['W'] = room1
    else:
      room1['N'] = room2
      room2['S'] = room1


def create_dungeon(size, items):
  '''Purpose:
        To construct the start location of the dungeon and create the dungeon as well
    Pre:
        :param size: the n in nxn dungeon
        :param items: a list of tuples
    Post:
        None
    :return:
        The first room in the dungeon with NSWE's content values assigned
  '''

  ##items refers to location which is a list of lists
  dungeon = []

  ##r refers to a singluar int from 0, to n
  for r in range(size):
    row = []
    ## run through the size again thus creating a row of ROOMS.
    for c in range(size):
        #the create_room functions makes an empty ROOM
        row.append(create_room())
    dungeon.append(row)

  ##dungeon is a list of lists where each small list contains a row's worth of dictionaires

  ##start from the first row and first col and go through in order putting two rooms to each other's information
  for row in range(size):
      ##(-1) is to make sure we do not pass in the last col because it does not have a col to the left.
    for col in range(size-1):
      connect(dungeon[row][col], 'row', dungeon[row][col+1])


  ##Does the same thing. Making each room point to each other's information
  for col in range(size):
    for row in range(size-1):
      connect(dungeon[row][col], 'col', dungeon[row+1][col])

  ## items being a list of lists, item = GWP, r= row, c = column
  for item,r,c in items:
    dungeon[r][c]['contents'] = item
  ##because the game always starts at the same place
  return dungeon[0][0]


def terminal(room):
   '''
   Purpose:
        To check if the room contains a game ending element

   Pre:
        :param room: a dict of information for a row
   Post:
        None
   :return:
        True if a trap or enemy is found else return False and continue game
   '''

   c = room['contents']
   return c in ['W', 'P']


def describe_room(room):
  '''
  Purpose:
      To go through a single room and print out the correct information for the room (Trap, Enemy or Goal)
  Pre:
      :param room: a dict containing a single room's worth of information
  Post:
      can print an array of prints showing warnings depening on room content
  :return:
    None
  '''

  #die on enemy
  if room['contents'] == 'W':
    print(flavour.content['W'])
    return
  ##die on trap now
  if room['contents'] == 'P':
    print(flavour.content['P'])
    return
  ##you have won this game
  if room['contents'] == 'G':
    print(flavour.content['G'])


  close_by = []
  ##NSWE, N...= to another room (meaning another dictionary)
  for n in 'NSEW':
      ##Basically check all around.

     if room[n] is not None:
         ##The if checks if the room isnt on an edge
         close_by.append(room[n]['contents'])

 ##Meaning nothing is closebym
  if 'W' not in close_by and 'P' not in close_by:
    print(flavour.closeby['E'])

  ##You are nearby an enemy
  if 'W' in close_by:
    print(flavour.closeby['W'])

  ##You are nearby a trap
  if 'P' in close_by:
    print(flavour.closeby['P'])


def read_replay(filename):
    '''
    Purpose:
        To convert a text file into a dictionary with the entire game described
    pre:
        :param filename: a string refering to a filename containing a dungeon
    post:
        None
    :return:
        dictionary with size, locations and journey with the same key and value names
    '''
    file = open(filename)
    ##this moves read line down 1. Thus giving us the locations of each special element
    size = int(file.readline().rstrip())
    locations = []

    for i in range(4):
        ##this opens the file. takes the first 5 lines which are the dungon commands
        line = file.readline().rstrip().split()
        ##line[0] = the type (goal or enemie) line[1] = (col) line[2] = row
        locations.append((line[0], int(line[1]), int(line[2])))

    #get the series of movements
    trip = file.readline().rstrip()
    file.close()

    ##return a dictionary that has the entire file described.
    return {'size': size,
            'locations': locations,
            'trip': trip}


def replay(size, locations, trip):
    '''
    Purpose:
        To act a main function that plays back the game
    Pre:
        :param size: a int representing n in nxn
        :param locations: a list of tuples representing the location of special elements
        :param trip: A list of chars representing the player moves
    Post:
        makes prints showing when the game is won, loss or nothing
        uses the 'dungeon' from 'create_dungeon()'
    :return:
        A int value representing win, neutral or loss
    '''
    ##start is a dictionary containg contents: ...., NSEW
    start = create_dungeon(size, locations)
    #keep track that we have not yet won
    gotG = False

    ## loc is now a dictionary
    loc = start
    ##What is describe_room
    describe_room(loc)

    ##
    for s in trip:
       ##by going from 0,0 and refering to the direction of movment, W or E means another room. Thus follows the path of motion
       ##(for later use) loc[s] assigns loc to be the next room in game. N means go to room above and repeace
       loc = loc[s]
       describe_room(loc)


       if terminal(loc): ##if true the game is over
         break

       ##This means the player has won end replay
       if loc['contents'] == 'G':
         gotG = True
         ##Means we picked up the Goal
         loc['contents'] = None
    ##Since we have to get both Goal and make it out (back to origin)
    if loc is start and gotG:
      print(flavour.final['W'])
      return 1000
    ##The player just ended the game without getting the goal
    elif loc is start:
      print(flavour.final['F'])
      return 0
    ##Fail safe to ensure that if somthing goes wrong we still lost the game
    else:
      print(flavour.final['L'])
      return -1000


game = read_replay(sys.argv[1])
replay(game['size'], game['locations'], game['trip'])