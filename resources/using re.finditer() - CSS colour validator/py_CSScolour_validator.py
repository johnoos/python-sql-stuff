import re

def main():
    pattern = r'#([A-Fa-f0-9]{3}|[A-Fa-f0-9]{6})\b'
    numlines = input()
    for i in range(int(numlines)):
        line = input()
        if ':' in line:
            for matchstring in re.finditer(pattern, line):
                print(f'#{matchstring.group(1)}')   
    
if __name__ == '__main__':
    main()