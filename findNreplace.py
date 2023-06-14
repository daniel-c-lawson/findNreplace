import os; import sys; import io
import string
import re
from project3 import *
from re import Match, sub
from main import characters, simple, mathematical, complicated
from functools import partial

configuration = {}

def matchStr(match):
    return " | ".join(match.groups())

def wrap(start, string, end = None, spacing = 0):
    if not end: end = start
    return f"{start}{' '*spacing}{string}{' '*spacing}{end}"

class Lines:
    def __init__(self, lines, blocks = []):
        self.lines = lines
        self.index = 0
        self.blocks = blocks

    def __iter__(self):
        return self
    def __next__(self):
        try: toReturn = self.lines[self.index]
        except: raise(StopIteration)
        self.index += 1
        return toReturn

    def lookahead(self, n):
        if self.index >= len(self.lines): return None
        return self.lines[self.index: self.index + n]
    def __str__(self):
        return str(self.lines[:self.index], self.lines[self.index:])
    def __repr__(self):
        toReturn = self.__str__() + '\n'
        toReturn += f"index = {self.index}"
        return toReturn

class Block:
    def unformatted(self, string, wrap = None):
        if wrap: return str(wrap) + string + str(wrap)
        return string

    def mathematical(self, string, wrap = None):
        if not wrap: wrap = ""
        for key, symbol in simple.items():
            string = string.replace(key, symbol)

        for key, char in characters.items():
            if key in ["sum"]: continue;
            string = string.replace("\\" + key, char)

        for key, item in mathematical.items():
            string = re.sub(key, str(wrap) + item + str(wrap), string)

        return string

    def formatted(self, string):
        for key, symbol in simple.items():
            string = string.replace(key, symbol)
        for key, char in characters.items():
            string = string.replace("\\" + key, char)
        if configuration['complex']:
            for key, symbol in complicated.items():
                string = string.replace(key, symbol)

        ## TODO: attempt inline splitting(?)

        return string

    def graphing(self, string):

        """ Non-functional Requirements
        make sure that nested brackets are ignored
        indicate wrapper, then wrap every node in that
        indicate arrow type
        indicate 'BST', then give bunch of lists, interpret as a BST.
            - [root][A][B][A1][A2][B1] --> BST
        indicate 'B-tree' or something, then give an inline group of lists.
            - Indicate 'end of children for this node', start taking in other children
            - [root][A, B][A1, A2, A3][B1]
            - or [ [[1] 2 [3]] 4 [[5] 6 [7]] ]  for a B-tree with root [4] and children [2] and [6]
        indicate 'flowchart', then give a bunch of lists, interpret as a flowchart
            - Should be able to make this easily:
                    A
            B               C
            B-2             C-2
                            C-3
            - maybe enable any node in a B-tree to 'flow down' a few levels




        #################### more recent notes:
        if
        until read ";;":
            {start}name{end} -> idN{start}{name{end}
            # "[[A]]" -> "id1[[A]]"

        after ";;":
        split each line along "---" or "-->" or smth:
            "A-->B" -> "id1-->id2 %%{A-->B}%%"
        """
        return string
    def getfuncs(self):
        return {
            'code': self.unformatted,
            'math': self.mathematical,
            'mermaid': self.graphing,
            'normal': self.formatted
        }

    def __str__(self):
        return self.handler.__name__
    def __repr__(self):
        toReturn = f"start = [{self.start}]\tstop = [{self.stop}]\n"
        toReturn += f"handler = {self.handler.__name__}"
        return toReturn

    def __init__(self, start, stop, handler):
        self.start = re.compile(start)
        self.stop = re.compile(stop)
        self.handler = self.getfuncs()[handler]
        self.handler_name = handler

class Node:
    def __init__(self, value, children = []):
        self.value = value
        self.children = children

    def __repr__(self):
        return f"[{self.value}] -> {[node.value for node in self.children]}"


