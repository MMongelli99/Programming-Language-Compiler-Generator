import re
from specs import tokens, rules
from dataclasses import dataclass
import warnings

class ScanError(Exception):
    def __init__(self, invalidity: str):
        self.invalidity = invalidity

class SyntaxError(Exception):
    def __init__(self, invalidity: str):
        self.invalidity = invalidity

def get_next_lexeme(error: Exception, tokens: dict, source_code: str) -> (str, str, int, int):
    '''Get longest pattern at start of input string. If no match, raise error.'''

    # Note: we always look for the longest string that matches a token pattern

    # Get all strings that match from start of source code
    matches = [(token, re.match(pattern, source_code)) for pattern, token in tokens.items()]
    matches = [(token, match) for token, match in matches if match!=None] # remove Nones

    if matches:
        token, match = max(matches, key=lambda m: len(m[1].group())) # longest matched string
        return token, match.group(), match.start(), match.end() # return token, lexeme, start idx, end idx
    else:
        # Get soonest occurence of each token in source code
        searches = [re.search(pattern, source_code) for pattern, token in tokens.items()]
        searches = list(filter(None, searches)) # remove Nones
        
        if searches:
            #longest_search = max(searches, key=lambda m: len(m[0])) # longest
            #searches = list(filter(lambda s: len(s.group())==len(longest_search.group()), searches)) # longest
            search = min(searches, key=lambda m: m.start()) # soonest occurence of a token found
            raise error(f"'{source_code[:search.start()]}'")
        else:
            raise error(f"'{source_code}'")

def tokenize(error: Exception, tokens: dict, source_code: str) -> [(str, str),]: 
    '''Breakup input file into lexemes and categoreize by token. Emit error if unrecognizable input is found.'''

    # tokenize (search for scan errors)
    token, lexeme, start, end = '', '', 0, 0
    source_code = source_code[end:]

    lexemes = []
    #offset = len(max(tokens, key=len))+1 # amount of spaces to put when printing tokenization
    while source_code != '':
        token, lexeme, start, end = get_next_lexeme(error, tokens, source_code)
        source_code = source_code[end:] # rest of source code after lexeme
        if token: 
            lexemes.append((token, lexeme))
            # unindent this line to print ignored lexemes as well
            #print(f"{token if token else ''}:{' '*(offset-len(token if token else ''))}'{lexeme}'")

    return lexemes

@dataclass(frozen=True)
class Node:
    name: str # name of rule
    children: tuple = () # each child is a pattern, each pattern is a tuple of nodes corresponding to a grammar rule
    
class UndefinedStartSymbolError(Exception):
    def __init__(self, message: str):
        self.message = message
class NameNotFoundError(Exception):
    def __init__(self, message: str):
        self.message = message

def get_node(curr_symbol: str) -> Node:
    '''Create a node in the parse tree for the given symbol with its pattern(s) as children.'''

    if curr_symbol in rules:
        # RULES ARE NON TERMINAL SYMBOLS
        get_node.used_grammar_rules.append(curr_symbol)

        children = []
        # convert strings to nodes
        for pattern in rules[curr_symbol]:
            child = tuple(get_node(symbol) for symbol in pattern) # pattern is a tuple of nodes
            children.append(child) # each child is a pattern defining the symbol
        children = tuple(children) # put all patterns into a tuple as children of the new node
        
        return Node(curr_symbol, children)
        
    elif curr_symbol in tokens.values():
        # TOKENS ARE TERMINAL SYMBOLS
        return Node(curr_symbol)

    else:
        raise NameNotFoundError(f"Symbol '{curr_symbol}' not defined as a rule or token.")

get_node.used_grammar_rules = []

def warn_unused_rules(error: Exception, rules: dict, lexemes: [(str, str),]):
    '''Recursively descend grammar and contextualize lexemes. Emit error if syntax is violated.'''

    entry_point = 'program'

    if entry_point not in rules: 
        raise UndefinedStartSymbolError(f"The start symbol called '{entry_point}' has not been defined.")

    parse_tree = get_node(entry_point)
    
    unused_grammar_rules = [rule for rule in rules if rule not in get_node.used_grammar_rules]
    if unused_grammar_rules:
        warnings.warn(f"{len(unused_grammar_rules)} unused rules in grammar ({','.join(unused_grammar_rules)})")

    #print(parse_tree)

def main():
    with open('test.txt', 'r') as source_file:

        source_code = source_file.read()

        print(f'INPUT:')
        print(f"'{source_code}'")
        print()

        print('TOKENIZING:')
        lexemes = tokenize(ScanError, tokens, source_code)
        for token, lexeme in lexemes:
            print(f"{token}: '{lexeme}'")
        print()

        print('PARSING:')
        warn_unused_rules(SyntaxError, rules, lexemes)

        print(lexemes)

if __name__=='__main__':
    main()
