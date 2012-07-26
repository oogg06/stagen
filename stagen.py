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


PARAMETERS_PATH     =   "/home/oscar/repos/stagen/params.cfg"

config_file =ConfigParser.RawConfigParser()
config_file.read(PARAMETERS_PATH)


TEMPLATE_PATH       =   config_file.get("basic_parameters", "TEMPLATE_PATH")
DEFAULT_EMPTY_FILE  =   config_file.get("basic_parameters", "DEFAULT_EMPTY_FILE")
DESTINATION_FOLDER_NAME=config_file.get("basic_parameters", "DESTINATION_FOLDER_NAME")
print "Destination is "+DESTINATION_FOLDER_NAME
SITE_TITLE             =config_file.get("basic_parameters", "SITE_TITLE")
LANG                   =config_file.get("basic_parameters", "LANG")
        
class Processor:
    def __init__(self):
        self.markdown=markdown.Markdown()

    def get_template_elements(self):
        """ Auxiliary function that extracts all parameters from the configuration file """
        elements=dict()
        elements['title']   =   SITE_TITLE
        elements['lang']    =   LANG
        return elements
    def get_parameter(self, param, section="basic_parameters"):
        """ Extract a parameter from the configuration file"""
        return self.config_file.get(section, param)
        
    
    def ensure_dir(self, filename):
        d = os.path.dirname(filename)
        if not os.path.exists(d):
            os.makedirs(d)
    
    
    def add_folder_name_to_filename(self, filename):
        if filename[0:2]=="./":
            return os.path.join(DESTINATION_FOLDER_NAME, filename[2:])
        return os.path.join(DESTINATION_FOLDER_NAME, filename)
        
    def build_destination_filename(self, filename):
        (name, extension)=os.path.splitext(filename)
        filename=name+".html"
        return self.add_folder_name_to_filename(filename)
        
    def process_file(self, filename):
        """ Reads a file, converts it from Markdown to HTML and inserts
        the converted HTML into a template
        """
        
        #If the filename is not a Markdown file, copy it as is and stop
        if not self.is_markdown_file(filename):
            destination_filename=self.add_folder_name_to_filename(filename)
            self.ensure_dir(destination_filename)
            shutil.copy(filename, destination_filename)
            return
        
        #This file uses Markdown syntax
        the_file=codecs.open(filename, mode="r", encoding="utf-8")
        text=the_file.read()
        html=self.markdown.convert(text)
        
        #Read basic elements to be inserted in the final HTML, like language or title
        elements=self.get_template_elements()
        
        the_template_file=open(TEMPLATE_PATH)
        
        destination_filename=self.build_destination_filename(filename)
        print "HTML result file stored in:"+destination_filename
        #We need to ensure that the destination directory (included in destination_filename really exists
        
        self.ensure_dir(destination_filename)
        
        
        
        
        #The new HTML file will have the same name, but replacing the extension ".md" with ".html"
        the_html_result=open(destination_filename, "w+")
        
        #This template is rendered by Cheetah
        template=Template(the_template_file.read(), searchList=[elements])
        template.contents=html
        
        the_html_result.write(str(template))
        the_html_result.close()

    def is_markdown_file(self, filename):
        (filename, extension)=os.path.splitext(filename)
        if (extension==".md"):
            print filename + " is a markdown file"
            return True
        return False
    
    
    def traverse(self, directory):
        
        for root, dirs, files in os.walk(directory):
            folder_to_visit=os.path.join(directory,)
            print "Folder to visit is "+folder_to_visit
            if DESTINATION_FOLDER_NAME in dirs:
                    dirs.remove(DESTINATION_FOLDER_NAME)
            for f in files:
                path_name=os.path.join(root, f)
                #print "Processing "+path_name
                self.process_file(path_name)
                        
    def traverse2(self, directory):
        print "Traversing to avoid "+DESTINATION_FOLDER_NAME
        for root, dirs, files in os.walk(directory):
            print "Dir is:"+dirs
            print "Destination is:"+DESTINATION_FOLDER_NAME
            if dirs==DESTINATION_FOLDER_NAME:
                print "Avoiding "+str(dirs)
                continue
            for f in files:
                path_name=os.path.join(root, f)
                self.process_file(path_name)
    
        
        
    
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
    #print args
    processor=Processor()
        
    if args.new:
        
        print "Building a new site in "+args.new+"..."
        stagen=Stagen()
        stagen.tree_creator(args.new)
        sys.exit()
    else:
        processor.traverse(".")