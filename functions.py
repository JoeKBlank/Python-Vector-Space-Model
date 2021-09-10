#######################################################################################
# CS 5800 Project 2
# Joseph K Blankenship
# DUE: June 30, 2021
# These are the functions used in Project 2
#
#######################################################################################

import nltk as nk
import re as re
from nltk.stem import LancasterStemmer
from nltk.corpus import stopwords
import string

from nltk.tokenize import word_tokenize
from classes import *
from collections import Counter
import math
import heapq

##################################################################################################################################
#function: createDatabaseReg
#Parameters: file = file string, docTextList = empty list, inIndex = empty list, listofDocs = empty list, myDict = empty dictionary
#this creates a regular database without stemming
##################################################################################################################################

def createDatabaseReg(file, docTextList, invertedIndex, listofDocs, Dict ):
    parseDocs1(file,listofDocs)
    createRetrIndex(file,docTextList)
    createIndex1(file, invertedIndex)
    addPostingsDF(invertedIndex, listofDocs) 
    for invIndex in invertedIndex:
        Dict[invIndex.term] = invIndex

    addDF(Dict, invertedIndex)
    calcIDF(Dict, invertedIndex)
    calcDocLength(Dict, invertedIndex, listofDocs)

##################################################################################################################################
#function: createDatabaseStem
#Parameters: file = file string, docTextList = empty list, inIndex = empty list, listofDocs = empty list, myDict = empty dictionary
#this creates a regular database with stemming!
##################################################################################################################################

def createDatabaseStem(file, docTextList, inIndex, listofDocs, myDict ):
    parseDocsStem(file,listofDocs)
    createRetrIndex(file,docTextList)
    createIndexStem(file, inIndex)
    addPostingsDF(inIndex, listofDocs) 
    for invIndex in inIndex:
        myDict[invIndex.term] = invIndex

    addDF(myDict, inIndex)
    calcIDF(myDict, inIndex)
    calcDocLength(myDict, inIndex, listofDocs)

##################################################################################################################################
#function: createDatabaseStop
#Parameters: file = file string, docTextList = empty list, inIndex = empty list, listofDocs = empty list, myDict = empty dictionary
#this creates a regular database with stopping!
##################################################################################################################################

def createDatabaseStop(file, docTextList, inIndex, listofDocs, myDict ):
    parseDocsStop(file,listofDocs)
    createRetrIndex(file,docTextList)
    createIndexStop(file, inIndex) 
    addPostingsDF(inIndex, listofDocs) 
    for invIndex in inIndex:
        myDict[invIndex.term] = invIndex

    addDF(myDict, inIndex)
    calcIDF(myDict, inIndex)
    calcDocLength(myDict, inIndex, listofDocs)

##################################################################################################################################
#function: createDatabaseStop_Stem
#Parameters: file = file string, docTextList = empty list, inIndex = empty list, listofDocs = empty list, myDict = empty dictionary
#this creates a regular database with stemming and stopping!
##################################################################################################################################

def createDatabaseStop_Stem(file, docTextList, inIndex, listofDocs, myDict ):
    parseDocsStem_Stop(file,listofDocs)
    createRetrIndex(file,docTextList)
    createIndexStem_Stop(file, inIndex) 
    addPostingsDF(inIndex, listofDocs) 
    for invIndex in inIndex:
        myDict[invIndex.term] = invIndex

    addDF(myDict, inIndex)
    calcIDF(myDict, inIndex)
    calcDocLength(myDict, inIndex, listofDocs)

##################################################################################################################################
# Function: parseDocs1 
# Parameters: A file as string and a list
# This function takes an input file of documents, separates them, and puts their tokens into a document class object
# This function returns a list of document class objects. Uses stopword list for punctuation
##################################################################################################################################

def parseDocs1(file, list = []):
    
    myList = []
    
    punctStops = set(string.punctuation)
    indicator = "*****************"
    path = file
    count = 0
    docCount = 0
    newstring = ''
    with open(path,'r') as myinput:
        for line in myinput:
            if count == 0:
                count += 1
                continue
            if indicator in line:
                count = 0
                myList = nk.word_tokenize(newstring)
                size = 0 


                myList = [word for word in myList if not word in punctStops] #Added punct Stops
                
                myList = Counter(myList)
                print("REG REG REG REG REG REG REG")
                print(myList) #TESTING
                list.append(document(docCount,size,myList.copy()))
                
                docCount += 1
                myList.clear()
                
                newstring = ''
                continue
            newstring = line + newstring




