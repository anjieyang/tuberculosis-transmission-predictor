from pdf_annotate import PdfAnnotator, Location, Appearance


class MapView:
    @staticmethod
    def coloring(map, path, size=10):
        annotator = PdfAnnotator(path + map.file_name)
        for cluster in map.clusters:
            cluster_id = str(cluster.id)
            cluster_color = tuple(value / 255 for value in cluster.color)
            for building in cluster.buildings:
                x = building.x
                y = building.y
                x1 = x - size
                x2 = x + size
                y1 = 3370 - y - size
                y2 = 3370 - y + size
                annotator.add_annotation(
                    annotation_type="square",
                    location=Location(x1=x1, y1=y1, x2=x2, y2=y2, page=0),
                    appearance=Appearance(fill=cluster_color, stroke_width=0),
                )
                annotator.add_annotation(
                    annotation_type="text",
                    location=Location(x1=x1, y1=y1, x2=x2, y2=y2, page=0),
                    appearance=Appearance(content=cluster_id, fill=(1, 1, 1), font_size=5),
                )
        annotator.write(path + map.file_name)

