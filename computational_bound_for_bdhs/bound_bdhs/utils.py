import pickle
from os.path import isdir
from os import makedirs

def serialize(data, file_path):
    initialiseFile(file_path)
    if file_path.endswith(".obj"):
        filehandler=open(file_path,"ab")
        pickle.dump(data, filehandler)
        filehandler.close()
    
def deserialize(file_path):
    if file_path.endswith(".obj"):
        filehandler=open(file_path, "rb")
        data=pickle.load(filehandler)
        filehandler.close()
        return data

def initialiseFile(file_path, overwrite: bool):
    """helper function that ensures a suitable file exists"""
    try:
        if overwrite:
            f = open(file_path, "w")
        else:
            f = open(file_path, "r")
            raise Exception("The {file} already exists and no premission has been given to overwrite.".format(file=file_path))
    except FileNotFoundError:
        file_path_parts = file_path.split('/')
        prefix=file_path_parts[:-1].join()
        if not isdir(prefix):
            makedirs(prefix)
        f = open(file_path, "x")
    finally:
        f.close()

def get_problems(problem_list):
    """helper function reading in cases by giving case names in the form initial_goal"""
    index = []
    with open(problem_list) as cases:
            for case in cases:
                case=case.split()
                initialState = case[0].strip()
                goalState = case[1].strip()
                caseName=initialState+"_"+goalState
                index.append(caseName)
    return index