#!/usr/bin/python3
"""
Main Solution file to start
"""
from features import Loan
import re
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
#Open the file to train the neural network.
#Parameters:
#	1. file name
#	2. file mode
#	3. Buffer 0:no buffer, -1:System Default, +ive: Buffer Size
LOAN_RECS = []

ISFIRSTLINE = True
#train_indessa
with open("./data/train_indessa.csv", "r", -1) as openfileobject:    
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
            LOAN_RECS.append(loan)
AVG_SALARY = 1
AVG_COLLECTED = 1
with open('./data/processed.csv', 'w') as file:
    for loan in LOAN_RECS:
        file.write(loan.getcsvline() + "\n")
        AVG_SALARY += loan.annual_inc
        AVG_COLLECTED += loan.tot_coll_amt
    AVG_SALARY /= len(LOAN_RECS)
    AVG_COLLECTED /= len(LOAN_RECS)
    AVG_COLLECTED /= 2
    for loan in LOAN_RECS:
        if loan.annual_inc == 1:
            loan.features[2] /= AVG_SALARY
            loan.features[3] /= AVG_SALARY
        if loan.tot_coll_amt == 1:
            loan.features[4] /= AVG_COLLECTED
            loan.features[5] /= AVG_COLLECTED
            loan.features[6] /= AVG_COLLECTED
FEARTURES = [loan.features for loan in LOAN_RECS]
RESULT = [loan.loan_status for loan in LOAN_RECS]
scaler = StandardScaler()
scaler.fit(FEARTURES)
FEARTURES = scaler.transform(FEARTURES)  
print("Training size " + str(len(FEARTURES)))
LAST_ROW = -100
CLF = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(20, 2), random_state=1)
CLF.fit(FEARTURES[:LAST_ROW], RESULT[:LAST_ROW])
OUT = CLF.predict(FEARTURES[LAST_ROW:])
ERROR_COUNT = 0
CORRECT_COUNT = 0
for i, v in enumerate(RESULT[LAST_ROW:]):
    if v == OUT[i]:
        CORRECT_COUNT += 1
    else:
        ERROR_COUNT += 1
print(OUT)
print(RESULT[LAST_ROW:])
print("Error " + str(ERROR_COUNT))
print("Correct " + str(CORRECT_COUNT))