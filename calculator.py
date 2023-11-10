#!/home/msahil/softwares/anaconda3/bin/python
#
try:
    import sys
    import math
    import numpy as np
    from termcolor import colored
    import copy
except:
    print('Required libraries not found::')
    print('Basic python libraries required:::::')
    print('       sys, math, numpy, termcolor, copy')
    exit()

arguments=sys.argv[2:]

def not_string(x):
    try:
        values=float(x)
        ans=True
    except ValueError:
        ans=False
    return ans


what=sys.argv[1]
what=what.upper()

if what != 'EXPR':
    data=[]
    for i in arguments:
        if not_string(i) == True:
            data.append(float(i))
        else:
            print('Non integer data points')
            exit()
    if np.isnan(np.sum(data))==True:
        print('Undefined values found')
        exit()
else:
    data=copy.deepcopy(arguments)




#===========================================================================================
#-------------------------------------------------------------------------------------------
if what == 'MEAN':
    print(np.mean(data))
#-------------------------------------------------------------------------------------------
elif what == 'AVERAGE':
    print(np.mean(data))
#-------------------------------------------------------------------------------------------
elif what == 'SUM':
    print(np.sum(data))
#-------------------------------------------------------------------------------------------
elif what == 'ADD':
    print(np.sum(data))
#-------------------------------------------------------------------------------------------
elif what == 'TOTAL':
    print(np.sum(data))
#-------------------------------------------------------------------------------------------
elif what == 'DIFFERENCE':
    if len(data) != 2 :
        print('Requires 2 values::')
        exit()
    else:
        print(data[0]-data[1])
#-------------------------------------------------------------------------------------------
elif what == 'PERCENTAGE':
    if len(data) != 2 :
        print('Requires 2 values::')
        exit()
    else:
        print((data[0]/data[1])*100)
#-------------------------------------------------------------------------------------------
elif what == 'MULTIPLY':
    if len(data) != 2 :
        print('Requires 2 values::')
        exit()
    else:
        print(data[0]*data[1])
#-------------------------------------------------------------------------------------------
elif what == 'DIVIDE':
    if len(data) != 2 :
        print('Requires 2 values::')
        exit()
    else:
        print(data[0]/data[1])
#-------------------------------------------------------------------------------------------
elif what == 'PRODUCTALL':
    print(math.prod(data))
#-------------------------------------------------------------------------------------------
elif what == 'POWER':
    if len(data) != 2 :
        print('Requires 2 values::')
        exit()
    else:
        print(data[0]**data[1])
#-------------------------------------------------------------------------------------------
elif what == 'LOG':
    print(list(np.log(data)))
#-------------------------------------------------------------------------------------------
elif what == 'LOGE':
    print(list(np.log(data)))
#-------------------------------------------------------------------------------------------
elif what == 'ANTI-LOG':
    print(list(np.exp(data)))
#-------------------------------------------------------------------------------------------
elif what == 'ANTI-LOGE':
    print(list(np.exp(data)))
#-------------------------------------------------------------------------------------------
elif what == 'LOG10':
    print(list(np.log10(data)))
#-------------------------------------------------------------------------------------------
elif what == 'ANTI-LOG10':
    print(list(np.power(10,data)))
#-------------------------------------------------------------------------------------------
elif what == 'LOG2':
    print(list(np.log2(data)))
#-------------------------------------------------------------------------------------------
elif what == 'ANTI-LOG2':
    print(list(np.power(2,data)))
#-------------------------------------------------------------------------------------------
elif what == 'COMBINATION':
    if len(data) != 2 :
        print('Requires 2 values::')
        exit()
    else:
        try:
            val1=int(data[0])
            val2=int(data[1])
        except ValueError:
            print('Requires integer input')
            exit()
        print(math.comb(val1,val2))
#-------------------------------------------------------------------------------------------
elif what == 'PERMUTATION':
    if len(data) != 2 :
        print('Requires 2 integers::')
        exit()
    else:
        try:
            val1=int(data[0])
            val2=int(data[1])
        except ValueError:
            print('Requires integer input')
            exit()
        print('NOTE: without repetition and with order')
        print(math.perm(val1,val2))
#-------------------------------------------------------------------------------------------
elif what == 'FACTORIAL':
    if len(data) != 1 :
        print('Requires 1 integer::')
        exit()
    else:
        try:
            val1=int(data[0])
        except ValueError:
            print('Requires integer input')
            exit()
        print(math.factorial(val1))
#-------------------------------------------------------------------------------------------
elif what == 'REMAINDER':
    if len(data) != 2 :
        print('Requires 2 values::')
        exit()
    else:
        print(math.fmod(data[0],data[1]))
#-------------------------------------------------------------------------------------------
elif what == 'HSD':
    if len(data) != 2 :
        print('Requires 2 integers::')
        exit()
    else:
        try:
            val1=int(data[0])
            val2=int(data[1])
        except ValueError:
            print('Requires integer input')
            exit()
        print(math.gcd(val1,val2))
#-------------------------------------------------------------------------------------------
elif what == 'EXPR':
    def inp(x):
        val=''
        for i in range(len(x)):
            val=val+x[i]
        return val
    try:
        ans=eval(inp(data))
    except:
        print('Unidentified functions detected::')
        print(colored('     Use python {math and/or numy} functions','green',attrs=['bold']))
        exit()
    print(ans)
#-------------------------------------------------------------------------------------------
else:
    print('Unknown:  ',what)