##################################################################################################################################
# Function: parseDocsStop 
# Parameters: A file as string and a list
# This function takes an input file of documents, separates them, and puts their tokens into a document class object
# This function returns a list of document class objects. Uses stopword list.
##################################################################################################################################

def parseDocsStop(file, list = []):
    myList = []
    stop = stopwords.words('english')
    customStop = []
    for word in stop:
        customStop.append(word.upper())
    punctStops = set(string.punctuation)
    for word in punctStops:
        customStop.append(word)
    indicator = "*****************"
    path = file
    count = 0
    docCount = 0
    newstring = ''
    with open(path,'r') as myinput:
        for line in myinput:
            if count == 0:
                count += 1
                continue
            if indicator in line:
                count = 0
                myList = nk.word_tokenize(newstring)
                myList = [word for word in myList if not word in customStop]
            
                size = 0
                myList = Counter(myList)
                print("STOP STOP STOP STOP STOP STOP")
                print(myList) #TESTING
                list.append(document(docCount,size,myList.copy()))
                docCount += 1
                
                myList.clear()
                
                newstring = ''
                continue
            newstring = line + newstring



##################################################################################################################################
# Function: parseDocsStem 
# Parameters: A file as string and a list
# This function takes an input file of documents, separates them, and puts their tokens into a document class object
# This function returns a list of document class objects. Uses stemming
##################################################################################################################################

def parseDocsStem(file, list = []):
    lancastStem = LancasterStemmer()
    myList = []
    
    indicator = "*****************"
    path = file
    count = 0
    docCount = 0
    newstring = ''
    with open(path,'r') as myinput:
        for line in myinput:
            if count == 0:
                count += 1
                continue
            if indicator in line:
                count = 0
                myList = nk.word_tokenize(newstring)
                
                newList = []
                for word in myList:
                    a = lancastStem.stem(word)
                    newList.append(a)
                size = 0
                print("STEM STEM STEM STEM STEM STEM")
                print(newList)
                newList = Counter(newList)
                list.append(document(docCount,size,newList.copy()))
                docCount += 1
                myList.clear()
                newList.clear()
                newstring = ''
                continue
            newstring = line + newstring

##################################################################################################################################
# Function: parseDocsStem_Stop
# Parameters: A file as string and a list
# This function takes an input file of documents, separates them, and puts their tokens into a document class object
# This function returns a list of document class objects. Uses stemming and stopping
##################################################################################################################################

def parseDocsStem_Stop(file, list = []):
    lancastStem = LancasterStemmer()
    myList = []
    stop = stopwords.words('english')
    customStop = []
    for word in stop:
        customStop.append(word.upper())
       
    punctStops = set(string.punctuation)
    for word in punctStops:
        customStop.append(word)
    indicator = "*****************"
    path = file
    count = 0
    docCount = 0
    newstring = ''
    with open(path,'r') as myinput:
        for line in myinput:
            if count == 0:
                count += 1
                continue
            if indicator in line:
                count = 0
                myList = nk.word_tokenize(newstring)
                myList = [word for word in myList if not word in customStop]
                newList = []
                for word in myList:
                    a = lancastStem.stem(word)
                    newList.append(a)
                size = 0
                
                newList = Counter(newList)
                print("STEM STOP STEM STOP STEM STOP")
                print(newList)
                list.append(document(docCount,size,newList.copy()))
                docCount += 1
                myList.clear()
                newList.clear()
                newstring = ''
                continue
            newstring = line + newstring



##################################################################################################################################
# Function: parseLisa1 
# Parameters: A file as string and a list
# This function takes an input file of documents, separates them, and puts their tokens into a document class object
# This function read lisa query documents because the INDICATOR is different. Regular.  LISA_QUE FILE WAS CHANGED
##################################################################################################################################

