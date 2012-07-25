stagen
======

A static site generator written in Python

To create a new site just type:

	
	stagen.py new <directory>

Populate the new directory with files with the extension .md (and of course written using Markdown syntax) and then build your site with


	stagen.py build

Requirements
============

To use it you will need

* A working Python environment
* Install Cheetah, a Python template engine (http://www.cheetahtemplate.org)
* Install Markdown, a Python package to process Markdown files (http://pypi.python.org/pypi/Markdown#downloads)
* Have a basic knowledge of Markdown syntax (http://pypi.python.org/pypi/Markdown#downloads)

Use
===

1. Edit the params.cfg file and modify the SITE_TILE (all your pages will show this message). Edit also the LANG parameter to the language you will use in your website
2. Edit the template.html file. This file has a basic HTML structure and header. All your pages will have this structure. You can also edit the CSS ;)
3. Edit the index.md and write all your thoughts. You can create also new .md files and fill them with whatever you want. Remember that when creating links you will have to link to .html result files, not .md files!
4. Run stagen.py and visit the newly-created html directory. There you will find your website in HTML