#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
Created on 29.05.2012
Last modified on 20.01.2012

@author: Adrianus Kleemans
'''

import cgi
import operator
import platform
import cgitb
import time
from datetime import datetime

def num(s):
	return ord(s) - 65

def log(s):
	if debug_mode:
		print s

def val(s):
    # letter values
	values = {'A': 1, 'B': 4, 'C': 4, 'D': 2, 'E': 1, 'F': 4, 'G': 3,
	          'H': 3, 'I': 1, 'J': 10, 'K': 5, 'L': 2, 'M': 4, 'N': 2,
	          'O': 1, 'P': 4, 'Qu': 10, 'R': 1, 'S': 1, 'T': 1, 'U': 2,
	          'V': 5, 'W': 4, 'X': 8, 'Y': 3, 'Z': 10}
	# bonus for letters
	bonus = {9: 20, 8: 15, 7: 10, 6: 6, 5: 3, 4: 0, 3: 0, 2: 0}
	
	# initial
	v = 0
	
	if len(s) == 2:
		v = 1
	else:
		for letter in s:
			v += values[letter]

	v += bonus[len(s)]
	return v

debug_mode = False
cgitb.enable()

print "Content-Type: text/plain;charset=utf-8"
print 

form = cgi.FieldStorage()
grid = form['grid'].value.upper()
print "You entered:", grid

if len(grid) != 16:
    print 'Please enter a grid with 16 letters.'
else:
    print 
    print grid[0:4]
    print grid[4:8]
    print grid[8:12]
    print grid[12:16]
    print
    # load dictionary
    f = open('dict_eng.txt', 'r')
    content = f.read()
    words = [n for n in content.split('\n')]
    words.pop() # remove last empty element
    f.close()

    print "Dictionary:", len(words), 'words loaded.'

    # graph of the 4x4 playing field
    graph = {'0': ['1', '4', '5'],
            '1': ['0', '2', '4', '5', '6'],
            '2': ['1', '3', '5', '6', '7'],
            '3': ['2', '6', '7'],
            '4': ['0', '1', '5', '8', '9'],
            '5': ['0', '1', '2', '4', '6', '8', '9', 'A'],
            '6': ['1', '2', '3', '5', '7', '9', 'A', 'B'],
            '7': ['2', '3', '6', 'A', 'B'],
            '8': ['4', '5', '9', 'C', 'D'],
            '9': ['4', '5', '6', '8', 'A', 'C', 'D', 'E'],
            'A': ['5', '6', '7', '9', 'B', 'D', 'E', 'F'],
            'B': ['6', '7', 'A', 'E', 'F'],
            'C': ['8', '9', 'D'],
            'D': ['8', '9', 'A', 'C', 'E'],
            'E': ['9', 'A', 'B', 'D', 'F'],
            'F': ['A', 'B', 'E'],
            }

    last = 'FEDC9AB76584123'
    rd = '0123456789ABCDEF'
    matches = []
    word_count = 0
    t1 = time.time() # timing
    
    # check if words are possible
    for word in words:
        # speed & correctness
        if len(word) < 2:
            continue
            
        possible = True
        promising = True
        starting_field = '0'
        hist = starting_field
            
        for letter in word:
            if letter not in grid:
                possible = False
           
        while possible:		
            l = len(hist)
            last_number = '0'
            if l > 1:
                last_number = int(hist[l-2:l-1], 16)
            this_number = int(hist[l-1:], 16)
                
            if grid[this_number] == word[l-1] and promising: # letter is correct & promising
                if l == len(word): # if last letter ist correct, word is valid
                    log("> Letter is valid, word found!")
                    matches.append(word)
                    possible = False
                else: # checking if adding new number is valid
                    log("> Letter correct, adding number")
                    this_index = len(graph[rd[this_number]])
                    letter_added = False
                    for i in range(0, this_index):
                        new_number = str(graph[rd[this_number]][i])
                        log("new number: "+new_number)
                        if new_number not in hist: # if field not in use
                            hist += new_number
                            letter_added = True
                            break
                    if not letter_added:
                        possible = False # dead end
            else: # letter not correct
                promising = True
                log("> Letter not correct or not promising")
                if len(hist) == 1: # change starting field
                    start = int(hist, 16)
                    if start == 15: # last possibility reached
                        log("> F reached with no possibilities")
                        possible = False
                    else:
                        hist = rd[int(hist, 16) + 1] # increment starting field
                else: # not starting field
                    # get index
                    line = graph[rd[last_number]]
                    log("> calculating index in "+str(line))
                    index = "lulz"
                    for j in range(0, len(line)):
                        if line[j] == rd[this_number]:
                            index = j
                            log("> index found: " + str(j))
                     
                     
                    last_index = len(graph[rd[last_number]])
                    incremented = False
                    log("> looping from "+ str(index) + " to " + str(last_index))
                    for i in range(index, last_index):
                        log("> possibilities: " + str(graph[rd[last_number]]))
                        new_number = graph[rd[last_number]][i]
                        log("> checking " + new_number + " = " + grid[int(new_number, 16)] + " for adding...")
                        if new_number not in hist: # only if field not already in use
                            log("> adding " + new_number)
                            hist = hist[:len(hist)-1] + new_number
                            incremented = True
                            break
                    if not incremented: # else go back one step
                        log("> not incremented, go back one step")
                        if last[:len(word)-1] == hist: # check if last possibility
                            log("> breaking, last possibility: " + hist)
                            possible = False
                        else:
                            hist = hist[:l-1]
                            promising = False
    
    # calculate most valuable matches
    matches_count = len(matches)
    l = dict(zip(matches, [val(n) for n in matches]))

    # get a sorted instance of dict (list of tuples)
    l = sorted(l.iteritems(), key = operator.itemgetter(1), reverse=True)
    
    calc_time = round(time.time()-t1, 3)
    f = open('log.txt', 'ab')
    f.write(grid + ', ' + str(datetime.now()) + ', ' + str(calc_time) + '\n')
    f.close()

    # Output
    print 'Calculation took', calc_time, 'seconds'
    print "\n", matches_count, "results found: "

    for i in l:
        print i[0], "-", i[1], "points"