def parseLisa1(file, list = []):
    myList = []
   
    punctStops = set(string.punctuation)
   
    indicator = "#"
    path = file
    count = 0
    docCount = 0
    newstring = ''
    with open(path,'r') as myinput:
        for line in myinput:
            if count == 0:
                count += 1
                continue
            if indicator in line:
                count = 0
                myList = nk.word_tokenize(newstring)
                myList = [word for word in myList if not word in punctStops]
                size = 0
                print("REG REG REG REG")
                print(myList) #TESTING
                list.append(documentFull(docCount,size,myList.copy()))
                docCount += 1
                
                myList.clear()
                newstring = ''
                continue
            
            
            newstring = line + " " + newstring

##################################################################################################################################
# Function: parseLisa_stop
# Parameters: A file as string and a list
# This function takes an input file of documents, separates them, and puts their tokens into a document class object
# This function read lisa query documents because the INDICATOR is different. Uses stopping LISA_QUE FILE WAS CHANGED
##################################################################################################################################

def parseLisa_stop(file, list = []):
    myList = []
    stop = stopwords.words('english')
    customStop = []
    for word in stop:
        customStop.append(word.upper())
        
    punctStops = set(string.punctuation)
    for word in punctStops:
        customStop.append(word)
    indicator = "#"
    path = file
    count = 0
    docCount = 0
    newstring = ''
    with open(path,'r') as myinput:
        for line in myinput:
            if count == 0:
                count += 1
                continue
            if indicator in line:
                count = 0
                myList = nk.word_tokenize(newstring)
                myList = [word for word in myList if not word in customStop]
                size = 0
                myList = myList      #removed set
                myNewList = []
                for word in myList:
                    myNewList.append(word)
                print("STOP STOP STOP STOP")
                print(myNewList) #TESTING
                list.append(documentFull(docCount,size,myNewList.copy()))
                docCount += 1
                
                myList.clear()
                newstring = ''
                continue
            
            
            newstring = line + " " + newstring


##################################################################################################################################
# Function: parseLisa_stem 
# Parameters: A file as string and a list
# This function takes an input file of documents, separates them, and puts their tokens into a document class object
# This function read lisa query documents because the INDICATOR is different. Uses Stemming. LISA_QUE FILE WAS CHANGED
##################################################################################################################################

def parseLisa_stem(file, list = []):
    myList = []
    lancastStem = LancasterStemmer()
    
    indicator = "#"
    path = file
    count = 0
    docCount = 0
    newstring = ''
    with open(path,'r') as myinput:
        for line in myinput:
            if count == 0:
                count += 1
                continue
            if indicator in line:
                count = 0
                myList = nk.word_tokenize(newstring)
                
                newList = []
                for word in myList:
                    a = lancastStem.stem(word)
                    newList.append(a)
                size = 0
                myList = newList        #removed set
                myNewList = []
                for word in myList:
                    myNewList.append(word)
                print("STEM STEM STEM STEM")
                print(myNewList)        #TESTING
                list.append(documentFull(docCount,size,myNewList.copy()))
                docCount += 1
                myList.clear()
                newList.clear()
                newstring = ''
                continue
            
            
            newstring = line + " " + newstring

##################################################################################################################################
# Function: parseLisa_stem_stop
# Parameters: A file as string and a list
# This function takes an input file of documents, separates them, and puts their tokens into a document class object
# This function read lisa query documents because the INDICATOR is different. USES stemming and stopping. LISA FILE WAS CHANGED
##################################################################################################################################

def parseLisa_stem_stop(file, list = []):
    myList = []
    lancastStem = LancasterStemmer()
    stop = stopwords.words('english')
    customStop = []
    for word in stop:
        customStop.append(word.upper())
        
    punctStops = set(string.punctuation)
    for word in punctStops:
        customStop.append(word)
    indicator = "#"
    path = file
    count = 0
    docCount = 0
    newstring = ''
    with open(path,'r') as myinput:
        for line in myinput:
            if count == 0:
                count += 1
                continue
            if indicator in line:
                count = 0
                myList = nk.word_tokenize(newstring)
                myList = [word for word in myList if not word in customStop]
                newList = []
                for word in myList:
                    a = lancastStem.stem(word)
                    newList.append(a)
                newList = newList  #removed set
                newList2 = []
                for word in newList:
                    newList2.append(word)
                print("STEM STOP STEM STOP STEM STOP")
                print(newList2)
                size = 0
                list.append(documentFull(docCount,size,newList2.copy()))
                docCount += 1
                myList.clear()
                newList.clear()
                newstring = ''
                continue
            
            
            newstring = line + " " + newstring

