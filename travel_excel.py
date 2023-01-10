import pandas
import openpyxl
import shutil


list_of_cell_dates = ["D10", "E10", "F10", "G10", "H10", "I10", "J10", "K10", "L10", "M10", "N10", "O10", "P10", "Q10",
                      "R10", "S10", "T10", "U10", "V10", "W10", "X10", "Y10", "Z10", "AA10"]

subject_cells = ["A12", "A13", "A14", "A15", "A16"]

class_tag_cells = ["B12", "B13", "B14", "B15", "B16"]

honorarium_cell_columns = ["D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q",
                           "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "AA"]

total_count_cells = ["AB12", "AB13", "AB14", "AB15", "AB16", "AB17"]


filename='static/files/tablica-prijevoz.xlsx'
original = r'static/files/tablica-prijevoz.xlsx'
target = r'static/files/temp_files/tablica-prijevoz.xlsx'
month_year_cell = "A10"
shutil.copyfile(original, target)

# TODO: Check if the file actually exists so it doesn't crash
def open_workbook(filename):
    return openpyxl.load_workbook(filename=filename)


# TODO: Check if the sheet actually exists so it doesn't crash
def select_worksheet(workbook):
    return workbook['Obrazac']

def travel(data):
    shutil.copyfile(original, target) #create a duplicate of .xls and open it
    workbook = open_workbook(target)
    worksheet = select_worksheet(workbook)
    print(data)
    """subjects = data["subject"]
    class_tags = data["class_tag"]
    hours = data["hours"]
    temp = 0
    hours_rows = []
    temp_hours = []
    for hour in hours:  # split list of hours into 5 list of max 24 elements (max. 24 workdays per subject)
        temp_hours.append(hour)
        temp = temp + 1
        if temp == 24:
            hours_rows.append(temp_hours)
            temp_hours = []
            temp = 0
    print(hours_rows)
    for i in range(0, len(subjects)):
        if subjects[i] != '':
            print(subject_cells[i])
            worksheet[subject_cells[i]] = subjects[i]
            worksheet[class_tag_cells[i]] = class_tags[i]
            row = get_row(i)
            total_count = 0
            for j in range(0, len(honorarium_cell_columns)):  # loop through each hours list and add them to excel file
                worksheet[honorarium_cell_columns[j] + row] = hours_rows[i][j]
                if hours_rows[i][j] != '':  # count total hours for each subject
                    total_count = total_count + int(hours_rows[i][j])
            worksheet[total_count_cells[i]] = total_count
    workbook.save(target)"""

