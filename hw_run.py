import os
import sys
import shutil
import zipfile


"""
RUN CONFIGURATION SETTINGS vvv
"""

# !! = SETTING MAY LIKELY NEED TO BE ALTERED WHEN ASSIGNMENT CHANGES

ASSIGNMENT_NAME = "homework12"
# used by other public variables
# !!

RUN_DIR = ""
# subdirectory in student submission file where run-file is located
# will almost always be "" (submission directory)

ALT_DIRS = [ASSIGNMENT_NAME]
# alternative directives to check for code if not found in RUN_DIR

CHECK_EXTENSION = ".py"
# run extension

RUN_DIRECT = True
# runs program directly by file name
# !!

RUN_WITH_TEST = False
# runs program implementing external test program
# !!

RUN_NAME = "number_map.py"
# program file to initiate execution with
# !!

RUN_NAME_SEARCH = "treemap.py"
# RUN_NAME_SEARCH = RUN_NAME
# program file to search for to ensure correct run directory
# will usually be the same as RUN_NAME
# in cases where a copied library file is set in RUN_NAME this value may differ

COMPLETION_MARKER = ASSIGNMENT_NAME
# used if RUN_NAME and RUN_NAME_SEARCH are different
# creates a ".complete" file with this name to signify completeness

TEST_NAME = "run.py"
# external test program file name (must be in main directory)

FILE_NAMES = ["treemap.py"]
# program file names
# !!

ZIP_NAME = "hw.zip"
# homework main zip folder

RUN_COMMENT_TITLES = []
# comment titles following code execution
# !!

CODE_COMMENT_TITLES = [["TreeMap (10%)", "map_insert (35%)", "map_to_str (15%)", "map_search (15%)", "main and tests (15%)"]]
# comment titles associated with code blocks in each file
# index of nested array corresponds with associated file index in FILE_NAMES variable
# EVEN IF FILE HAS NO COMMENTS, EMPTY LIST '[]' MUST BE PLACED HERE FOR EACH FILE
# !!

ADDITIONAL_COMMENTS = ["Style (5%)", "Documentation (5%)", "Submission", "Total"]
# aditional comment titles
# !!

NOTEPAD_CMD = "notepad"
# text editor command

MAIN_DIR = os.getcwd()
# gets the current directory to be used for reference in "run" functions
# CURRENT CODE SHOULD NOT NEED TO BE ALTERED

"""
RUN CONFIGURATION SETTINGS ^^^
"""


def run_program_python(dir, name):  # manages python file execution
    if RUN_DIRECT:
        cmd = "py " + name
        os.chdir(dir)

        try:
            os.system(cmd)
        except:
            pass

        os.chdir(MAIN_DIR)
    
    if RUN_WITH_TEST:
        cmd = "py " + TEST_NAME + ' "' + name + '" "' + dir + '"'
        
        try:
            os.system(cmd)
            # test file must be in CSA+ main working directory
            # all information to change directories / run code provided in command line arguments
            
        except:
            pass


def run_program(dir, name):  # program run wrapper
    run_program_python(dir, name)


def extract(name, dir):  # extracts zip files
    with zipfile.ZipFile(name, 'r') as zip_ref:
        zip_ref.extractall(dir)


def view(run_path, file=None):  # displays user files in terminal
    
    cct_iter = 0

    for included in FILE_NAMES:
        try:
            run = os.path.join(run_path, included)

            if os.path.isfile(run):  # displays file if it is present
                print("\n---------------------")
                print("FILE: " + included)
                print("DIR: " + run_path)
                print("---------------------")

                with open(run, "r", encoding='utf-8') as f:  # displays file text
                    print(f.read())

                print("\n---------------------")
                
            else:
                print(f'< FILE "{included}" NOT FOUND - SKIPPING >')
            
            if file is not None:
            
                comment_arr = []
            
                for comment in CODE_COMMENT_TITLES[cct_iter]:  # gets grader comments
                    comment_arr.append(input(comment + " comments: "))

                data = ""

                if len(FILE_NAMES) > 1 and len(CODE_COMMENT_TITLES[cct_iter]) > 0:  # formats comments for single and multi-file projects
                    if len(RUN_COMMENT_TITLES) > 0 or cct_iter > 0:
                        data = "\n"
                        # ensures newline isn't added at start of comment file
                        
                    data += "< " + included + " >\n"
                
                for index in range(len(CODE_COMMENT_TITLES[cct_iter])):  # adds grader comments to string
                    data += CODE_COMMENT_TITLES[cct_iter][index] + ": " + comment_arr[index] + "\n"

                with open(os.path.join("comments", file + ".txt"), "a") as f:  # writes comments to local file
                    f.write(data)
                    
                try:
                    if RUN_NAME == RUN_NAME_SEARCH:  # creates completion marker file
                        os.rename(run, os.path.join(run_path, RUN_NAME + ".complete"))
                    else:
                        open(os.path.join(run_path, COMPLETION_MARKER + ".complete"), "w").close()
                except:
                    pass

            cct_iter += 1
        except Exception as a:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            
            print(a)
            print(exc_type, fname, exc_tb.tb_lineno)
            print("< UNEXPECTED ERROR ENCOUNTERED >")


