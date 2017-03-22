#!/usr/bin/python3
import re
class Loan:
    """
    Loan class will get the line and preprocess it. and stores all the feature in an array
    """
    def __init__(self, fields):
		#Clean  Up the data
        self.member_id = int(fields[0])
        self.loan_status = int(fields[44])
        loan_amnt = float(fields[1])
        funded_amnt = float(fields[2])
        funded_amnt_inv = float(fields[3])
        term = int(fields[4].split(" ")[0])
        #batch_enrolled = fields[5]
        int_rate = float(fields[6])
        #grade = fields[7]
        sub_grade = [0 for _ in range(35)]
        temp = fields[8]
        sub_grade[(ord(temp[0]) - 65)*5 + int(temp[1]) -1] = 1
        #emp_title = fields[9]
        temp = fields[10]
        emp_length = 0 if temp[0] == '<' else 10 if temp.split(" ")[0][-1:] == '+' else (
            5 if temp == 'n/a' else int(temp.split(" ")[0]))
        temp = fields[11]
        home_ownership = [0, 0, 0, 0]
        home_ownership[
            0 if temp == "RENT" else 1 if temp == "MORTGAGE" else 2 if temp == "OWN" else 3
        ] = 1
        annual_inc = float(fields[12] or '1')
        verification_status = [0, 0, 0, 0]
        verification_status[
            0 if fields[13] == 'Verified' else 1 if fields[13] == 'Not Verified' else (
                2 if fields[13] == 'Source Verified' else 3)
        ] = 1
        pymnt_plan = 0 if fields[14] == 'n' else 1
        #desc = fields[15]
        #purpose = fields[16]
        #title = fields[17]
        #zip_code = fields[18]
        #addr_state = fields[19]
        dti = float(fields[20] or '0')
        delinq_2yrs = int(fields[21] or '0')
        inq_last_6mths = int(fields[22] or '0')
        mths_since_last_delinq = int(fields[23] or '0')
        mths_since_last_record = int(fields[24] or '0')
        open_acc = int(fields[25] or '0')
        pub_rec = int(fields[26] or '0')
        #revol_bal = float(fields[27] or '0')
        revol_util = float(fields[28] or '0')
        total_acc = int(fields[29] or '0')
        initial_list_status = 0 if fields[30] == 'w' else 1
        total_rec_int = float(fields[31] or '0')
        total_rec_late_fee = float(fields[32] or '0')
        recoveries = float(fields[33] or '0')
        collection_recovery_fee = float(fields[34] or '0')
        collections_12_mths_ex_med = int(fields[35] or '0')
        mths_since_last_major_derog = int(fields[36] or '0')
        application_type = 1 if fields[37] == 'INDIVIDUAL' else 0
        #verification_status_joint = fields[38]
        last_week_pay = (int(re.match(r"^\d+", fields[39]).group(0)) if not re.match(r"^\d+", fields[39]) == None else 0)
        acc_now_delinq = int(fields[40] or '0')
        tot_coll_amt = float(fields[41] or '1')
        tot_cur_bal = float(fields[42] or '0')
        #total_rev_hi_lim = float(fields[43])
        self.annual_inc = annual_inc
        self.tot_coll_amt = tot_coll_amt
        #print(str(loan_amnt) + " : " + str(funded_amnt) + " : " + str(annual_inc))
        self.features = [
            funded_amnt / (1 + loan_amnt),
            funded_amnt_inv / (1 + funded_amnt),
            (loan_amnt - funded_amnt) / (1 + annual_inc),
            funded_amnt / (1 + annual_inc),
            total_rec_late_fee / (1+ tot_coll_amt),
            total_rec_int / (1+ tot_coll_amt),
            collection_recovery_fee / (1 + tot_coll_amt),
            term,
            int_rate,
            emp_length,
            pymnt_plan,
            dti,
            delinq_2yrs,
            inq_last_6mths,
            mths_since_last_delinq,
            mths_since_last_record,
            open_acc,
            pub_rec,
            revol_util,
            total_acc,
            initial_list_status,
            recoveries,
            collections_12_mths_ex_med,
            mths_since_last_major_derog,
            application_type,
            last_week_pay,
            acc_now_delinq,
            tot_cur_bal
        ] + home_ownership + verification_status + sub_grade

    def getcsvline(self):
        """
         A getter method for providing csv type line for one entry
        """
        return str(self.member_id) + "," + ",".join([str(x) for x in self.features]) + "," + str(self.loan_status)
