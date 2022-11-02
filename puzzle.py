import copy #used for deepcopy
import timeit #used for keeping track of time of search

def main():
    print("Welcome to Harshi Doddapaneni's 8-puzzle solver!\n")
    # Allow user to choose default puzzle or make their own
    print("Type '1' to use a default puzzle, or '2' to enter your own puzzle.")
    choice = int(input())
    #default hard coded choice
    if choice == 1:
        problem = (['1', '2', '3'], ['5', '0', '6'], ['4', '7', '8'])
     #take in input for custom puzzle   
    elif choice == 2:
        print("Enter your puzzle, using a zero to represent the blank. "+ "Please only enter valid 8-puzzles. Enter the puzzle demilimiting"
        +  " numbers with a space. Type RET only when finished." + '\n')
        #take in user input and make the puzzle
        puzzle_row_one = input("Enter the first row: ")
        puzzle_row_two  = input("Enter the second row: ")
        puzzle_row_three = input("Enter the third row: ")
        puzzle_row_one = puzzle_row_one.split(' ')
        puzzle_row_two = puzzle_row_two.split(' ')
        puzzle_row_three = puzzle_row_three.split(' ')
        #make problem given data
        problem = puzzle_row_one, puzzle_row_two ,puzzle_row_three
    # Allow user to select what alg they would like to use to solve the problem
    print("Select an algorithm:") 
    print("(1)Uniform Cost Search")
    print("(2)A* with the Misplaced Tile Heuristic")
    print("(3)A* with the Manhattan Distance Heuristic")   

    alg_ans = int(input())   
    #Begin solving, and will print result
    #general_search is start and end
    if alg_ans == 1:
        print("Starting Uniform Cost Search")
        print(general_search(problem, alg_ans))
    elif alg_ans == 2:
        print("Starting A* w Misplaced Tile")
        print(general_search(problem, alg_ans))
    elif alg_ans == 3:
        print("Starting A* w Manhattan Distance")
        print(general_search(problem, alg_ans))    
    else:
        print("Invalid input")

class Node:
    #mv's are going to be used to check where 0 can potentially move. At  most, 4 available squares. 
    def __init__(self, state):
        self.state = state #current puzzle
        self.mv1 = None #move variation 1
        self.mv2 = None #move variation 2
        self.mv3 = None #move variation 3
        self.mv4 = None #move variation 4
        self.hc = 0     #heuristic
        self.depth = 0  #depth

def general_search(puzzle, alg):
    #begin timer when user finishes selection
    start = timeit.default_timer()
    #prev tracks all the states of the puzzle we have already seen, puzzleq is queue 
    #we will have different hcost based on alg choosen. UCS does not even use hcost
    prev = []
    puzzleq = []
    if alg == 1:
        hcost = 0           #uniform hcost is 0
    if alg == 2:
        hcost = misplaced_tiles(puzzle) #go to func and get num of wrong tiles
    if alg == 3:
        hcost = manhattan_distance(puzzle) #go to func and get distance of each tile to goal
   
    #size will be used to get max queue size. count will be used for nodes expanded
    size = 0
    #we will need a max size because queue size decreases when we pop, so we will use msize to keep track of highest
    msize = 0
    
    count = 0
    #input the inital puzzle problem and initalize values, and add it to the queue
    #this state is now seen so we can add it to prev
    n = Node(puzzle)
    n.depth = 0
    n.hc = hcost
    puzzleq.append(n)
    prev.append(n.state) 
    size += 1   #can increment size when appending
    FLAG = 1

    while FLAG:     #should only get out of while when goal reached
        if alg == 2:
             puzzleq.sort(key=lambda ans: (ans.depth + ans.hc)) # using lambda sort, sorts by sum of depth and hc which is want we want

        if alg == 3:
            puzzleq.sort(key=lambda ans: (ans.depth + ans.hc))  #sorts by sum of depth and hc which is want we want  

        nodes = puzzleq.pop(0) 
        #pop top node, and we can decrement size of queue
        size -= 1
        count += 1
        #check if equal to goal
        if nodes.state == (['1', '2', '3'], ['4', '5', '6'], ['7', '8', '0']):
            count -= 1
            #stop the time and print output, and break out
            stop = timeit.default_timer()
            print("Goal state!")
            print("Solution depth was " + str(nodes.depth))
            print("Number of nodes expanded: " + str(count))
            print("Max queue size: " + str(msize))
            print("Runtime: " + str(stop - start))
            break
        #keep printing until goal found
        print("Best state to expand with a g(n) = " + str(nodes.depth) + " and h(n) = " + str(nodes.hc)
                  + " is...\n" + str(nodes.state[0]) + "\n" + str(nodes.state[1]) +  "\n" + str(nodes.state[2]) 
                  + "\nExpanding...\n")
      
        #start searching the next batch of potential states
        next = expand_node(nodes, prev)
        moves = [next.mv1, next.mv2, next.mv3, next.mv4]
            #get the updated depth(increment every step) and make sure to get h(n) value by calling respective alg
        for step in moves:
            if step is not None:
                if alg == 2:
                    step.depth = nodes.depth + 1
                    step.hc = misplaced_tiles(step.state)
                elif alg == 3:
                    step.depth = nodes.depth + 1
                    step.hc = manhattan_distance(step.state)
                elif alg == 1:
                    step.depth = nodes.depth + 1
                    step.hc = 0
                #we can add these next step states. Add them to the queue and increment size    
                puzzleq.append(step)
                size += 1
                prev.append(step.state)
        #just getting the max size at this time
        msize = max(msize, size)

