# An automatic searcher on airbnb.com

# Overview

Code searches through the airbnb and finds properties that fit the predifined set of instructions. 

The result is saved in an .xlsx file as a set of links.

# Installation instructions

1) Clone the repository

2) Create virtual environment (python -m venv)

3) Install requirements (pip install -r requirements.txt)

4) Set up path to your selenim Chrome drive (in const.py)

5) Run app (python run.py)

The lattest version of chrome drive is also required

# Project structure

run.py - main file, that launches an app

You need to set up maximum price of facility (in roubles), and dates of travel

const.py - file, where it is necessary to set up location (LOCATION)

main_class.py - main selenium file

urls_to_xls.py - function, that saves found properties' urls  to an .xls  file

urls.xlsx - file with links to properties
