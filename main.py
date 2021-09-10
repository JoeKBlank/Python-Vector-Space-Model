#######################################################################################
# CS 5800 Project 2
# Joseph K Blankenship
# DUE: June 30, 2021
# INCLUDES NLTK PACKAGE AND NUMPY PACKAGE
#
#This the main program for project 2.
#######################################################################################

import nltk as nk
import os
import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
from classes import *
from functions import *

def main():
    from classes import results
    #THIS PROGRAM BUILDS THE INDEX FIRST IN DYNAMIC MEMORY
    myFile = "lisatxtfiles_devset\lisa10_test.txt"
    lisaFileQue = "lisatxtfiles_devset\lisaQue.txt"
    lisaQue = [] #LISA_main6004.txt #lisa10_test.txt #lisa500.txt

    docList = []
    docTextList = []
    invertedIndex = []
    Dict = {}

    myQuery = ''
##################################################################################################################################
#MAIN MENU
##################################################################################################################################

    print("Welcome!")
    print("Enter 1: To run all LISA queries and print relevance results [tfidf, plain]")
    print("Enter 2: To run all LISA queries and print relevance results [tfidf, stopped]")
    print("Enter 3: To run all LISA queries and print relevance results [tfidf, stemmed]")
    print("Enter 4: To run all LISA queries and print relevance results [non-normalized tf: tfidf, plain]")
    print("Enter 5: To run all LISA queries and print relevance results [non-normalized tf: tfidf, stopped]")
    print("Enter 6: To run all LISA queries and print relevance results [non-normalized tf: tfidf, stemmed]")
    print("Enter 7: To run your own query [tfidf, plain]")
    print("Enter 8: To run your own query [tfidf, stopped]")
    print("Enter 9: To run your own query [tfidf, stemmed]")
    print("Enter 10: To run your own query [non-normalized tf: tfidf, plain]")
    print("Enter 11: To run your own query [non-normalized tf: tfidf, stopped]")
    print("Enter 12: To run your own query [non-normalized tf: tfidf, stemmed]")
    print("Enter 13: To run a doc as a query [tfidf, plain]")
    print("Enter 14: To run a doc as a query [tfidf, stemmed]")
    print("Enter 15: To view a document")
    print("Enter 16: To quit")
    print("Enter 17: MAX TRY LISA. tfidf, stopped, stemmed")
    print("Enter 18: To run all LISA queries and print relevance results [non-normalized tf, plain]")
    print("Enter 19: run doc as query [tf, plain]")
    print("ENTER 20 FOR REAL TF comps plain")
    s = "0"
    while s == "0" and s != "4":
        s = input("Enter Selection Here:")
##################################################################################################################################
#To run all LISA queries and print relevance results [tfidf, plain]
##################################################################################################################################
        if s == "1": 
            print("please wait!")
            createDatabaseReg(myFile, docTextList, invertedIndex, docList, Dict )
            print("Running LISA Queries [tfidf, plain]")
            parseLisa1(lisaFileQue, lisaQue)
            i = 1
            y = input("select query to test or enter \"A\" for all, C for compare mode or enter a query num to compare: " )
            #y = "c"
            if y == ('A' or 'a'):
                for documentFull in lisaQue:
                    print(f"    Query {i}: ")
                    retrieved = []
                    retrieved = cosineScore(documentFull.tokens,docList,Dict) #changed documentFull.Tokens to document
                    j = 1
                    for docScore in retrieved:
                        print(f" Result #{j} {(docScore.docID + 1)}")
                        j += 1
                    i += 1
            elif y == "C": #COMPARE MODE
                print("doing comparisions:")
                queryNum = 1
                judgedRel = readRelevantList() #list of relevance objects
                comps = [] #list of results objects
                k = 0
                i = 1
                for documentFull in lisaQue:
                    
                    retrieved = []
                    retrieved = cosineScore(documentFull.tokens,docList,Dict) #returns a single list of score objects (score, ID)
                    j = 1
                    print(f"Query {i}")
                    for docScore in retrieved:
                        print(f" Result #{j} {(docScore.docID + 1)}")
                        j += 1
                    i += 1
                    comps.append(results(queryNum, retrieved.copy())) #Appends a results object including the right Qnum and copy of score obj list
                    comps[k].calcP_top5(judgedRel[k])
                    comps[k].calcP_top10(judgedRel[k])
                    comps[k].calcP_top15(judgedRel[k])
                    comps[k].calcR_top15(judgedRel[k])
                    comps[k].calc_MAP(judgedRel[k])
                    comps[k].calc_PercisionRecallCurveVals(judgedRel[k])
                    k += 1
                    queryNum += 1
                #r = 1
                #list1 = comps[0].preList
                #print(list1)
                #list2 = comps[0].reList
                #print(list2)
                #plt.plot(list2,list1)
                #plt.savefig(f'fig_{r}.png')
                for results in comps:
                    print(results.query)
                    print(results.pre_5)
                    print(results.pre_10)
                    print(results.pre_15)
                    print(results.re_15)
                    #plt.plot(results.preList.copy(),results.reList.copy())
                    #plt.savefig(f'fig_{r}.png')
                    #r += 1
                    #if results.map > 0:
                    #    print(results.map)
                    #else:
                    #    print(f"could not be found.")
            else:
                
                y = int(y)
                retrieved = cosineScore(lisaQue[(y - 1)].tokens,docList,Dict)
                j = 1
                for docScore in retrieved:
                    print(f" Result #{j} {(docScore.docID + 1)}")
                    j += 1

