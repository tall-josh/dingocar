import sys, select 
 
def timeout_input(message, sec, default=None): 
    print(f"{message}: --> ") 
    i, o, e = select.select( [sys.stdin], [], [], sec ) 
    if (i): 
        return sys.stdin.readline().strip()
    else: 
        return default
