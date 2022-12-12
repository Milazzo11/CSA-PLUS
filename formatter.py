import os


### USERS CAN DEFINE AND USE ADDITIONAL FORMAT FUNCTIONS IF DESIRED


def dat_split(line):  # format helper function
    lform = line.split(":", 1)
    
    for x in range(len(lform)):
        lform[x] = lform[x].strip()
        
    return lform


def scores_no_rubric(line):  # formats lines to remove rubric
    data = dat_split(line)
    
    try:
        if data[-1][0] == "-" and data[-1][1] != "0":
            return data[-1] + "\n"
        elif data[0][:5].upper() == "TOTAL":
            return "SCORE:" + line[6:]
    except:
        pass
    
    return ""


def scores_part_rubric(line):  # formats lines to partially remove rubric
    data = dat_split(line)
    
    try:
        if data[-1][0] == "-" and data[-1][1] != "0":
            return data[-1] + "; " + data[0] + "\n"
        elif data[-1][0] == "*":
            return data[-1][1:] + "; " + data[0] + "\n"
        elif data[0][:5].upper() == "TOTAL":
            return "SCORE:" + line[6:]
    except:
        pass
    
    return ""

    
def scores_w_rubric(line):  # displays feedback on new line
    data = dat_split(line)
    
    if len(data) != 2:
        return line
    
    try:
        return data[0] + ":\n" + data[1] + "\n"
    except:
        return ""


### USERS CAN CHANGE OPTIONS IF ADDITIONAL FUNCTIONS ADDED
print("FORMATTING OPTIONS:")
print("0 - display lost points with comments and rubric section")
print("1 - only display lost points with comments (no rubric)")
print("2 - display feedback on separate line (keep rubric)")

m = input("> ")

fline_func = scores_part_rubric

if m == "1":
    fline_func = scores_no_rubric
elif m == "2":
    fline_func = scores_w_rubric

for file in os.listdir("comments"):  # iterates through comment files
    
    formdat = ""
    
    with open(os.path.join("comments", file), "r") as f:
        for line in f:
            formdat += fline_func(line)
            
    with open(os.path.join("fcomms", file), "w") as f:
        f.write(formdat)