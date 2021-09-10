##################################################################################################################################
# CS 5800 Project 2
# Joseph K Blankenship
# DUE: June 30, 2021
# This module contains several classes for use in project 2:
##################################################################################################################################

#from collections import Counter

##################################################################################################################################
# Class: invIndex
#   This is an inverted index that holds the collection
#   terms, documents associate with the terms, and the
#   metrics associate with the term
##################################################################################################################################

from nltk.corpus.reader.framenet import PrettyList


class invIndex:
        def __init__(self, term, docfq = 0, idf = 0, docList = []): #moved termfq from this class, watch for major changes!
            self.term = term
            self.docfq = docfq
            self.idf = idf
            self.docList = [] 
        
        def printTerm(self):
            print(self.term)
            
        
        def getTerm(self):
            return self.term

        def addDoc(self, docID):
            self.docList.append(docID)


##################################################################################################################################
# Class: document
#   This is a document which holds the collection of tokens 
#   associate with the docID. The documentID is simply an 
#   index number.
##################################################################################################################################

class document():
    from collections import Counter
    def __init__(self, docID, length = 0, tokens = {}):
        self.docID = docID
        self.length = length
        self.tokens = tokens

##################################################################################################################################
# Class: documentFull
#   This is a document which holds the full text documents 
#   associated with the docID. The documentID is simply an 
#   index number.
##################################################################################################################################
class documentFull():
    def __init__(self, docID, fulltext = '', tokens = []):
        self.docID = docID
        self.tokens = tokens
        self.fulltext = fulltext

##################################################################################################################################
# Class: docScore
#   This holds the document score for the respective document
##################################################################################################################################

class docScore:
    def __init__(self, docID, score):
        self.docID = docID
        self.score = score

    def __lt__(self, other):
        return self.score < other.score

##################################################################################################################################
# Class: relevance
#   This holds the document score for the respective document
##################################################################################################################################

class relevance:
    def __init__(self, query = 0, relDocs = []):
        self.query = query
        self.relDocs = relDocs

##################################################################################################################################
# Class: results
#   This holds resulting compared to prejudged docs
##################################################################################################################################

class results:
    def __init__(self, query = 0, retrieved = []):
        self.query = query
        self.pre_5 = 0
        self.pre_10 = 0
        self.pre_15 = 0
        self.re_15 = 0
        self.map = 0
        self.retrieved = retrieved
        self.preList = []
        self.reList = []

    def calcP_top5(self,judgedDocs = []):
        found = 0
        track = 0
        for docScore in self.retrieved:
            track += 1
            if (docScore.docID + 1) in judgedDocs.relDocs:
                found += 1
            if track == 5:
                break
            
        self.pre_5 = (found/5)
        
    
    def calcP_top10(self,judgedDocs = []):
        found = 0
        track = 0
        for docScore in self.retrieved:
            track += 1
            if (docScore.docID + 1) in judgedDocs.relDocs:
                found += 1
            if track == 10:
                break
            
        self.pre_10 = (found/10)

    def calcP_top15(self,judgedDocs = []):
        found = 0
        track = 0
        for docScore in self.retrieved:
            track += 1
            if (docScore.docID + 1) in judgedDocs.relDocs:
                found += 1
            if track == 15:
                break
            
        self.pre_15 = (found/15)
        

    def calcR_top15(self, judgedDocs = []):
        found = 0
        for docScore in self.retrieved:
            if (docScore.docID + 1) in judgedDocs.relDocs:
                found += 1
        self.re_15 = (found / len(judgedDocs.relDocs))

    def calc_MAP(self, judgedDocs = []):
        found = 0
        position = 1
        m = len(judgedDocs.relDocs)
        p_val = 0

        for docScore in self.retrieved:
            if (docScore.docID + 1) in judgedDocs.relDocs:
                found += 1
                p_val = p_val + (found/position)
            position += 1
        
        if found == m:
            self.map = (1/m) * p_val
        else:
            self.map = -1

    def calc_PercisionRecallCurveVals(self,judgedDocs = []):
        found = 0
        track = 0
        k = 0
        for docScore in self.retrieved:
            track += 1
            if (docScore.docID + 1) in judgedDocs.relDocs:
                found += 1
            if track == 15:
                break
            k += 1
            self.preList.append(found/k)
            self.reList.append((found / len(judgedDocs.relDocs)))

        