def clean(text):
    text = text.replace("ウ", "\\")
    myList = [m.start() for m in re.finditer("\$\$", text)]
    toRemove = []
    for item in myList:
        if text[item + 2] != '\n':
            toRemove.append(item)
    if len(toRemove) == 0:
        toReturn = text
    else:
        toReturn = ""
        if len(toRemove) == 1:
            return text[0:toRemove[0]] + text[toRemove[0]+2:]
        for i in range(len(toRemove)):
            if i == 0:
                toReturn += text[:toRemove[i]];
                continue
            toReturn += text[toRemove[i-1] +2: toRemove[i]]
        toReturn += text[toRemove[-1]+2:]

    if toReturn[0] == '~' and toReturn[1] == '$':
        toReturn = toReturn[1:]
    if toReturn[-1] == '~' and toReturn[-2] == '$':
        toReturn = toReturn[:-1]
    return toReturn




def identical(f, g): # TODO: replace with {whether the file has changed}
    filePos = (f.tell(), g.tell())
    f.seek(0,0); g.seek(0,0)
    toReturn = (f.read()) == (g.read())
    f.seek(filePos[0]); g.seek(filePos[1])
    return toReturn


def charToLine(file, char): # IIRC: given a character count from checkFreq, returns the line number
    filePos = file.tell()
    file.seek(0,0)
    toReturn = 0
    index = 0; i = 0
    while(1):
        if i == char:break

        charIn = file.read(1)
        while(charIn == ' '):
            charIn = file.read(1)

        if charIn == '\n': toReturn += 1; index = -1;
        index += 1
        i += 1
    file.seek(filePos, 0)
    return (toReturn, index)

def checkFreq(file, matches = ['`', '\\'], threshold = 6, span = 7, debug: bool = False):
    filePos = file.tell()
    file.seek(0, 0)
    string = [' ']*span
    i = 0
    while(1):
        char = file.read(1)
        if (char == ' '): continue
        if not char: break
        else: string[i%span] = char
        i += 1
        for match in matches:
            if ( sum(char == match for char in string)>= threshold ):
                return (match, i)
    # print(string)
    # for match in matches:
    #     print(f"number of {{{match}}}: {sum( (item == match) for item in string)}")

    file.seek(filePos, 0)
    return False


def findNreplace(input: string, config_input) -> None:
    global configuration; configuration = config_input
    # print("findNreplace: configuration = ", configuration)
    debug = configuration['debug']
    output = f"output-{ (input.split('/')[-1]).split('.')[0] }.txt"
    f = open(input, "r"); g = open(output, "w+");

    replacer = Block('', '', 'normal').formatted
    lines = Lines(f.readlines())
    lines.blocks = [
        Block("[ -]*```mermaid\n", "[ -]*```.*?\n", 'mermaid'),
        Block("[ -]*```.*?\n", "[ -]*```.*?\n", 'code'),
        Block("[ -]*<", "[ -]*>\n", 'code'),
        Block("\$\$\n", '\$\$\n', 'math'),
    ]
    for line in lines:
        for block in lines.blocks:
            if block.start.match(line):
                g.write(line)
                line = lines.__next__()
                while not block.stop.match(line):
                    g.write(block.handler(line))
                    # print(f"\t{block}: {block.handler(line.strip())}")
                    try: line = lines.__next__()
                    except: break
                g.write(line)
                try: line = lines.__next__()
                except:
                    f.close(); g.close();
                    if not debug: os.rename(output, input)
                    return
                break
        line = line.split('`');
        lineItems = line.__iter__()
        for item in lineItems: # distinguish between items within and outside of the set
            g.write(replacer(item))
            try: item = lineItems.__next__(); # .__next__() returns an exception for ends
            except: break;
            g.write(f"`{item}`")
    # freq = checkFreq(g)
    freq = False
    if(freq):
        print(f"ERROR: output for {(input.split('/')[-1])} has too many '{freq[0]}' characters at position {charToLine(g, freq[1])}")
    if not(freq or debug) and identical(f, g):
        print("\t   no change!")
        f.close(); g.close();
        print(f"\t   removing {output}")
        os.remove(output);
        return

    f.close(); g.close();
    if not (freq or debug): os.rename(output, input)


"""
get within triple-ticks: "(^```.*\n)([\w].*\n)(^```.*$)"gm

get stuff inside ticks: (`[^`]*`)
???: ^(?=(.*`){2,})((?P<good>[\w\s]*)(\`.*?\`))*
"""