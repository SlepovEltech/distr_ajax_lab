#!flask/bin/python
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin

import re
import sys
import csv

#Wikidata sections
from SPARQLWrapper import SPARQLWrapper, JSON
from wikidata.client import Client

from entity_dictionary import entity_dict 
from predicate_dictionary import predicate_dict
 
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

endpoint_url = "https://query.wikidata.org/sparql"

def find_entity_by_substring(substr:str):
    result = []
    for key in entity_dict.keys():
        if(key.find(substr) != -1):
            result.append(key)
    return result

def find_predicate_by_substring(substr:str):
    result = []
    for key in predicate_dict.keys():
        if(key.find(substr) != -1):
            result.append(key)
    return result
    
@app.route('/autocomplete/entity')
def entity_autocomplete():
    substr = str(request.args.get('term'))
    return jsonify(find_entity_by_substring(substr))

@app.route('/autocomplete/predicate')
def predicate_autocomplete():
    substr = str(request.args.get('term'))
    substr = str(substr)
    return jsonify(find_predicate_by_substring(substr))

@app.route('/distributed', methods=['POST'])
def query_from_distributed_lab():

    subject = request.form.get('subjectInput')
    predicate = request.form.get('predicateInput')
    obj = request.form.get('objectInput')

    print(subject, predicate, obj)
    if predicate in predicate_dict:
        predicate = "wdt:"+predicate_dict[predicate]

    if subject in entity_dict:
        subject = "wd:"+entity_dict[subject] 
    else:
        select_key = subject
        subject = "?"+subject
        select_var = subject

    if obj in entity_dict:
        obj = "wd:"+entity_dict[obj] 
    else:
        select_key = obj
        obj = "?"+obj
        select_var = obj
    
    sparql_query =  """SELECT """ + select_var + """ WHERE{ """+ subject + " " + predicate + " " + obj+ """}"""
    print(sparql_query)
    response = extract_results_from_response(sparql_query)
 
    result = "<h1>Result: </h1>"
    for resp in response:
        result += "<br><h1><a href="+resp[select_key]['value'] +">" + resp[select_key]['value'] + "</a>"
  
    return result

if __name__ == '__main__':
    app.run(debug=True)






