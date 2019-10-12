import copy, random, os, sys

board_alphabet=[" ","A","B","C","D","E","F","G","H","I","J"]
board_size=[len(board_alphabet),10]
width_line=board_size[1]*7
ships = {
  "M": ["Lotniskowiec", 5,{}],
  "O": ["Marynarka", 4,{}],
  "C": ["Okręt podwodny", 3,{}],
  "D": ["Niszczyciel", 3,{}],
  "E": ["Łódź patrolowa",2,{}], 
  "G": ["Łodź rybacka", 1,{}]
}
mark_success="\u220E"
mark_sunk="\u22A0"
mark_false="\u2022"
mark_shiled='HH'

# DRAW BOARD FUNCTIONS
def newLine():
    print ('')


def end_row():
  for i in range(width_line):
    print('-',end="")
  print ('')


def print_sign(sign):
  s=" "
  if (len(str(sign))>1):
    s=""
  print(s,sign,' ',  end="|")


def print_board(board):
  print('\n')
  for i in range(board_size[0]):
    print_sign(board_alphabet[i])
  newLine()
  end_row()  
  for y in range(board_size[1]):    
    print_sign(y+1)
    for x in range(board_size[0]-1):
      sign = " "
      if board[x][y] == mark_false or board[x][y] == mark_success or board[x][y] == mark_sunk:
        sign= board[x][y] 
      elif board[x][y]==-1:
        sign=' '    
      print_sign(sign)
    newLine()
    end_row()


def prepare_board():
  board=[]
  for y in range(board_size[1]):
    board_row = []
    for x in range(board_size[0]):
      board_row.append(-1)
    board.append(board_row)
  return board

# LOGIC FUNCTIONS
def validate(board,ship,x,y,ori):
  if (ori == 'v' and x + ship > board_size[0]-1) or (ori == 'h' and y + ship > board_size[1]-1):
    return False
  elif ori == 'v':
    for i in range(ship):
      if board[x + i][y] != -1:
        return False
  elif ori == 'h':
    for i in range(ship):
      if board[x][y + i] != -1:
        return False      
  return True


def drawShield(x, y, ship_length, ori, board, mark):
  if(ori=='v'):   
    for i in range(ship_length+2):
      for j in range(3):
        if(x+i>=0 and y+j>=0 and x+i<board_size[0]-1 and y+j < board_size[1]):
          board[x+i][y+j]=mark
  if(ori=='h'):   
    for i in range(ship_length+2):
      for j in range(3):
        if(y+i>=0 and x+j>=0 and y+i < board_size[1] and x+j < board_size[0]-1):
          board[x+j][y+i]=mark


def place_ship(board, ship, s, ori, x, y):
  drawShield(x-1, y-1, ship, ori, board, mark_shiled)  
  ships[s][2]={"x" : x, 'y' : y, 'ori' : ori}
  if ori == "v":    
    for i in range(ship):
      board[x + i][y] = s      
  
  elif ori == "h":    
    for i in range(ship):
      p = y + i 
      board[x][p] = s
  return board


def computer_place_ships(board,ships):
  
  for ship in ships.keys():
    valid = False    
    while(not valid):
      x = random.randint(1, board_size[1]) - 1
      y = random.randint(1, board_size[1]) - 1
      o = random.randint(0, 1)      
      if o == 0:
        ori = "v"
      else:
        ori = "h"     
      valid = validate(board, ships[ship][1], x, y, ori)
    board = place_ship(board, ships[ship][1], ship, ori, x, y)
   # print ("Komputer wybrał miejsce dla: ", ships[ship][0]+":", ships[ship][1])
  return board


def user_input_validate():
  coord=['', '']
  while True:
    str_coord="Gdzie strzelasz? Podaj koordynaty w formacie xy -> "
    if str_coord == 'q':
      sys.exit()

    try:
      user_input = input(str_coord)
      coord[0] = user_input[:1]
      coord[1] = user_input[1:]
      
      if coord[0] == 'q':
        import sys
        exit(0)

      if(len(coord) != 2 or isinstance(coord[1], int)):
        raise Exception("Koordynaty nieprawidłowe.\n")      
      
      coord[0] = coord[0].upper()
      coord[1] = int(coord[1]) - 1

      if(coord[0] not in board_alphabet):
        raise Exception("Kolumna podana nieprawidłowo")
      else:
        for i, item in enumerate(board_alphabet):
          if item == coord[0]:
            coord[0] = i - 1
      
      if coord[1]>board_size[1]:
        raise Exception("Numer wiersza podany nieprawidłowo")
      return coord
      
    except ValueError:
      print("Koordynaty nieprawidłowe.\n")
    except Exception as e:
      print(e)


def make_move(board,x,y):
  if board[x][y] == -1 or board[x][y] == mark_shiled:
    return 0
  elif board[x][y] == mark_false or board[x][y] == mark_success:
    return 1
  return 2


def user_move(board):
  x, y = user_input_validate()
  os.system('clear')
  res_str=("Pudło", "Miejsce zajęte. Próbuj dalej", "Trafiony","\n\n\n~~~~~~~~~~~~~~~Wygrałeś~~~~~~~~~~~~~~~\n\n\n")
  res = make_move(board, x, y)
  if res == 2:
    print(res_str[res], board_alphabet[x + 1] + ":" + str(y + 1))
    
    if check_sink(board, x, y):
      board[x][y] = mark_sunk
    elif board[x][y] != mark_sunk:
      board[x][y] = mark_success
    
    if check_win(board):
      print(res_str[3])
    return board
  elif res == 0:
    print(board_alphabet[x+1] + ":" + str(y + 1), res_str[res])
    board[x][y] = mark_false
    return board
  elif res == 1:
    print(res_str[res])
  return board


def check_sink(board,x,y):
  ship = board[x][y]
  if ship in ships:
    board[-1][ship][1] -= 1
    if board[-1][ship][1] == 0:
      drawShield(ships[ship][2]['x'] - 1, ships[ship][2]['y'] - 1, ships[ship][1], ships[ship][2]['ori'], board, mark_false)
      for i in range(ships[ship][1]):      
        if ships[ship][2]['ori'] == 'h':
          board[ships[ship][2]['x']][ships[ship][2]['y'] + i] = mark_sunk
        elif ships[ship][2]['ori'] == 'v':
          board[ships[ship][2]['x'] + i][ships[ship][2]['y']] = mark_sunk
          
      print('~~~~~~~~~ ', ships[ship][0] + " zatopiony", '~~~~~~~~~\n')
      return True


def check_win(board):
  for key,value in computer_board[-1].items():
    if value[1]>0:
      return False   
  return True

print('\n______ ZACZYNAMY GRĘ BATTLESHIP_______\n')

board = prepare_board()
computer_board=computer_place_ships(board, ships)

computer_board.append(copy.deepcopy(ships))

i = 1
while True: 
  print_board(computer_board)
  print('\nWciśnij [q] by zakończyć grę\n')
  print('\n----Statki na tablicy----')
 
  for key, value in computer_board[-1].items():
    sunk=''
    if value[1] == 0:
      sunk = ' zatopiony'    
    print(value[0],':', ships[key][1], end = sunk + "\n")
  print('----------------------------\n') 
   
  print('Ruch: #', i)

  user_move(computer_board)
  i += 1
