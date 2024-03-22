import sys
import os
from parser import Parser
from writer import Writer
from syntax import UrbanSyntax


def def convert_pdf_to_md(filename):
    parser = Parser(filename)
    parser.extract()
    piles = parser.parse()

    syntax = UrbanSyntax()

    writer = Writer()
    writer.set_syntax(syntax)
    writer.set_mode('simple')
    writer.set_title('test') # Name of file
    writer.write(piles)

    print('Your markdown is at', writer.get_location())

    return writer.get_location() 