##################################################################################################################################
#To run all LISA queries and print relevance results [tfidf, stopped]      
##################################################################################################################################
        if s == "2": 
            print("please wait!")
            createDatabaseStop(myFile, docTextList, invertedIndex, docList, Dict )
            print("Running LISA Queries [tfidf, stopped]")
            parseLisa_stop(lisaFileQue, lisaQue)
            i = 1
            y = input("select query to test or enter \"A\" for all, C for compare mode or enter a query num to compare: " )
            if y == 'A':
                for documentFull in lisaQue:
                    print(f"    Query {i}: ")
                    retrieved = []
                    retrieved = cosineScore(documentFull.tokens,docList,Dict)
                    j = 1
                    for docScore in retrieved:
                        print(f" Result #{j} {(docScore.docID + 1)}")
                        j += 1
                    i += 1
            elif y == "C":
                print("doing comparisions:")
                queryNum = 1
                judgedRel = readRelevantList() #list of relevance objects
                comps = [] #list of results objects
                k = 0
                i = 1
                for documentFull in lisaQue:
                    
                    retrieved = []
                    retrieved = cosineScore(documentFull.tokens,docList,Dict) #returns a single list of score objects (score, ID)
                    j = 1
                    print(f"Query {i}")
                    for docScore in retrieved:
                        print(f" Result #{j} {(docScore.docID + 1)}")
                        j += 1
                    i += 1
                    comps.append(results(queryNum, retrieved.copy())) #Appends a results object including the right Qnum and copy of score obj list
                    comps[k].calcP_top5(judgedRel[k])
                    comps[k].calcP_top10(judgedRel[k])
                    comps[k].calcP_top15(judgedRel[k])
                    comps[k].calcR_top15(judgedRel[k])
                    comps[k].calc_MAP(judgedRel[k])
                    k += 1
                    queryNum += 1
                for results in comps:
                    print(results.query)
                    print(results.pre_5)
                    print(results.pre_10)
                    print(results.pre_15)
                    print(results.re_15)
                    #if results.map > 0:
                    #    print(results.map)
                    #else:
                    #    print(f"could not be found.")
                #for results in comps:
                #    print(f"Percision at k = 5: Query {results.query}:")
                #    print(results.pre_5)
                #    print(f"Percision at k = 10: Query {results.query}:")
                #    print(results.pre_10)
                #    print(f"Percision at k = 15: Query {results.query}:")
                #    print(results.pre_15)
                #    print(f"MAP for Query:{results.query}:")
                #    if results.map > 0:
                #        print(results.map)
                #    else:
                #        print(f"could not be found.")
            else:
                y = int(y)
                retrieved = cosineScore(lisaQue[(y - 1)].tokens,docList,Dict)
                j = 1
                for docScore in retrieved:
                    print(f" Result #{j} {(docScore.docID + 1)}")
                    j += 1
            break 
