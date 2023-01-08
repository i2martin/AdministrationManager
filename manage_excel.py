import pandas
import openpyxl

list_of_cell_dates = ["D10", "E10", "F10", "G10", "H10", "I10", "J10", "K10", "L10", "M10", "N10", "O10", "P10", "Q10",
                      "R10", "S10", "T10", "U10", "V10", "W10", "X10", "Y10", "Z10", "AA10"]

subject_cells = ["A12", "A13", "A14", "A15", "A16"]
class_tag_cells = ["B12", "B13", "B14", "B15", "B16"]


# filename='static/files/tablica-honorari.xlsx'


# TODO: Check if the file actually exists so it doesn't crash
def open_workbook(filename):
    return openpyxl.load_workbook(filename=filename)


# TODO: Check if the sheet actually exists so it doesn't crash
def select_worksheet(workbook):
    return workbook['List1']

def get_row(i):
    if i == 0:
        return "B"
def honorarium(data):
    workbook = open_workbook('static/files/tablica-honorari.xlsx')
    worksheet = select_worksheet(workbook)
    subjects = data["subject"]
    class_tags = data["class_tag"]
    hours = data["hours"]
    #TODO: Fix line 33 to split hours properly
    hours_rows = [hours[x:x + 23] for x in range(0, len(hours), len(hours)/5)]
    print(hours_rows)
    """for i in range(0, subjects):
        if subjects[i] != '':
            worksheet[subject_cells[i]] = subjects[i]
            worksheet[subject_cells[i]] = class_tags[i]
            row = get_row(i)
            for j in range (0,24):"""


