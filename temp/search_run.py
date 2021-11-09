# from  aStar.pancake.problemPancakeUnitCost import problemPancakeUnitCost
# from  aStar.heuristics.gapUnitCost import gapUnitCost

from  aStar.pancake.problemPancakeArbitraryCost import problemPancakeArbitraryCost
from  aStar.heuristics.gapArbitraryCost import gapArbitraryCost

# from  aStar.slidingTile.problemEightPuzzleUnitCost import problemEightPuzzleUnitCost
# from  aStar.heuristics.eightPuzzleUnitCost import manhattanUnitCost

from  aStar.slidingTile.problemEightPuzzleArbitraryCost import problemEightPuzzleArbitraryCost
from  aStar.heuristics.eightPuzzleArbitraryCost import manhattanArbitraryCost



# file_to_run_search=['pancake/pancakeTestCases/fivePancakes.txt','pancake/pancakeTestCases/fourPancakes.txt','pancake/pancakeTestCases/threePancakes.txt','pancake/pancakeTestCases/sixPancakes.txt','pancake/pancakeTestCases/sevenPancake.txt']
# storage='experiments/solution_lengths_unit_cost_pancake.txt'
# for file in file_to_run_search:
#     se = SearchOnly(problemPancakeUnitCost, gapUnitCost, file, storage)
#     se.run()

file_to_run_search=['pancake/pancakeTestCases/fivePancakes.txt','pancake/pancakeTestCases/fourPancakes.txt','pancake/pancakeTestCases/threePancakes.txt','pancake/pancakeTestCases/sixPancakes.txt','pancake/pancakeTestCases/sevenPancake.txt']
storage='experiments/solution_lengths_arbitrary_cost_pancake.txt'
for file in file_to_run_search:
    se = SearchOnly(problemPancakeArbitraryCost, gapArbitraryCost, file, storage)
    se.run()

# file_to_run_search=file_to_run_search=[162,122,81,41,40]
# storage='experiments/solution_lengths_unit_cost_eight_puzzle.txt'
# for file in file_to_run_search:
#     se = SearchOnly(problemEightPuzzleUnitCost, manhattanUnitCost, "slidingTile/slidingTileTestCases/8slidingTile"+str(file)+".txt", storage)
#     se.run()

file_to_run_search=file_to_run_search=[162,122,81,41,40]
storage='experiments/solution_lengths_arbitrary_cost_eight_puzzle.txt'
for file in file_to_run_search:
    se = SearchOnly(problemEightPuzzleArbitraryCost, manhattanArbitraryCost, "slidingTile/slidingTileTestCases/8slidingTile"+str(file)+".txt", storage)
    se.run()