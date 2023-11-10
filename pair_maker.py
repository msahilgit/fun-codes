#!/home/msahil/softwares/anaconda3/bin/python

try:
    import sys
    import os.path
    import getopt
    import numpy as np
    import copy as c
    from termcolor import colored
except:
    print('Required libraries not found::')
    print('Basic python libraries required:::::')
    print('       sys, os, getopt, numpy, termcolor, copy')
    exit()

arguments=sys.argv[1:]
if len(arguments) == 0:
    print('No arguments provided:')
    print(colored('Usage: ','cyan',attrs=['bold']),
            colored('pair_maker -f input.ndx -1 grp1 -2 grp2 -n output-index-name -o output.ndx','yellow',attrs=['bold']))
    print(colored('        ERROR','red',attrs=['bold']))
    exit()


try:
    args,vals=getopt.getopt(arguments,'f:a:b:n:o:r:h')
except getopt.error as err:
    print(str(err))
    print(colored('        ERROR','red',attrs=['bold']))
    print(colored('Usage: ','cyan',attrs=['bold']),
            colored('pair_maker -f input.ndx -a grp1 -b grp2 -n output-index-name -o output.ndx','yellow',attrs=['bold']))
    sys.exit(2)

#defaults
outname='pairwise_indexes'
outfile='sahil.ndx'
#

flags=[]
for arg,val in args:
    flags.append(arg)
    if arg == '-h':
        print('        HELP MESSAGE  ')
        print('This code make a pairwise index file (in gromacs format) to be used as input in \n '+
                'gromacs distance command for calculation of pairwise distance between two index groups: \n '+
                'Usage: \n'+
                '-h : help \n'+
                '-f : input index file \n'+
                '-a and -b are index group numbers/names \n'+
                '-n : output index name \n'+
                '-o : output index file name \n')
        exit()
    elif arg == '-f':
        infile=val
        if os.path.exists(infile):
            continue
        else:
            print('Input index file (-f '+str(infile)+') not found:')
            print(colored('        ERROR','red',attrs=['bold']))
            exit()
    #
    elif arg == '-a':
        namea=val
    elif arg == '-b':
        nameb=val
    elif arg == '-n':
        outname=val
    elif arg == '-o':
        outfile=val
        if os.path.exists(outfile):
            print(colored('WARNING: the output file ('+outfile+') already exist, will be overwritten','red'))


#
if ('-f' not in flags) == True:
    print('input index file (-f option) not provided')
    print(colored('        ERROR','red',attrs=['bold']))
    exit()
else:
    if infile[-4:] != '.ndx':
        print(colored('WARNING: Is it index file (not .ndx extension)','red'))
    inp = {}
    for line in open(infile,'r'):
        items = line.strip().split()
        if len(items) == 0:
            raise IndexError('Empty lines in index file:: \n should not be there')
        if items[0] == '[':
            nn = ''
            for k in items[1:-1]:
                nn = nn + k
            inp[nn] = []
        else:
            try:
                for k in items:
                    inp[nn].append(k)
            except:
                raise ValueError('Cannot read input index file: \n'+
                        'Please check your input index file')

no_name = False
keys = inp.keys()
for i in ['-a','-b']:
    if (i not in flags) == True:
        no_name = True
    else:
        nn = eval('name'+str(i[1]))
        if nn.isdigit() == True:
            nn = list(keys)[int(nn)]
        if (nn not in inp.keys()) == False:
            globals()[f"index{i[1]}"] = inp[nn]
            print('Index ('+nn+') successfully read from input index file')
        else:
            print('index name ('+nn+') not found in input index file ('+infile+')')
            no_name=True
if no_name == True:
    print('Index names not provided (-a and -b options): Two index name/numbers need to  be provided')
    print('    OR Wrong names are provided: ')
    print('Below names were read from input index file: ')
    for i in enumerate(keys):
        print('         ',i)
    print(colored('        ERROR','red',attrs=['bold']))
    exit()
if namea == nameb:
    print(colored('WARNING: Same index groups are provided: ARE YOU SURE?? ','red'))

pairind = np.array([[i,j] for i in indexa for j in indexb])

output = open(outfile,'w')
output.write('[ '+outname+' ]\n')
for i in pairind:
    output.write(i[0]+' '+i[1]+'\n')
output.close()

print('Pairwise indexes ('+outname+') were successsfully written to output index file ('+outfile+')')