##################################################################################################################################
# Function: createRetrIndex
# Parameters: file = user imput file, list = an empty list
# This creates a list of documentFull objects which hold the full text of the documents
# to be retrieved by user after a query
##################################################################################################################################
def createRetrIndex(file, list = []):
    
    path = file
    docString = ''
    indicator = "*****************"
    docCount = 0
    with open(path,'r') as myinput:
        for line in myinput:
            if indicator in line:
                list.append(documentFull(docCount,docString))
                docCount += 1
                docString = ''
                continue
            else:
                docString = docString + '\n' + line

    #return list



##################################################################################################################################
# Function: createIndex1
# Parameters: This function takes a file string and a list
# This function creates the entire list of tokens for the collection
# This functions creates a list of invIndex objects for each term in the document collection
##################################################################################################################################
def createIndex1(file, list = []):

    mydoc = open(file).read()
    sentences = nk.word_tokenize(mydoc)
    token_set =  sorted(set(sentences))
    for token in token_set:
        list.append(invIndex(token))
    
    sentences.clear()
    token_set.clear()
    

##################################################################################################################################
# Function: createIndexStop
# Parameters: This function takes a file string and a list
# This function creates the entire list of tokens for the collection
# This functions creates a list of invIndex objects for each term in the document collection. USES STOP
##################################################################################################################################
def createIndexStop(file, list = []):

    mydoc = open(file).read()
    stop = stopwords.words('english')
    customStop = []
    for word in stop:
        customStop.append(word.upper())
        
    punctStops = set(string.punctuation)
    for word in punctStops:
        customStop.append(word)
    sentences = nk.word_tokenize(mydoc)
    sentences = [word for word in sentences if not word in customStop]
    #print(sentences)
    token_set =  sorted(set(sentences))
    for token in token_set:
        list.append(invIndex(token))
    

##################################################################################################################################
# Function: createIndexStem
# Parameters: This function takes a file string and a list
# This function creates the entire list of tokens for the collection
# This functions creates a list of invIndex objects for each term in the document collection. USES STEM
##################################################################################################################################
def createIndexStem(file, list = []):
    lancastStem = LancasterStemmer()
    mydoc = open(file).read()
    mydoc = nk.word_tokenize(mydoc)
    newList = []
    for word in mydoc:
        a = lancastStem.stem(word)
        newList.append(a)
    token_set =  sorted(set(newList))
    for token in token_set:
        list.append(invIndex(token))
    
    newList.clear()
    mydoc.clear()

##################################################################################################################################
# Function: createIndexStem_Stop
# Parameters: This function takes a file string and a list
# This function creates the entire list of tokens for the collection
# This functions returns a list of invIndex objects for each term in the document collection
##################################################################################################################################
def createIndexStem_Stop(file, list = []):
    lancastStem = LancasterStemmer()
    stop = stopwords.words('english')
    customStop = []
    for word in stop:
        customStop.append(word.upper())
        
    punctStops = set(string.punctuation)
    for word in punctStops:
        customStop.append(word)
    mydoc = open(file).read()
    mydoc = nk.word_tokenize(mydoc)
    mydoc = [word for word in mydoc if not word in customStop]
    newList = []
    for word in mydoc:
        a = lancastStem.stem(word)
        newList.append(a)
    token_set =  sorted(set(newList))
    for token in token_set:
        list.append(invIndex(token))
    
    newList.clear()
    mydoc.clear()

##################################################################################################################################
# Function: addPostingsDF
# Parameters: myIndex is list of invIndex type objects and docList is a list of document type objects
# Adds the respective postings of each term in each document. Then it adds document frequency to the invIndex terms
##################################################################################################################################
def addPostingsDF(myIndex, docList):
    
    for invIndex in myIndex:
        term = invIndex.getTerm()
        for document in docList:
            if term in document.tokens:
                invIndex.docList.append(document) 
    
    for invIndex in myIndex:
        invIndex.docfq = len(invIndex.docList) 


