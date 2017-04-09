#! /usr/bin/env python3

"""
latex-convert.py
Converts EECS 203 Homework .pdf to a .tex template

Kevin Zheng kevzheng@umich.edu
"""

import os
import sys
import tabula


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 latex-convert.py [file.pdf]")
        sys.exit(0)

    pdf_file = sys.argv[1]
    template_file = "template.txt"
    script_path = os.path.dirname(os.path.realpath(__file__))

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

    df = process_pdf(pdf_file)

    # Write to output .tex file
    output_file = os.path.splitext(os.path.basename(pdf_file))[0] + ".tex"
    write_tex(df, os.path.join(script_path, template_file), output_dir, output_file)


def make_problem(points, section, problem_num, statement, problem_sections):
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
        for section in problem_sections:
            section = section.strip()
            if section:
                problem += '({})\\\\\n'.format(section)
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
    df = tabula.read_pdf(pdf_file)

    # Problems that go on for two lines do not have 'Points'
    df = df.dropna(axis=0, subset=['Points']).reset_index()

    # Fill in missing 'Section'
    df['Section'] = df['Section'].replace(method='ffill')

    # Split at first period and space
    df['Number'], df['Problem'] = df['Problem'].str.split('.', 1).str
    df['Number'], df['Parts'] = df['Number'].str.split(' ', 1).str

    # Split 'Parts' by comma into a list
    df['Parts'] = df['Parts'].str.split(",")

    # Clean up ) and ""
    df['Problem'] = df['Problem'].map(lambda x: str(x).rstrip(')'))
    df['Problem'].map(lambda x: x + '"' if not x.endswith(('"', '”')) else x)

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
