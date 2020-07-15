import json

class Textbook:
    
    def __init__(self, sub, code, link, desc="No description"):
        self.dict = {
            "subject": sub,
            "code": code,
            "link": link,
            "description": desc
        }

def add_book(textbook):

    data = json.dumps(textbook, default=lambda x: x.__dict__)

    with open('textbooks.txt', 'a+') as outfile:
        json.dump(textbook.dict, outfile, indent=4)


    

def get_book(sub, code):

    with open('textbooks.txt', 'r') as textbooks:
        data = json.load(textbooks)

        print(type(data))
    return 1


testbook = Textbook("test", 123, ".com")
dogbook = Textbook("dog", 321, "woof")

#get_book("dog", "dog")

add_book(testbook)
add_book(dogbook)