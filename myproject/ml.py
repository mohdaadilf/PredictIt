# ML imports here
import pandas as pd
from sklearn import preprocessing
from sklearn.tree import DecisionTreeClassifier, _tree
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.svm import SVC
import csv
import warnings
import os
# GLOBAL VARIABLES
severityDictionary = dict()
description_list = dict()
precautionDictionary = dict()
condition = ''
precaution_list = []
predicted_disease = ''
predicted_disease_description = ''
predicted_disease_description2 = ''
symptoms_given = []
present_disease = ''
symptoms_exp = []
yes_or_no = []
le = ''
reduced_data = []
precaution_list2 = ''
basedir = os.path.abspath(os.path.dirname(__file__))

def get_symptoms_list():
    df = pd.read_csv(f'{basedir}/datasets/symptom_severity.csv')
    symptom_list = df['itching'].tolist()
    symptom_list.append('itching')
    symptoms_spaced = []
    for symptom in symptom_list:
        symptoms_spaced.append(symptom.replace('_',' '))
    symptoms_dict = dict(zip(symptoms_spaced, symptom_list))
    return symptom_list, symptoms_spaced, symptoms_dict

def list_to_string(mylist):
    mystring = ""
    for item in mylist:
        mystring += item.replace('_', ' ') + ', '
    mystring = mystring[:-2]
    return mystring

def train():
    # training part
    global le
    global reduced_data
    training = pd.read_csv(f'{basedir}/datasets/Training.csv')
    testing = pd.read_csv(f'{basedir}/datasets/Testing.csv')
    cols = training.columns
    cols = cols[:-1]
    x = training[cols]
    y = training['prognosis']
    y1 = y

    reduced_data = training.groupby(training['prognosis']).max()

    # mapping strings to numbers
    le = preprocessing.LabelEncoder()
    le.fit(y)
    y = le.transform(y)

    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.33, random_state=42)
    testx = testing[cols]
    testy = testing['prognosis']
    testy = le.transform(testy)

    clf1 = DecisionTreeClassifier()
    clf = clf1.fit(x_train, y_train)
    scores = cross_val_score(clf, x_test, y_test, cv=3)

    model = SVC()
    model.fit(x_train, y_train)

    importances = clf.feature_importances_
    indices = np.argsort(importances)[::-1]
    features = cols

    symptoms_dict = {}

    for index, symptom in enumerate(x):
        symptoms_dict[symptom] = index

    return clf, cols


def getDicts():
    global description_list
    global severityDictionary
    global precautionDictionary
    with open(f'{basedir}/datasets/symptom_Description.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            _description = {row[0]: row[1]}
            description_list.update(_description)

    with open(f'{basedir}/datasets/symptom_severity.csv') as csv_file:

        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            _diction = {row[0]: int(row[1])}
            severityDictionary.update(_diction)

    with open(f'{basedir}/datasets/symptom_precaution.csv') as csv_file:

        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            _prec = {row[0]: [row[1], row[2], row[3], row[4]]}
            precautionDictionary.update(_prec)


def check_pattern(dis_list, inp):
    import re
    pred_list = []
    ptr = 0
    patt = "^" + inp + "$"
    regexp = re.compile(inp)
    for item in dis_list:

        if regexp.search(item):
            pred_list.append(item)
            # return 1,item
    if(len(pred_list) > 0):
        return 1, pred_list
    else:
        return ptr, dis_list


def print_disease(node):
    global le
    node = node[0]
    val = node.nonzero()
    disease = le.inverse_transform(val[0])
    return disease


def tree_to_code(tree, feature_names, symptom1):
    global condition
    global symptoms_given
    tree_ = tree.tree_
    feature_name = [
        feature_names[i] if i != _tree.TREE_UNDEFINED else "undefined!"
        for i in tree_.feature
    ]

    chk_dis = ",".join(feature_names).split(",")
    symptoms_present = []

    while True:
        conf, cnf_dis = check_pattern(chk_dis, symptom1)
        if conf == 1:
            # print("searches related to input: ")
            # for num,it in enumerate(cnf_dis):
            #     print(num,")",it)
            # if num!=0:
            #     print(f"Select the one you meant (0 - {num}):  ", end="")
            #     conf_inp = int(input(""))
            # else:
            conf_inp = 0

            disease_input = cnf_dis[conf_inp]
            break

    def recurse(node, depth):
        global condition
        global present_disease
        global precaution_list
        global predicted_disease
        global predicted_disease_description
        global predicted_disease_description2
        global symptoms_given
        global reduced_data
        symptoms_given = []
        indent = "  " * depth
        if tree_.feature[node] != _tree.TREE_UNDEFINED:
            name = feature_name[node]
            threshold = tree_.threshold[node]

            if name == disease_input:
                val = 1
            else:
                val = 0
            if val <= threshold:
                recurse(tree_.children_left[node], depth + 1)
            else:
                symptoms_present.append(name)
                recurse(tree_.children_right[node], depth + 1)
        else:
            present_disease = print_disease(tree_.value[node])
            red_cols = reduced_data.columns
            symptoms_given = red_cols[reduced_data.loc[present_disease].values[0].nonzero()]

    recurse(0, 1)
    return symptoms_given


def recurse2(num_days):
    global condition
    global present_disease
    global precaution_list
    global precaution_list2
    global predicted_disease
    global predicted_disease_description
    global predicted_disease_description2
    global symptoms_given
    global symptoms_exp
    global yes_or_no
    global severityDictionary

    for i, option in enumerate(yes_or_no):
        if option == 'yes':
            symptoms_exp.append(list(symptoms_given)[i])

    def sec_predict(symptoms_exp):
        df = pd.read_csv(f'{basedir}/datasets/Training.csv')
        X = df.iloc[:, :-1]
        y = df['prognosis']
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.3, random_state=20)
        rf_clf = DecisionTreeClassifier()
        rf_clf.fit(X_train, y_train)

        symptoms_dict = {}

        for index, symptom in enumerate(X):
            symptoms_dict[symptom] = index

        input_vector = np.zeros(len(symptoms_dict))
        for item in symptoms_exp:
            input_vector[[symptoms_dict[item]]] = 1

        return rf_clf.predict([input_vector])

    def calc_condition(exp, days):
        sum = 0
        for item in exp:
            sum = sum+severityDictionary[item]
        if((sum*days)/(len(exp)+1) > 13):
            condition1 = "You should take the consultation from doctor."
        else:
            condition1 = "It might not be that bad but you should take precautions."
        return condition1

    

    # predicts the second disease
    second_prediction = sec_predict(symptoms_exp)
    # calculates and stores the condition
    condition = calc_condition(symptoms_exp, num_days)

    # if first and 2nd disease are same, do this
    if(present_disease[0] == second_prediction[0]):
        predicted_disease = present_disease[0]  # disease predicted

        # its description
        predicted_disease_description = description_list[present_disease[0]]
        predicted_disease_description2 = ''

    else:  # different first and second diseases
        predicted_disease = present_disease[0] + " or " + second_prediction[0]  # diseases predicted
        # descriptions
        predicted_disease_description = description_list[present_disease[0]]  
        predicted_disease_description2 = description_list[second_prediction[0]]
    # gives the list of things to do.
    precaution_list = precautionDictionary[present_disease[0]]
    precaution_list2 = precautionDictionary[second_prediction[0]]
    

if __name__ == "__main__":
    a = 2