##################################################################################################################################
#To run all LISA queries and print relevance results [tfidf, stemmed]
##################################################################################################################################        
        elif s == '3':
            print("please wait!")
            createDatabaseStem(myFile, docTextList, invertedIndex, docList, Dict )
            print("Running LISA Queries [tfidf, stemmed]")
            parseLisa_stem(lisaFileQue, lisaQue)
            i = 1
            y = input("select query to test or enter \"A\" for all, C for compare mode or enter a query num to compare: " )
            if y == 'A':
                for documentFull in lisaQue:
                    print(f"    Query {i}: ")
                    retrieved = []
                    retrieved = cosineScore(documentFull.tokens,docList,Dict)
                    j = 1
                    for docScore in retrieved:
                        print(f" Result #{j} {(docScore.docID + 1)}")
                        j += 1
                    i += 1
            elif y == "C":
                print("doing comparisions:")
                queryNum = 1
                judgedRel = readRelevantList() #list of relevance objects
                comps = [] #list of results objects
                k = 0
                i = 1
                for documentFull in lisaQue:
                    
                    retrieved = []
                    retrieved = cosineScore(documentFull.tokens,docList,Dict) #returns a single list of score objects (score, ID)
                    j = 1
                    print(f"Query {i}")
                    for docScore in retrieved:
                        print(f" Result #{j} {(docScore.docID + 1)}")
                        j += 1
                    i += 1
                    comps.append(results(queryNum, retrieved.copy())) #Appends a results object including the right Qnum and copy of score obj list
                    comps[k].calcP_top5(judgedRel[k])
                    comps[k].calcP_top10(judgedRel[k])
                    comps[k].calcP_top15(judgedRel[k])
                    comps[k].calcR_top15(judgedRel[k])
                    comps[k].calc_MAP(judgedRel[k])
                    k += 1
                    queryNum += 1
                for results in comps:
                    print(results.query)
                    print(results.pre_5)
                    print(results.pre_10)
                    print(results.pre_15)
                    print(results.re_15)
                    #if results.map > 0:
                    #    print(results.map)
                    #else:
                    #    print(f"could not be found.")
                #for results in comps:
                #    print(f"Percision at k = 5: Query {results.query}:")
                #    print(results.pre_5)
                #    print(f"Percision at k = 10: Query {results.query}:")
                #    print(results.pre_10)
                #    print(f"Percision at k = 15: Query {results.query}:")
                #    print(results.pre_15)
                #    print(f"MAP for Query:{results.query}:")
                #    if results.map > 0:
                #        print(results.map)
                #    else:
                #        print(f"could not be found.")
            else:
                y = int(y)
                retrieved = cosineScore(lisaQue[(y - 1)].tokens,docList,Dict)
                j = 1
                for docScore in retrieved:
                    print(f" Result #{j} {(docScore.docID + 1)}")
                    j += 1
            break
