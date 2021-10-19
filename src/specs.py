# Note: dicts overwrite duplicate keys so it wont matter if you write one twice

tokens = {
    # pattern:  token
    r' ':       None, # whitespace
    r'\n':      None, # newline
    r'#.*':     None, # comment
    r'[0-9]+':  'number',
    r'\+':      'plus',
    r'\-':      'minus'
}

rules = {
    # rule: {
    #   pattern1,
    # pattern2,
    # ...
    # }

    # Note: define a rule with no patterns, jsut to see what gets messed up
    'program':{
        ('val',): '%(val)s;',
        ('val', 'plus', 'val'): 
            '''%(val)s %(plus)s %(val)s;'''
    }, #('program','val')]
    'val':{
        ('number',): 
            '''%(number)s'''
    },
    'disjoint rule': {
        ('plus',)
    }
}

'''
key = node

program (NT)
    |-> val (NT)
    |-> val plus val 
'''
