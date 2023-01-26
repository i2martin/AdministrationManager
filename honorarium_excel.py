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

filename = 'static/files/tablica-honorari.xlsx'
original = r'static/files/tablica-honorari.xlsx'
target = r'static/files/temp_files/tablica-honorari.xlsx'

shutil.copyfile(original, target)


# TODO: Check if the file actually exists so it doesn't crash
def open_workbook(filename):
    return openpyxl.load_workbook(filename=filename)


# TODO: Check if the sheet actually exists so it doesn't crash
def select_worksheet(workbook):
    return workbook['List1']


def get_row(i):
    if i == 0:
        return "12"
    if i == 0:
        return "13"
    if i == 0:
        return "14"
    if i == 0:
        return "15"
    if i == 0:
        return "16"


# TODO: Save template data in memory and edit it instead of creating a copy
def honorarium(data, workdays, user):
    shutil.copyfile(original, target)  # create a duplicate of .xls and open it
    workbook = open_workbook(target)
    worksheet = select_worksheet(workbook)
    subjects = data["subject"]
    class_tags = data["class_tag"]
    hours = data["hours"]
    for i in range(0, len(workdays)):
        worksheet[list_of_cell_dates[i]] = workdays[i]
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
    total_hours = 0
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
            total_hours = total_hours + total_count

    if total_hours != 0:
        worksheet[total_count_cells[5]] = total_hours
    if user.organisation is not None:
        worksheet["A3"] = user.organisation
    else:
        worksheet["A3"] = "Vaša organizacija/škola"
    if user.name is not None and user.surname is not None:
        worksheet["F7"] = user.name + " " + user.surname
    if user.work_address is not None:
        worksheet["A4"] = user.work_address
    else:
        worksheet["A4"] = "Vaša adresa rada"
    workbook.save(target)
