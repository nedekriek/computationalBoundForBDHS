def countInversions(initial):
    inversions=0
    gameSize=len(initial)
    for i, item in enumerate(initial):
        if item == 0:
            continue
        for j in range(1,gameSize-i):
            item2=initial[i+j]
            if item2 == 0:
                continue
            elif item > item2:
                inversions+=1
    return inversions

def enum_lex_perm(n,k):
    #Johnson trotter enumeration 
    if k>1:
        prevPermutations = enum_lex_perm(n,k-1)
        current_permutations = []
        for permutation in prevPermutations:
            remaining = []
            for i in range(1,n+1):
                if i not in permutation:
                    remaining.append(i)
            for j in remaining:
                newPermutation=permutation + [j]
                current_permutations.append(newPermutation) 
        return current_permutations
    else:
        return [[i] for i in range(1,n+1)]

def generate_test_cases(puzzle_size, puzzle_type, goalString):
    #TODO updated to give correct answer if grid is even sized according to: https://www.cs.bham.ac.uk/~mdr/teaching/modules04/java2/TilesSolvability.html
    #TODO allow arbitrary goal state
    permutations=enum_lex_perm(puzzle_size+1, puzzle_size+1)
    test_cases =  open("search_problems/"+puzzle_type+"/"+str(puzzle_size)+puzzle_type+".txt", "w")

    for perm in permutations:
        for i in range(0, len(perm)):
            perm[i]= perm[i] - 1

        state=[None for i in range(9)]
        for index, value in enumerate(perm):
            state[value]=index
        if puzzle_type == "sliding_tile":
            if countInversions(state) %2 == 0:     
                perm=[str(num) for num in perm]
                test_cases.write("".join(perm)+" "+goalString+"\n")
        elif puzzle_type == "pancake":
            perm=[str(num) for num in perm]
            test_cases.write("".join(perm)+" "+goalString+"\n")
    
    test_cases.close()

generate_test_cases(8,"sliding_tile","801234567")