##################################################################################################################################
# Fundtion: addDF
# Parameters: Dictionary and invertedIndex
# This function nests a dictionary inside the dictionary which holds the invertedIndex
# with an object for each term and the document frequency
##################################################################################################################################
def addDF(userDict, index):
    
    counter = 0
    for invIndex in index:
        term = invIndex.term
        indexVar = userDict.get(term)
        for document in invIndex.docList:
            counter += 1
        userDict[term] = {'obj' : indexVar, 'df' : counter}
        counter = 0

##################################################################################################################################
# Function: calcIDF
# Parameters: userDict is a user dictionary containing objects and document frequencies of the collection terms
# index is an inverted index of objects, which contain the keys for every dictionary term
# This calculates the IDF for each term and assigns it to the appropriate space in the dictionary
##################################################################################################################################
def calcIDF(userDict, index):

    for invIndex in index:
        term = invIndex.term
        indexVar = userDict.get(term)
        df = userDict[term]['df']
        if df > 0:
            indexVar['obj'].idf = math.log((6004/df),10) 
            userDict[term] = indexVar
            


##################################################################################################################################
#Function: getPostings
#Parameters: this gets object of a terms that contains a list of documents containing said term
##################################################################################################################################
def getPostings(t,Dict):
    if t in Dict:
        return Dict[t]['obj']
    else:
        return 0

##################################################################################################################################
#Function: returnTop15
#Parameters: This function takes a heapified array
#Returns the top X scores of a heapified array of score class objects
##################################################################################################################################
def returnTop15(scores):
    if not scores:
        "no scores"
        return
    else:
        relevantDocList = []
        for x in range(10):     #changed for testing small file
            relevantDoc = heapq.heappop(scores)
            
            relevantDocList.append(relevantDoc)
            

        return relevantDocList


##################################################################################################################################
# Function: cosineScore
# Parameters: q = user query, docList = list of documents with document lengths, 
# Dict = dictionary of objects containing term frequency and idf
# This calculates the cosineScore for the documents in relation to a given query.
# This treates the wf(t,d) as the tf-idf. This is technically the fastcosine from the book.
##################################################################################################################################

def cosineScore(q,docList,Dict) :
    
    scores = []
    length = []
    i = 0
    for document in docList:
        scores.append(0)
    
    for document in docList:
        
        length.append(document.length)
        
    
    qlength = len(q)
    
    for x in range(qlength):
        term = q[x]
        termObj = getPostings(term,Dict) #Get obj with postings list of documents containing x term in query q
        
        if termObj != 0:
            for document in termObj.docList:
                if term in document.tokens:
                    tf = document.tokens[term] #extract term frequency of term from document
                    maxtf_tuple = document.tokens.most_common(1)
                    maxtf2_list = [x[1] for x in maxtf_tuple]
                    maxtf3_extract = maxtf2_list.pop()
                    ntf = (tf/maxtf3_extract)
                    scores[document.docID] += (ntf * termObj.idf)
               

                
        else:
            continue
            

    i = 0           
    h = len(docList)
    heaplist = []
    for x in range(h):
    
        if scores[i] != 0:
            
            scores[i] = scores[i] / length[i]
            
            
            scoreVar = docScore(i, (scores[i] * -1)) #heapq only stores min heaps so mult by -1
            heapq.heappush(heaplist, scoreVar)
            i += 1
            
        else:
            scoreVar = docScore(i, 0)
            heapq.heappush(heaplist, scoreVar)
            i += 1

    scores.clear()
    length.clear()
    
    return returnTop15(heaplist)    

