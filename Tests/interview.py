# -*- coding: utf-8 -*-
"""
Script for testing assignment

The script will execute the interview.exe with the data_xxx.txt as input.
The  expected results (truth data) expected from the interview.exe for the input data is updated in the xxx_expected.txt
The actual output from interview.exe and the expected output are compared and the html test report is generated as report.html.

@author: Vijayasree
"""
import unittest

OUTPUT_FILE = "Results/report.html"

INPUT_INT_DATA = "Resources/data_int.txt"
EXPECTED_INT_DATA = "Resources/data_int_expected.txt"

INPUT_FLOAT_DATA = "Resources/data_float.txt"
EXPECTED_FLOAT_DATA = "Resources/data_float_expected.txt"

INPUT_MIXED_DATA = "Resources/data_mixed.txt"
EXPECTED_MIXED_DATA = "Resources/data_mixed_expected.txt"

INPUT_NAN_DATA = "Resources/data_nan.txt"
EXPECTED_NAN_DATA = "Resources/data_nan_expected.txt"

APPLICATION = "interview.exe"

s = ""
TC = 0
P = 0

#Assuming returncode is 0 for successful calculation
class InterviewTest (unittest.TestCase):
    def setUp(self):
        self.module = execute_application

    #All test cases will run in alpabetical order
    #This will execute last and print or generate report
    #report.html
    def test_zprintResults(self):
        global s
        global TC
        global P

        head = "<html><body>"
        table = "<table border=\"1\" width=\"100%\"><tr bgcolor=\"#335588\"><th>Test Case ID</th><th>Test case description</th><th>Expected Result</th><th>Actual Result</th><th>Test Result</th>"
        TestCases = "<h2>Total Test Cases Executed = {}</h2>".format(TC)
        PassedCases = "<h4><font color=\"green\">Total Test Cases Passed = {}</font></h4>".format(P)
        FailedCases = "<h4><font color=\"red\">Total Test Cases Failed = {}</font></h4>".format(TC - P)
        tableEnd = "</table>"
        tail = "</body></html>"

        f = open (OUTPUT_FILE, "w+")
        f.write(head)
        f.write(TestCases)
        f.write(PassedCases)
        f.write(FailedCases)
        f.write(table)
        f.write(s)
        f.write(tableEnd)
        f.write(tail)
        f.close()
        #print (s)

    #This test case can be used to validate all integer values passed to executable
    #based on return code and expected value pass or fail decided
    def test_int(self):
        print ("Int")
        expected = read_expected_value(EXPECTED_INT_DATA)
        returncode, output, error = self.module (APPLICATION, INPUT_INT_DATA) 
        actual = read_out_value(output)
        html_report_formatter("Integer Numbers", returncode, actual, error, expected)
        

    #This test case can be used to validate all float values passed to executable
    #based on return code and expected value pass or fail decided
    def test_float(self):
        print ("Float")
        expected = read_expected_value(EXPECTED_FLOAT_DATA)
        returncode, output, error = self.module (APPLICATION, INPUT_FLOAT_DATA) 
        actual = read_out_value(output)
        html_report_formatter("Decimal Numbers", returncode, actual, error, expected)

    #This test case can be used to validate all mix of Int and Float values passed to executable
    #based on return code and expected value pass or fail decided
    def test_mixed(self):
        print ("Mixed")
        expected = read_expected_value(EXPECTED_MIXED_DATA)
        returncode, output, error = self.module (APPLICATION, INPUT_MIXED_DATA) 
        actual = read_out_value(output)
        html_report_formatter("Mixed numbers", returncode, actual, error, expected)

    #This test case can be used to validate failure handling of executable
    #based on return code and expected value pass or fail decided
    def test_failure_handling(self):
        print ("Failure Case")
        expected = read_expected_value(EXPECTED_NAN_DATA)
        returncode, output, error = self.module (APPLICATION, INPUT_NAN_DATA) 
        actual = read_out_value(output)
        html_failure_data_formatter ("Failure Handling", returncode, actual, error, expected)