#loop around the puzzle to find where the 0 is. Return this
def find_blank(nodes):
    row = 0
    col = 0
    #iterate through the puzzle and find 0
    for r in range(len(nodes.state)):
        for c in range(len(nodes.state)):
            if int(nodes.state[r][c]) == 0:
                row = r
                col = c
    #return placememnt of 0            
    return row, col

def move_up(nodes, prev, row, col):
    if(row > 0):
        #swap up
        move_up = copy.deepcopy(nodes.state)
        temp_up = move_up[row][col]
        move_up[row][col] = move_up[row - 1][col]
        move_up[row - 1][col] = temp_up
        #checks to make sure we are not going back to prev states
        if move_up not in prev:
            nodes.mv1 = Node(move_up)

def move_down(nodes, prev, row, col):
    check  = len(nodes.state) - 1
    if row < check:
        #swap down
        move_down = copy.deepcopy(nodes.state)
        temp_down = move_down[row][col]
        move_down[row][col] = move_down[row + 1][col]
        move_down[row + 1][col] = temp_down
        #checks to make sure we are not going back to prev states
        if move_down not in prev:
            nodes.mv2 = Node(move_down)       

def move_right(nodes, prev, row, col):
    check  = len(nodes.state) - 1
    if col < check:
        #swap right
        move_right = copy.deepcopy(nodes.state)
        temp_right = move_right[row][col]
        move_right[row][col] = move_right[row][col+1]
        move_right[row][col+1] = temp_right
        #checks to make sure we are not going back to prev states
        if move_right not in prev:
            nodes.mv3 = Node(move_right)    

def move_left(nodes, prev, row, col):
     if col>0:
        #swap left
        move_left = copy.deepcopy(nodes.state)
        temp_left= move_left[row][col]
        move_left[row][col] = move_left[row][col - 1]
        move_left[row][col - 1] = temp_left
        #checks to make sure we are not going back to prev states
        if move_left not in prev:
            nodes.mv4 = Node(move_left)  
     
#Now we know where the 0 is. Now we can check all the possible ways it can move based on it's location
#remember, there are multiple ways to move but at max 4
def expand_node(nodes, prev):
    row,col = find_blank(nodes)

    #move up option  
     
    move_up(nodes, prev, row, col)
    #move down option         
    move_down(nodes, prev, row, col)
    #move right option
    move_right(nodes, prev, row, col)
    #moves left option
  
    move_left(nodes, prev, row, col)

    return nodes

#count the total number of misplaced tiles. Check with expected value and actual value. 
#If they are different, count++. Check all tiles. 
def misplaced_tiles(state):
    tiles_count = 0
    goal = [[1, 2, 3], [4, 5, 6], [7, 8, 0]] #hardcoded this to compare, easy to modify. Can also make a sep func to compare
    #iterate through the state
    for column in range(len(state)):
        for row in range(len(state)):
            #check if they are same
            if int(state[column][row]) != goal[column][row]: 
                if int(state[column][row]) != goal[column][row]:
                    #make sure we are not at blank
                    if int(state[column][row]) != 0:
                        tiles_count += 1
    return tiles_count

#get the proper row and col that you should have in goal state. 
#Will use these values to compare distance off in manhattan
def goal_state(state,r,c):
    #find num and get corresponding values for row and col 
    num = state[r][c]
    row = 0
    col = 0
    if num == 1: #tile 1 should be in row 0, col 0
        row = 0
        col = 0
    if num == 2:#tile 2 should be in row 0, col 1
        row = 0
        col = 1
    if num == 3:#tile 3 should be in row 0, col 2
        row = 0
        col = 2
    if num == 4:#tile 4 should be in row 1, col 0
        row = 1
        col = 0
    if num == 5:#tile 5 should be in row 1, col 1
        row = 1
        col = 1
    if num == 6:#tile 6 should be in row 1, col 2
        row = 1
        col = 2
    if num == 7:#tile 7 should be in row 2, col 0
        row = 2
        col = 0
    if num == 8:#tile 8 should be in row 2, col 1
        row = 2
        col = 1
    #function should not be called on 0
    return row, col

#Find the number of moves for each tile to be in proper place. 
#We can do this by finding proper values for goal using goal puzzle and actual value for each number. 
#Take the sum off the difference of both. This will give us the distance.
def manhattan_distance(state):
    goal = [[1, 2, 3], [4, 5, 6], [7, 8, 0]] #will use to compare
    moves_count = 0 #track total moves 
    actualr = 0 #actual row of num
    actualc = 0 #actual col of of num
    goalr = 0   #goal row of num
    goalc = 0   #goal col of num

    for l in range(1, 8): #loop through 1 - 8 and search for the tile
        #loop through the state
        for i in range(len(state)):
            for j in range(len(state)):
                if int(state[i][j]) == l: #if number found, store and compare
                    actualr = i
                    actualc = j
                if goal[i][j] == l:
                    goalr, goalc = goal_state(goal,i,j)
        #finds the distance of row and col and sums 
        moves_count += abs(goalr-actualr) 
        moves_count += abs(goalc-actualc)
    #return the h(n)         
    return moves_count

main()
