""" keywords regex sorting lambda """
import io
import re

def decode_message(file_path):
    """ keywords match() re.match() """
    pattern = r'\[ID: ([0-9]+)\] ([A-Za-z0-9]+)'
    tuples_list = []

    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            match = re.match(pattern, line)
            if match:
                tuples_list.append((match.group(1), match.group(2)))
    
    # sort the tuples
    tuples_list.sort(key=lambda x: x[0], reverse=True)

    # extract a list of only the words
    words = [x[1] for x in tuples_list]
    
    # insert '-' between pairs of entries
    final_string = "-".join(words)

    print(final_string)

decode_message('mytextfile.txt')    
