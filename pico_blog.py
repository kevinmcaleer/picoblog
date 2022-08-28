# Pico_blog - a simple blog application written in MicroPython for the Pico W 
# Kevin McAleer
# August 2022

from phew import server, template, logging, connect_to_wifi
from phew.template import render_template
import os
from secret import ssid, password

# if no blog folder exists create one

connect_to_wifi(ssid, password)
logging.info("connected to wifi")

logging.debug("checking if blog folder exists")
folders = os.listdir()
if "blog" not in folders:
    logging.debug("blog not found, so creating it")
    os.mkdir("blog")

def file_list(list_of_files:list)->str:
    html = "<ul>"
    
    for file in list_of_files:
        new_item = file.replace('.md','')
        html += f"<li>{new_item}</li>"
    html += "</ul>"
    return html

def render_markdown(md_file):
    html = ""
    with open(md_file,'r') as f:
        line = f.readline()
        while line:
            if '#' in line:
                line = line.replace('#','<h1>') + '</h1>'
            if "---" in line:
                line = '<hr>'
            if "##" in line:
                line = line.replace('#','<h2>') + '</h2>'
            if "###" in line:
                line = line.replace('#','<h3>') + '</h3>'
            if "####" in line:
                line = line.replace('#','<h4>') + '</h4>'
            if "#####" in line:
                line = line.replace('#','<h5>') + '</h5>'
            html += line
            line = f.readline()
        
    return html
        

@server.route("/")
def index(request):
    logging.debug("index page")
    files = os.listdir("blog")
    
    nav_list = file_list(files)
    logging.debug(nav_list)
    return render_template("index.html",nav_list=nav_list, content=render_markdown('blog/test.md'))

server.run()