#! /usr/bin/env python3

import tabula
import os
import sys

# EFFECTS Creates a problem in the format of:
# \question[[points]] Section [section] Problem [problem]\\
# ([statement])
# \begin{solution}\\
#
#
#
# \end{solution}
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


def makeProblem(points, section, problemNum, statement, problemSections):
    problem = ('\\question[{}] Section {} '.format(points, section) +
               'Problem {} \\\\\n{}\n'.format(problemNum, statement) +
               '\\begin{solution}\\\\\n')
    for section in problemSections:
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

    # Split 'Problem' into 'Problem Num' and 'Problem Sections' with '('
    df['Problem Num'], df['Problem'] = df['Problem'].str.split(' ', 1).str
    df['Problem Sections'], df['Problem'] = df['Problem'].str.split('(', 1).str
    df['Problem Sections'] = df['Problem Sections'].str.split(",")

    # Delete right ')' and add missing ' " '
    df['Problem'] = df['Problem'].map(lambda x: x.rstrip(')'))
    df['Problem'].map(lambda x: x + '"' if not x.endswith(('"', '”')) else x)

    return df


def write_tex(df, template_file, output_dir, output_file):
    output = open(os.path.join(output_dir, output_file), 'w')

    # Write output file
    with open(template_file, 'r') as template:
        for line in template:
            if line == "!split\n":
                # Print problems
                for i in range(len(df)):
                    points = df["Points"][i]
                    section = df["Section"][i]
                    problemNum = df["Problem Num"][i]
                    statement = df["Problem"][i]
                    problemSections = df["Problem Sections"][i]
                    output.write(makeProblem(points, section,
                                 problemNum, statement, problemSections))
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
