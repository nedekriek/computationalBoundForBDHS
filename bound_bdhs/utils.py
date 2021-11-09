import pickle
#from os.path import isdir as check_directory_path
from os import makedirs

def serialize(data, filename):
    initialiseFile(filename)
    if filename.endswith(".obj"):
        filehandler=open(filename,"ab")
        pickle.dump(data, filehandler)
        filehandler.close()
    
def deserialize(filename):
    if filename.endswith(".obj"):
        filehandler=open(filename, "rb")
        data=pickle.load(filehandler)
        filehandler.close()
        return data

def initialiseFile(file_path, overwrite: bool):
    """helper function that ensures a suitable file exists"""
    if overwrite:
         f = open(file_path, "w")
    else:
        try:
            f = open(file_path, "r")
            raise Exception("The {file} already exists and no premission has been given to overwrite.".format(file=file_path))
        except IOError:
            #make file
            f = open(file_path, "c")
        finally:
            f.close()

# def initialiseDir(directory_path):
#     """helper function that makes missing directories on a path"""
#     if not check_directory_path(directory_path):
#         makedirs(directory_path)

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