def run_handle(path):  # handles program run
    print("---------------------")

    run_path = os.path.join(path, RUN_DIR)

    if not os.path.isfile(os.path.join(run_path, RUN_NAME_SEARCH)):  # uses alternate run directories if needed
        for alt in ALT_DIRS:
            if os.path.isfile(os.path.join(os.path.join(path, alt), RUN_NAME_SEARCH)):
                run_path = os.path.join(path, alt)
                break
    
    copyfiles = os.listdir("copylib")
    
    for file in copyfiles:  # copies necessary files to student submission folder
        try:
            if os.path.isfile(os.path.join("copylib", file)):
                shutil.copy(os.path.join("copylib", file), run_path)
            else:
                shutil.copytree(os.path.join("copylib", file), os.path.join(run_path, file))
        except Exception as e:
            print("< HOMEWORK RESOURCE COPY FAILURE >")
            print(e)

    run_program(run_path, RUN_NAME)
    # runs program
    
    for file in copyfiles:  # removes copied resource files from student submission folder
        try:
            if os.path.isfile(os.path.join(run_path, file)):
                os.remove(os.path.join(run_path, file))
            else:
                shutil.rmtree(os.path.join(run_path, file))
        except Exception as e:
            print("< HOMEWORK RESOURCE DELETION FAILURE >")
            print(e)
            
    print("---------------------")

    complete = ""

    while complete.upper() != "Y" and complete.upper() != "N":  # queries for run completion information
        complete = input("Run complete? (Y/N): ")
                
    if complete.upper() == "N":  # handles incomplete program case
        complete = input("Rerun program (R), View/Rerun program (V), Edit/Rerun program (E), or mark incomplete (I): ")

        if complete.upper() == "R":  # reruns program
            complete, run_path = run_handle(path)
            
        elif complete.upper() == "V":  # displays code and reruns program
            view(run_path)
            
            input("Press enter to rerun...")
            
            complete, run_path = run_handle(path)
            
        elif complete.upper() == "E":  # opens files in editor and reruns program
            
            print("---------------------\nDisplay options:\n---------------------")
            
            x = 0
            file_num = len(FILE_NAMES)
            
            while (True):
                for x in range(file_num):
                    print(f"{x}: {FILE_NAMES[x]}")
                
                print(f"{file_num}: Quit and rerun")
                
                option = input("> ")
                
                if int(option) == file_num:
                    break
                
                try:
                    os.system(NOTEPAD_CMD + " " + os.path.join(run_path, FILE_NAMES[int(option)]))
                except Exception as e:
                    print("< SELECTION ERROR >")
                    print(e)
            
            complete, run_path = run_handle(path)
        else:
            complete = "N"
    
    return complete, run_path


def main():
    try:
        extract(ZIP_NAME, "hw")
        os.remove(ZIP_NAME)
        # extracts and removes homework zip file

    except:
        print("No hw.zip file.  Grading continuation program commencing...")
    
    try:  # creates comments folder if needed
        os.mkdir("comments")
    except:
        pass
        
    try:  # creates incomplete folder if needed
        os.mkdir("incomplete")
    except:
        pass
        
    try:  # creates copylib folder if needed
        os.mkdir("copylib")
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
                
                complete, run_path = run_handle(path)
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

                    view(run_path, file[:-4])

                    print()

                    comment_arr = []
                    data = ""

                    if len(FILE_NAMES) > 1:
                        for comments in CODE_COMMENT_TITLES:
                            if comments != []:
                                data = "\n"

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
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            
            print(a)
            print(exc_type, fname, exc_tb.tb_lineno)
            print("< ERROR - SKIPPING >\n")


if __name__ == "__main__":
    main()