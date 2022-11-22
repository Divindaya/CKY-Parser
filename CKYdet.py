#########################################################
##  CS 4750 (Fall 2022), Assignment #3                 ##
##   Script File Name: CKYdet.py                       ##
##       Student Name: Divine Badibanga                ##
##         Login Name: Dnbadibanga                     ##
##              MUN #: 201765203                       ##
#########################################################
import sys

## This function implements the CKY algorithm on a given sentence, using a given grammar
##
## args:
## words (String) - sentence
## G (String) - grammar
def CKY(words, G):

    words = words.split()
    n = len(words)
    G = G.split("\n")

    # Create DP table
    P = []
    for i in range(n+1):
        row = []
        for j in range(n+1):
            row.append([])
        P.append(row)

    # Initialize DP table
    for j in range(1, n+1):
        for i in range(j, 0, -1):
            i -= 1
            P[i][j] = []

    # Fill in individual-word parses in table
    for j in range(1, n+1):
        # Apply all possible rules of the form N -> word
        for rule in G:
            if words[j-1] in rule:
                if words[j-1] == rule.split()[2::][0].replace('"', ''):
                    parts = rule.split()
                    last = rule.replace('->', '')
                    P[j-1][j].append(last)
                    # While possible, apply all possible rules of the form
                    # N -> N' to basic word-parses
                    for rule in G:
                        if '"' not in rule and len(rule.split()) == 3:
                            if parts[0] == rule.split()[2::][0] and len(parts[0]) == len(rule.split()[2::][0]):
                                P[j-1][j].append(rule.split()[0] +" ["+last+"]")

    # Fill in remaining cases in table, progressing upwards to the right
    # diagonal fashion from the base-cases diagonal, by running rules in the
    # given grammer G in reverse
    for j in range(2, n+1):
        for i in range(j, 0, -1):
            i -= 2
            if i < 0:
                break
            start = i + 1
            end = j
            # Fill in table entry (i, j) by checking each of the k possibilities
            # for splitting the sentence-fragment defined by markers i through
            # j into two pieces and seeing if you can run a rule in G in reverse
            # wrt the previously-computed parses for those pieces
            for k in range(start, end):
                if len(P[i][k]) != 0 and len(P[k][j]) != 0:
                    for NT_A in P[i][k]: # iterate over each form in P[i][k]
                        for NT_B in P[k][j]: # compare above NT with each form in P[k][j]
                            # apply valid rules of form NT -> NT_A NT_B
                            for rule in G:
                                if '"' not in rule and len(rule.split()) == 4: # only rules of form NT -> NT_A NT_B
                                    if NT_A.split()[0] == rule.split()[2::][0] and NT_B.split()[0] == rule.split()[2::][1]:
                                        parts = rule.split()
                                        last = rule.split()[0] + " ["+NT_A+"]["+NT_B+"]"
                                        P[i][j].append(last) # append previously applied rules
                                        # Apply all possible rules of the form N' -> N''
                                        for rule in G:
                                            if '"' not in rule and len(rule.split()) == 3:
                                                if parts[0] == rule.split()[2::][0]:
                                                    P[i][j].append(rule.split()[0] +" ["+last+"]")
    # print results of parsing
    show(P[0][n])
    
## This function prints the results of running the given sentence
## with the given grammar using the CKY algorithm
def show(s):
    count = 0
    for i in range(0, len(s)):
        # print all parses starting with S
        if s[i][0] == 'S':
            count += 1
            print('   Parse #', count, ': ', s[i])

    # if no parse was printed, there was no valid parse
    if count == 0:
        print('   No valid parse')

# retrieve files
grammar = sys.argv[1]
utterance = sys.argv[2]

# open files
gr = open(grammar, "r")
gr = gr.read()
utt = open(utterance, "r")
utt = utt.read()

# for each sentence in utterance file, call CKY() on it and print results
for i in range(len(utt.split('\n'))):
    if utt.split('\n')[i] != '':
        print('Utterance #', i+1, ':')
        CKY(utt.split('\n')[i], gr)
        print()
