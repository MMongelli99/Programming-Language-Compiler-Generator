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
    #   pattern2,
    #   ...
    # }

    'program':{
        ('val',),
        ('val', 'plus', 'val')
    }, #('program','val')]
    'val':{
        ('number',)
    },
    #'hi': {
    #    ('plus',)
    #}
}

'''
key = node

program (NT)
    |-> val (NT)
    |-> val plus val 
'''