##################################################################################################################################
#To run all LISA queries and print relevance results [non-normalized tf: tfidf, plain]")
##################################################################################################################################        
        elif s == '4':
            print("please wait!")
            createDatabaseReg(myFile, docTextList, invertedIndex, docList, Dict )
            print("Running LISA Queries [non-normalized tf: tfidf, plain]")
            parseLisa1(lisaFileQue, lisaQue)
            i = 1
            y = input("select query to test or enter \"A\" for all, C for compare mode or enter a query num to compare: " )
            if y == 'A' :
                for documentFull in lisaQue:
                    print(f"    Query {i}: ")
                    retrieved = []
                    retrieved = cosineScore2(documentFull.tokens,docList,Dict)
                    j = 1
                    for docScore in retrieved:
                        print(f" Result #{j} {(docScore.docID + 1)}")
                        j += 1
                    i += 1
            
            elif y == "C":
                print("doing comparisions:")
                queryNum = 1
                judgedRel = readRelevantList() #list of relevance objects
                comps = [] #list of results objects
                k = 0
                i = 1
                for documentFull in lisaQue:
                    
                    retrieved = []
                    retrieved = cosineScore2(documentFull.tokens,docList,Dict) #returns a single list of score objects (score, ID)
                    j = 1
                    print(f"Query {i}")
                    for docScore in retrieved:
                        print(f" Result #{j} {(docScore.docID + 1)}")
                        j += 1
                    i += 1
                    comps.append(results(queryNum, retrieved.copy())) #Appends a results object including the right Qnum and copy of score obj list
                    comps[k].calcP_top5(judgedRel[k])
                    comps[k].calcP_top10(judgedRel[k])
                    comps[k].calcP_top15(judgedRel[k])
                    comps[k].calcR_top15(judgedRel[k])
                    comps[k].calc_MAP(judgedRel[k])
                    k += 1
                    queryNum += 1
                for results in comps:
                    print(results.query)
                    print(results.pre_5)
                    print(results.pre_10)
                    print(results.pre_15)
                    print(results.re_15)
                    #if results.map > 0:
                    #    print(results.map)
                    #else:
                    #    print(f"could not be found.")
                #for results in comps:
                #    print(f"Percision at k = 5: Query {results.query}:")
                #    print(results.pre_5)
                #    print(f"Percision at k = 10: Query {results.query}:")
                #    print(results.pre_10)
                #    print(f"Percision at k = 15: Query {results.query}:")
                #    print(results.pre_15)
                #    print(f"MAP for Query:{results.query}:")
                #    if results.map > 0:
                #        print(results.map)
                #    else:
                #        print(f"could not be found.")
            else:
                y = int(y)
                retrieved = cosineScore2(lisaQue[(y - 1)].tokens,docList,Dict)
                j = 1
                for docScore in retrieved:
                    print(f" Result #{j} {(docScore.docID + 1)}")
                    j += 1
                break
##################################################################################################################################
#To run all LISA queries and print relevance results [non-normalized tf: tfidf, stopped] 
##################################################################################################################################
        elif s == '5':
            print("please wait!")
            createDatabaseStop(myFile, docTextList, invertedIndex, docList, Dict )
            print("Running LISA Queries [non-normalized tf: tfidf, stopped]")
            parseLisa_stop(lisaFileQue, lisaQue)
            i = 1
            y = input("select query to test or enter \"A\" for all, C for compare mode or enter a query num to compare: " )
            if y == 'A':
                for documentFull in lisaQue:
                    print(f"    Query {i}: ")
                    retrieved = []
                    retrieved = cosineScore2(documentFull.tokens,docList,Dict)
                    j = 1
                    for docScore in retrieved:
                        print(f" Result #{j} {(docScore.docID + 1)}")
                        j += 1
                    i += 1
            
            elif y == "C":
                print("doing comparisions:")
                queryNum = 1
                judgedRel = readRelevantList() #list of relevance objects
                comps = [] #list of results objects
                k = 0
                i = 1
                for documentFull in lisaQue:
                    
                    retrieved = []
                    retrieved = cosineScore2(documentFull.tokens,docList,Dict) #returns a single list of score objects (score, ID)
                    j = 1
                    print(f"Query {i}")
                    for docScore in retrieved:
                        print(f" Result #{j} {(docScore.docID + 1)}")
                        j += 1
                    i += 1
                    comps.append(results(queryNum, retrieved.copy())) #Appends a results object including the right Qnum and copy of score obj list
                    comps[k].calcP_top5(judgedRel[k])
                    comps[k].calcP_top10(judgedRel[k])
                    comps[k].calcP_top15(judgedRel[k])
                    comps[k].calcR_top15(judgedRel[k])
                    comps[k].calc_MAP(judgedRel[k])
                    k += 1
                    queryNum += 1
                for results in comps:
                    print(results.query)
                    print(results.pre_5)
                    print(results.pre_10)
                    print(results.pre_15)
                    print(results.re_15)
                    #if results.map > 0:
                    #    print(results.map)
                    #else:
                    #    print(f"could not be found.")
                #for results in comps:
                #    print(f"Percision at k = 5: Query {results.query}:")
                #    print(results.pre_5)
                #    print(f"Percision at k = 10: Query {results.query}:")
                #    print(results.pre_10)
                #    print(f"Percision at k = 15: Query {results.query}:")
                #    print(results.pre_15)
                #    print(f"MAP for Query:{results.query}:")
                #    if results.map > 0:
                #        print(results.map)
                #    else:
                #        print(f"could not be found.")
            else:
                y = int(y)
                retrieved = cosineScore2(lisaQue[(y - 1)].tokens,docList,Dict)
                j = 1
                for docScore in retrieved:
                    print(f" Result #{j} {(docScore.docID + 1)}")
                    j += 1
            break
