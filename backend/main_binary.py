from flask import Flask, jsonify, render_template, request
from elasticsearch import Elasticsearch
import skfuzzy as fuzz
import numpy as np
from collections import Counter
import json
from collections import defaultdict
from helper import Backend_Helper


es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
app = Flask(__name__) #Create the flask instance, __name__ is the name of the current Python module


# priceDict = {}
# hdDict = {}
# productTitleDict = {}
# allDocs ={}

@app.route('/api/search', methods=['POST'])
def searchBinary():
    data = request.get_json()
    clean_data = Backend_Helper.clean_frontend_json(data)
    query = createBinarySearchQuery(clean_data)
    res = es.search(index="amazon", body=query)
    #print(res)
    return jsonify(Backend_Helper.refineResult(res))



def createBinarySearchQuery(fieldNameToValueDict) :
    body = defaultdict(lambda: defaultdict(lambda : defaultdict(lambda: defaultdict(dict))))

    terms = []
    ranges = []
    sameFieldMultpleValues = []

    for fieldName in fieldNameToValueDict :

        if not fieldNameToValueDict[fieldName]:
            continue
        #normal match
        #Ranged terms, example : ram : { minRam : 2,maxRam : 4}
        #If that's the case, then search for minRam and maxRam in fieldNameToValueDict, get them and add range to the query
        if type(fieldNameToValueDict[fieldName]) is dict and ("minValue" in fieldNameToValueDict[fieldName] or "maxValue" in fieldNameToValueDict[fieldName]) :
            #Extract name of field, and set the name of min and max values to minField and maxField, example : minRam and maxRam.
            #minValueName = "min"+fieldName[0].upper()+fieldName[1:]
            #maxValueName = "max"+fieldName[0].upper()+fieldName[1:]
            if not fieldNameToValueDict[fieldName]["minValue"] or not fieldNameToValueDict[fieldName]["maxValue"]:
                continue

            #Extract the values of minField and maxField from the JSON coming from the front end
            if "minValue" in fieldNameToValueDict[fieldName] and  "maxValue" in fieldNameToValueDict[fieldName] :
                minValue = fieldNameToValueDict[fieldName]["minValue"]
                maxValue = fieldNameToValueDict[fieldName]["maxValue"]
                ranges.append({"range" : {fieldName : {"lte" : maxValue,"gte" : minValue }}})

            elif "minValue" in fieldNameToValueDict[fieldName] :
                minValue = fieldNameToValueDict[fieldName]["minValue"]
                ranges.append({"range" : {fieldName : {"gte" : minValue }}})

            elif "maxValue" in fieldNameToValueDict[fieldName] :
                maxValue = fieldNameToValueDict[fieldName]["maxValue"]
                ranges.append({"range" : {fieldName : {"lte" : maxValue}}})

        #--------------------------------------------------------------------------------------------------------------------------------#
        #In case of multiple values for the same field, example : ram : [2,4,6], ram is either 2, 4 or 6.
        elif "value" in fieldNameToValueDict[fieldName] :
            if type(fieldNameToValueDict[fieldName]["value"]) is list :
                if type(fieldNameToValueDict[fieldName][0]) is str :
                    fieldNameToValueDict[fieldName] = [x.lower() for x in fieldNameToValueDict[fieldName]]
                sameFieldMultpleValues.append({"terms" : {fieldName :fieldNameToValueDict[fieldName] }})
        #--------------------------------------------------------------------------------------------------------------------------------#
        #A normal numerical match, example : ram : 8, ram is 8
            elif type(fieldNameToValueDict[fieldName]["value"]) is int or type(fieldNameToValueDict[fieldName]["value"]) is float :
                terms.append({"term" : {fieldName : fieldNameToValueDict[fieldName]["value"]}})
            #--------------------------------------------------------------------------------------------------------------------------------#
            #A normal string match as brandName or hardDriveType
            else :
                #Example : match "{ ram : 8}"
                terms.append({"term" : {fieldName : fieldNameToValueDict[fieldName]["value"].lower()}})
            #--------------------------------------------------------------------------------------------------------------------------------#

    body["query"]["bool"]["must"] = []
    if len(terms) > 0 :
        body["query"]["bool"]["must"].append(terms)
    if len(ranges) > 0 :
        body["query"]["bool"]["must"].append(ranges)
    if len(sameFieldMultpleValues) > 0 :
        body["query"]["bool"]["must"].append(sameFieldMultpleValues)

    body.update({"size":100})

    print(json.dumps(body))


    return body


@app.route('/api/sample', methods=['GET'])
def getSample():
  allDocs = es.search(index="amazon", body={
    "query": {
      "match": {
        "avgRating": 5
      }
    },
    "size": 10
  })

  outputProducts = Backend_Helper.refineResult(allDocs)
  return jsonify(outputProducts)  # original from alfred

if __name__ == "__main__":
    app.run(debug=True)
