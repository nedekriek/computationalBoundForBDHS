test_cases="slidingTile/slidingTileTestCases/8slidingTile.txt"
batch_size=500
count=0
batch_number=1
file_prefix="slidingTile/slidingTileTestCases/8slidingTile"

file=open(file_prefix+str(batch_number)+".txt", "w")

with open(test_cases) as main_test_case_file:
    for line in main_test_case_file:
        count+=1
        if count<500:
            file.write(line)
        else:
            file.close()
            count=1
            batch_number+=1
            file=open(file_prefix+str(batch_number)+".txt", "w")
            file.write(line)