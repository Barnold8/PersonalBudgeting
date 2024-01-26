import json
import sys
import re
from datetime import datetime

def help():

    help_data = {

        "-v/-V" : "This flag shows all of the values in the file loaded, if you include a name from the file after this flag, it will only print the contents associated with said name. -v is for basic data printing and -V is a prettified version",
        "-t" : "This flag requires a name and then a number value, this adds money owed to the user account",
        "-e" : "This flag requires a name and then a number value, this removes money owed to the user account",
        "-n" : "This prints all the usernames associated with the file",
        "-a" : "This flag requires a name, a number and optionally a note. This creates a new user with a starting total owed, and additionally a note to go with the initialisation.",
        "-h" : "This is the flag to garner help"
    }
    print("\n\n")
    for key,value in help_data.items():
        print(key,value,"\n")

    pass

def parseFileName(inp: str) -> str:
    return inp if "." in inp else f"{inp}.json"

def dumpFile(data : dict, fname: str) -> None:

    with open(parseFileName(sys.argv[1]), "w") as json_file:
        json.dump(data, json_file, indent=2) 

def parseNumber(inp: str) -> float:

    pattern = r"[-+]?\d*\.?\d+"

    matches = re.findall(pattern, inp)

    if len(matches) > 1:
        left = matches[0]
        matches.remove(matches[0])
        right =  "".join(num for num in matches)[:2]
        return float(left + "." + right)
    else:
        return float(matches[0]) if len(matches) != 0 else 0.0

def loadFile(fname: str):

    payload = None

    try:
        with open(parseFileName(fname),"r") as jsonFile:
                payload = json.load(jsonFile) 

    except FileNotFoundError as ferror:
        print(f"Error in 'loadFile' function: {ferror}")
        exit()

    return payload

def printUser(name: str, data: dict) -> None:

    try:

        print(f"Name: {name}")

        print(f"{data[name]['Category']}: {name}\n\nTotal owed: {data[name]['Total owed']}\n")
        print("LOGS:")

        for log in data[name]["Payment logs"]:
            print(f"\t{log}")
        
        print("\n")

    except KeyError:
        print(f"Error: Trouble finding {name} in the file. Ensure they are there.")


def main():

    data = None

    if(len(sys.argv) < 2):
        data = loadFile(input("No file was passed into the program, please enter the file name/path here:\t"))
    else:
        data = loadFile(sys.argv[1])

    if data != None and len(sys.argv) > 2:

        if(sys.argv[2][0] != "-"):
            print("Error: a dash is needed to determine the flag state of the program here. For example, -v is used to show a specific users data")
            exit()

        match sys.argv[2]:
            case "-v":
                
                if len(sys.argv) > 3:

                    try:
                        print(data[sys.argv[3]])

                    except KeyError:
                        print(f"Error: Trouble finding {sys.argv[3]} in the file. Ensure they are there.")

                else:
                    for package in data:
                        print(f"Name: {package}")
                        print(data[package])
            case "-V":

                if len(sys.argv) > 3:

                    try:
                        printUser(sys.argv[3],data)
                    except KeyError:
                        print(f"Error: Trouble finding {sys.argv[3]} in the file. Ensure they are there.")

                else:
                    for package in data:
                        printUser(package,data)
                    pass
                

            case "-t":
                try:
                    data[sys.argv[3]]['Total owed'] -= parseNumber(sys.argv[4])
                    logs = data[sys.argv[3]]["Payment logs"]    
                    date = datetime.today().strftime('%Y-%m-%d')
                    date = date.replace("-","/")

                    if len(sys.argv) == 6:
                        logs.append(f"{date} - Money taken: {sys.argv[5]}")
                    else:
                        logs.append(f"{date} - Money taken: No additional note")

                    dumpFile(data,sys.argv[1])

                except KeyError:

                    print(f"{sys.argv[3]} is not found within the file given. Ensure they are there.")

            case "-e":

                try:
                    data[sys.argv[3]]['Total owed'] += parseNumber(sys.argv[4])
                    logs = data[sys.argv[3]]["Payment logs"]    
                    date = datetime.today().strftime('%Y-%m-%d')
                    date = date.replace("-","/")

                    if len(sys.argv) == 6:
                        logs.append(f"{date} - Money entered: {sys.argv[5]}")
                    else:
                        logs.append(f"{date} - Money entered: No additional note")

                    dumpFile(data,sys.argv[1])

                except KeyError:

                    print(f"{sys.argv[3]} is not found within the file given. Ensure they are there.")

            case "-h":
                help()

            case "-H":
                help()

            case "-f":
                help()

            case "-F":
                help()

            case "-n":
                for package in data:
                    print(package)

            case "-a":
                
                if sys.argv[3] not in data.keys():
                    owed = parseNumber(sys.argv[4]) if len(sys.argv) > 3 else 0.0
                    date = datetime.today().strftime('%Y-%m-%d')
                    date = date.replace("-","/")
                    additionalNote = (f"{date} - Intialised user {sys.argv[3]} " + sys.argv[5]) if len(sys.argv) > 5 else f"{date} - Intialised user {sys.argv[3]}"
                    data[sys.argv[3]] = {
                        "Payment logs": [additionalNote],
                        "Category": "Person",
                        "Total owed": owed
                    }
                    dumpFile(data,sys.argv[1])
                else:
                    print(f"Error: User {sys.argv[3]} already exists")
                pass

            case _:
                print("Error: Trouble processing command. Maybe flag isnt in list of flags? Maybe user is in the current file")
                pass
    else:
        #TODO: add file creation in the event that no file is found
        pass
main()