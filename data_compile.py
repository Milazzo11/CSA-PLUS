import gspread
import time
import os


gc = gspread.service_account(filename="credentials.json")
gsheet = gc.open_by_url(INSERT_YOUR_GOOGLE_DOC_HERE)

"""
 You have a ton of glaring issues in your code.
 You are literally leaking the google sheet - I can edit it if I wanted to. I can see everyone's names and grades.
 
 Also, you really need to refactor your code and use classes. Feel free to message on discord.
 Do not use google sheets as a way to serve up a grade - plenty of better ways...

"""

wsheet = gsheet.get_worksheet(0)
# gets google sheet and worksheet

wsheet.update("A1", "Names")
wsheet.update("B1", "Scoring")
# adds titles

data = []

for file in os.listdir("comments"):  # iterates through comment files
    file_data = file.split(",")

    name = file_data[0].split("-")[-1].strip() + ", " + file_data[1].split()[0]
    # extracts student name from comment file names
    # configured with RIT file naming configurations
    # must be changed to use for non-RIT CS grading

    if name[-4:] == ".txt":
        name = name[:-4]

    with open(os.path.join("comments", file), "r") as f:  # adds student comments/scoring to list
        data.append((name, f.read()))

data.sort()
# sorts list

iter = 2

for people in data:

    wsheet.update("A" + str(iter), people[0])
    # adds student name to worksheet

    wsheet.update("B" + str(iter), people[1].replace("\n", "\n\n"))
    # adds student comments to worksheet
    # adds more spacing for easier viewing when data copied to grade book

    iter += 1
    time.sleep(2)
    # waits 1 second to comply with API rate limits 