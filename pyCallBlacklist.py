#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Encoding: UTF-8

import getopt, sys, time

from functions import onError, usage, outputQuestion, listNumbers, lookupNumber

actionList = False
actionSearch = ""
limit = 0
outFile = ""
appendDate = False
printQuestion = False
verbose = False


############### handle arguments ###############
try:
    myopts, args = getopt.getopt(sys.argv[1:], 'ln:s:o:apvh', 
                                 ['list', 'number:', 'search:', 'outfile:', 'appenddate', 'print', 
                                  'verbose', 'help'])

except getopt.GetoptError as e:
    onError(1, str(e))

if len(sys.argv) == 1:  # no options passed
    onError(2, 2)
    
for option, argument in myopts:
    if option in ('-l', '--list'):
        actionList = True
    elif option in ('-p', '--print'):
        printQuestion = True
    elif option in ('-n', '--number'):
        limit = int(argument)
    elif option in ('-s', '--search'):
        actionSearch = argument
    elif option in ('-o', '--outfile'):
        outFile = argument
    elif option in ('-a', '--appenddate'):
        appendDate = True
    if option in ('-v', '--verbose'):
        verbose = True
    elif option in ('-h', '--help'):
        usage(0)
        
if not actionList and not actionSearch:
    onError(3, 3,)
    
if actionList and actionSearch:
    onError (5, "More than one action chosen")
        
if printQuestion:
    if not actionList and not actionSearch:
        onError(4, "Option 'print' requires either option 'list' or option 'search' to be set")
    
if actionList and not limit:
    limit = 10
elif actionSearch and not limit:
    limit = 1
    
if actionSearch and limit > 4:
    onError(6, "With option 'search' number of replies can't be larger than 4.\n    You set it to %s" % limit)
        
if outFile and appendDate:
    date = time.strftime("%Y%m%d%H%M%S")
    outFile = "%s-%s" % (outFile, date)
        
if printQuestion:
    if actionList:
        action = "list"
    elif actionSearch:
        action = "search"
    outputQuestion(action, limit, actionSearch, verbose)
elif actionList:
    listNumbers(limit, outFile, verbose)
elif actionSearch:
    lookupNumber(actionSearch, limit, verbose)
    