##################################################################################################################################
#To run all LISA queries and print relevance results [non-normalized tf: tfidf, stemmed]
##################################################################################################################################
        elif s == '6':
            print("please wait!")
            createDatabaseStem(myFile, docTextList, invertedIndex, docList, Dict )
            print("Running LISA Queries [non-normalized tf: tfidf, stemmed]")
            parseLisa_stem(lisaFileQue, lisaQue)
            i = 1
            y = input("select query to test or enter \"A\" for all, C for compare mode or enter a query num to compare: " )
            if y == 'A':
                for documentFull in lisaQue:
                    print(f"    Query {i}: ")
                    retrieved = []
                    retrieved = cosineScore2(documentFull.tokens,docList,Dict)
                    j = 1
                    for docScore in retrieved:
                        print(f" Result #{j} {(docScore.docID + 1)}")
                        j += 1
                    i += 1
        
            elif y == "C":
                print("doing comparisions:")
                queryNum = 1
                judgedRel = readRelevantList() #list of relevance objects
                comps = [] #list of results objects
                k = 0
                i = 1
                for documentFull in lisaQue:
                    
                    retrieved = []
                    retrieved = cosineScore2(documentFull.tokens,docList,Dict) #returns a single list of score objects (score, ID)
                    j = 1
                    print(f"Query {i}")
                    for docScore in retrieved:
                        print(f" Result #{j} {(docScore.docID + 1)}")
                        j += 1
                    i += 1
                    comps.append(results(queryNum, retrieved.copy())) #Appends a results object including the right Qnum and copy of score obj list
                    comps[k].calcP_top5(judgedRel[k])
                    comps[k].calcP_top10(judgedRel[k])
                    comps[k].calcP_top15(judgedRel[k])
                    comps[k].calcR_top15(judgedRel[k])
                    comps[k].calc_MAP(judgedRel[k])
                    k += 1
                    queryNum += 1
                for results in comps:
                    print(results.query)
                    print(results.pre_5)
                    print(results.pre_10)
                    print(results.pre_15)
                    print(results.re_15)
                    #if results.map > 0:
                    #    print(results.map)
                    #else:
                    #    print(f"could not be found.")
                #for results in comps:
                #    print(f"Percision at k = 5: Query {results.query}:")
                #    print(results.pre_5)
                #    print(f"Percision at k = 10: Query {results.query}:")
                #    print(results.pre_10)
                #    print(f"Percision at k = 15: Query {results.query}:")
                #    print(results.pre_15)
                #    print(f"MAP for Query:{results.query}:")
                #    if results.map > 0:
                #        print(results.map)
                #    else:
                #        print(f"could not be found.")
            else:
                y = int(y)
                retrieved = cosineScore2(lisaQue[(y - 1)].tokens,docList,Dict)
                j = 1
                for docScore in retrieved:
                    print(f" Result #{j} {(docScore.docID + 1)}")
                    j += 1
            break
##################################################################################################################################
#To run your own query [tfidf, plain]
##################################################################################################################################
        elif s == "7":
            print("please wait!")
            createDatabaseReg(myFile, docTextList, invertedIndex, docList, Dict )
            myQuery = input("[tfidf, plain] Enter Query:")  
            queryList = readQuery(myQuery)
            retrieved = []
            retrieved = cosineScore(queryList,docList,Dict)
            i = 1
            for docScore in retrieved:
                print(f" Result #{i} {(docScore.docID + 1)}")
                i += 1
            
            break
