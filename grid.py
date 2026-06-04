import time 

def make_grid():
  global rows, cols
  lvl = input("What difficulty would you like (easy, medium, hard)? ").lower() # grid size changes 
  if lvl == 'easy':
      rows = 10
      cols = 10
  elif lvl == 'medium':
      rows = 7
      cols = 7
  elif lvl == 'hard':
      rows = 5
      cols = 5
  else: # invalid input
      print("Invalid input.")
      time.sleep(0.7)
      print("Setting default difficulty to medium.")
      rows = 7
      cols = 7
      
  grid = [['.' for col in range(cols)] for row in range(rows)]

 # grid coordinates
  header = [" "] + [str(col).ljust(4) for col in range(cols)] # got help with the (ljust(2)) part; which makes sure no shifting happens
  print("  ".join(header))

  for row in range(rows):
      row_header = f"{row:2} " + "  ".join(str(cell).ljust(4) for cell in grid[row]) # got help for the .join() part (makes sure no shifting happens)
      print(row_header)
      print()
  
  return grid, rows, cols