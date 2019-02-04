#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Encoding: UTF-8

import configparser, os, sys, urllib.request, urllib.error, urllib.parse, json, codecs

import xml.etree.ElementTree as ET

##### read config file
config = configparser.ConfigParser()
config.read("%s/config.ini" % os.path.dirname(os.path.realpath(__file__)))  # read config file

#missatSamtal = config.get('missatsamtal', 'api')
missatSamtalFormat = config.get('missatsamtal', 'format')
missatSamtalList = config.get('missatsamtal', 'list')
missatSamtalSearch = config.get('missatsamtal', 'search')
missatSamtalPost = config.get('missatsamtal', 'post')

#vemRingde = config.get('vemringde', 'api')
vemRingdeFormat = config.get('vemringde', 'format')
vemRingdeList = config.get('vemringde', 'list')
vemRingdeSearch = config.get('vemringde', 'search')

timeOut = int(config.get('misc', 'timeOut'))

##### what to do on errors
def onError(errorCode, extra):
    print("\n*** Error:")
    if errorCode == 1:
        print(extra)
        usage(errorCode)
    elif errorCode == 2:
        print("    No options given")
        usage(errorCode)
    elif errorCode == 3:
        print("    No program part chosen")
        usage(errorCode)
    elif errorCode in (4, 5, 6, 8, 12, 13):
        print("    %s" % extra)
        sys.exit(errorCode)
    elif errorCode in (7, 9, 10, 11):
        print("    %s" % extra)

##### some help
def usage(exitCode):
    print("\nUsage:")
    print("----------------------------------------")
    print("%s -l [-n <number of answers>] [-o <out file> [-a]] [-v]" % sys.argv[0])
    print("      Lists the most common numbers and their companies, max 500")
    print()
    print("%s -s <phone number> [-n <number of answers>] [-v]" % sys.argv[0])
    print("      Searches for <phone number> and shows information")
    print()
    print("%s -h" % sys.argv[0])
    print("      Prints this")
    print()
    print("    Options:")
    print("        -n <number of answers> limits the outputs")
    print("            defaults to 10 with -l, and 1 on -s")
    print("        -o output to file")
    print("        -a append current date and time to out files name")
    print("        -v verboses output")
    sys.exit(exitCode)
    
def outputQuestion(action, limit, number, verbose):
    if verbose:
        print("The url for missatsamtal.se would be:")
    
    if action == "list":
        print("%s&limit=%s" % (missatSamtalList, limit))
    elif action == "search":
        print("%s&number=%s&numberOfCompanies=%s" % (missatSamtalSearch, number, limit))
    
    if verbose:
        print("The url for vemringde.se would be:")
        
    if action == "list":
        print("%s&limit=%s" % (vemRingdeList, limit))
    elif action == "search":
        print("%s&q=%s&limit=%s" % (vemRingdeSearch, number, limit))    
        
def getResponse(url, verbose):
    try:
        response = urllib.request.urlopen(url, timeout=timeOut).read()  # get data from server
        if verbose:
            print("--- Got data")
    except urllib.error.URLError as e:
        if verbose:
            print("*** There was an error: %r" % e)
            print("*** Could not get data")
           
    if verbose:
        print("--- Response:\n    %s" % response)
        
    return response
        
def listNumbers(limit, outFile, verbose):
    numberList = []
    
    if outFile:
        if verbose:
            print("Creating %s..." % outFile)
        myFile = codecs.open(outFile, 'w', "utf-8")
        
    
    if verbose:
        print("--- Listing numbers...")
        print("--- URL: %s&limit=%s" % (missatSamtalList, limit))
        
    response = getResponse("%s&limit=%s" % (missatSamtalList, limit), verbose)
    
    if missatSamtalFormat == "json":
        data = json.loads(response)
    elif missatSamtalFormat == "xml":
        xmlRoot = ET.fromstring(response)  # read xml
        
        for xmlChild in xmlRoot:
            name = ""
            number = ""
            if verbose:
                print("%s" % (xmlChild.tag))
            for xmlInnerChild in xmlChild:
                if xmlInnerChild.tag.lower() == "number":
                    number = xmlInnerChild.text
                    if verbose:
                        print(xmlInnerChild.tag)
                        print(number)
                elif xmlInnerChild.tag.lower() == "name":
                    name = xmlInnerChild.text
                    if verbose:
                        print(xmlInnerChild.tag)
                        print(name)
                if name and number:
                    numberList.append({'number': number, 'name': name})
                
    for numbers in numberList:
        print(numbers)
        if outFile:
            if verbose:
                print("Writing %s,%s to file..." % (numbers['number'], numbers['name']))
            myFile.write("%s,%s\n" % (numbers['number'], numbers['name']))
        
    if outFile:            
        myFile.close()
            
    
      
def lookupNumber(number, numberOfCompanies, verbose):
    companyList = []
    
    if verbose:
        print("--- Getting info for %s..." % number)
        print("--- URL: %s&number=%s&numberOfCompanies=%s" % (missatSamtalSearch, number, numberOfCompanies))
        
    response = getResponse("%s&number=%s&numberOfCompanies=%s" % (missatSamtalSearch, number, numberOfCompanies), verbose) 
                    
    if missatSamtalFormat == "json":
        data = json.loads(response)
    elif missatSamtalFormat == "xml":
        xmlRoot = ET.fromstring(response)  # read xml
        
        for xmlChild in xmlRoot:
            name = ""
            number = ""
            if xmlChild.tag.lower() == "comments":
                comments = xmlChild.text
                print("Comments: %s" % comments)
            else:
                if verbose:
                    print(xmlChild.tag)
            for xmlInnerChild in xmlChild:
                name = ""
                comments = ""
                for xmlInnerInnerChild in xmlInnerChild:
                    if xmlInnerInnerChild.tag.lower() == "name":
                        name = xmlInnerInnerChild.text
                        if verbose:
                            print(xmlInnerInnerChild.tag)
                            print(name)
                    elif xmlInnerInnerChild.tag.lower() == "comments":
                        comments = xmlInnerInnerChild.text
                        if verbose:
                            print(xmlInnerInnerChild.tag)
                            print(comments)
                    if name and comments:
                        companyList.append({'name': name, 'comments': comments})
        
    for company in companyList:
        print(company)
        
        
        
        