##################################################################################################################################
#To run your own query [tfidf, stopped]
##################################################################################################################################
        elif s == "8":
            print("please wait!")
            createDatabaseStop(myFile, docTextList, invertedIndex, docList, Dict )
            myQuery = input("[tfidf, stemmed] Enter Query:")  
            queryList = readQuery_stop(myQuery)
            retrieved = cosineScore(queryList,docList,Dict)
            i = 1
            for docScore in retrieved:
                print(f" Result #{i} {(docScore.docID + 1)}")
                i += 1
            break
##################################################################################################################################
#To run your own query [tfidf, stemmed]
##################################################################################################################################
        elif s == "9":
            print("please wait!")
            createDatabaseStem(myFile, docTextList, invertedIndex, docList, Dict )
            myQuery = input("[tfidf, stemmed] Enter Query:")  
            queryList = readQuery_stem(myQuery) #changed to stem_stop
            retrieved = cosineScore(queryList,docList,Dict)
            i = 1
            for docScore in retrieved:
                print(f" Result #{i} {(docScore.docID + 1)}")
                i += 1
            break
##################################################################################################################################
#To run your own query [non-normalized tf: tfidf, plain]
##################################################################################################################################
        elif s == "10":
            print("please wait!")
            createDatabaseReg(myFile, docTextList, invertedIndex, docList, Dict )
            myQuery = input("[non-normalized tf: tfidf, plain] Enter Query:")  
            queryList = readQuery(myQuery)
            retrieved = cosineScore2(queryList,docList,Dict)
            i = 1
            for docScore in retrieved:
                print(f" Result #{i} {(docScore.docID + 1)}")
                i += 1
            break  
##################################################################################################################################
#To run your own query [non-normalized tf: tfidf, stopped]        
##################################################################################################################################  
        elif s == "11":
            print("please wait!")
            createDatabaseStop(myFile, docTextList, invertedIndex, docList, Dict )
            myQuery = input("[non-normalized tf: tfidf, stopped] Enter Query:")  
            queryList = readQuery_stop(myQuery)
            retrieved = cosineScore2(queryList,docList,Dict)
            i = 1
            for docScore in retrieved:
                print(f" Result #{i} {(docScore.docID + 1)}")
                i += 1
            break
##################################################################################################################################
#To run your own query [non-normalized tf: tfidf, stemmed]
##################################################################################################################################
        elif s == "12":
            print("please wait!")
            createDatabaseStem(myFile, docTextList, invertedIndex, docList, Dict )
            myQuery = input("[non-normalized tf: tfidf, stemmed] Enter Query:")  
            queryList = readQuery_stem(myQuery)
            retrieved = cosineScore2(queryList,docList,Dict)
            
            i = 1
            for docScore in retrieved:
                print(f" Result #{i} {(docScore.docID + 1)}")
                i += 1
            break
##################################################################################################################################
#To run a doc as a query [tfidf, plain]
##################################################################################################################################       
        elif s == "13":
            print("please wait!")
            createDatabaseReg(myFile, docTextList, invertedIndex, docList, Dict )
            uDoc = input("Enter document number: ")
            docObj = getDoc2(docTextList, uDoc)
            queryList = readQuery(docObj)
            retrieved = cosineScore(queryList,docList,Dict)
            i = 1
            for docScore in retrieved:
                print(f" Result #{i} {(docScore.docID + 1)}")
                i += 1
            break
##################################################################################################################################
#To run a doc as a query [tfidf, stemmed]
##################################################################################################################################
        elif s == "14":
            print("please wait!")
            createDatabaseStem(myFile, docTextList, invertedIndex, docList, Dict )
            uDoc = input("Enter document number: ")
            docObj = getDoc2(docTextList, uDoc)
            queryList = readQuery_stem(docObj)
            retrieved = cosineScore(queryList,docList,Dict)
            i = 1
            for docScore in retrieved:
                print(f" Result #{i} {(docScore.docID + 1)}")
                i += 1
            break
##################################################################################################################################
#To view a document
##################################################################################################################################
        elif s == "15":
            createDatabaseReg(myFile, docTextList, invertedIndex, docList, Dict )
            userDoc = input("Enter document number:") 
            while userDoc != 'q':
                getDoc(docTextList, userDoc)
                userDoc = input('Enter another doc or press q: ')
            break  
