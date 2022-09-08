import json
import time

import xlrd
import requests
from math import sqrt

class Building_Number:

    def __init__(self, id, x, y, real_x =0.0, real_y=0.0, color=(1,0,0),
                 prefix = None, suffix = None, from_range = False,
                 original_range = None, category = 'valid'):
        # Param
        # id : (int) the building number
        # x : (float) x coordinate in the pdf map
        # y : (float) y coordinate in the pdf map
        # color : (tuple of three elements) char color
        # prefix : (string) prefix in the building number
        # suffix : (string) suffix in the building number
        # from_range : (bool) whether the building number comes from a range
        # original_range: (string) the original range the building number comes from
        # category: (string) 'valid' , 'unclear' or 'garbage'

        # real_x : (float) Longitude
        # real_y : (float) Latitude
        self.id = id
        self.x = x
        self.y = y
        self.color = color
        self.prefix = prefix
        self.suffix = suffix
        self.category = category
        self.real_x = real_x
        self.real_y = real_y

        self.from_range = from_range
        self.original_range = original_range

    def __lt__(self, other):
        return self.real_x < other.real_x

    def get_id(self):
        return self.id

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def set_x(self, k):
        self.x = k

    def set_y(self, k):
        self.y = k

    def get_real_x(self):
        return self.real_x

    def get_real_y(self):
        return self.real_y

    def set_real_x(self, k):
        self.real_x = k

    def set_real_y(self, k):
        self.real_y = k

    def get_color(self):
        return self.color

    def get_prefix(self):
        return self.prefix

    def get_suffix(self):
        return self.suffix

    def get_category(self):
        return self.category

    def get_from_range(self):
        return self.from_range

    def get_original_range(self):
        return self.original_range

    def print(self): # used for debug
        print("ID = {} | Real X = {} | Real Y = {}".format(self.get_id(), self.get_real_x(), self.get_real_y()))

    @staticmethod
    def find_distance(a, b):
        # return sqrt( ((a.get_real_x() - b.get_real_x())**2) + ((a.get_real_y() - b.get_real_y())**2) )

        # return sqrt(((a.get_real_x() - b.get_real_x()) ** 2) + ((a.get_real_y() - b.get_real_y()) ** 2))

        url = f"https://maps.googleapis.com/maps/api/distancematrix/json?origins={a.get_real_x()}%2C{a.get_real_y()}&destinations={b.get_real_x()}%2C{b.get_real_y()}&mode=walking&key=AIzaSyCJiBASl_zLoCAds2gdYIENrQRTVPJksK0"

        try_count = 3
        while try_count > 0:
            try:
                print("a = {}, {}\nb = {}, {}".format(a.get_real_x(), a.get_real_y(), b.get_real_x(),
                                                                     b.get_real_y()))
                response = requests.get(url)
                response = json.loads(response.text)
                distance = response['rows'][0]['elements'][0]['distance']['value']
                print("distance = {}".format(distance))
                return distance
            except Exception as ex:
                if try_count <= 0:
                    print("Failed to retrieve " + url + "\n" + str(ex))
                    return -1
                else:
                    print("Error " + str(ex) + " occurred " + str(3 - try_count) + "times.")
                    try_count -= 1
                    time.sleep(0.5)

    def __sub__(self, other):
        return Building_Number(id=self.get_id(), color=self.get_color(), prefix=self.get_prefix(), suffix=self.get_suffix(),
                                    from_range=self.get_from_range(), original_range=self.get_original_range(),
                               category=self.get_category(),
                               x=self.get_x() - other.get_x(), y=self.get_y() - other.get_y(),
                               real_x=self.get_real_x() - other.get_real_x(), real_y=self.get_real_y() - other.get_real_y())

    def __add__(self, other):
        return Building_Number(id=self.get_id(), color=self.get_color(), prefix=self.get_prefix(), suffix=self.get_suffix(),
                                    from_range=self.get_from_range(), original_range=self.get_original_range(),
                               category=self.get_category(),
                               x=self.get_x() + other.get_x(), y=self.get_y() + other.get_y(),
                               real_x=self.get_real_x() + other.get_real_x(), real_y=self.get_real_y() + other.get_real_y())

    def __mul__(self, other):
        return Building_Number(id=self.get_id(), color=self.get_color(), prefix=self.get_prefix(), suffix=self.get_suffix(),
                                    from_range=self.get_from_range(), original_range=self.get_original_range(),
                               category=self.get_category(),
                               x=self.get_x() * other, y=self.get_y() * other,
                               real_x=self.get_real_x() * other, real_y=self.get_real_y() * other)

def read_data_from_xls(file):
    book = xlrd.open_workbook(file)
    sheet1 = book.sheet_by_index(0)

    building_number_list = []
    for i in range(1, sheet1.nrows):
        try:
            id = int(sheet1.cell(i, 0).value)
            x = float(sheet1.cell(i, 1).value)
            y = float(sheet1.cell(i, 2).value)
            color = (float(sheet1.cell(i, 3).value), float(sheet1.cell(i, 4).value), float(sheet1.cell(i, 5).value))
            prefix = sheet1.cell(i, 6).value
            suffix = sheet1.cell(i, 7).value
            from_range = sheet1.cell(i, 8).value
            original_range = sheet1.cell(i, 9).value
            category = sheet1.cell(i, 10).value
            real_x = float(sheet1.cell(i, 11).value)
            real_y = float(sheet1.cell(i, 12).value)
            if category != 'garbage':
                building_number_list.append(
                    Building_Number(id=id, x=x, y=y,
                                    color=color, prefix=prefix, suffix=suffix,
                                    from_range=from_range, original_range=original_range, category=category,
                                    real_x=real_x, real_y=real_y)
                )
        except:
            continue
    return building_number_list