##################################################################################################################################
# Function: cosineScore2
# Parameters: q = user query, docList = list of documents with document lengths, 
# Dict = dictionary of objects containing term frequency and idf
# This calculates the cosineScore for the documents in relation to a given query.
# This treates the wf(t,d) as the non-normalized-tf tfidf. This is technically the fastcosine from the book
##################################################################################################################################
def cosineScore2(q,docList,Dict) :
    
    scores = []
    length = []
    i = 0
    for document in docList:
        scores.append(0)
    #initialize scores and length lists
    for document in docList:
        length.append(document.length)
        i += 1
    
    #qlength = len(q) #Get length of terms in query
    
    qlength = len(q)
   
    for x in range(qlength):
        term = q[x]
        termObj = getPostings(term,Dict) #Get obj with postings list of documents containing x term in query q
        if termObj != 0:
            for document in termObj.docList:
                
                tf = document.tokens[term] #extract term frequency of term from document
                
                scores[document.docID] += (tf * termObj.idf) 
        else:
            continue
            

    i = 0
    h = len(docList)
    heaplist = []
    for x in range(h):
    
        if scores[i] != 0:
            scores[i] = scores[i] / length[i]
            
            scoreVar = docScore(i, (scores[i] * -1))
            heapq.heappush(heaplist, scoreVar)
            i += 1
            
        else:
            scoreVar = docScore(i, 0)
            heapq.heappush(heaplist, scoreVar)
            i += 1
    scores.clear() 
    length.clear() 
    
    return returnTop15(heaplist)

##################################################################################################################################
# Function: cosineScore3
# Parameters: q = user query, docList = list of documents with document lengths, 
# Dict = dictionary of objects containing term frequency and idf
# This calculates the cosineScore for the documents in relation to a given query.
# This treates the wf(t,d) as the regular non-normalized-tf. This is technically the fastcosine from the book
##################################################################################################################################
def cosineScore3(q,docList,Dict) :
    
    scores = []
    length = []
    i = 0

    #initialize scores and length lists
    for document in docList:
        scores.append(0)
        length.append(document.length)
        i += 1
    
    
    qlength = len(q)
    
    for x in range(qlength):
        term = q[x]
        termObj = getPostings(term,Dict) #Get obj with postings list of documents containing x term in query q
        if termObj != 0:
            for document in termObj.docList:
                tf = document.tokens[term] #extract term frequency of term from document
                
                scores[document.docID] += tf 
        else:
            continue
            

    i = 0
    h = len(docList)
    heaplist = []
    for x in range(h):
    
        if scores[i] != 0:
            scores[i] = scores[i] / length[i]
            
            scoreVar = docScore(i, (scores[i] * -1))
            heapq.heappush(heaplist, scoreVar)
            i += 1
            
        else:
            scoreVar = docScore(i, 0)
            heapq.heappush(heaplist, scoreVar)
            i += 1
    scores.clear() 
    length.clear() 
    
    return returnTop15(heaplist)

##################################################################################################################################
#Function calcDocLength
#Parameters: an index of document objects holding the tokens for each the respective document
#This function treats each term in document with a tfidf weighting
##################################################################################################################################
def calcDocLength(dict, invertedindex, doclist):
    i = 1
    for invIndex in invertedindex:
        term = invIndex.term
        termObj = getPostings(term,dict)
       

        for document in termObj.docList:
            if term in document.tokens:
                
                tf = document.tokens[term]
                
                maxtf_tuple = document.tokens.most_common(1)
                maxtf2_list = [x[1] for x in maxtf_tuple]
                maxtf3_extract = maxtf2_list.pop()
                
                tf = (tf/maxtf3_extract)           #Calculate normalized TF again.
                maxtf2_list.clear()
               
                tfidf = (tf * termObj.idf)
                weight = math.pow(tfidf,2)
                document.length = (document.length + weight)
                
        
        i += 1

    for document in doclist:
        document.length = math.sqrt(document.length)
        
        




##################################################################################################################################
#Function: readQuery
#Parameters: this function reads a query string
#Returns a list of query tokens
##################################################################################################################################
def readQuery(q):
    q = q.upper()
    queryTokens = nk.word_tokenize(q)
   
    return queryTokens

##################################################################################################################################
#Function: readQuery_stop
#Parameters: this function reads a query string
#Returns a list of query tokens
##################################################################################################################################
def readQuery_stop(q):
    stop = stopwords.words('english')
    customStop = []
    for word in stop:
        customStop.append(word.upper())
        
    punctStops = set(string.punctuation)
    for word in punctStops:
        customStop.append(word)
    q = q.upper()
    queryTokens = nk.word_tokenize(q)
    queryTokens = [word for word in queryTokens if not word in customStop]
    
    return queryTokens

