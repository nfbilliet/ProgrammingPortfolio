import re
"""
#Isolate all unique characters that exist in the input file
with open("puzzle_input.txt", "r") as myFile:
    data = myFile.read()
unique_char = set(data)
print(unique_char)
#{'%', '6', '8', '4', '&', '.', '-', '/', '*', '7', '#', '$', '@', '0', '9', '2', '\n', '=', '3', '5', '1', '+'}
#{'%', '-', '/', '*', '#', '$', '@', '=', '+'} are the unique characters that indicate a part
"""

#Read all the lines and store them into a list with all the newline characters removed
with open("puzzle_input.txt", "r") as myFile:
    data = myFile.read().splitlines()
    line_length = len(data[0])
    nmb_lines = len(data)

print(line_length)
print(nmb_lines)

def extract_nmb_idx(fileData):
    """
    Scan the file and locate all the numbers that are present in the file 
    For each of these numbers determine the line number where they occur and the position in the string
    This information will be stored in a tuple with the form (line_nmb, (begin_idx, end_idx+1))

    return 2 lists with the numbers stored in one and the indices in the other
    """
    #Construct a recursive iterator to find all groups of characters that are positive digits
    nmb_iterators = [re.finditer(r'-?\d+', line) for line in data]   
    #Initialize 2 empty lists to store our values
    isolated_nmbs = []
    isolated_nmb_idx = []
    #Initialize a line idx variable that will run parallel to the for loop over each iterator
    line_idx = 0
    for iter in nmb_iterators:
        #Each re-iterator will produce all the matches found in the string
        for match in iter:
            isolated_nmbs.append(int(match.group()))
            #group returns a tuple of the begin_idx and end_idx+1 for a given match in the string
            isolated_nmb_idx.append((line_idx,match.span()))
        line_idx+=1
    return isolated_nmbs, isolated_nmb_idx

#"""
isolated_nmbs, isolated_nmb_idx = extract_nmb_idx(data)
print(isolated_nmbs)
#print(isolated_nmb_idx)
#"""
#Include a '\' before every character because re reserves these characters for defining specific operations
def extract_sign_idx(fileData, signifier_list = ['\%',"\-" '\/', '\*', '\#', '\$', '\@', '\=', '\+']): 
    #Identify all part signifiers and compile them into a list
    #Construct a regular expression pattern from all listed signifiers
    signifier_pattern = re.compile("|".join(signifier_list))
    sign_iterators = [re.finditer("\W", line) for line in data]
    signs= []
    sign_idx = []
    line_idx = 0
    for iter in sign_iterators:
        for match in iter:
            signs.append(match.group())
            sign_idx.append((line_idx, match.start()))
        line_idx+=1
    return signs,sign_idx

signs, sign_idx = extract_sign_idx(data)
print(set(signs))
#print(sign_idx)

def compute_valid_idx(nmb_idx):
    """
    Generate a list of tuples containing index tuples of positions that require a signifier to denote the part
    as valid. Given a line idx, denoted with l_i, and set of str position idx, (s_b, s_e) we need to check the
    following indices for signifier
        * [(l_{i-1}, s_{b-1}) - (l_{i-1}, s_{e+1})]
        * [(l_{i}, s_{b-1}), (l_{i}, s_{e+1})]
        * [(l_{i+1}, s_{b-1}) - (l_{i+1}, s_{e+1})]
            @ where the lowest possible line idx can be 0 and the highest possible line idx can be the number of lines in the input file minus 1
            @ where the lowest possible inline idx can be 0 and where the highest inline index can be the length of the line minus 1 
    """
    #& takes the intersection between two sets of numbers, using this will filter out non-existent idx
    possible_line_idx = list(set(range(0, nmb_lines)) & set([nmb_idx[0]-1, nmb_idx[0], nmb_idx[0]+1]))
    possible_inline_idx = list(set(range(0, line_length)) & set(range(nmb_idx[1][0]-1, nmb_idx[1][1]+1)))
    valid_idx = {(line_idx, inline_idx) for line_idx in possible_line_idx for inline_idx in possible_inline_idx}
    #Generate the set of indices that correspond to the positions the numbers occupy in the text
    nmb_idx_set = {(nmb_idx[0], inline_idx) for inline_idx in range(nmb_idx[1][0], nmb_idx[1][1])} 
    #The difference between the two sets will result in the indices that produce all non redundant signifier idx
    return valid_idx-nmb_idx_set

def valid_nmb_sum(isolated_nmbs, isolated_nmb_idx, sign_idx):
    sum = 0
    for nmb, nmb_idx_range in zip(isolated_nmbs, isolated_nmb_idx):
        valid_idx = compute_valid_idx(nmb_idx_range)
        for valid_idx_pair in valid_idx:
            if valid_idx_pair in sign_idx:
                sum+=nmb
                break #Add number only once to the sum and avoid multiple additions due to multiple valid_idx_pairs
    return sum

print(valid_nmb_sum(isolated_nmbs, isolated_nmb_idx, sign_idx))

#480856
#480856
#593335
#597015