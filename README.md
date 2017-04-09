# latex-convert

Converts an EECS 203 pdf into a standard LaTeX template:  
![alt tag](https://github.com/kev-zheng/latex-convert/blob/master/pictures/homework_example_EECS203.png =100x20)

![alt tag](https://github.com/kev-zheng/latex-convert/blob/master/pictures/tex_example_EECS203.png)

#### Resulting example PDF  
  
![alt tag](https://github.com/kev-zheng/latex-convert/blob/master/pictures/pdf_example_EECS203.png)

## Installation
Clone this repository into a preferred directory and move into it with:
```
git clone https://github.com/kev-zheng/latex-convert.git
cd latex-convert
```
Make file executable and create a symlink to use this script anywhere
```
chmod +x latex-convert.py
ln -s $PWD/latex-convert.py /usr/local/bin/latex-convert
```

## Dependencies
latex-convert.py uses __Python 3__,  __Pandas__, and __Tabula__.
Install [pandas](http://pandas.pydata.org/) and [tabula (Python wrapper)](https://github.com/chezou/tabula-py) using your preferred package manager.
```
pip3 install pandas
pip3 install tabula-py
pip3 install requests
```
tabula-py also requires you to have Java 7 or 8 installed, so make sure to check tabula-py's dependencies.
## Usage
Run in .pdf directory
```
latex-convert [FILEPATH.pdf]
```
Your finished .tex file should be in a new directory called "FILEPATH"