##################################################################################################################################
#Function: readQuery_stem_stop
#Parameter: this function reads a query string
#Returns a list of query tokens that are stemmed
##################################################################################################################################
def readQuery_stem_stop(q):
    stop = stopwords.words('english')
    customStop = []
    for word in stop:
        customStop.append(word.upper())
    punctStops = set(string.punctuation)
    for word in punctStops:
        customStop.append(word)
    lancastStem = LancasterStemmer()
    q = q.upper()
    q = word_tokenize(q)
    q = [word for word in q if not word in customStop]
    newList = []
    for w in q:
        a = lancastStem.stem(w)
        newList.append(a)
    print(q)
    query_token =  sorted(q) #changed var
    
    
    return query_token

##################################################################################################################################
#Function: readQuery_stem
#Parameter: this function reads a query string
#Returns a list of query tokens that are stemmed
##################################################################################################################################
def readQuery_stem(q):
    lancastStem = LancasterStemmer()
    q = word_tokenize(q)
    newList = []
    for w in q:
        a = lancastStem.stem(w)
        newList.append(a)
    #print(q)
    query_token_set =  sorted(newList)        
    
    return query_token_set

##################################################################################################################################
#Function: getDoc
#Parameters: this function takes a list of objects containing fulltext documents and a user-entered docID
##################################################################################################################################
def getDoc(list, docID):
    docID = int(docID)
    docID = docID - 1
    doc = list[docID].fulltext
    print(doc)


##################################################################################################################################
#Function: getDoc2
#Parameters: this function takes a list of objects containing fulltext documents returns a doc as string for query
##################################################################################################################################
def getDoc2(list, docID):
    docID = int(docID)
    docID = docID - 1
    doc = list[docID].fulltext
    print(doc)
    return doc


##################################################################################################################################
#Function: readRelevantLisa
#Parameters: this function takes no file name and returns a list of lisa document objects with relevant docs
##################################################################################################################################

def readRelevantList():
    from classes import relevance
    judgedDocs = "Results\L17_LISA_RJNUM.txt"
    listofRelevantDocs = []

    fileStream = open(judgedDocs).read().split()

    count = 0
    additionList = []

    
    for x in fileStream:
        if count == 0:
            queryNum = int(x)
            count += 1
        elif count == 1:
            countdown = int(x)
            count += 1
        elif countdown != 0:
            relDoc = int(x)
            additionList.append(relDoc)
            countdown -= 1
            if countdown == 0:
                count = 0
                listofRelevantDocs.append(relevance(queryNum,additionList.copy()))
                additionList.clear()

        
    return listofRelevantDocs


##################################################################################################################################
# Function: cosineScore4
# Parameters: q = user query, docList = list of documents with document lengths, 
# Dict = dictionary of objects containing term frequency and idf
# This calculates the cosineScore for the documents in relation to a given query.
# This was an attempt to not normalize the length
##################################################################################################################################
def cosineScore4(q,docList,Dict) :
    
    scores = []
    length = []
    i = 0

    #initialize scores and length lists
    for document in docList:
        scores.append(0)
        length.append(1)
        i += 1
    
    
    qlength = len(q)
    
    for x in range(qlength):
        term = q[x]
        termObj = getPostings(term,Dict) #Get obj with postings list of documents containing x term in query q
        if termObj != 0:
            for document in termObj.docList:
                tf = document.tokens[term] #extract term frequency of term from document
                maxtf_tuple = document.tokens.most_common(1)
                maxtf2_list = [x[1] for x in maxtf_tuple]
                maxtf3_extract = maxtf2_list.pop()
                ntf = (tf/maxtf3_extract)
                scores[document.docID] += ntf 
        else:
            continue
            

    i = 0
    h = len(docList)
    heaplist = []
    for x in range(h):
    
        if scores[i] != 0:
            scores[i] = scores[i] / length[i]
            
            scoreVar = docScore(i, (scores[i] * -1))
            heapq.heappush(heaplist, scoreVar)
            i += 1
            
        else:
            scoreVar = docScore(i, 0)
            heapq.heappush(heaplist, scoreVar)
            i += 1
    scores.clear() 
    length.clear() 
    
    return returnTop15(heaplist)
