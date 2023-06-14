import os; import sys; import io
from findNreplace import *
from string import Template
import re
from functools import partial
from data import *

COUNT = [10]

configuration = {}

def hasExtension(fileName):
    for extension in extensions:
        if fileName[-len(extension):] == extension:
            return True
    return False



def main(args = []):
    def flagMap(map, default = None):
        print("configuration", configuration);
        print("map", map)
        nonlocal flags
        to_return = None
        if isinstance(map, dict):
            print("YESSSS")
        else:
            print("NOOOOO")
        if (not isinstance(map, dict)) and isinstance(map, str): # map is a single character
            return bool(map in flags)
        assert isinstance(map, dict)
        for key in map:
            if key in flags:
                assert not to_return; # can't have multiple flags here
                to_return = map[key];
        if not to_return:
            return default
        return to_return


    def replace(input):
        if configuration['debug']:
            print(f"\tDEBUGGING {input}")
        else:
            print(f"\t{input}")

        try:
            nonlocal dir;
            myDir = dir
        except NameError: myDir = ""
        input = myDir + input

        findNreplace(input, configuration)

    def fakeArgs():
        print("fakeArgs: ", end = "")
        i = 1
        for arg in args:
            try:
                sys.argv[i] = arg
            except:
                sys.argv.append(arg)
            i += 1
    if args: fakeArgs();

    # collect flags
    i = 1; flags = []
    if sys.argv[i][0] == '-':
        flags = sys.argv[i][1:]
        i += 1
    else:
        while len(sys.argv[i]) == 1:
            flags.append(sys.argv[i])
            i+= 1

    configuration['location'] = flagMap({'l': 'local', 'r': 'dbox'}, default='absolute')
    configuration['folder'] = flagMap('f');
    configuration['debug'] = flagMap('d');
    configuration['complex'] = flagMap('c'); # there may have been a reason I removed the 'complicated' dictionary

    if configuration['location'] == 'local':
        if sys.argv[i][0] != '/': sys.argv[i] = '/' + sys.argv[i]
        sys.argv[i] = os.getcwd() + sys.argv[i]
    if configuration['location'] == 'dbox':
        if sys.argv[i][0] != '/': sys.argv[i] = '/' + sys.argv[i]
        sys.argv[i] = '/home/danielmint/Dropbox/Documents/Notes' + sys.argv[i]

    if configuration['folder']:
        dir = sys.argv[i]
        if dir[-1] != '/': dir += '/'
        if not os.access(dir, os.R_OK):
            print(f"ERROR: no such directory '{dir}'")
            return();
        list = [fileName for fileName in os.listdir(dir) if (fileName[0] != '.' and hasExtension(fileName))]
        print(dir)
        for fileName in list:
            # print("\t" + fileName)
            replace(fileName)

    if not configuration['folder']:
        fileName = sys.argv[i]
        if not os.access(fileName, os.R_OK):
            print(f"ERROR: no such file '{fileName}'")
            return();
        replace(fileName)


    print(f"configuration =", configuration)

    if('d' in flags or 'g' in flags):
        input("\nPress Enter to Exit...")


def main2(): # debug function rather than execute function
    # main(["-dl", "input.txt"])
    string = "dasdf fdsa"
    print((re.search( r"(?<=s)d" , string)))


    exit(0)

if __name__ == '__main__':
    # main2()

    if len(sys.argv) == 1:
        print("No input given. Acting on /home/danielmint/Documents/Fall_2022/...")
        main(["f", "/home/danielmint/Documents/Fall_2022/"])
    else:
        main()
    # main(["/home/danielmint/Documents/Fall_2022/CS 450.md"])
    # main(["-dl", "input.txt"])
# | Text              | Normal            | Math              |
# | _asdf_            | <u>asdf</u>       | \underline{asdf}  |
# | *word*            | *word*            | 𝑤𝑜𝑟𝑑               |
# | *word *           | *word*            | *word *           |