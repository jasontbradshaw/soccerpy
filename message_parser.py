
def parse(text):
    """
    Here is what amounts to a simple lisp parser for parsing the server's
    returned messages into an intermediate format that's easier to deal
    with than the raw (often poorly formatted) text.
    """
    
    # result acts as a stack that holds the strings grouped by nested parens
    result = []
    
    # the current level of indentation, used to append chars to correct level
    indent = 0
    
    # the non-indenting characters we find. these are kept in a buffer until
    # we indent or dedent, and then are added to the current indent level all
    # at once, for efficiency.
    s = []
    for c in text:
        if c == "(":
            s = []
            # find current level of nesting
            cur = result
            for i in xrange(indent):
                cur = cur[-1]
                
            # add our buffered string onto the previous level
            if len(s) > 0:
                cur.append(''.join(s))
                s = []
            
            # append a new level of nesting to it
            cur.append([])
            
            # increase the indent level so we can get back to this level
            indent += 1
        elif c == ")":
            # append remaining string buffer before dedenting
            if len(s) > 0:
                cur = result
                for i in xrange(indent):
                    cur = cur[-1]
                    
                # append our buffered string to the results
                cur.append(''.join(s))
                s = []
            
            # we finished with one level, so dedent back to the previous one
            indent -= 1
        elif c != " ":
            # append the current string character to the buffer list
            s.append(c)
        elif c == " " and len(s) > 0:
            cur = result
            for i in xrange(indent):
                cur = cur[-1]
                
            # append our buffered string to the results
            cur.append(''.join(s))
            s = []

    return result

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
           from pprint import pprint
           with open("client_recv", 'r') as f:
               for line in f:
                   print line.strip()
                   print
                   pprint(parse(line.strip()))
                   print "----"
                   raw_input()
                   print
    else:
        with open("client_recv", 'r') as f:
            for line in f:
                parse(line.strip())
