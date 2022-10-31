def main():
    print("Welcome to Harshi Doddapaneni's 8-puzzle solver!\n")

    print("Type '1' to use a default puzzle, or '2' to enter your own puzzle.")
    choice = int(input())

    if choice == 1:
        puzzle = (['1', '2', '3'], ['5', '0', '6'], ['4', '7', '8'])
        
    elif choice == 2:
        print("Enter your puzzle, use a zero to represent the blank")

        r_one = input("Enter the first row:")
        r_two = input("Enter the second row:")
        r_three = input("Enter the third row:")
        r_one = r_one.split(' ')
        r_two = r_two.split(' ')
        r_three = r_three.split(' ')

        problem = r_one, r_two, r_three

    alg_choice  = "Select an algorithm\n"
    alg_choice += "1.Uniform Cost Search\n"
    alg_choice += "2.A* with the Misplaced Tile Heuristic\n"
    alg_choice += "3.A* with the Manhattan Distance Heuristic\n"    
    
    print(alg_choice)
    alg_ans = int(input())             
    
