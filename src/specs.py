# Note: dicts overwrite duplicate keys so it wont matter if you write one twice
# Should duplicate token names be allowed?
tokens = {
    # pattern:  token
    r' ':       None, # whitespace
    r'\n':      None, # newline
    r'#.*':     None, # comment
    r'[0-9]+':  'number',
    r'\+':      'plus',
    r'\-':      'minus',
}

rules = {
    # rule: {
    #   pattern1: code,
    #   pattern2: code,
    #   ...
    # }

    # Note: define a rule with no patterns, jsut to see what gets messed up
    'program':{
        ('val',): 
            '''%(val)s;''',
        #('num',): 
        #    '''%(num)s;''',
        ('val', 'plus', 'val'): 
            '''%(val)s %(plus)s %(val)s;'''
    }, #('program','val')]
    'val':{
        ('number',): 
            '''%(number)s'''
    },
    #'num':{
    #    ('number',): 
    #        '''%(number)s'''
    #},
}

'''
key = node

program (NT)
    |-> val (NT)
    |-> val plus val 
'''
