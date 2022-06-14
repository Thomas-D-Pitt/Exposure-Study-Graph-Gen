import matplotlib.pyplot as plt
import pandas as pd
import sys




# Change these Values
P_NUM = "1-11"
DATA_TYPE = "ALL"
QUESTION = "Q7"
SHOW = True
file_name = "./exposureStudyResponses.xlsx"
AVERAGE = True
NANS_AS_ZEROS = False
#

SAVE = not SHOW
sheet =  ["Responses"]

class constants():
    THERMAL = 0
    MIC = 1
    LIGHT = 2
    PIR = 3
    RADAR = 4
    ACC = 5
    CAM = 6

    Q1 = 0
    Q2 = 1
    Q3 = 2
    Q4 = 3
    Q5a = 4
    Q5b = 5
    Q6a = 6
    Q6b = 7
    Q6c = 8
    Q7 = 9

class question_text():
    Q1 = "This use of my data would be beneficial to me"
    Q2 = "I think scenarios like this happen today"
    Q3 = '(If "disagree: or "strongly disagree" for Q2) I think scenarios like this will happen within 2 years'
    Q4 = '(If "disagree: or "strongly disagree" for Q3) I think scenarios like this will happen within 10 years'
    Q5a = "How would you feel about the data collection in the situation described above if you were not told with whom the data would be shared, how long it would be kept, or how long it would be used for"
    Q5b = "How would you feel about the data collection in the situation described above if you were given no additional information about the scenario"
    Q6a = "I would like to be notified every thime the data collection occurs"
    Q6b = "I would like to be notified only the first time the data collection occurs"
    Q6c = "I would like to be notified every once in a while when this data collection occurs"
    Q7 = "If you had the choice, would you allow or deny this data collection"

def makePlot():
    ROW = (P_NUM - 1) * 8 + getattr(constants, DATA_TYPE)


    df = pd.read_excel(io=file_name, sheet_name=sheet)


    dataPairs = []
    i = 0
    while i * 11 + 2 + getattr(constants, QUESTION) < len(df["Responses"].columns):
        val = df["Responses"].iloc[ROW,i * 11 + 2 + getattr(constants, QUESTION)]
        if (isNaN(val) and NANS_AS_ZEROS) or type(val) == str: #val is NaN
            if QUESTION == "Q7":
                if "*" in val:
                    val = int(val.replace("*", "")) * .5 + .25
                    dataPairs.append((i+1, val))
                else:
                    val = .5
                    dataPairs.append((i+1, val))
        else:
            dataPairs.append((i+1, val))
        
        i += 1
    plt.clf()
    plt.plot(*zip(*dataPairs))
    plt.xlabel('Exposure Level')
    plt.ylabel('Response')
    title = F'{DATA_TYPE} data for PID: {df["Responses"].iloc[(P_NUM - 1) * 8, 0]}'
    plt.title(title) 
    if QUESTION != "Q7":
        plt.ylim([.5, 5.5])
    else:
        plt.ylim([-.1, 1.1])
    plt.xlim([.5, 6.5])
    
    if SHOW:
        plt.show()
    if SAVE:
        plt.savefig(F"{QUESTION}_{DATA_TYPE}_{df['Responses'].iloc[(P_NUM - 1) * 8, 0]}.png", format = 'png')

def isNaN(val):
    return val != val

def makePlotAvg():
    
    df = pd.read_excel(io=file_name, sheet_name=sheet)

    dataPairs = []
    i = 0
    while i * 11 + 2 + getattr(constants, QUESTION) < len(df["Responses"].columns):
        dataPairs.append((i, 0))
        i += 1
    for participant in P_NUM:
        ROW = (participant - 1) * 8 + getattr(constants, DATA_TYPE)
        i = 0
        while i * 11 + 2 + getattr(constants, QUESTION) < len(df["Responses"].columns):
            val = df["Responses"].iloc[ROW,i * 11 + 2 + getattr(constants, QUESTION)]
            
            if (isNaN(val) and NANS_AS_ZEROS) or type(val) == str: #val is NaN
                if QUESTION == "Q7":
                    if "*" in val:
                        val = int(val.replace("*", "")) * .5 + .25
                        dataPairs[i] = ((i+1, dataPairs[i][1] + val))
                    else:
                        val = .5
                        dataPairs[i] = ((i+1, dataPairs[i][1] + val))
            else:
                dataPairs[i] = ((i+1, dataPairs[i][1] + val))

            i += 1

    for i in range(len(dataPairs)):
        dataPairs[i] = (dataPairs[i][0], dataPairs[i][1] / len(P_NUM))
    plt.clf()
    plt.plot(*zip(*dataPairs))
    plt.xlabel('Exposure Level')
    plt.ylabel('Response')
    PID = ""
    for i in P_NUM:
        PID += df["Responses"].iloc[(i - 1) * 8, 0] + ", "
    PID = PID[:-2]
    if P_NUM_ALL:
        title = F'Avg. {DATA_TYPE}, {QUESTION}, PID: ALL'
    else:
        title = F'Avg. {DATA_TYPE}, {QUESTION}, PID: {PID}'
    
    plt.suptitle(title, fontsize=10)
    plt.title(getattr(question_text, QUESTION),fontsize=7)
    if QUESTION != "Q7":
        plt.ylim([.5, 5.5])
    else:
        plt.ylim([-.1, 1.1])
    plt.xlim([.5, 6.5])
    
    if SHOW:
        plt.show()
    if SAVE:
        if P_NUM_ALL:
            plt.savefig(F"{QUESTION}_Avg_{DATA_TYPE}_ALL.png", format = 'png')
        else:
            plt.savefig(F"{QUESTION}_Avg_{DATA_TYPE}_{PID}.png", format = 'png')


if __name__ == '__main__':
    if DATA_TYPE == "ALL":
        DATA_TYPE = ["THERMAL", "MIC", "LIGHT", "PIR", "RADAR", "ACC", "CAM"]
    if P_NUM == '1-11':
        P_NUM_ALL = True
    else:
        P_NUM_ALL = False
    P_NUM_arr = P_NUM.split(",")
    P_NUM = []
    for part in P_NUM_arr:
        if "-" in part:
            split = part.split("-")
            for i in range(int(split[0]), int(split[1])+1):
                P_NUM.append(i)
        else:
            P_NUM.append(int(part))

    if len(P_NUM) == 1:
        P_NUM = P_NUM[0]

    if not SHOW and not SAVE:
        print("both show and save are false")

    elif type(P_NUM) == list:
        arr = P_NUM
        if AVERAGE:
            if type(DATA_TYPE) == list:
                types = DATA_TYPE
                for data in types:
                    DATA_TYPE = data
                    makePlotAvg()
            else:
                makePlotAvg()
        else:
            if type(DATA_TYPE) == list:
                types = DATA_TYPE
                for elem in P_NUM:
                    P_NUM = elem
                    for data in types:
                        DATA_TYPE = data
                        makePlot()
            else:
                for elem in P_NUM:
                    P_NUM = elem
                    makePlot()
    
    else:
        if type(DATA_TYPE) == list:
            types = DATA_TYPE
            for data in types:
                DATA_TYPE = data
                makePlot()
        else:
            makePlot()