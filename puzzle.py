def main():
    print("Welcome to Harshi Doddapaneni's 8-puzzle solver!\n")

    print("Type '1' to use a default puzzle, or '2' to enter your own puzzle.")
    choice = int(input())

    if choice == 1:
        problem = (['1', '2', '3'], ['5', '0', '6'], ['4', '7', '8'])
        
    elif choice == 2:
        print("Enter your puzzle, use a zero to represent the blank")
        #take in user input and make the puzzle
        r_one = input("Enter the first row:")
        r_two = input("Enter the second row:")
        r_three = input("Enter the third row:\n")
        r_one = r_one.split(' ')
        r_two = r_two.split(' ')
        r_three = r_three.split(' ')

        problem = r_one, r_two, r_three
    # Allow user to select what alg they would like to use to solve the problem
    alg_choice  = "Select an algorithm\n"
    alg_choice += "1.Uniform Cost Search\n"
    alg_choice += "2.A* with the Misplaced Tile Heuristic\n"
    alg_choice += "3.A* with the Manhattan Distance Heuristic\n"   
    print(alg_choice)
    alg_ans = int(input())   
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

    def __init__(self, state, path):
        self.state = state
        self.mv1 = None #move variation 1 and so on
        self.mv2 = None 
        self.mv3 = None
        self.mv4 = None
        self.hc = 0     
        self.depth = 0
        self.path = path

def general_search(puzzle, alg):
    
    prev = []
    puzzleq = []
    if alg == 1:
        h = 0
    if alg == 2:
        h = misplaced_tiles(puzzle)
    if alg == 3:
        h = manhattan_distance(puzzle)


    n = Node(puzzle)
    n.depth = 0
    n.hc = 0
    puzzleq.append(n)
    prev.append(n.state)
    FLAG = 1

    while FLAG:
        if len(puzzleq) == 0:
            return []
        if alg == 2:
            puzzleq = sorted(puzzleq, key=lambda ans: (ans.depth + ans.hc))
        if alg == 3:
            puzzleq = sorted(puzzleq, key=lambda ans: (ans.depth + ans.hc))    

        nodes = puzzleq.pop(0)

        if nodes.state == (['1', '2', '3'], ['4', '5', '6'], ['7', '8', '0']):
            print("Goal state!")
            print("Solution depth" + str(nodes.depth))
            break
      
        next = expand_node(nodes, prev)
        moves = [next.mv1, next.mv2, next.mv3, next.mv4]

        for step in moves:
                if alg == 2:
                    step.depth = nodes.depth + 1
                    step.hc = misplaced_tiles(step.state)
                elif alg == 3:
                    step.depth = nodes.depth + 1
                    step.hc = manhattan_distance(step.state)
                elif alg == 1:
                    step.depth = nodes.depth + 1
                    step.hc = 0
def find_blank(nodes):
    row = 0
    col = 0
    for r in range(len(nodes.state)):
        for c in range(len(nodes.state)):
            if int(nodes.state[r][c]) == 0:
                row = r
                col = c
    return row, col

#Now we know where the 0 is. Now we can check all the possible ways it can move based on it's location
#remember, there are multiple ways to move but at max 4
def expand_node(nodes, prev):
    row,col = find_blank(nodes)
    check  = len(nodes.state) - 1
    #move up option            
    if row>0:
        #swap up
        move_up = copy.deepcopy(nodes.state)
        temp_up = move_up[row][col]
        move_up[row][col] = move_up[row - 1][col]
        move_up[row - 1][col] = temp_up
        #checks to make sure we are not going back to prev states
        if move_up not in prev:
            nodes.mv1 = Node(move_up)
    #move down option
    if row < check:
        #swap down
        move_down = copy.deepcopy(nodes.state)
        temp_down = move_down[row][col]
        move_down[row][col] = move_down[row + 1][col]
        move_down[row + 1][col] = temp_down
        #checks to make sure we are not going back to prev states
        if move_down not in prev:
            nodes.mv2 = Node(move_down)
    #move right option
    if col < check:
        #swap right
        move_right = copy.deepcopy(nodes.state)
        temp_right = move_right[row][col]
        move_right[row][col] = move_right[row][col+1]
        move_right[row][col+1] = temp_right
        #checks to make sure we are not going back to prev states
        if move_right not in prev:
            nodes.mv3 = Node(move_right)  
    #moves left option
    if col>0:
        #swap left 
        move_left = copy.deepcopy(nodes.state)
        temp_left= move_left[row][col]
        move_left[row][col] = move_left[row][col - 1]
        move_left[row][col - 1] = temp_left
        #checks to make sure we are not going back to prev states
        if move_left not in prev:
            nodes.mv4 = Node(move_left)  

    return nodes

def misplaced_tiles(state):
    tiles_count = 0
    goal = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
    for column in range(len(state)):
        for row in range(len(state)):
            if int(state[column][row]) != goal[column][row]: 
                if int(state[column][row]) != goal[column][row]:
                    if int(state[column][row]) != 0:
                        tiles_count += 1
    return tiles_count

def goal_state(state,r,c):
    
    num = state[r][c]
    row = 0
    col = 0
    if num == 1:
        row = 0
        col = 0
    if num == 2:
        row = 0
        col = 1
    if num == 3:
        row = 0
        col = 2
    if num == 4:
        row = 1
        col = 0
    if num == 5:
        row = 1
        col = 1
    if num == 6:
        row = 1
        col = 2
    if num == 7:
        row = 2
        col = 0
    if num == 8:
        row = 2
        col = 1
    #function should not be called on 0
    return row, col

def manhattan_distance(state):
    goal = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
    moves_count = 0
    curr_row = 0
    curr_col = 0
    goal_row = 0
    goal_col = 0

    for l in range(1, 8):
        for i in range(len(state)):
            for j in range(len(state)):
                if int(state[i][j]) == l:
                    curr_row = i
                    curr_col = j
                if goal[i][j] == l:
                    goal_row, goal_col = goal_state(goal,i,j)

        moves_count += abs(goal_row-curr_row) 
        moves_count += abs(goal_col-curr_col)
             
    return moves_count

main()