##################################################################################################################################
#To quit
################################################################################################################################## 
        elif s == "16":
            return

##################################################################################################################################
#MAX TRY STOP STEM TFIDF
################################################################################################################################## 
        elif s == "17":
            print("please wait!")
            createDatabaseStop_Stem(myFile, docTextList, invertedIndex, docList, Dict )
            print("Running LISA Queries [MAX]")
            parseLisa_stem_stop(lisaFileQue, lisaQue)
            i = 1
            y = input("select query to test or enter \"A\" for all, C for compare mode or query num for your own: " )
            #y = "c"
            if y == 'A':
                for documentFull in lisaQue:
                    print(f"    Query {i}: ")
                    retrieved = []
                    retrieved = cosineScore(documentFull.tokens,docList,Dict)
                    j = 1
                    for docScore in retrieved:
                        print(f" Result #{j} {(docScore.docID + 1)}")
                        j += 1
                    i += 1
            
            elif y == "C": #COMPARE MODE
                print("doing comparisions:")
                queryNum = 1
                judgedRel = readRelevantList() #list of relevance objects
                comps = [] #list of results objects
                k = 0
                i = 1
                for documentFull in lisaQue:
                    
                    retrieved = []
                    retrieved = cosineScore(documentFull.tokens,docList,Dict) #returns a single list of score objects (score, ID)
                    j = 1
                    print(f"Query {i}")
                    for docScore in retrieved:
                        print(f" Result #{j} {(docScore.docID + 1)}")
                        j += 1
                    i += 1
                    comps.append(results(queryNum, retrieved.copy())) #Appends a results object including the right Qnum and copy of score obj list
                    comps[k].calcP_top5(judgedRel[k])
                    comps[k].calcP_top10(judgedRel[k])
                    comps[k].calcP_top15(judgedRel[k])
                    comps[k].calcR_top15(judgedRel[k])
                    comps[k].calc_MAP(judgedRel[k])
                    k += 1
                    queryNum += 1
                for results in comps:
                    print(results.query)
                    print(results.pre_5)
                    print(results.pre_10)
                    print(results.pre_15)
                    print(results.re_15)
                    #if results.map > 0:
                    #    print(results.map)
                    #else:
                    #    print(f"could not be found.")
                #for results in comps:
                #    print(f"Percision at k = 5: Query {results.query}:")
                #    print(results.pre_5)
                #    print(f"Percision at k = 10: Query {results.query}:")
                #    print(results.pre_10)
                #    print(f"Percision at k = 15: Query {results.query}:")
                #    print(results.pre_15)
                #    print(f"Recall at 15 retrieved: ")
                #    print(results.re_15)
                #    print(f"MAP for Query:{results.query}:")
                #    if results.map > 0:
                #        print(results.map)
                #    else:
                #        print(f"could not be found.")
            else:
                y = int(y)
                retrieved = cosineScore2(lisaQue[(y - 1)].tokens,docList,Dict)
                j = 1
                for docScore in retrieved:
                    print(f" Result #{j} {(docScore.docID + 1)}")
                    j += 1

##################################################################################################################################
#To run all LISA queries and print relevance results [non-normal tf, plain]
##################################################################################################################################
        if s == "18": 
            print("please wait!")
            createDatabaseReg(myFile, docTextList, invertedIndex, docList, Dict )
            print("Running LISA Queries [non-normal tf, plain]")
            parseLisa1(lisaFileQue, lisaQue)
            i = 1
            y = input("select query to test or enter \"A\" for all, C for compare mode: " )
            #y = "c"
            if y == 'A':
                for documentFull in lisaQue:
                    print(f"    Query {i}: ")
                    retrieved = []
                    retrieved = cosineScore3(documentFull.tokens,docList,Dict)
                    j = 1
                    for docScore in retrieved:
                        print(f" Result #{j} {(docScore.docID + 1)}")
                        j += 1
                    i += 1
            elif y == "C": #COMPARE MODE
                print("doing comparisions:")
                queryNum = 1
                judgedRel = readRelevantList() #list of relevance objects
                comps = [] #list of results objects
                k = 0
                i = 1
                for documentFull in lisaQue:
                    
                    retrieved = []
                    retrieved = cosineScore3(documentFull.tokens,docList,Dict) #returns a single list of score objects (score, ID)
                    j = 1
                    print(f"Query {i}")
                    for docScore in retrieved:
                        print(f" Result #{j} {(docScore.docID + 1)}")
                        j += 1
                    i += 1
                    comps.append(results(queryNum, retrieved.copy())) #Appends a results object including the right Qnum and copy of score obj list
                    comps[k].calcP_top5(judgedRel[k])
                    comps[k].calcP_top10(judgedRel[k])
                    comps[k].calcP_top15(judgedRel[k])
                    comps[k].calcR_top15(judgedRel[k])
                    comps[k].calc_MAP(judgedRel[k])
                    k += 1
                    queryNum += 1
                for results in comps:
                    print(results.query)
                    print(results.pre_5)
                    print(results.pre_10)
                    print(results.pre_15)
                    print(results.re_15)
                    #if results.map > 0:
                    #    print(results.map)
                    #else:
                    #    print(f"could not be found.")



