#!/usr/bin/python3
"""
Main Solution file to start
"""
from features import Loan
import re
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler

def get_processed_data(filename,isTest):
    """
    Open the file to train the neural network.
    Parameters:
    	1. file name
    	2. file mode
    	3. Buffer 0:no buffer, -1:System Default, +ive: Buffer Size
    """
    loan_recs = []
    isfirstline = True
    #train_indessa
    with open("./data/"+filename+".csv", "r", -1) as openfileobject:
        for line in openfileobject:
            if isfirstline:
                isfirstline = False
            else:
                line = re.sub(r'(,")"{2,}', r'\1XXXXX', line)
                line = re.sub(r'[^,"]"{2,}[^",]', r'XXXXX', line)
                line = re.sub(r'"{2,}(",)', r'XXXXX\1', line)
                line = re.sub(r'(\w\d,)".+"(,<?\s?\d\d?\+? years?|,n/a)', r"\1XXXXX\2", line)
                line = re.sub(r'(,\w+,)"[^"]*"(,\d{3}xx)', r'\1XXXXX\2', line)
                line = re.sub(',".+",', ",XXXXX,", line)
                if isTest:
                    line = line.strip() + ",0"
                loan = Loan([x.strip() for x in line.split(",")])
                loan_recs.append(loan)
    avg_salary = 1
    avg_collected = 1
    # with open('./data/processed.csv', 'w') as file:
    #     for loan in loan_recs:
    #         file.write(loan.getcsvline() + "\n")
    for loan in loan_recs:
        avg_salary += loan.annual_inc
        avg_collected += loan.tot_coll_amt
    avg_salary /= (2 * len(loan_recs))
    avg_collected /= (2 * len(loan_recs))
    for loan in loan_recs:
        if loan.annual_inc == 1:
            loan.features[2] /= avg_salary
            loan.features[3] /= avg_salary
        if loan.tot_coll_amt == 1:
            loan.features[4] /= avg_collected
            loan.features[5] /= avg_collected
            loan.features[6] /= avg_collected
    return loan_recs

def predictor(train, predict):
    """
    This functions runs the program
    on a subset of training data
    and uses rest to test
    """
    train_features = [loan.features for loan in train]
    train_result = [loan.loan_status for loan in train]
    test_features = [loan.features for loan in predict]
    classifier = MLPClassifier(solver='lbfgs', alpha=1e-5,
                               hidden_layer_sizes=(20,5, 2), random_state=1)
    scalar = StandardScaler()
    scalar.fit(train_features)
    train_features = scalar.transform(train_features)
    test_features = scalar.transform(test_features)
    print("Training size " + str(len(train_features)))
    print("Predict size " + str(len(test_features)))
    classifier.fit(train_features, train_result)
    return [x[1] for x in classifier.predict_proba(test_features)]

def run():
    """
        Run this for test data
    """
    loan_rec_train = get_processed_data("train_indessa",False)
    loan_rec_test = get_processed_data("test_indessa",True)
    result = predictor(loan_rec_train, loan_rec_test)
    member_arr = [loan.member_id for loan in loan_rec_test]
    with open('./data/predicted.csv', 'w') as file_:
        file_.write(" member_id, loan_status\n")
        for i, mem_id in enumerate(member_arr):
            file_.write(str(mem_id) + "," + str(result[i]) + "\n")

def testrun():
    """
        Run this for test data
    """
    no_of_test = -100
    loan_rec_train = get_processed_data("train_indessa",False)
    result = predictor(loan_rec_train[:no_of_test], loan_rec_train[no_of_test:])
    act_res = [loan.loan_status for loan in loan_rec_train[no_of_test:]]
    print(result)
    print(act_res)
    correct = 0
    error = 0
    for i, ival in enumerate(act_res):
        if ival == round(result[i]):
            correct += 1
        else:
            error += 1
    print("Correct : " + str(correct))
    print("Error : " + str(error))
#testrun()
run()
#get_processed_data("test",True)
