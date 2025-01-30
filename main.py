import os, re, string

def read_file(path_to_file: str) -> str:
    #read and return contents of the file
    with open(path_to_file) as file:
        contents = file.read()
        return contents

def find_text_files() -> tuple[list, dict]:
    """Find .txt files in the current directory, and all subdirectories.
    Return a list and a dictionary: list with filenames and dictionary with filenames as keys and file paths as values."""
    files_dict = {}
    files_list = []
    for root, _, files in os.walk(os.path.dirname(__file__)):
        for file in files:
            if file.endswith(".txt"):
                files_dict[file] = root + "/" + file
                files_list.append(file)
    return files_dict, files_list

def count_words(path_to_file: str):
    """Counts the number of words in a string by splitting at whitespaces."""
    #read contents
    contents = read_file(path_to_file)
    #count words
    number_of_words = len( contents.split() )
    print(f"{number_of_words} words in the document.\n")

def words_to_ignore() -> list:
    """Asks the user for words to ignore in the analysis. Includes a set of common words in English."""
    ignored_words = []

    print("Would you like to ignore some common words? (Such as a, an, you, I, ...)\n")
    if input("Type 'y' to ignore the common words or anythine else to include them. ") == "y":
        common_words = ["the", "and", "i", "to", "of", "a", "an", "in", "that", "it", "he", "she", "you", "they", "was", "is",
        "his", "her", "my", "have", "as", "with", "had", "which", "at", "for", "but", "not", "me", "be", "we", "there", "from",
        "this", "upon", "so", "him", "our", "your", "yours", "been", "yes", "no", "on", "were", "are", "by", "would", "out", "up",
        "down", "what", "when", "where", "could", "has", "do", "should", "will", "who", "if", "may", "am", "us", "over", "can", "must",
        "shall", "about", "before", "after", "than", "did", "how", "why", "here", "then", "into", "or", "well", "some", "them", "any",
        "might", "much", "more", "just", "its", "such", "their", "through", "most", "too", "these", "those", "own", "being", "whom",
        "very", "made", "make", ]
        ignored_words.extend(common_words)
        print("Common words added to the ignore list!\n")

    print("Are there any words you'd like to ignore?")
    while True:
        new_word = input("Write a word to ignore or leave blank to continue. ").strip().lower()
        if new_word == "":
            break
        else:
            if new_word in ignored_words:
                print(f"{new_word} is already listed!\n")
            else:
                ignored_words.append(new_word)
                print(f"'{new_word}' added to the ignore list!\n")
    
    return ignored_words


def report_top100_words(path_to_file: str) -> dict:
    #Read the file
    contents = read_file( path_to_file )

    file_name = re.search(r"/([^/]*)$", path_to_file).group(1)

    #Remove punctuation
    contents = contents.translate( contents.maketrans("", "", string.punctuation + "0123456789") )
    #to lower case and split text into words
    words = contents.lower().split()

    #ask the user for words to ignore
    ignored_words = words_to_ignore()    
    
    #count the occurences of each word
    result = {}
    for word in words:
        word.strip()
        if word in ignored_words:
            continue
        elif word not in result:
            result[word] = 1
        else:
            result[word] += 1
    
    #sort the words
    result = sorted( result.items(), key= lambda item: item[1], reverse=True)
    #turn into a dictionary
    result = dict( result )

    #print report
    print(f"""
*** Report for {file_name} ***
    """)

    #report word count
    count_words(path_to_file)

    i = 1
    for word, count in result.items():
        print(f"{i}: {word} ({count} occurences)")
        if i % 10 == 0 and i != 100:
            user_input = input("Press Enter to continue. Type 'f' to finish analysis. ")
            if user_input == "f":
                break
        i += 1
        if i > 100:
            break

    print("*** end of report ***")
    input("Press Enter to continue. ")

def count_characters(path_to_file: str) -> dict:
    """Counts each lower-case alphabet in a file."""
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

def report_alphabet(path_to_file: str) -> None:
    #extract values
    characters = count_characters(path_to_file)
    #sort the dictionary
    characters = dict( sorted( characters.items(), key= lambda item: item[1], reverse=True) )
    file_name = re.search(r"/([^/]*)$", path_to_file).group(1)

    #print report
    print(f"""
*** Report for {file_name} ***
    """)
    count_words(path_to_file)
    lines = 0
    for char, count in characters.items():
        print(f"The '{char}' was found {count} times.")
        lines += 1
        if lines >= 7:
            input("Press Enter to see more. ")
            lines = 0
    print("*** end of report ***")
    input("Press Enter to continue. ")




def analyze_file():
    """First searches the directory and subdirectories for .txt files.
User chooses a file to analyze and type of analysis: alphabet count, word count, or top100 words by occurence."""
    #retrieve info about the files: filenames and path
    files_dict, files_list = find_text_files()

    while True:
        #print the options for the user
        print("Text files found:\n")
        for index, file in enumerate(files_list):
            print(f"\t{index}: {file}")
        print()
        choice = input("Which file would you like to analyze? Please enter its number or 'q' to exit: ")

        #quit if input is q
        if choice == "q":
            break

        #try to parse the user input to find the correct file
        try:
            choice_path = files_dict[files_list[int(choice)]]
        except IndexError:
            input("ERROR: Please input a valid number. Press Enter to continue. ")
            continue
        except ValueError:
            input("ERROR: Please input a valid number. Press Enter to continue. ")
            continue

        #Request type of analysis
        print("""
        Types of analysis:
        1: Occurence of each alphabet
        2: Top100 words in the text
        """)
        analysis_type = input("What kind of analysis would you like to perform? Type 'q' to quit. ")

        #exit on "Q" input
        if analysis_type == "q":
            break

        #Check if the input is correct
        try:
            analysis_type = int( analysis_type.strip() )
        except ValueError:
            input("ERROR: Please input a valid number. Press Enter to continue. ")
            continue

        match analysis_type:
            case 1: report_alphabet(choice_path)
            case 2: report_top100_words(choice_path)
            case _:
                input("ERROR: Please input a valid number. Press Enter to continue. ")
                continue

        #print the report
        
    
    print("""
************************
*** Have a nice day! ***
************************
    """)
    

def main():
    print("""
***************************
*** Welcome to bookbot! ***
***************************
    """)
    
    analyze_file()

main()
