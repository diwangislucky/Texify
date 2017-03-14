# latex-convert

Converts an EECS 203 pdf into a standard LaTeX template:   
![alt tag](https://github.com/kev-zheng/latex-convert/blob/master/pictures/tex_example_EECS203.png)

####Resulting example PDF  
  
![alt tag](https://github.com/kev-zheng/latex-convert/blob/master/pictures/pdf_example_EECS203.png)

## Installation
Clone this repository into a preferred directory and move into it with:
```
git clone https://github.com/kev-zheng/latex-convert.git
cd latex-convert
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
Run:
```
python3 latex-convert.py [filename.pdf]
```
Or use the included .sh file by making it executable:
```
chmox +x run.sh
./run.sh [filename.pdf]
```

Your finished .pdf files should be in a new directory called "homework"
