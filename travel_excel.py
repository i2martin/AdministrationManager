from io import BytesIO
from os.path import isfile
import openpyxl
from datetime import datetime

from flask import send_file
from requests import get

months_croatia = ["Siječanj", "Veljača", "Ožujak", "Travanj", "Svibanj", "Lipanj", "Srpanj", "Kolovoz", "Rujan",
                  "Listopad", "Studeni", "Prosinac"]

list_of_cell_dates = ['A11', 'A12', 'A13', 'A14', 'A15', 'A16', 'A17', 'A18', 'A19', 'A20', 'A21', 'A22', 'A23', 'A24',
                      'A25', 'A26', 'A27', 'A28', 'A29', 'A30', 'A31', 'A32', 'A33']

km_arrival_cells = ['B11', 'B12', 'B13', 'B14', 'B15', 'B16', 'B17', 'B18', 'B19', 'B20', 'B21', 'B22', 'B23', 'B24',
                    'B25', 'B26', 'B27', 'B28', 'B29', 'B30', 'B31', 'B32', 'B33']

km_return_cells = ['C11', 'C12', 'C13', 'C14', 'C15', 'C16', 'C17', 'C18', 'C19', 'C20', 'C21', 'C22', 'C23', 'C24',
                   'C25', 'C26', 'C27', 'C28', 'C29', 'C30', 'C31', 'C32', 'C33']

honorarium_cell_columns = ["D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q",
                           "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "AA"]

vehicle_cells = ['D11', 'D12', 'D13', 'D14', 'D15', 'D16', 'D17', 'D18', 'D19', 'D20', 'D21', 'D22', 'D23', 'D24',
                 'D25', 'D26', 'D27', 'D28', 'D29', 'D30', 'D31', 'D32', 'D33']

total_count_cells = ["AB12", "AB13", "AB14", "AB15", "AB16", "AB17"]

filename = 'static/files/tablica-prijevoz.xlsx'
original = r'static/files/tablica-prijevoz.xlsx'
target = r'static/files/temp_files/tablica-prijevoz.xlsx'
month_year_cell = "A10"


def open_workbook(f_name):
    return openpyxl.load_workbook(filename=f_name)


def select_worksheet(workbook):
    return workbook['Obrazac']


# TODO: Save template data in memory and edit it instead of creating a copy
def travel(data, workdays, user):
    day_of_report = datetime.now().strftime("%d.%m.%Y.")
    current_month = months_croatia[datetime.now().month - 1]
    current_year = datetime.now().year
    total_arrival = 0
    total_return = 0
    if isfile(filename):
        # TODO: find a better way to link to a file
        request = get('http://127.0.0.1:5000/static/files/tablica-prijevoz.xlsx')
        buffer = BytesIO(request.content)
        workbook = open_workbook(buffer)
        worksheet = select_worksheet(workbook)
        km_arrival = data["km_arrival"]
        del data["km_arrival"]
        km_return = data["km_return"]
        del data["km_return"]
        vehicle = data["vehicle"]
        del data["vehicle"]
        del data["submit"]
        if len(data) > 0:
            print(data)
            data_keys = list(data.keys())  # convert dictionairy to list
            for i in range(0, len(data_keys)):
                worksheet[list_of_cell_dates[i]] = workdays[int(data_keys[i])]
                worksheet[km_arrival_cells[i]] = km_arrival[int(data_keys[i])]
                total_arrival = total_arrival + float(km_arrival[int(data_keys[i])])
                worksheet[km_return_cells[i]] = km_return[int(data_keys[i])]
                total_return = total_return + float(km_return[int(data_keys[i])])
                worksheet[vehicle_cells[i]] = vehicle[int(data_keys[i])]

        # add user specific fields to excel table (if they are set)
        if user.work_address is not None:
            worksheet["B6"] = user.work_address
        if user.home_address is not None:
            worksheet["B7"] = user.home_address
        if user.name is not None and user.surname is not None:
            worksheet["C5"] = user.name + " " + user.surname

        worksheet["B35"] = total_arrival
        worksheet["C35"] = total_return
        worksheet["D35"] = total_arrival + total_return
        worksheet["C38"] = day_of_report
        worksheet["A10"] = current_month + "/" + str(current_year)

        if user.transportation_fee is not None:
            worksheet["C39"] = user.transportation_fee
            worksheet["D40"] = user.transportation_fee * (total_arrival + total_return)

        workbook.save(buffer)
        buffer.seek(0)
        return send_file(BytesIO(buffer.read()), mimetype="application/vnd.ms-excel", download_name="prijevoz.xlsx", as_attachment=True)

