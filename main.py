import os.path as p

def main(path_to_file: str):
    with open(path_to_file) as file:
        contents = file.read()
        print(contents)



path = p.dirname(__file__)
main(path + "/books/frankenstein.txt")