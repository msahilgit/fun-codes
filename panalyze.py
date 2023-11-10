#!/home/msahil/anaconda3/bin/python

try:
    import sys
    import getopt
    import math
    import numpy as np
    from termcolor import colored
except:
    print('Required libraries not found::')
    print('Basic python libraries required:::::')
    print('       sys, getopt, math, numpy, termcolor, copy')
    exit()

arguments=sys.argv[1:]

try:
    args,vals=getopt.getopt(arguments,'q:p:')
except getopt.error as err:
    print(str(err))
    print(colored('        ERROR','red',attrs=['bold']))
    sys.exit(2)

err_out=False

for arg,val in args:
    if arg == '-q':
        inp=val
    elif arg == '-p':
        if (val.upper() in ['TRUE','Y','YES']):
            err_out=True
        elif (val.upper() in ['FALSE','N','NO']):
            err_out=False
        else:
            print('print error requires boolean value')
            print(colored('        ERROR','red',attrs=['bold']))
            exit()

if ('-q' in arguments):
    pass
else:
    print('No input expression provided (-q option)')
    print(colored('        ERROR','red',attrs=['bold']))
    exit()


#-------------------------------------------------------------------------------------------

try:
    ans=eval(inp)
except Exception as err:
    print('Unidentified functions/arguments detected::')
    print(colored('     Use python {math and/or numy} functions','green',attrs=['bold']))
    if ('-p' in arguments):
        if err_out == True:
            print('')
            print(colored(str(err),'red',attrs=['bold']))
    else:
        print(colored('        Use -p to print error','green',attrs=['bold']))
    exit()
print(ans)

#-------------------------------------------------------------------------------------------
#===========================================================================================
