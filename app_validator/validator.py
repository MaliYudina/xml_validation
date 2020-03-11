import lxml
from lxml import etree
import logging


INIT_XML_FILE = 'init_xml.xml'
XSD_FILE = 'xsd_file.xsd'
XSD_TRANS_FILE = 'trans_xsd.xsd'
XSLT_FILE = 'xslt_file.xslt'
FINAL_XML = 'final_xml.xml'


logging.basicConfig(level=logging.INFO)
LOG = logging.getLogger('validator')


def make_schema(schema_stream):
    """
    Obtain XML schema from XSD file.
    """
    LOG.info("-----> Parsing XSD file to obtain XML schema")
    tree = etree.fromstring(schema_stream)
    schema = etree.XMLSchema(tree)
    LOG.info("Schema obtained")
    return schema


def validate_xml(schema, xml_stream):
    """
    Validate initial XML file using XSD file.
    """
    LOG.info("-----> Validating the initial XML against the Schema")
    parser = etree.XMLParser(schema=schema)
    etree.fromstring(xml_stream, parser)
    LOG.info("Validation passed. XML corresponds to the Schema")


def apply_template(xml_stream, xslt_stream):
    """
    Apply template style on the validated XML file.
    """
    LOG.info("-----> Transforming the validated initial XML file using XSLT")
    xslt = etree.fromstring(xslt_stream)
    transform_obj = etree.XSLT(xslt)
    xml = etree.fromstring(xml_stream)
    tr_xml = transform_obj(xml)
    LOG.info("Transformation is done")
    return etree.tostring(tr_xml, pretty_print=True, encoding='utf8')


def final_write(tr_xml):
    """
    Writing down the new validated XML content as new XML file.
    """
    logging.info("-----> Writing down the final XML file")
    with open(FINAL_XML, 'wb') as f:
        f.write(tr_xml)
    logging.info("Successfully finish the program!")


def main():
    try:
        in_xml = open(INIT_XML_FILE, 'rb').read()
        in_xsd = open(XSD_FILE, 'rb').read()
        in_xsd_output = open(XSD_TRANS_FILE, 'rb').read()
        in_xslt = open(XSLT_FILE, 'rb').read()

        schema_xml = make_schema(in_xsd)
        validate_xml(schema=schema_xml, xml_stream=in_xml)
        schema_xml = make_schema(in_xsd_output)
        transformed = apply_template(xml_stream=in_xml, xslt_stream=in_xslt)
        validate_xml(schema=schema_xml, xml_stream=transformed)
        final_write(tr_xml=transformed)
    except lxml.etree.XMLSyntaxError as err:
        LOG.exception(err)
    except OSError as err:
        LOG.exception('invalid or missing file: %s', err)
