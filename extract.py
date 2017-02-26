import pandas as pd
import os
import sys

def makeProblem(points, section, problemNum, statement):
    problem = r"\question[" + str(points) + "]"
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

if os.path.exists("template.txt"):
    template = open("template.txt", "r")

else:
    print("'template.txt' does not exist")
    sys.exit(0)

homework = open("homework.txt", "w")
homework.write(template.read())

df = pd.read_excel('203HW8W17.xlsx')
df['Section'] = df['Section'].replace(method='ffill')
df['Problem Num'], df['Problem'] = df['Problem'].str.split(' ',1).str

for i in range(len(df)):
    points = df["Points"][i]
    section = df["Section"][i]
    problemNum = df["Problem Num"][i]
    statement = df["Problem"][i]
    homework.write(makeProblem(points, section, problemNum, statement))

end = r"\end{questions}" + "\n\n\n" + r"\end{document}"
homework.write(end)

homework.close()