#! /usr/bin/env python3

# latex-convert.py
# Constructs a .tex file using an EECS 203 PDF homework
# and the "template.txt" file

import tabula
import os
import sys

# Creates a problem in the format of:
# \question[[points]] Section [section] Problem [problem]\\
# ([statement])
# \begin{solution}\\
#
#
#
# \end{solution}
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


def make_problem(points, section, problem_num, statement, problem_sections):
    problem = ('\\question[{}] Section {} '.format(points, section) +
               'Problem {} \\\\\n{}\n'.format(problem_num, statement) +
               '\\begin{solution}\\\\\n')
    for section in problem_sections:
        section = section.strip()
        if section:
            problem += '({})\\\\\n'.format(section)
    problem += ('\n\n\n\n\\end{solution}\n'
                '%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%'
                '%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n'
                '%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%'
                '%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n')
    return problem


def usage_fail():
    print("Usage: python3 latex-convert.py [file.pdf]")
    sys.exit(0)


def check_files(pdf_file, template_file):
    if not os.path.exists(pdf_file) or not os.path.exists(template_file):
        print("Error: " + pdf_file + " or " + " template_file does not exist")
        usage_fail()


def process_pdf(pdf_file):
    df = tabula.read_pdf(pdf_file)

    # Problems that go on for two lines do not have 'Points'
    df = df.dropna(axis=0, subset=['Points']).reset_index()

    # Fill in missing 'Section'
    df['Section'] = df['Section'].replace(method='ffill')

    # Split 'Problem' into 'Number' and 'Parts' with '('
    df['Number'], df['Problem'] = df['Problem'].str.split(' ', 1).str
    df['Parts'], df['Problem'] = df['Problem'].str.split('(', 1).str

    # Added handling for nan parts - aka no problem statement
    df['Parts'] = df['Parts'].str.split(",").fillna("N/A - Check Spec")

    # Delete right ')' and add missing ' " '
    df['Problem'] = df['Problem'].map(lambda x: str(x).rstrip(')'))
    df['Problem'].map(lambda x: x + '"' if not x.endswith(('"', '”')) else x)

    return df


def write_tex(df, template_file, output_dir, output_file):
    output = open(os.path.join(output_dir, output_file), 'w')

    # Write output file
    with open(template_file, 'r') as template:
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


def main():
    if len(sys.argv) != 2:
        usage_fail()

    pdf_file = sys.argv[1]
    check_files(pdf_file, "template.txt")

    process_pdf(pdf_file)

    # Open output file and directory
    if not os.path.exists("homework"):
        os.makedirs("homework")

    output_dir = os.path.join("homework", os.path.splitext(pdf_file)[0])
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    output_file = os.path.splitext(pdf_file)[0] + ".tex"

    df = process_pdf(pdf_file)

    write_tex(df, "template.txt", output_dir, output_file)


if __name__ == '__main__':
    main()
