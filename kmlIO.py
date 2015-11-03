'''
kmlIO.py
Defines methods for inputting and outputting to kml
'''

from PyGPS.NMEA import Point
import xml.etree.ElementTree as ElementTree
import xml.dom.minidom as minidom

# Converts list of points to a KML file
def pointsToKml(points, filename):
    root = ElementTree.Element("kml")
    root.attrib["xmlns"] = "http://www.opengis.net/kml/2.2"
    document = ElementTree.SubElement(root, "Document")
    for i in range(0,len(points)):
        placemark = ElementTree.SubElement(document, "Placemark")

        name = ElementTree.SubElement(placemark, "name")
        name.text = str(i)

        description = ElementTree.SubElement(placemark, "description")
        description.text = "Point number: " + str(i)

        point = ElementTree.SubElement(placemark, "Point")
        coordinates = ElementTree.SubElement(point, "coordinates")
        coordinates.text = str(points[i].lng) + "," + str(points[i].lat) + "," + str(points[i].alt)

    # Write out to file
    rough_string = ElementTree.tostring(root, "utf-8")
    parsed_string = minidom.parseString(rough_string)
    final_string = parsed_string.toprettyxml(indent="\t")
    with open(filename, 'w') as f:
        f.write(final_string)
