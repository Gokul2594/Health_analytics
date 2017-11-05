from openerp import http
import openerp
import openerp.modules.registry
import ast
from openerp import http
from openerp.http import request
from openerp.addons.web.controllers.main import Home
from openerp.addons.web.controllers.main import Session
from openerp.addons.web.controllers import main
import datetime
import pytz
import xmlrpclib
import json
import psycopg2
import os
import sys
import pandas as pd
import pickle
from sklearn.cross_validation import train_test_split
from sklearn import tree
import numpy as np

dir_name = os.path.dirname(os.path.abspath(__file__))
feature = {}
result = {}

class Home(Home):
    
    //method to predict if hemogram level is healthy or not 
    @http.route('/health/hemogram', type='json', auth="public",csrf=False)
    def hemogram(self,hemo_data):
        #~ hemo_data = {str(key): str(value) for key, value in hemo_data.items()}
        
        //check if the patient is male and make prediction
        if str(hemo_data['sex']) == "male":
            hemogram_csv = pd.read_csv(dir_name + "/dataset/hemogram_men.csv")
            columns = hemogram_csv.iloc[:,0:len(hemogram_csv.columns)]
            for column in hemogram_csv.columns:
                try:
                    feature[column] = hemo_data[column]
                except:
                    pass
            vals = [feature['hemoglobin'],feature['pcv'],feature['rbc'],feature['mchc'],feature['mcv'],feature['mch'],feature['esr'],feature['platelets_count']]
            
            //picke the prediction to reduce the processing time, if the pickle files are present skip this step 
            if not os.path.exists(dir_name + "/pickle_files/hemogram_men.pickle"):
                read_csv = pd.read_csv(dir_name + "/dataset/hemogram_men.csv")
                X = hemogram_csv.iloc[:,0:-1] 
                y = hemogram_csv.iloc[:,-1]
                X_train,X_test,y_train,y_test = train_test_split(X,y, random_state=2)
                model = tree.DecisionTreeClassifier(criterion='gini')
                model = model.fit(X_train,y_train)
                with open(dir_name + '/pickle_files/hemogram_men.pickle','wb+') as data:
                    pickle.dump(model,data)
                if model.predict(vals) == 1:
                    result['predictions'] = "healthy"
                else:
                    result['predictions'] = "unhealthy"
                return result
       
            else:
                print "Pickle file " + "hemogram_men.csv" + ".pickle already present"
                with open(dir_name + '/pickle_files/hemogram_men.pickle','rb+') as data:
                    model = pickle.load(data)
                    if model.predict(vals) == 1:
                        result['predictions'] = "healthy"
                    else:
                        result['predictions'] = "unhealthy"
                    return json.dumps(result)
       
    //if the patient is women, make predictions
        else:
            hemogram_csv = pd.read_csv(dir_name + "/dataset/hemogram_women.csv" )
            columns = hemogram_csv.iloc[:,0:len(hemogram_csv.columns)]
            for column in hemogram_csv.columns:
                try:
                    feature[column] = hemo_data[column]
                except:
                    pass
            vals = [feature['hemoglobin'],feature['pcv'],feature['rbc'],feature['mchc'],feature['mcv'],feature['mch'],feature['esr'],feature['platelets_count']]
            if not os.path.exists(dir_name + "/pickle_files/hemogram_women.pickle"):
                read_csv = pd.read_csv(dir_name + "/dataset/hemogram_men.csv")
                X = hemogram_csv.iloc[:,0:-1] 
                y = hemogram_csv.iloc[:,-1]
                X_train,X_test,y_train,y_test = train_test_split(X,y, random_state=2)
                model = tree.DecisionTreeClassifier(criterion='gini')
                model = model.fit(X_train,y_train)
                with open(dir_name + '/pickle_files/hemogram_women.pickle','wb') as data:
                    pickle.dump(model,data)
                if model.predict(vals) == 1:
                    result['predictions'] = "healthy"
                else:
                    result['predictions'] = "unhealthy"
                return json.dumps(result)
            else:
                print "Pickle file " + "hemogram_women.csv" + ".pickle already present"
                with open(dir_name + '/pickle_files/hemogram_women.pickle','rb') as data:
                    model = pickle.load(data)
                    if model.predict(vals) == 1:
                        result['predictions'] = "healthy"
                    else:
                        result['predictions'] = "unhealthy"
                    return json.dumps(result)
    
    //method to predict if biochemecial parameter test is healthy or not
    @http.route('/health/bio_chemical_parameters', type='json', auth="public",csrf=False)
    def bio_chemical_parameters(self,bio_chemical_data):
        if bio_chemical_data['sex'] == "male":
            biochemical_parameters_men_csv = pd.read_csv(dir_name + "/dataset/biochemical_parameters_men.csv")
            columns = biochemical_parameters_men_csv.iloc[:,0:len(biochemical_parameters_men_csv.columns)]
            for column in biochemical_parameters_men_csv.columns:
                try:
                    feature[column] = bio_chemical_data[column]
                except:
                    pass
            vals = [feature['fbs/ppbs'],feature['blood_urea'],feature['creatinine'],feature['uric_acid']]
            if not os.path.exists(dir_name + "/pickle_files/biochemical_parameters_men.pickle"):
                read_csv = pd.read_csv(dir_name + "/dataset/biochemical_parameters_men.csv")
                X = biochemical_parameters_men_csv.iloc[:,0:-1] 
                y = biochemical_parameters_men_csv.iloc[:,-1]
                X_train,X_test,y_train,y_test = train_test_split(X,y, random_state=2)
                model = tree.DecisionTreeClassifier(criterion='gini')
                model = model.fit(X_train,y_train)
                with open(dir_name + '/pickle_files/biochemical_parameters_men.pickle','wb+') as data:
                    pickle.dump(model,data)
                if model.predict(vals) == 1:
                    result['predictions'] = "healthy"
                else:
                    result['predictions'] = "unhealthy"
                return json.dumps(result)
            else:
                print "Pickle file " + "biochemical_parameters_men.csv" + ".pickle already present"
                with open(dir_name + '/pickle_files/biochemical_parameters_men.pickle','rb+') as data:
                    model = pickle.load(data)
                    if model.predict(vals) == 1:
                        result['predictions'] = "healthy"
                    else:
                        result['predictions'] = "unhealthy"
                    return json.dumps(result)
        else:
            biochemical_parameters_women_csv = pd.read_csv(dir_name + "/dataset/biochemical_parameters_women.csv" )
            columns = biochemical_parameters_women_csv.iloc[:,0:len(biochemical_parameters_women_csv.columns)]
            for column in biochemical_parameters_women_csv.columns:
                try:
                    feature[column] = bio_chemical_data[column]
                except:
                    pass
            vals = [feature['fbs/ppbs'],feature['blood_urea'],feature['creatinine'],feature['uric_acid']]
            if not os.path.exists(dir_name + "/pickle_files/biochemical_parameters_women.pickle"):
                read_csv = pd.read_csv(dir_name + "/dataset/biochemical_parameters_women.csv")
                X = biochemical_parameters_women_csv.iloc[:,0:-1] 
                y = biochemical_parameters_women_csv.iloc[:,-1]
                X_train,X_test,y_train,y_test = train_test_split(X,y, random_state=2)
                model = tree.DecisionTreeClassifier(criterion='gini')
                model = model.fit(X_train,y_train)
                with open(dir_name + '/pickle_files/biochemical_parameters_women.pickle','wb') as data:
                    pickle.dump(model,data)
                if model.predict(vals) == 1:
                    result['predictions'] = "healthy"
                else:
                    result['predictions'] = "unhealthy"
                return json.dumps(result)
            else:
                print "Pickle file " + "biochemical_parameters_women.csv" + ".pickle already present"
                with open(dir_name + '/pickle_files/biochemical_parameters_women.pickle','rb') as data:
                    model = pickle.load(data)
                    if model.predict(vals) == 1:
                        result['predictions'] = "healthy"
                    else:
                        result['predictions'] = "unhealthy"
                    return json.dumps(result)
    
    //method to predict if liver function test is healthy or not
    @http.route('/health/liver_function_test', type='json', auth="public",csrf=False)
    def liver_function_test(self,liver_function_data):
        liver_function_csv = pd.read_csv(dir_name + "/dataset/liver_function_test.csv")
        columns = liver_function_csv.iloc[:,0:len(liver_function_csv.columns)]
        for column in liver_function_csv.columns:
            try:
                feature[column] = liver_function_data[column]
            except:
                pass
        vals = [feature['total_protein'],feature['albumin'],feature['globulin'],feature['a/g_ratio'],feature['sgot'],feature['sgpt'],feature['alkaline_phosphate'],feature['bilirubin_total'],feature['bilirubin_direct'],feature['gamma_gt']]
        if not os.path.exists(dir_name + "/pickle_files/liver_function_test.pickle"):
            read_csv = pd.read_csv(dir_name + "/dataset/liver_function_test.csv")
            X = liver_function_csv.iloc[:,0:-1] 
            y = liver_function_csv.iloc[:,-1]
            X_train,X_test,y_train,y_test = train_test_split(X,y, random_state=2)
            model = tree.DecisionTreeClassifier(criterion='gini')
            model = model.fit(X_train,y_train)
            with open(dir_name + '/pickle_files/liver_function_test.pickle','wb+') as data:
                pickle.dump(model,data)
            if model.predict(vals) == 1:
                    result['predictions'] = "healthy"
            else:
                result['predictions'] = "unhealthy"
        else:
            print "Pickle file " + "lipid_profile.csv" + ".pickle already present"
            with open(dir_name + '/pickle_files/liver_function_test.pickle','rb+') as data:
                model = pickle.load(data)
                if model.predict(vals) == 1:
                    result['predictions'] = "healthy"
                else:
                    result['predictions'] = "unhealthy"
                return json.dumps(result)
    
    //method to predict if lipid profile test is healthy or not
    @http.route('/health/lipid_test', type='json', auth="public",csrf=False)
    def lipid_profile(self,lipid_profile_data):
        lipid_profile_csv = pd.read_csv(dir_name + "/dataset/lipid_profile.csv")
        columns = lipid_profile_csv.iloc[:,0:len(lipid_profile_csv.columns)]
        for column in lipid_profile_csv.columns:
            try:
                feature[column] = lipid_profile_data[column]
            except:
                pass
        vals = [feature['total_cholesterol'],feature['hdl_cholesterol'],feature['ldl_cholesterol'],feature['triglycerides'],feature['total_cholesterol/hdl_ratio']]
        if not os.path.exists(dir_name + "/pickle_files/lipid_profile.pickle"):
            read_csv = pd.read_csv(dir_name + "/dataset/lipid_profile.csv")
            X = lipid_profile_csv.iloc[:,0:-1] 
            y = lipid_profile_csv.iloc[:,-1]
            X_train,X_test,y_train,y_test = train_test_split(X,y, random_state=2)
            model = tree.DecisionTreeClassifier(criterion='gini')
            model = model.fit(X_train,y_train)
            with open(dir_name + '/pickle_files/lipid_profile.pickle','wb+') as data:
                pickle.dump(model,data)
            if model.predict(vals) == 1:
                result['predictions'] = "healthy"
            else:
                result['predictions'] = "unhealthy"
        else:
            print "Pickle file " + "lipid_profile.csv" + ".pickle already present"
            with open(dir_name + '/pickle_files/lipid_profile.pickle','rb+') as data:
                model = pickle.load(data)
                if model.predict(vals) == 1:
                    result['predictions'] = "healthy"
                else:
                    result['predictions'] = "unhealthy"
                return json.dumps(result)
    
    
    @http.route('/health/complete_test', type='json', auth="public",csrf=True)
    def complete_test(self,data):
        complete = {}
        print data[0],"!!!!!!!!!!!!!!!!!!!!!!!!!!!"
        complete['hemo_result'] = json.loads(self.hemogram(data[0]))
        complete['bio_chemical_result'] = json.loads(self.bio_chemical_parameters(data[1]))
        complete['lipid_result'] = json.loads(self.lipid_profile(data[2]))
        complete['liver_func_result'] = json.loads(self.liver_function_test(data[3]))
        return json.dumps(complete)
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
