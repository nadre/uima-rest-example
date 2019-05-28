#!/usr/bin/env python
# coding: utf-8
#!flask/bin/python
from flask import Flask, request, jsonify
from cassis import *

app = Flask(__name__)

with open('typesystem.xml', 'rb') as f:
    typesystem = load_typesystem(f)


@app.route('/rest/textanalysis/analyseText/', methods=['POST'])
def analyse_text():
    xmi = str(request.data, "UTF-8")

    cas = load_cas_from_xmi(xmi, typesystem=typesystem)

    concept_annotation = typesystem.get_type('de.averbis.extraction.types.Concept')

    for sentence in cas.select('de.averbis.extraction.types.Sentence'):

        cas.add_annotation(concept_annotation(begin=sentence.begin, end=sentence.end, dictCanon='Pythonator'))

    xmi = cas.to_xmi()

    return xmi

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)