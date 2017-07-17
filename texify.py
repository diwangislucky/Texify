#! /usr/bin/env python3

"""
latex-convert.py
Converts EECS 203 Homework .pdf to a .tex template

TODO: Templating using Jinja2
      Command line argument parsing

Kevin Zheng kevzheng@umich.edu
"""

import os
import sys
import tabula
import numpy as np
import pandas as pd

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 latex-convert.py [file.pdf]")
        sys.exit(0)

    pdf_file = sys.argv[1]
    template_file = "template.txt"
    script_path = os.path.dirname(os.path.realpath(__file__))

    # Check if pdf_file, template file are valid
    if not os.path.exists(pdf_file) or \
       not os.path.exists(os.path.join(script_path, template_file)):
        print("Error: {} or {} does not exist".format(pdf_file, template_file))
        sys.exit(0)

    # Open output file and directory
    if not os.path.exists("homework"):
        os.makedirs("homework")

    # Make new directory for homework
    output_dir = os.path.splitext(os.path.abspath(pdf_file))[0]
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    else:
        if input("{} exists. Overwrite contents? [y/N] ") != 'y':
            sys.exit(0)

    df = process_pdf(pdf_file)

    # Write to output .tex file
    output_file = os.path.splitext(os.path.basename(pdf_file))[0] + ".tex"

    write_tex(df, os.path.join(script_path, template_file), output_dir, output_file)


def make_problem(points, section, problem_num, statement, parts):
    """Return a string in the format of:
    \question[[points]] Section [section] Problem [problem]\\
    ([statement])
    \begin{solution}\\
    (a)\\
    (b)\\
    \end{solution}
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    """
    problem = ('\\question[{}] Section {} '.format(points, section) +
               'Problem {} \\\\\n{}\n'.format(problem_num, statement) +
               '\\begin{solution}\\\\\n')
    try:
        for part in parts:
            part = part.strip()
            if part:
                problem += '({})\\\\\n'.format(part)
    except TypeError:
        pass
    problem += ('\n\n\n\n\\end{solution}\n'
                '%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%'
                '%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n'
                '%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%'
                '%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n')
    return problem


def process_pdf(pdf_file):
    """Import and process .pdf file using Tabula and Pandas"""
    pd.options.display.max_colwidth = 100

    df = tabula.read_pdf(pdf_file, pages="all")

    # Fill in missing 'Section'
    df['Section'] = df['Section'].replace(method='ffill')

    # Concatenate problems that go on for multiple lines
    for i in range(len(df)):
        if ~np.isnan(df['Points'][i]):
            for x in range(i + 1, len(df)):
                if np.isnan(df['Points'][x]):
                    df['Problem'][i] += " {}".format(df['Problem'][x])
                else:
                    break

    # Clean up multi-lined problems without 'Points'
    df = df.dropna(axis=0, subset=['Points']).reset_index()

    # Remove unnecessary characters
    for c in r"""."'^“”/√_""":
        df['Problem'] = df['Problem'].str.replace(c, '')
    # Add $$ to math symbols
    for c in r"""<>""":
        df['Problem'] = df['Problem'].str.replace(c, '${}$'.format(c))

    # Extract numbers and problem
    df['Number'] = df['Problem'].str.extract('(^\d+\.?\d*)', expand=False)
    df['Parts'] = df['Problem'].str.extract('^\d+\.?\d*\s*([a-z,]+)', expand=False)

    # Split 'Parts' by comma into a list
    df['Parts'] = df['Parts'].str.split(",")

    return df


def write_tex(df, template_path, output_dir, output_file):
    """Write new output file with dataframe and template.txt"""
    output = open(os.path.join(output_dir, output_file), 'w')

    # Write output file
    with open(template_path, 'r') as template:
        for line in template:
            if line == "!split\n":
                for i in df.index:
                    output.write(make_problem(df["Points"][i],
                                              df["Section"][i],
                                              df["Number"][i],
                                              df["Problem"][i],
                                              df["Parts"][i]))
            else:
                output.write(line)
    output.close()


if __name__ == '__main__':
    main()