# This function can be used to execute the application
# Inputs: executable, the executable file of the application
#         data, the input data file for the application
# Outputs: return code, standard output, and error output from the execution
import statistics
import subprocess
def execute_application(executable, data):
    dim = []
    proc = subprocess.run(
            [executable, data],
            encoding="utf-8",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
    return proc.returncode, proc.stdout, proc.stderr

    
''' 
def execute_application(executable, input_file):
    output = []
    f = open (input_file, "r+")
    lines = f.readlines()
    f.close()
    error = 0
    returncode = 0
    for line in lines:
        data = list(line.split(','))
        numbers = [] 
        for i in data:
            if (i.isnumeric() == True):
                numbers.append(float(i))
                continue
            elif (is_float(i) == True):
                numbers.append(float(i))
                continue
            else:
                returncode = 1
                error = "Not a number"
                break

        if (error == 0):
            avg = sum (numbers) / len (numbers)
            sd = statistics.stdev(numbers)
            output.append([avg, sd])
        else:
            output.append(["Error", "Not a number"])

    #print (output)
    return returncode, output,  error
'''

def is_float(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

#This function is used to read the expected value file and return the expected value as list.
def read_expected_value (filename):
    with open(filename) as f:
        expected = f.read().splitlines()       
    return expected

#This function is used to read the output from interview.exe and return the actual value as list.
def read_out_value (output):
    actual = [y for y in (x.strip() for x in output.splitlines()) if y]
    return actual


# This function is used for HTML Failure data generation
def html_failure_data_formatter(testcase, returncode, output, error, expected):
    global s
    global TC
    global P
    
    TC += 1

    if (returncode != 0):
        if (compare_results(expected, output) == True):
            s += "<tr><td>{}</td><td>{}</td><td>{}</td><td>{}<br/>Return Code = {}<br/>Error = {}</td><td><font color=\"green\">Passed</font></td></tr>".format(TC, testcase, expected, output, returncode, error)
            P += 1
        else:
            s += "<tr><td>{}</td><td>{}</td><td>{}</td><td>{} <br/>Return Code = {}<br/>Error = {}<br/>Expected != Actual</td><td><font color=\"red\">Failed</font></td></tr>".format(TC, testcase, expected, output, returncode, error)
    else:
        s += "<tr><td>{}</td><td>{}</td><td>{}</td><td>{} <br/>Return Code = {}<br/>Error = {}</td><td><font color=\"red\">Failed</font></td></tr>".format(TC, testcase, expected, output, returncode, error)

#This is used for HTML report genreration
def html_report_formatter(testcase, returncode, output, error, expected):
    global s
    global TC
    global P
    
    TC += 1

    if (returncode == 0):
        if (compare_results(expected, output) == True):
            s += "<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td><font color=\"green\">Passed</font></td></tr>".format(TC, testcase, expected, output)
            P += 1
        else:
            s += "<tr><td>{}</td><td>{}</td><td>{}</td><td>{} <br/>Return Code = {}<br/>Error = {}<br/>Expected != Actual</td><td><font color=\"red\">Failed</font></td></tr>".format(TC, testcase, expected, output, returncode, error)
    else:
        s += "<tr><td>{}</td><td>{}</td><td>{}</td><td>{} <br/>Return Code = {}<br/>Error = {}</td><td><font color=\"red\">Failed</font></td></tr>".format(TC, testcase, expected, output, returncode, error)

#This function is used tocompare the expected and the actual results.
def compare_results(expected, output):
    exp_len = len(expected)
    out_len = len(output)

    if (exp_len != out_len):
        return False
    for i in range(exp_len):
        if (expected[i] == output[i]):
            continue
        else:
            return False
    
    return True

if __name__ == '__main__':
    unittest.main()

