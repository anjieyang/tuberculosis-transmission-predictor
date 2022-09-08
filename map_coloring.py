# color the clusters in original pdf maps
# Since I haven't figured out an algorithm to detect whether two clusters are neighboring,
# the coloring algorithm is...almost random coloring :)
# by Yue Zhang
import re
from common_modules import Building_Number
import os
import xml.etree.ElementTree as ET
from pdf_annotate import PdfAnnotator, Appearance, Location

class Cluster: # Cluster class

    def __init__(self, id, buildings):
        # Param
        # id : (int) cluster id
        # buildings : (list of Building_Number) buildings that belong to this cluster
        self.buildings = buildings
        self.id = id
        # center : (Building_Number) geometrical center of the cluster
        # color : color of the cluster
        self.center = self.find_center()
        self.color = None

    def __lt__(self, other):
        return self.center.get_x() < other.center.get_x()

    def get_id(self):
        return self.id

    def set_color(self, color):
        self.color = color

    def get_color(self):
        return self.color

    def find_center(self):
        x_sum = 0
        y_sum = 0
        real_x_sum = 0
        real_y_sum = 0
        for building in self.buildings:
            x_sum += building.get_x()
            y_sum += building.get_y()
            real_x_sum += building.get_real_x()
            real_y_sum += building.get_real_y()
        center_x = x_sum / len(self.buildings)
        center_y = y_sum / len(self.buildings)
        real_center_x = real_x_sum / len(self.buildings)
        real_center_y = real_y_sum / len(self.buildings)
        return Building_Number(id=self.get_id(), x=center_x, y=center_y, real_x=real_center_x, real_y=real_center_y)

    def draw_on_map(self, annotator, r, pdf_y_max):
        # Param
        # annotator : (PdfAnnotator)
        # r : (int) radius of the annotation
        # pdf_y_max : (int) height of PDF maps
        for building in self.buildings:
            x = building.get_x()
            y = building.get_y()
            id = building.get_id()
            prefix = building.get_prefix()
            suffix = building.get_suffix()
            x1 = x-r
            x2 = x+r
            y1 = pdf_y_max-y-r
            y2 = pdf_y_max-y+r
            if prefix is None:
                text = str(id)
            else:
                text = prefix + ' ' + str(id)
            if suffix is not None:
                text += ' ' + suffix

            annotator.add_annotation(
                annotation_type='square', location=Location(x1=x1, y1=y1, x2=x2, y2=y2, page=0),
                appearance=Appearance(fill=self.get_color())
            )
            annotator.add_annotation(
                annotation_type='text', location=Location(x1=x1, y1=y1, x2=x2, y2=y2, page=0),
                appearance=Appearance(content=text, fill=(1,1,1), font_size=3)
            )

DATA_PATHS = ['division_K_means']
from constants import PDF_PATH, PDF_Y_MAX
# COLORS = ['red', 'blue', 'yellow','brown', 'black', 'orange','purple', 'green']
COLORS = [(1,0,0), (0,0,1), (1,1,0),(0.4,0.2,0), (0,0,0), (0,0.5,1),(0.5,0,0.5), (0,1,0)]
RADIUS = 5
if __name__ == "__main__":
    for data_path in DATA_PATHS:
        hamlets = os.listdir(data_path)
        for hamlet in hamlets:
            if len(re.findall('division.xml', hamlet)) == 0:
                continue
            print("In {}".format(hamlet.removesuffix('.xml')))
            clusters = []
            # read .xml file
            file = ET.parse(data_path + '/' + hamlet)
            root = file.getroot()
            for group in root:
                buildings = []
                for building in group:
                    id = int(building.attrib['ID'])
                    x = float(building.attrib['X'])
                    y = float(building.attrib['Y'])
                    real_x = float(building.attrib['Longitude'])
                    real_y = float(building.attrib['Latitude'])
                    prefix = building.attrib['Prefix']
                    suffix = building.attrib['Suffix']
                    if prefix == 'None':
                        prefix = None
                    if suffix == 'None':
                        suffix = None
                    buildings.append(Building_Number(id=id, x=x, y=y, real_x=real_x, real_y=real_y,
                                                     prefix=prefix, suffix=suffix))
                if len(buildings) == 0:
                    continue
                else:
                    clusters.append(Cluster(len(clusters), buildings))

            clusters.sort()
            for i in range(len(clusters)):
                clusters[i].set_color(COLORS[i % len(COLORS)])

            # im = Image.new(mode='RGB', size=(X_MAX, Y_MAX), color='white')
            # draw = ImageDraw.Draw(im)
            annotator = PdfAnnotator(PDF_PATH + '/' + hamlet.removesuffix('_division.xml')
                                     + '_Building_No_2021_Wall.pdf')

            for cluster in clusters:
                cluster.draw_on_map(annotator=annotator, r=RADIUS, pdf_y_max=PDF_Y_MAX)

            # image_path = data_path + '/' + hamlet.removesuffix('.xml') + '.PNG'
            # im.save(image_path, 'PNG')
            pdf_path = data_path + '/' + hamlet.removesuffix('.xml') + '.pdf'
            annotator.write(pdf_path)

