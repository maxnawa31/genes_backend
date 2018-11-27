from flask import Flask, jsonify
from flask_cors import CORS, cross_origin
from master_list_genes import master_list_genes
import csv
import pygtrie

app = Flask(__name__)
CORS(app)


gene_trie = pygtrie.CharTrie()
all_matching_genes = []

@app.before_first_request
def add_words_to_trie():
    for gene in master_list_genes:
        gene_trie[gene] = True

@app.route('/search/')
def empty_search():
    return jsonify([])

@app.route('/search/<char>')
def gene_search(char):
    if gene_trie.has_key(char.upper()):
        return jsonify(gene_trie.keys(char.upper()))
    if not gene_trie.has_subtrie(char.upper()):
        return jsonify([])
    return jsonify(gene_trie.keys(prefix=char.upper()))

@app.route('/genes/<gene>')
def get_gene(gene):
    with open('./variants.tsv') as tsvfile:
        reader = csv.DictReader(tsvfile, dialect='excel-tab')
        for row in reader:
            if row['Gene'] == gene.upper():
                all_matching_genes.append(row)
        return jsonify(all_matching_genes)


