from html.parser import HTMLParser
import sys

class MyHTMLParser(HTMLParser): 
    def handle_starttag(self, tag, attrs):
        print(f"Start : {tag}")   
        if len(attrs) > 0:
            for attr in attrs:
                print(f"-> {attr[0]} > {attr[1]}")
            
    def handle_startendtag(self, tag, attrs):
        print(f"Empty : {tag}")
        if len(attrs) > 0:
            for attr in attrs:
                print(f"-> {attr[0]} > {attr[1]}")        

    def handle_endtag(self, tag):
        print(f"End   : {tag}")
            
        
    def handle_data(self, data):
        return

def main():
    parser = MyHTMLParser()
    numlines = input()
    print(f'{numlines}')
    for line in range(int(numlines)):
        line = input()
        parser.feed(line)

if __name__ == "__main__":
    main()