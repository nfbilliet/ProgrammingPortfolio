"""
--- Day 1: Trebuchet?! ---

--Part 1--
Something is wrong with global snow production, and you've been selected to take a look. 
The Elves have even given you a map; on it, they've used stars to mark the top fifty locations that are likely to be having problems.
You've been doing this long enough to know that to restore snow operations, you need to check all fifty stars by December 25th.
Collect stars by solving puzzles. Two puzzles will be made available on each day in the Advent calendar; the second puzzle is unlocked when you complete the first. Each puzzle grants one star. Good luck!
You try to ask why they can't just use a weather machine ("not powerful enough") and where they're even sending you ("the sky") and why your map looks mostly blank ("you sure ask a lot of questions") 
and hang on did you just say the sky ("of course, where do you think snow comes from") when you realize that the Elves are already loading you 
into a trebuchet ("please hold still, we need to strap you in"). As they're making the final adjustments, they discover that their calibration 
document (your puzzle input) has been amended by a very young Elf who was apparently just excited to show off her art skills. 
Consequently, the Elves are having trouble reading the values on the document. The newly-improved calibration document consists of lines of text; 
each line originally contained a specific calibration value that the Elves now need to recover. On each line, the calibration value can be found 
by combining the first digit and the last digit (in that order) to form a single two-digit number.

For example:

1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet

In this example, the calibration values of these four lines are 12, 38, 15, and 77. Adding these together produces 142.

Consider your entire calibration document. What is the sum of all of the calibration values?

--Part 2--
Your calculation isn't quite right. It looks like some of the digits are actually spelled out with letters: 
one, two, three, four, five, six, seven, eight, and nine also count as valid "digits".

Equipped with this new information, you now need to find the real first and last digit on each line. 
For example:

two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen

eightwo == eighttwo

In this example, the calibration values are 29, 83, 13, 24, 42, 14, and 76. Adding these together produces 281.

What is the sum of all of the calibration values?

****TO DO****

1) Turn all numbers that are represented as words into number integers (No capital letters included)
    e.g. 'one' substring needs to be converted to '1'
2) Filter out any non-integer string character from the string
    e.g. 'one2aaa3' -> '12aaa3' -> '123'
3) If the string of numbers contains more than 2 numbers only the first and last should be saved
    e.g. 'one2aaa3' -> '12aaa3' -> '123' -> '13'
4) Convert the string integers to actual integers
    e.g. 'one2aaa3' -> '12aaa3' -> '123' -> '13' -> 13
5) Return the sum of all integers
"""
import re


keys = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
values = ['1ne', '2wo', '3hree', '4our', '5ive', '6ix', '7even', 'e8ght', 'n9ne']
words_to_nmbs = dict(zip(keys, values))

def calculate_calibration(fname, debug=False):
    "The calibration data is contained within a txt file"
    with open(fname, 'r') as myFile:
        "Read the individual lines and split the data on a line basis"
        input_data = myFile.read().splitlines() 

    """
    Use a regular expresion to filter out any non-integer character from the lines
        - re.sub(pattern, sub, string) -> replace the pattern with the sub in the given string
        - We wish to substitute any the word for the numbers with the actual integers
            * we compile the dictionary keys to a Pattern object where we seperate the keys with '|' to indicate different possible subpatterns (logical OR)
            * We use the anonymous function to use the Match object obtained from the sub function to utilize as the dict key value 
            * The matched substring can be obtained from the match object using the group functionality which groups all the matched characters
    We use a list expression to maintain the individual numbers seperately

    The sub function does not allow overlapping sequences to be taken into account. We repeat the substitution to capture any words that were not converted to numbers
    """
    pattern = re.compile('|'.join(keys))
    words_to_nmbs_fp_data = [re.sub(pattern, lambda x: words_to_nmbs[x.group()], line) for line in input_data]
    words_to_nmbs_sp_data = [re.sub(pattern, lambda x: words_to_nmbs[x.group()], line) for line in words_to_nmbs_fp_data]
    """
    Use a regular expresion to filter out any non-integer character from the lines
        - re.sub(pattern, sub, string) -> replace the pattern with the sub in the given string
        - We wish to substitute any non-integer which we can specify with '[^0-9]' as our pattern
            * [1-9] signifies any character within the set of 0-9
            * adding the ^ in front of the first character of the array denotes that we wish to target any character that is not included in this set
            * "" denotes substitution with an empty character
    We use a list expression to maintain the individual numbers seperately
    """
    filtered_data = [re.sub("[^0-9]", "", line) for line in words_to_nmbs_sp_data]

    """
    If a number consists of more then 2 numbers the first and last numbers should be kept
        - join is used instead of '+' operator due to the increase in efficiency
    """
    length_adj_data = ["".join([str_nmb[0],str_nmb[-1]]) for str_nmb in filtered_data] 
    #print(length_adj_data)
    "Convert the string representation of the numbers to actual integers"
    integer_data = [int(str_nmb) for str_nmb in length_adj_data]

    if debug:
        print(input_data)
        print(words_to_nmbs_sp_data)
        print(filtered_data)
        print(integer_data)
    return(sum(integer_data))

#print(calculate_calibration('test_input_p1.txt'))
#print(calculate_calibration('test_input_p2.txt'))
print(calculate_calibration('puzzle_input.txt'))
#print(calculate_calibration("debug.txt", debug=True))
