# CMPT 145:
#Name: Muhammad Usman Ahmed
#ID 11275853
#NSID mua942
#Assigment: 2 Q3
##Lab L02
import flavourSW as flavour
import sys as sys

def create_room():
    room = {}
    room['contents'] = None
    room['N'] = None
    room['E'] = None
    room['S'] = None
    room['W'] = None
    return room


def connect(room1, axis, room2):
    if axis == 'row':
      room1['E'] = room2
      room2['W'] = room1
    else:
      room1['N'] = room2
      room2['S'] = room1


def create_dungeon(size, items):
  dungeon = []
  for r in range(size):
    row = []
    for c in range(size):
        row.append(create_room())
    dungeon.append(row)

  for row in range(size):
    for col in range(size-1):
      connect(dungeon[row][col], 'row', dungeon[row][col+1])

  for col in range(size):
    for row in range(size-1):
      connect(dungeon[row][col], 'col', dungeon[row+1][col])

  for item,r,c in items:
    dungeon[r][c]['contents'] = item

  return dungeon[0][0]


def terminal(room):
   c = room['contents']
   return c in ['W', 'P']


def describe_room(room):
  if room['contents'] == 'W':
    print(flavour.content['W'])
    return
  if room['contents'] == 'P':
    print(flavour.content['P'])
    return
  if room['contents'] == 'G':
    print(flavour.content['G'])

  close_by = []
  for n in 'NSEW':
     if room[n] is not None:
         close_by.append(room[n]['contents'])
 
  if 'W' not in close_by and 'P' not in close_by:
    print(flavour.closeby['E'])
  if 'W' in close_by:
    print(flavour.closeby['W'])
  if 'P' in close_by:
    print(flavour.closeby['P'])


def read_replay(filename):
    file = open(filename)
    size = int(file.readline().rstrip())
    locations = []
    for i in range(4):
        line = file.readline().rstrip().split()
        locations.append((line[0], int(line[1]), int(line[2])))
    trip = file.readline().rstrip()
    file.close()
    return {'size': size,
            'locations': locations,
            'trip': trip}


def replay(size, locations, trip):
    start = create_dungeon(size, locations)
    gotG = False
    loc = start

    describe_room(loc)
    for s in trip:
       loc = loc[s]
       describe_room(loc)
       if terminal(loc):
         break
       if loc['contents'] == 'G':
         gotG = True
         loc['contents'] = None

    if loc is start and gotG:
      print(flavour.final['W'])
      return 1000
    elif loc is start:
      print(flavour.final['F'])
      return 0
    else:
      print(flavour.final['L'])
      return -1000


game = read_replay(sys.argv[1])
replay(game['size'], game['locations'], game['trip'])