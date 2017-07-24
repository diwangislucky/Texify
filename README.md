# Texify

Converts an EECS 203 pdf into a standard LaTeX template using Tabula and Pandas:  
![alt tag](https://github.com/kev-zheng/texify/blob/master/pictures/homework_example_EECS203.png)
![alt tag](https://github.com/kev-zheng/texify/blob/master/pictures/tex_example_EECS203.png)

#### Resulting example PDF  
![alt tag](https://github.com/kev-zheng/texify/blob/master/pictures/pdf_example_EECS203.png)

## Installation
Clone this repository into a preferred directory and move into it with:
```
git clone https://github.com/kev-zheng/texify.git
cd texify
```

## Dependencies
texify.py uses __Python 3__,  __Pandas__, and __Tabula__.
Install [pandas](http://pandas.pydata.org/) and [tabula (Python wrapper)](https://github.com/chezou/tabula-py) using your preferred package manager.
```
pip install pandas
pip install tabula-py
pip install requests
```
tabula-py also requires you to have Java 7 or 8 installed, so make sure to check tabula-py's dependencies.
## Usage
Run in .pdf directory
```
python3 texify [FILEPATH.pdf]
```
Your finished .tex file should be in a new directory called "FILEPATH"

