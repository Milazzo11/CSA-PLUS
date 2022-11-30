import gspread
import time
import os


w = input("INPUT WORKSHEET NUMBER > ")

gc = gspread.service_account(filename="credentials.json")
gsheet = gc.open_by_url("https://docs.google.com/spreadsheets/d/10Md0RhjnPVyUNR_grxa46mNGy_dZoMT_Dbd8nUdMrLk/edit?usp=sharing")
wsheet = gsheet.get_worksheet(int(w))
# gets google sheet and worksheet

wsheet.update("A1", "Names")
wsheet.update("B1", "Scoring")
# adds titles

data = []

m = input('ENTER DATA COPY MODE (raw: "R" or formatted "F") > ')

dirname = "comments"

if m.upper() == "F":
    dirname = "fcomms"

for file in os.listdir(dirname):  # iterates through comment files
    file_data = file.split(",")

    name = file_data[0].split("-")[-1].strip() + ", " + file_data[1].split()[0]
    # extracts student name from comment file names

    if name[-4:] == ".txt":
        name = name[:-4]

    with open(os.path.join(dirname, file), "r") as f:  # adds student comments/scoring to list
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