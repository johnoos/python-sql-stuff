def distance(pat1, pat2):
    counter = 0 
    if len(pat1) != len(pat2):
        raise ValueError("Strands must be of equal length.")
    for index in range(len(pat1)):
        # alternatively, for _ in enumerate(len(pat1))
        if pat1[index] == pat2[index]: 
            if len(pat1[i]) == 0:
                return 0 
        else:
            counter += 1
    return counter        