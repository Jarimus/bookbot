import os
import re

def read_file(path_to_file: str) -> str:
    #read and return contents of the file
    with open(path_to_file) as file:
        contents = file.read()
        return contents

def count_words(path_to_file: str) -> int:
    #read contents
    contents = read_file(path_to_file)
    #count words
    number_of_words = len( contents.split() )
    return number_of_words

def count_characters(path_to_file: str) -> dict:
    #extract contents of the file in lowercase
    contents = read_file(path_to_file).lower()
    characters = {}

    #count the occurences of each alphabet
    for char in contents:
        if char not in "abcdefghijklmnopqrstuvwxyz":
            continue
        if char not in characters:
            characters[char] = 0
        characters[char] += 1
    
    return characters

def report(path_to_file: str) -> None:
    #extract values
    number_of_words = count_words(path_to_file)
    characters = count_characters(path_to_file)
    file_name = re.search(r"/([^/]*)$", path_to_file).group(1)

    #print report
    print(f"*** Report for {file_name} ***")
    print(f"{number_of_words} words in the document.")
    print()
    for char, count in characters.items():
        print(f"The '{char}' was found {count} times.")
    print("*** end of report ***")
    input("Press Enter to continue.")
    print()

def find_text_files():
    files_dict = {}
    files_list = []
    for root, _, files in os.walk(os.path.dirname(__file__)):
        for file in files:
            if file.endswith(".txt"):
                files_dict[file] = root + "/" + file
                files_list.append(file)
    return files_dict, files_list


def analyze_file():
    #retrieve info about the files: filenames and path
    files_dict, files_list = find_text_files()

    while True:
        #print the options for the user
        print("Text files found:")
        for index, file in enumerate(files_list):
            print(f"{index}: {file}")
        choice = input("Which file would you like to analyze? Please enter its number or Q to exit: ")

        #quit if input is Q
        if choice == "Q":
            break

        #try to parse the user input to find the correct file
        try:
            choice_path = files_dict[files_list[int(choice)]]
        except IndexError:
            print()
            print("ERROR: Please input a valid number. Press Enter to continue.")
            input()
            continue
        except ValueError:
            print()
            print("ERROR: Please input a valid number. Press Enter to continue.")
            input()
            continue

        #print the report
        report(choice_path)
    
    print("*** Have a nice day! ***")
    

def main():
    print("*** Welcome to bookbot! ***")
    
    analyze_file()

main()