##################################################################################################################################
#To run a doc as a query [tf, plain]
##################################################################################################################################       
        elif s == "19":
            print("please wait!")
            createDatabaseReg(myFile, docTextList, invertedIndex, docList, Dict )
            uDoc = input("Enter document number: ")
            docObj = getDoc2(docTextList, uDoc)
            queryList = readQuery(docObj)
            retrieved = cosineScore3(queryList,docList,Dict)
            i = 1
            for docScore in retrieved:
                print(f" Result #{i} {(docScore.docID + 1)}")
                i += 1
            break

##################################################################################################################################
#To run all LISA queries and print relevance results [REAL TF]
##################################################################################################################################
        if s == "20": 
            print("please wait!")
            createDatabaseReg(myFile, docTextList, invertedIndex, docList, Dict )
            print("Running LISA Queries [REAL tf, plain]")
            parseLisa1(lisaFileQue, lisaQue)
            i = 1
            y = input("select query to test or enter \"A\" for all, C for compare mode: " )
            #y = "c"
            if y == 'A':
                for documentFull in lisaQue:
                    print(f"    Query {i}: ")
                    retrieved = []
                    retrieved = cosineScore4(documentFull.tokens,docList,Dict)
                    j = 1
                    for docScore in retrieved:
                        print(f" Result #{j} {(docScore.docID + 1)}")
                        j += 1
                    i += 1
            elif y == "C": #COMPARE MODE
                print("doing comparisions:")
                queryNum = 1
                judgedRel = readRelevantList() #list of relevance objects
                comps = [] #list of results objects
                k = 0
                i = 1
                for documentFull in lisaQue:
                    
                    retrieved = []
                    retrieved = cosineScore4(documentFull.tokens,docList,Dict) #returns a single list of score objects (score, ID)
                    j = 1
                    print(f"Query {i}")
                    for docScore in retrieved:
                        print(f" Result #{j} {(docScore.docID + 1)}")
                        j += 1
                    i += 1
                    comps.append(results(queryNum, retrieved.copy())) #Appends a results object including the right Qnum and copy of score obj list
                    comps[k].calcP_top5(judgedRel[k])
                    comps[k].calcP_top10(judgedRel[k])
                    comps[k].calcP_top15(judgedRel[k])
                    comps[k].calcR_top15(judgedRel[k])
                    comps[k].calc_MAP(judgedRel[k])
                    k += 1
                    queryNum += 1
                for results in comps:
                    print(results.query)
                    print(results.pre_5)
                    print(results.pre_10)
                    print(results.pre_15)
                    print(results.re_15)
                    #if results.map > 0:
                    #    print(results.map)
                    #else:
                    #    print(f"could not be found.")

##################################################################################################################################
#QUERY STAGE
################################################################################################################################## 
    
    if retrieved:
        print("Press q to quit")
        userRelDoc = input("Enter document number from above to view: ")
        while userRelDoc != 'q':
            getDoc(docTextList, userRelDoc)
            userRelDoc = input('Enter another doc or press q: ')
    
    else:
        return
        

    
    return

if __name__ == "__main__":
    main()