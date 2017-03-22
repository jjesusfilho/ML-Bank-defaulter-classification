#!/usr/bin/python3
"""
Main Solution file to start
"""
from features import Loan
import re
from sklearn.neural_network import MLPClassifier
#Open the file to train the neural network.
#Parameters:
#	1. file name
#	2. file mode
#	3. Buffer 0:no buffer, -1:System Default, +ive: Buffer Size
FEARTURES = []
RESULT = []

ISFIRSTLINE = True
#train_indessa
with open("train_indessa.csv", "r", -1) as openfileobject:
    with open('processed.csv', 'w') as file:
        for line in openfileobject:
            if ISFIRSTLINE:
                ISFIRSTLINE = False
            else:
                line = re.sub(r'(,")"{2,}', r'\1XXXXX', line)
                line = re.sub(r'[^,"]"{2,}[^",]', r'XXXXX', line)
                line = re.sub(r'"{2,}(",)', r'XXXXX\1', line)
                line = re.sub(r'(\w\d,)".+"(,<?\s?\d\d?\+? years?|,n/a)', r"\1XXXXX\2", line)
                line = re.sub(r'(,\w+,)"[^"]*"(,\d{3}xx)', r'\1XXXXX\2', line)
                line = re.sub(',".+",', ",XXXXX,", line)
                loan = Loan([x.strip() for x in line.split(",")])
                FEARTURES.append(loan.fetchfeaturesarr())
                RESULT.append(loan.getoutput())
                file.write(loan.getcsvline() + "\n")

print("Training size " + str(len(FEARTURES)))
CLF = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(10, 2), random_state=1)
CLF.fit(FEARTURES, RESULT)
OUT = CLF.predict(FEARTURES[-50:])
ERROR_COUNT = 0
CORRECT_COUNT = 0
for i, v in enumerate(RESULT[-50:]):
    if v == OUT[i]:
        CORRECT_COUNT += 1
    else:
        ERROR_COUNT += 1
print(OUT)
print(RESULT[-50:])
print("Error " + str(ERROR_COUNT))
print("Correct " + str(CORRECT_COUNT))