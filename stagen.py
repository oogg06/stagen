#!/usr/bin/env python

#Stagen reads all .md files in a directory and subdirectories, and transforms them
#into HTML. The resulting HTML in inserted in an HTML template that Cheetah will
#render.

from Cheetah.Template import Template
import markdown
import codecs
import ConfigParser
import os
import sys
import shutil
import argparse

TEMPLATE_PATH="/etc/stagen/templates/default/template.html"
PARAMETERS_PATH="/etc/stagen/params.yaml"
DEFAULT_EMPTY_FILE="/etc/stagen/index.md"
DESTINATION_FOLDER_NAME="html"


class Processor:
    def __init__(self):
        self.markdown=markdown.Markdown()
        self.config_file=ConfigParser.RawConfigParser()
        self.config_file.read(PARAMETERS_PATH)
        
    def get_template_elements(self):
        """ Auxiliary function that extracts all parameters from the configuration file """
        elements=dict()
        elements['title']   =   self.get_parameter("SITE_TITLE")
        elements['lang']    =   self.get_parameter("LANG")
        return elements
    def get_parameter(self, param, section="basic_parameters"):
        """ Extract a parameter from the configuration file"""
        return self.config_file.get(section, param)
        
    
    def ensure_dir(self, filename):
        d = os.path.dirname(filename)
        if not os.path.exists(d):
            os.makedirs(d)
    
        
    def build_destination_filename(self, filename):
        filename=filename[:-3]+".html"
        if filename[0:2]=="./":
            return os.path.join(DESTINATION_FOLDER_NAME, filename[2:])
        return os.path.join(DESTINATION_FOLDER_NAME, filename)
        
    def process_file(self, filename):
        """ Reads a file, converts it from Markdown to HTML and inserts
        the converted HTML into a template
        """
        
        #This file uses Markdown syntax
        the_file=codecs.open(filename, mode="r", encoding="utf-8")
        text=the_file.read()
        html=self.markdown.convert(text)
        
        #Read basic elements to be inserted in the final HTML, like language or title
        elements=self.get_template_elements()
        
        the_template_file=open(TEMPLATE_PATH)
        
        destination_filename=self.build_destination_filename(filename)
        print "Destination:"+destination_filename
        #We need to ensure that the destination directory (included in destination_filename really exists
        self.ensure_dir(destination_filename)
        #The new file will have the same name, but replacing the extension ".md" with ".html"
        the_html_result=open(destination_filename, "w+")
        
        #This template is rendered by Cheetah
        template=Template(the_template_file.read(), searchList=[elements])
        template.contents=html
        
        the_html_result.write(str(template))
        the_html_result.close()
        
        
        
        
class FileTraverser:
    def __init__(self):
        pass
    def is_markdown_file(self, filename):
        extension=filename[-3:]
        if (extension==".md"):
            return True
        return False
    
    def traverse(self, directory):
        processor=Processor()
        for root, dirs, files in os.walk(directory):
            if dirs==DESTINATION_FOLDER_NAME:
                continue
            for f in files:
                if self.is_markdown_file(f):
                    path_name=os.path.join(root, f)
                    print "Markdown:"+path_name
                    processor.process_file(path_name)
                else:
                    pass

class Stagen:
    def __init__(self):
        pass
    
    
    def tree_creator(self, website_name):
        """ Creates the basic structure of a site in a folder called website_name"""
        #Creates a directory called html, where the HTML result will be places
        if os.path.exists(website_name):
            print "Directory already exists, aborting..."
            os.abort()
        os.mkdir(website_name)
        shutil.copy(DEFAULT_EMPTY_FILE, website_name )
        #creates a directory called html/css where the css will be places
        print "Site created!"
    
    
if __name__ == '__main__':
    
    parser=argparse.ArgumentParser(description="Stagen: Static site generator in Python")
    parser.add_argument("-n", "--new", metavar="dir", type=str, help="create a new site in the provided directory")
    
    
    args=parser.parse_args()
    print args
    processor=Processor()
        
    if args.new:
        print args.new
        print "Building a new site in "+args.new+"..."
        stagen=Stagen()
        stagen.tree_creator(args.new)
        sys.exit()
    else:
        print "Building this site..."
        file_traverser=FileTraverser()
        
        file_traverser.traverse(".")