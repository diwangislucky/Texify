import pandas as pd
import os
import sys

# EFFECTS Creates a problem in the format of:
# \question[points] Section [section] Problem [problem]\\
# ([statement])
# \begin{solution}\\
#
#
#
# \end{solution}
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

def makeProblem(points, section, problemNum, statement):
    problem = "\n" + r"\question[" + str(points) + "]"
    problem += r" Section " + str(section)
    problem += r" Problem " + str(problemNum) + r"\\" + "\n"
    problem += statement + "\n"
    problem += r"\begin{solution}\\" + "\n\n\n\n"
    problem += r"\end{solution}" + "\n"
    problem += '%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%' \
               '%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n' \
               '%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%' \
               '%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%'
    return problem


def main():

    # Check arguments
    if len(sys.argv) != 2:
        print("Usage: python3 latex-convert.py [file.csv]")
        sys.exit(0)
    data_file = sys.argv[1]

    if not os.path.exists(data_file):
        print("Error: " + data_file + " does not exist")
        print("Usage: python3 latex-convert.py [file.csv]")

    # Check template
    if not os.path.exists("template.txt"):
        print("'template.txt' does not exist")
        sys.exit(0)

    # Process csv
    df = pd.read_csv(data_file)

    # Fill in missing sections
    df['Section'] = df['Section'].replace(method='ffill')

    # Split problems and problem numbers
    df['Problem Num'], df['Problem'] = df['Problem'].str.split(' ', 1).str

    # Open file to write
    if not os.path.exists("homework"):
        os.makedirs("homework")
    homework = open(os.path.join("homework", "homework.txt"), 'w')

    # Write output file
    with open('template.txt', 'r') as template:
        for line in template:
            if line == "!split\n":
                # Print problems
                for i in range(len(df)):
                    points = df["Points"][i]
                    section = df["Section"][i]
                    problemNum = df["Problem Num"][i]
                    statement = df["Problem"][i]
                    homework.write(makeProblem(points,
                                        section, problemNum, statement))
            else:
                homework.write(line)

    homework.close()
    os.rename(os.path.join("homework", "homework.txt"),
                                        os.path.join("homework", data_file[:-4] + '.tex'))


if __name__ == '__main__':
    main()
