## latex-convert.py

Converts a .csv formatted table in the following format: 
  
![alt tag](https://github.com/kev-zheng/latex-convert/blob/master/homework_table_EECS203.png)
  
into a standard LaTeX template  
![alt tag](https://github.com/kev-zheng/latex-convert/blob/master/tex_example_EECS203.png)

Resulting example PDF
![alt tag](https://github.com/kev-zheng/latex-convert/blob/master/pdf_example_EECS203.png)

## Installation
Clone this repository into a preferred directory and move into it with:
```
git clone https://github.com/kev-zheng/latex-convert.git
cd latex-convert
```

## Usage
First format your pdf file into the correct .csv format  
PDF readers like Adobe Acrobat, Okular should have this functionality

Place the .csv into the latex-convert folder

Run:
```
 python3 latex-convert.py [filename]
```
