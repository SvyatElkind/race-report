"""Module contains helper functions for creating Response in xml or json format"""

from typing import Union, Optional
from flask import request, Response, jsonify
import xml.etree.ElementTree as ET

from app.constants import FORMAT_PARAMETER, XML_FORMAT, DRIVER_TAG, ENCODING,\
    ERROR_TAG, APPLICATION_XML


def xml_to_str(xml_tree: ET.Element) -> str:
    """Convert xml to string.

    Args:
        xml_tree: xml tree to convert.
    """
    return ET.tostring(xml_tree, encoding=ENCODING, xml_declaration=True)


def create_xml_tree(root: ET.Element, data: Union[list[dict], dict, str]) -> ET.Element:
    """Function for recursive xml tree generation.

    Parse income data to xml tree.

    Args:
        root: root element of the tree.
        data: data to parse.

    Returns:
        xml tree.
    """
    # Go through list and create Element for every object inside the list.
    if type(data) == list:
        for obj in data:
            root.append(create_xml_tree(ET.Element(DRIVER_TAG), obj))
    # Each key value pair is on element in xml
    elif type(data) == dict:
        for k, v in data.items():
            child = ET.Element(k)
            child.text = str(v)
            root.append(child)
    # Used for error response where xml contains only one element:
    # <error>error message</error>
    elif type(data) == str:
        root.text = str(data)
    return root


def create_response(response_format: Optional[str],
                    data: Union[list[list], list],
                    root: str) -> Response:
    """Generates response in json or xml format.

    Args:
        response_format: response format.
        data: data that should be parsed.
        root: root element in xml which is used when response format is xml.

    Returns:
        Response object in json or xml
    """
    if response_format == XML_FORMAT:
        # Create xml for Response.
        xml_tree = create_xml_tree(ET.Element(root), data)
        return Response(xml_to_str(xml_tree), mimetype=APPLICATION_XML)
    return jsonify(data)


def error_response(e: Exception):
    """Generates error response in xml or json format"""
    if request.args.get(FORMAT_PARAMETER) == XML_FORMAT:
        xml_tree = create_xml_tree(root=ET.Element(ERROR_TAG), data=str(e))
        return Response(xml_to_str(xml_tree), mimetype=APPLICATION_XML)
    return jsonify(error=str(e)), 200
