'''
kmlIO.py
Defines methods for outputting to KML files
'''

from PyGPS.NMEA import Point
import xml.etree.ElementTree as ElementTree
import xml.dom.minidom as minidom

def pointsToKml(points, filename):
    '''
    Converts a list of NMEA.Point to a KML file
    Args:
        points: The list of points to write to a KML file
        filename: The filename to output the KML data to
    '''
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
        coordinates.text = '{0}, {1}, {2}'.format(points[i].lng, points[i].lat, points[i].alt)

    # Write out to file
    rough_string = ElementTree.tostring(root, "utf-8")
    parsed_string = minidom.parseString(rough_string)
    final_string = parsed_string.toprettyxml(indent="\t")
    with open(filename, 'w') as f:
        f.write(final_string)

def pathToKml(path, filename):
    '''
    Converts a path (ordered list of NMEA.Points) to a KML file
    Args:
        path: Ordered list of NMEA.Points
        filename: The filename to output the KML data to
    '''
    root = ElementTree.Element("kml")
    root.attrib["xmlns"] = "http://www.opengis.net/kml/2.2"
    document = ElementTree.SubElement(root, "Document")
    document.append(_getPathPlacemark(path))

    # Write out to file
    rough_string = ElementTree.tostring(root, "utf-8")
    parsed_string = minidom.parseString(rough_string)
    final_string = parsed_string.toprettyxml(indent="\t")
    with open(filename, 'w') as f:
        f.write(final_string)

def _getPathPlacemark(path):
    '''
    (Private) Converts a path to an placemark.
    Args:
        path: Ordered list of NMEA.Point that represent a path
    Returns:
        ElementTree.Element that is the placemark
    '''
    placemark = ElementTree.Element(document, "Placemark")
    name = ElementTree.SubElement(placemark, "name")
    name.text = "Path"
    description = ElementTree.SubElement(placemark, "description")
    description.text = "Path with: " + str(len(path)) + " waypoints."
    styleurl = ElementTree.SubElement(placemark, 'styleUrl')
    styleurl.text = "#m_ylw-pushpin"
    linestring = ElementTree.SubElement(placemark, 'LineString')
    tessellate = ElementTree.SubElement(linestring, 'tessellate')
    tessellate.text = "1"
    coordinates = ElementTree.SubElement(linestring, "coordinates")
    coordinates.text = ""
    for point in path:
        coordinates.text += '{0}, {1}, '.format(point.lng, point.lat)
