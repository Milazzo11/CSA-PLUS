import os
import shutil
import zipfile


"""
RUN CONFIGURATION SETTINGS vvv
"""

"""

PUT THESE IN A CSA_CONSTANTS.PY

"""


RUN_DIR = ""
# run directory
# will almost always be "" (current directory)

CHECK_EXTENSION = ".py"
# run extension

RUN_DIRECT = True
# runs program directly by file name

RUN_WITH_TEST = False
# runs program implementing external test program

RUN_NAME = "pentagons.py"
# program file to initiate execution with

TEST_NAME = ""
# external test program file name (must be in main directory)

FILE_NAMES = [RUN_NAME]
# program file names

ZIP_NAME = "hw.zip"
# homework main zip folder

RUN_COMMENT_TITLES = ["Task 1 functionality (15%)", "Task 2 functionality (20%)"]
# comment titles following code execution

CODE_COMMENT_TITLES = [["Task 1 program correctness (15%)", "Task 2 program correctness (40%)"]]
# comment titles associated with code blocks in each file
# index of nested array corresponds with associated file index in FILE_NAMES variable

ADDITIONAL_COMMENTS = ["Style (5%)", "Documentation (5%)", "Total"]
# aditional comment titles

MAIN_DIR = os.getcwd()
# gets the current directory to be used throughout the program

"""
RUN CONFIGURATION SETTINGS ^^^
"""


def run_program_python(dir, name):  # manages python file execution
    if RUN_DIRECT:
        cmd = "py " + name
        os.chdir(dir)
        os.system(cmd)
        os.chdir(MAIN_DIR)
    
    if RUN_WITH_TEST:
        cmd = "py " + TEST_NAME + ' "' + name + '" "' + dir + '"'
        os.system(cmd)
        # test file must be in CSA+ main working directory


def run_program(dir, name):  # program run wrapper
    run_program_python(dir, name)


def extract(name, dir):  # extracts zip files
    with zipfile.ZipFile(name, 'r') as zip_ref:
        zip_ref.extractall(dir)


def view(file):  # displays user files in terminal
    
    cct_iter = 0

    for included in FILE_NAMES:
        try:
            path = os.path.join("hw", file)
            run = os.path.join(os.path.join(path, RUN_DIR), included)

            if not os.path.isfile(run):
                print(f'< FILE "{included}"" NOT FOUND - SKIPPING >')
                return

            print("\n---------------------")
            print(included)
            print("---------------------")

            with open(run, "r", encoding='utf-8') as f:  # displays file text
                print(f.read())

            print("\n---------------------")

            comment_arr = []

            for comment in CODE_COMMENT_TITLES[cct_iter]:  # gets grader comments
                comment_arr.append(input(comment + " comments: "))

            data = ""

            if len(FILE_NAMES) > 1:  # formats comments for single and multi-file projects
                data = "\n< " + included + " >\n"

            for index in range(len(CODE_COMMENT_TITLES[cct_iter])):  # adds grader comments to string
                data += CODE_COMMENT_TITLES[cct_iter][index] + ": " + comment_arr[index] + "\n"

            with open(os.path.join("comments", file + ".txt"), "a") as f:  # writes comments to local file
                f.write(data)
                
            os.rename(run, os.path.join(os.path.join(path, RUN_DIR), RUN_NAME + ".complete"))

            cct_iter += 1
        except Exception as a:
            print(a)
            print("< UNEXPECTED ERROR ENCOUNTERED >")


def run_handle(path):  # handles program run
    print("---------------------")
    run_program(os.path.join(path, RUN_DIR), RUN_NAME)
    # runs program

    print("---------------------")

    complete = ""

    while complete.upper() != "Y" and complete.upper() != "N":  # queries for run completion information
        complete = input("Run complete? (Y/N): ")
                
    if complete.upper() == "N":  # handles incomplete program case
        complete = input("Rerun program (R) or mark incomplete (I): ")

        if complete.upper() == "R":  # reruns program
            complete = run_handle(path)
        else:
            complete = "N"
    
    return complete


def main():
    try:
        extract(ZIP_NAME, "hw")
        os.remove(ZIP_NAME)
        # extracts and removes homework zip file

    except:
        print("No hw.zip file.  Grading continuation program commencing...")
    
    try:
        os.mkdir(os.path.join(MAIN_DIR, "comments"))
        os.mkdir(os.path.join(MAIN_DIR, "incomplete"))
        # creates comments and incomplete folders if they do not exist

    except:
        pass

    files = os.listdir("hw")

    for file in files:  # iterates through homework files
        try:
            if file[-4:] == ".zip" and os.path.isfile(os.path.join("hw", file)):
                path = os.path.join("hw", file[:-4])
                extract(os.path.join("hw", file), path)

                print("Student Info:")
                print(file[:-4])
                
                complete = run_handle(path)
                # initiates run handler and gets completion code

                if complete.upper() == "Y":  # queries for behavior comments on successful completion
                    comment_arr = []

                    for comment in RUN_COMMENT_TITLES:  # gets grader comments
                        comment_arr.append(input(comment + " comments: "))

                    os.remove(os.path.join("hw", file))

                    data = ""

                    for index in range(len(RUN_COMMENT_TITLES)):  # adds grader comments to string
                        data += RUN_COMMENT_TITLES[index] + ": " + comment_arr[index] + "\n"

                    with open(os.path.join("comments", file[:-4] + ".txt"), "w") as f:
                        f.write(data)

                    view(file[:-4])

                    print()

                    comment_arr = []

                    if (len(FILE_NAMES) > 1):
                        data = "\n"
                    else:
                        data = ""

                    for comment in ADDITIONAL_COMMENTS:  # gets additional comments
                        comment_arr.append(input(comment + " comments: "))
                    
                    for index in range(len(ADDITIONAL_COMMENTS)):  # adds grader comments to string
                        data += ADDITIONAL_COMMENTS[index] + ": " + comment_arr[index] + "\n"

                    with open(os.path.join("comments", file[:-4] + ".txt"), "a") as f:  # writes comments to local file
                        f.write(data)

                else:
                    shutil.copyfile(os.path.join("hw", file), os.path.join("incomplete", file))
                    os.remove(os.path.join("hw", file))
                    # puts unsuccessfully run or invalidly named files in the incomplete directory
                
                print("---------------------\n\n")
            
            elif file[-3:] == CHECK_EXTENSION and os.path.isfile(os.path.join("hw", file)):  # handles non-directory (lone) files
                q = input("Mark file " + file + " as incomplete? (Y/N): ")

                if q.upper() == "Y":
                    shutil.copyfile(os.path.join("hw", file), os.path.join("incomplete", file))

                os.remove(os.path.join("hw", file))

                print("---------------------\n\n")

        except Exception as a:  # handles file/other errors
            print(a)
            print("< ERROR - SKIPPING >")


if __name__ == "__main__":
    main()