#!/home/msahil/anaconda3/bin/python

try:
    import numpy as np
    import scipy.stats as sct
    import sys
    import getopt
    import os.path
    from termcolor import colored
    import copy
    from difflib import get_close_matches
    from tqdm import tqdm
except:
    print('Required libraries not found')
    print('Basic libraries required:  ')
    print('     numpy, scipy, sys, getopt, os, copy, termcolor, tqdm')
    exit()

#=====================================================================================
#=====================================================================================
# f:input_file1, x:column in f, w:operation, c:comments, b:bootstrap value, s:starting point, e:ending point, r:operation over r values
# t:time column (default=0), o:output_file, m:values in output
# p:operation_type1 {{can be different for different subcommands}}
#
# INPUT TYPES:
#	Integer inputs:
#	-x  |	
#	-t  |	
#	-y  |	
#	-m  |	integer 1 (noutput)
#	-r  |	integer 2 (operational_value1)
#	-b  |	integer 3 (operational_value2)
#	Numeric inputs:
#	-s  |	
#	-e  |	
#	-v  |	numeric 1 (value1)
#	-u  |	numeric 2 (value2)
#	String inputs:
#	-p  |	string 1  (operation_type1)
#	-q  |	string 2  (operation_type2)
#	Others:
#	-f  |	
#	-c  |	
#	-o  |	
#	-a  |	
#=====================================================================================
#=====================================================================================
def not_string(x):
    try:
        values=float(x)
        ans=True
    except ValueError:
        ans=False
    return ans
#-------------------------------------------------------------------------------------
def extra_args(given,required): 
    extras=[] 
    for i in given: 
        if (i not in required): 
            extras.append(i) 
    if len(extras) > 0:
        print('The following arguments are not required for the given commands::')
        print('        ',extras)
        print('      ',colored('WILL BE IGNORED','red',attrs=['underline']),'\n')
#-------------------------------------------------------------------------------------
def which_duplicates(x):
    duplicates=[]
    uniques=[]
    if len(x) == len(set(x)):
        return duplicates
    else:
        for i in x:
            if (i not in uniques):
                uniques.append(i)
            else:
                duplicates.append(i)
        return set(duplicates)
#-------------------------------------------------------------------------------------
def zero_divide_error():
    print('Cannot divide by zero..')
    print(colored('        ERROR','red',attrs=['bold']))
    exit()
#=====================================================================================
#========================================================================================
arguments=sys.argv[2:]

if len(arguments) == 0:
    print('No input arguments')
    print(colored('        ERROR','red',attrs=['bold']))
    exit()

#=====================================================================================
#========================================================================================
try:
    args,vals=getopt.getopt(arguments,'f:g:c:x:y:b:t:s:e:v:m:o:a:p:q:r:u:')
except getopt.error as err:
    print(str(err))
    print(colored('        ERROR','red',attrs=['bold']))
    sys.exit(2)

comments=['@','#']
column1=1
column2=2
tc=0
noutput=1
output_status='w'

flags=[]
for arg,val in args:
    flags.append(arg)
    if arg == '-f':
        input_file1=val
        if os.path.exists(input_file1):
            continue
        else:
            print('input_file_1 not found')
            print(colored('        ERROR','red',attrs=['bold']))
            exit()
    elif arg == '-g':
        input_file2=val
        if os.path.exists(input_file2):
            continue
        else:
            print('input_file_2 not found')
            print(colored('        ERROR','red',attrs=['bold']))
            exit()
    elif arg == '-o':
        output_file=val
    elif arg == '-x':
        if val.isdigit() == True :
            column1=int(val)
        else:
            print('option -x requires integer value')
            print(colored('        ERROR','red',attrs=['bold']))
            exit()
    elif arg == '-y':
        if val.isdigit() == True :
            column2=int(val)
        else:
            print('option -y requires integer value')
            print(colored('        ERROR','red',attrs=['bold']))
            exit()
    elif arg == '-c':
        comments=list(val)
    elif arg == '-b':
        if val.isdigit() == True :
            def bootstrap(x):
                means=[]
                for i in range(int(val)):
                    means.append(np.nanmean(np.array([x[j] for j in np.random.randint(len(x),size=len(x))])))
                return means
            operational_value2=int(val)
        else:
            print('option -b requires integer value')
            print(colored('        ERROR','red',attrs=['bold']))
            exit()
    elif arg == '-t':
        if val.isdigit() == True :
            tc=int(val)
        else:
            print('option -t requires integer value')
            print(colored('        ERROR','red',attrs=['bold']))
            exit()
    elif arg == '-s':
        if not_string(val) == True :
            start=float(val)
        else:
            print('Option -s requires numeric value')
            print(colored('        ERROR','red',attrs=['bold']))
            exit()
    elif arg == '-e':
        if not_string(val) == True:
            last=float(val)
        else:
            print('Option -e requires numeric value (default end)')
            print(colored('        ERROR','red',attrs=['bold']))
            exit()
    elif arg == '-v':
        if not_string(val) == True :
            value1=float(val)
        else:
            print('Option -v requires numeric value')
            print(colored('        ERROR','red',attrs=['bold']))
            exit()
    elif arg == '-u':
        if not_string(val) == True :
            value2=float(val)
        else:
            print('Option -u requires numeric value')
            print(colored('        ERROR','red',attrs=['bold']))
            exit()
    elif arg == '-m':
        if val.isdigit() == True:
            noutput=int(val)
        else:
            print('option -m requires integer value')
            print(colored('        ERROR','red',attrs=['bold']))
            exit()
    elif arg == '-a':
        if val.upper()=='YES':
            output_status='a'
        elif val.upper() =='NO':
            output_status='w'
        else:
            print('Unrecognized argument for append.')
            print(colored('    -a yes/no','green',attrs=['bold']))
            print(colored('        ERROR','red',attrs=['bold']))
            exit()
    elif arg == '-p':
        operation_type1=val
    elif arg == '-q':
        operation_type2=val
    elif arg == '-r':
        if val.isdigit() == True:
            operational_value1=int(val)
        else:
            print('option -r requires integer value')
            print(colored('        ERROR','red',attrs=['bold']))
            exit()
           

#========================================================================================
#========================================================================================
duplicates = which_duplicates(flags)
if len(duplicates) > 0:
    for i in duplicates:
        print('Flag provided more than once: ',i)
    print(colored('    Each flag should be provided only once','green',attrs=['bold']))
    print(colored('        ERROR','red',attrs=['bold']))
    exit()
#========================================================================================
#========================================================================================
what=sys.argv[1]
what=what.upper()
if what[0] == '-':
    print('Syntax error::')
    print(colored('    Looks like no command is provided:','green',attrs=['bold']))
    print(' ')
    print(colored('syntax:: statistics command_name -f input_file1 -arguments input_values','cyan',attrs=['bold']))
    print(' ')
    print(colored('        ERROR','red',attrs=['bold']))
    exit()

all_functions=['MIN','MINAT','ROW-MIN','MAX','MAXAT','ROW-MAX','VALUEAT','NEARESTVALUE','MEDIAN','MEAN','WEIGHTED-MEAN','BMEAN','STD','SEM','BSTD','ROW-MEAN','ROW-MEDIAN','NORMALIZE','CORRELATION','BINDING-TIME']

if (what not in all_functions)==True:
    print('Unknown Command:   ',what)
    close_matches=get_close_matches(what,all_functions)
    if len(close_matches) > 0:
        print(colored('    Did you mean any of the following:','green',attrs=['bold']))
        for i in close_matches:
            print('      ',i)
        print('')
    print(colored('        ERROR','red',attrs=['bold']))
    exit()
#========================================================================================
#========================================================================================
if ( '-f' in arguments):
    pass
else:
    print('No input file provided (-f option)')
    print(colored('        ERROR','red',attrs=['bold']))
    exit()

try:
    raw_data1=np.loadtxt(input_file1,comments=comments)
except ValueError:
    print('The input data file could not be read::..!')
    print(colored('    Look for comment lines in file (-c option)','green',attrs=['bold']))
    print(colored('        ERROR','red',attrs=['bold']))
    exit()


if len(raw_data1) == 0:
    print('')
    print(colored('    check the input file','green',attrs=['bold']))
    print('No data in the input file (-f option)')
    print(colored('        ERROR','red',attrs=['bold']))
    exit()


if raw_data1.ndim == 1:
    data1=copy.deepcopy(raw_data1)
    times1=np.array(range(1,len(data1)+1))
    stacked_data1=np.column_stack((times1,data1))
#--------------------------------------------------------------------------
elif raw_data1.ndim == 2:
    if ('-s' in arguments):
        start_index=(np.abs(raw_data1[:,tc]-start)).argmin()
    else:
        start_index=0
    if ('-e' in arguments):
        end_index=(np.abs(raw_data1[:,tc]-last)).argmin() + 1
    else:
        end_index=len(raw_data1)
    raw_data1=raw_data1[start_index:end_index]
    try:
        tried=len(raw_data1[1])
    except:
        print('No data remains in input-file1 after shortlisting')
        print(colored('    check your -s / -e options','green',attrs=['bold']))
        print(colored('        ERROR','red',attrs=['bold']))
        exit()
    #----------------------------------------------------------------------
    times1=raw_data1[:,tc]
    rest_data1=np.delete(raw_data1,tc,axis=1)
    if len(raw_data1[1]) < column1+1 :
        print('Column-index1 out of range')
        print(colored('        ERROR','red',attrs=['bold']))
        exit()
    else:
        data1=raw_data1[:,column1]
    stacked_data1=np.column_stack((times1,data1))
else:
    print('Unreadable data')
    print('    ',colored('This programs works for time series data, i.e., either 1D or 2D','green',attrs=['bold']))



if np.isnan(np.sum(raw_data1)) == True:
    print('Undefined Values in the input-data1')
    print(colored('     Check the input_file1 for NaN values','green',attrs=['bold']))
    print(colored('        This program ignore NaN values','green',attrs=['bold']))
    print(colored('        CAN BE A POSSIBLE ERROR','red',attrs=['blink']))

#========================================================================================
#========================================================================================
if ('-g' in arguments):
    try:
        raw_data2=np.loadtxt(input_file2,comments=comments)
    except:
        print('The input-file2 could not be read::..!')
        print(colored('    Look for comment lines in file (-c option)','green',attrs=['bold']))
        print(colored('        ERROR','red',attrs=['bold']))
        exit()

    if len(raw_data2) == 0:
        print('')
        print(colored('    check the input-file2','green',attrs=['bold']))
        print('No data in the input-file2 (-g option)')
        print(colored('        ERROR','red',attrs=['bold']))
        exit()
        
    if raw_data2.ndim == 1:
        data2=copy.deepcopy(raw_data2)
        times2=np.array(range(1,len(data2)+1))
        stacked_data2=np.column_stack((times2,data2))

    elif raw_data2.ndim == 2:
        if ('-s' in arguments):
            start_index=(np.abs(raw_data2[:,tc]-start)).argmin()
        else:
            start_index=0
        if ('-e' in arguments):
            end_index=(np.abs(raw_data2[:,tc]-last)).argmin() + 1
        else:
            end_index=len(raw_data2)
        raw_data2=raw_data2[start_index:end_index]
        try:
            tried=len(raw_data2[1])
        except:
            print('No data remains in input-file2 after shortlisting')
            print(colored('    check your -s / -e options','green',attrs=['bold']))
            print(colored('        ERROR','red',attrs=['bold']))
            exit()
        #----------------------------------------------------------------------
        times2=raw_data2[:,tc]
        rest_data2=np.delete(raw_data2,tc,axis=1)
        if len(raw_data2[1]) < column2+1 :
            print('Column-index2 out of range')
            print(colored('    Use -y column-number','green',attrs=['bold']))
            print(colored('        ERROR','red',attrs=['bold']))
            exit()
        else:
            data2=raw_data2[:,column2]
        stacked_data2=np.column_stack((times2,data2))
    else:
        print('Unreadable data')
        print('    ',colored('This programs works for time series data, i.e., either 1D or 2D','green',attrs=['bold']))

    if np.isnan(np.sum(raw_data2)) == True:
        print('Undefined Values in the input-data2')
        print(colored('     Check the input_file2 for NaN values','green',attrs=['bold']))
        print(colored('       This program ignore NaN values','green',attrs=['bold']))
        print('        ',colored('CAN BE A POSSIBLE ERROR','red',attrs=['blink']))

    if len(raw_data1) != len(raw_data2):
        print(colored('NOTE: ','cyan',attrs=['bold']),'input-data1 and input-data2 have different lengths of data')
        print('        ',colored('CAN BE A POSSIBLE ERROR','red',attrs=['blink']))
#========================================================================================
#========================================================================================

if ('-o' in arguments):                                  #opening output file in provided status
    if os.path.exists(output_file):
        if ('-a' not in arguments) == True :
            rename_number=0
            while True:
                rename_number=rename_number+1
                new_name='#'+output_file+'.'+str(rename_number)+'#'
                if os.path.exists(new_name):
                    pass
                else:
                    os.rename(output_file,new_name)
                    break
            print('output_file exist::  Renamed to ',new_name)
            print(colored('       Use append (-a option) to append/overwrite','green',attrs=['bold']))
    
    outputfile=open(output_file,output_status)

#========================================================================================
#========================================================================================
#Overall, the following datas are available  to operate on:
#	data1
#	times1
#	rest_data1      | not for 1d data
#	stacked_data1
#	raw_data1
#			Same for data2
#========================================================================================
#========================================================================================
#========================================================================================
if what == 'MIN':

    all_flags=['-f','-x','-c','-t','-s','-e','-y']
    extra_args(flags,all_flags)

    print(what,':   ',np.nanmin(data1))
#========================================================================================
#---------------------------------------------------------------------------------------
#========================================================================================
elif what == 'MINAT':

    all_flags=['-f','-x','-c','-t','-s','-e','-y']
    extra_args(flags,all_flags)

    if raw_data1.ndim < 2:
        print('MINAT operation requires 2-D data')
        print(colored('        ERROR','red',attrs=['bold']))
        exit()
    else:
        print('MIN   ',np.nanmin(data1),'     AT   ',times1[np.where(data1 == np.nanmin(data1))])
#========================================================================================
#---------------------------------------------------------------------------------------
#========================================================================================
elif what == 'ROW-MIN':

    all_flags=['-f','-x','-c','-t','-s','-e','-y','-o','-a']
    extra_args(flags,all_flags)

    if ('-o' in arguments):
        outfile=output_file
    else:
        outfile='sahil.out'
        print('No output file is provided. Output in file: ',outfile)
        print(colored('    Use -o outfile','green',attrs=['bold']))
    if raw_data1.ndim == 1:
        print('The input data has only one column.')
        print(colored('        ERROR','red',attrs=['bold']))
        exit()
    elif raw_data1.ndim == 2:
        if len(raw_data1[1]) == 2:
            out=[]
            for i in range(len(raw_data1)):
                out.append(np.nanmin(raw_data1[i]))
            with open(outfile,'a') as f:
                print('#The input data has only two columns... Using both of them.\n')
                np.savetxt(f,out,fmt='%1.4f')
        elif len(raw_data1[1]) > 2:
            if ('-p' in arguments):
                if operation_type1.upper() == 'ALL-COLS':
                    print('Using all rows:')
                    data_to_use=raw_data1
                elif operation_type1.upper() == 'EXCEPT-REF-COL':
                    data_to_use=rest_data1
                    outs='stacked'
                    print('Using all except ref column')
                else:
                    print('Invalid argument for -p')
                    print(colored('    -p all-cols / except-ref-col','green',attrs=['bold']))
                    exit()
            else:
                data_to_use=rest_data1
                outs='stacked'
            out=[]
            for i in range(len(data_to_use)):
                out.append(np.nanmin(data_to_use[i]))
            if outs == 'stacked':
                out=np.column_stack((times1,out))
            with open(outfile,'a') as f:
                np.savetxt(f,out,fmt='%1.4f')
#========================================================================================
#---------------------------------------------------------------------------------------
#========================================================================================
elif what == 'MAX':

    all_flags=['-f','-x','-c','-t','-s','-e','-y']
    extra_args(flags,all_flags)

    print(what,':   ',np.nanmax(data1))
#========================================================================================
#---------------------------------------------------------------------------------------
#========================================================================================
elif what == 'MAXAT':

    all_flags=['-f','-x','-c','-t','-s','-e','-y']
    extra_args(flags,all_flags)

    if raw_data1.ndim < 2:
        print('MAXAT operation requires 2-D data')
        print(colored('        ERROR','red',attrs=['bold']))
        exit()
    else:
        print('MAX   ',np.nanmax(data1),'     AT   ',times1[np.where(data1 == np.nanmax(data1))])
#========================================================================================
#---------------------------------------------------------------------------------------
#========================================================================================
elif what == 'ROW-MAX':
    if ('-o' in arguments):
        outfile=output_file
    else:
        outfile='sahil.out'
        print('No output file is provided. Output in file: ',outfile)
        print(colored('    Use -o outfile','green',attrs=['bold']))
    if raw_data1.ndim == 1:
        print('The input data has only one column.')
        print(colored('        ERROR','red',attrs=['bold']))
        exit()
    elif raw_data1.ndim == 2:
        if len(raw_data1[1]) == 2:
            out=[]
            for i in range(len(raw_data1)):
                out.append(np.nanmax(raw_data1[i]))
            with open(outfile,'a') as f:
                print('#The input data has only two columns... Using both of them.\n')
                np.savetxt(f,out,fmt='%1.4f')
        elif len(raw_data1[1]) > 2:
            if ('-p' in arguments):
                if operation_type1.upper() == 'ALL-COLS':
                    print('Using all rows:')
                    data_to_use=raw_data1
                elif operation_type1.upper() == 'EXCEPT-REF-COL':
                    data_to_use=rest_data1
                    outs='stacked'
                    print('Using all except ref column')
                else:
                    print('Invalid argument for -p')
                    print(colored('    -p all-cols / except-ref-col','green',attrs=['bold']))
                    exit()
            else:
                data_to_use=rest_data1
                outs='stacked'
            out=[]
            for i in range(len(data_to_use)):
                out.append(np.nanmax(data_to_use[i]))
            if outs == 'stacked':
                out=np.column_stack((times1,out))
            with open(outfile,'a') as f:
                np.savetxt(f,out,fmt='%1.4f')
#========================================================================================
#---------------------------------------------------------------------------------------
#========================================================================================
elif what == 'VALUEAT':

    all_flags=['-f','-x','-c','-t','-s','-e','-y','-v']
    extra_args(flags,all_flags)

    if raw_data1.ndim < 2:
        print('VALUEAT operation requires 2-D data')
        print(colored('        ERROR','red',attrs=['bold']))
        exit()
    else:
        if ( '-v' not in arguments) == True:
            print('Argument value not provided (-v option)')
            print(colored('        ERROR','red',attrs=['bold']))
            exit()
        else:
            pos=np.where(data1 == value1)
            if np.shape(pos)[1] == 0:
                print('No matching results with the given value:   ',value1)
                print(colored('    Look for nearestvalue...!! ','green',attrs=['bold']))
            else:
                print('Value   ',value1,'     AT   ',times1[pos])
#========================================================================================
#---------------------------------------------------------------------------------------
#========================================================================================
elif what == 'NEARESTVALUE':

    all_flags=['-f','-x','-c','-t','-s','-e','-y','-v','-m']
    extra_args(flags,all_flags)

    if ( '-v' not in arguments) == True:
        print('Argument value1 not provided (-v option)')
        print(colored('        ERROR','red',attrs=['bold']))
        exit()
    elif noutput > len(data1):
        print('Required number of outputs are more than data')
        print(colored('        ERROR','red',attrs=['bold']))
        exit()
    else:
        if raw_data1.ndim == 1:
            data_to_use=copy.deepcopy(data1)
            vvs=[]
            for i in range(noutput):
                ind=(np.abs(data_to_use - value1)).argmin()
                vvs.append(data_to_use[ind])
                data_to_use=np.delete(data_to_use,ind)
            print(vvs)
        elif raw_data1.ndim == 2:
            data_to_use=np.column_stack((times1,data1))
            vvs=[]
            for i in range(noutput):
                ind=(np.abs(data_to_use[:,1] - value1)).argmin()
                vvs.append(list(data_to_use[ind]))
                data_to_use=np.delete(data_to_use,ind,axis=0)
            print(vvs)
        else:
            print('The program is for 2-D time series only')
            print(colored('        ERROR','red',attrs=['bold']))
            exit()
#========================================================================================
#---------------------------------------------------------------------------------------
#========================================================================================
elif what == 'MEDIAN':
    if ('-p' not in arguments) == True :
        print(what,':   ',np.nanmedian(data1))
    else:
        if operation_type1.upper() == 'CUMULATIVE':
            def cumulative_median(x):
                av=[]
                av.append(x[0])
                for i in range(1,len(x)):
                    av.append(np.nanmedian(x[:i+1]))
                return av
            out=cumulative_median(data1)
            tout=times1
            final_out=np.column_stack((tout,out))
            cline='#REF-COLUMN  CUMULATIVE-MEDIAN  \n'
        else:
            if ('-r' not in arguments) == True:
                print('Operational value not provided')
                print(colored('     Use -r option','green',attrs=['bold']))
                exit()
            else:
                if operational_value1 > len(data1):
                    print('Operational value is greater than total length of input_data1')
                    print('    ',colored('CAN BE A SOURCE OF ERROR','red',attrs=['underline']))
                if (operation_type1.upper() in ['RUNNING','ROLLING']):
                    def running_median(x,r):
                        av=[]
                        for i in range(0,len(x)-r+1):
                            av.append(np.nanmedian(x[i:i+r-1]))
                        return av
                    out=running_median(data1,operational_value1)
                    tout=times1[operational_value1-1:]
                    final_out=np.column_stack((tout,out))
                    cline='#REF-COLUMN  RUNNING-MEDIAN  \n'
                elif operation_type1.upper() == 'BLOCK':
                    def block_median(x,r,times1):
                        i=0
                        j=r-1
                        av=[]
                        tav=[]
                        while j < len(x):
                            av.append(np.nanmedian(x[i:j]))
                            tav.append([times1[i],times1[j]])
                            i=i+r
                            j=j+r
                        if j-r < len(x):
                            av.append(np.nanmedian(x[i:]))
                            tav.append([times1[i],times1[-1]])
                        return tav, av
                    tout,out=block_average(data1,operational_value1,times1)
                    final_out=np.column_stack((tout,out))
                    cline='#FROM  TO  BLOCK-MEDIAN  \n'
                else:
                    print('Invalid Operation type (-p option)')
                    print(colored('     Use -p cumulative/running|rolling/block','green',attrs=['bold']))
                    print(colored('        ERROR','red',attrs=['bold']))
                    exit()
        if ('-o' in arguments):
            outfile=output_file
        else:
            outfile='sahil.out'
            print('No output file is provided. Output in file: ',outfile)
            print(colored('    Use -o outfile','green',attrs=['bold']))
        with open(outfile,'a') as f:
            f.write(cline)
            np.savetxt(f,final_out,fmt='%1.4f')
#========================================================================================
#---------------------------------------------------------------------------------------
#========================================================================================
elif what == 'MEAN':
    if ('-p' not in arguments) == True :
        print(what,':   ',np.nanmean(data1))
    else:
        if operation_type1.upper() == 'CUMULATIVE':
            def cumulative_average(x):
                av=[]
                av.append(x[0])
                for i in range(1,len(x)):
                    av.append(np.nanmean(x[:i+1]))
                return av
            out=cumulative_average(data1)
            tout=times1
            final_out=np.column_stack((tout,out))
            cline='#REF-COLUMN  CUMULATIVE-MEAN  \n'
        elif operation_type1.upper() == 'REVERSE-CUMULATIVE':
            def cumulative_average(x):
                av=[]
                av.append(x[0])
                for i in range(1,len(x)):
                    av.append(np.nanmean(x[:i+1]))
                return av
            out=cumulative_average(np.flip(data1))
            tout=np.flip(times1)
            final_out=np.column_stack((tout,out))
            cline='#REF-COLUMN  CUMULATIVE-MEAN  \n'
        else:
            if ('-r' not in arguments) == True:
                print('Operational value not provided')
                print(colored('     Use -r option','green',attrs=['bold']))
                exit()
            else:
                if operational_value1 > len(data1):
                    print('Operational value is greater than total length of input_data1')
                    print('    ',colored('CAN BE A SOURCE OF ERROR','red',attrs=['underline']))
                if (operation_type1.upper() in ['RUNNING','ROLLING']):
                    def running_average(x,r):
                        av=[]
                        for i in tqdm(range(0,len(x)-r+1),desc='RUNNING'):
                            av.append(np.nanmean(x[i:i+r-1]))
                        return av
                    out=running_average(data1,operational_value1)
                    tout=times1[operational_value1-1:]
                    final_out=np.column_stack((tout,out))
                    cline='#REF-COLUMN  RUNNING-AVERAGE  \n'
                elif operation_type1.upper() == 'BLOCK':
                    def block_average(x,r,times1):
                        i=0
                        j=r-1
                        av=[]
                        tav=[]
                        while j < len(x):
                            av.append(np.nanmean(x[i:j]))
                            tav.append([times1[i],times1[j]])
                            i=i+r
                            j=j+r
                        if j-r+1 < len(x):
                            av.append(np.nanmean(x[i:]))
                            tav.append([times1[i],times1[-1]])
                        return tav, av
                    tout,out=block_average(data1,operational_value1,times1)
                    final_out=np.column_stack((tout,out))
                    cline='#FROM  TO  BLOCK-AVERAGE  \n'
                elif operation_type1.upper() == 'WEIGHTED':
                    print('Invalid Operation type (-p option)')
                    print(colored('     Looking for weighted-average:: Use weighted-mean','green',attrs=['bold']))
                    print(colored('        ERROR','red',attrs=['bold']))
                    exit()
                elif operation_type1.upper() == 'BOOTSTRAP':
                    print('Invalid Operation type (-p option)')
                    print(colored('     Looking for mean by bootstrapping:: Use bmean','green',attrs=['bold']))
                    print(colored('        ERROR','red',attrs=['bold']))
                    exit()
                else:
                    print('Invalid Operation type (-p option)')
                    print(colored('     Use -p cumulative/running|rolling/block','green',attrs=['bold']))
                    print(colored('        ERROR','red',attrs=['bold']))
                    exit()
        if ('-o' in arguments):
            outfile=output_file
        else:
            outfile='sahil.out'
            print('No output file is provided. Output in file: ',outfile)
            print(colored('    Use -o outfile','green',attrs=['bold']))
        with open(outfile,'a') as f:
            f.write(cline)
            np.savetxt(f,final_out,fmt='%1.4f')
#========================================================================================
#---------------------------------------------------------------------------------------
#========================================================================================
elif what == 'WEIGHTED-MEAN':
    if ('-g' in arguments):
        weights=data2
    else:
        try:
            weights=raw_data1[:,column2]
        except:
            print('Weights couldnot be read from input-file1')
            print(colored('    Use -y to define weights column','green',attrs=['bold']))
            print(colored('        ERROR','red',attrs=['bold']))
            exit()

    if len(data1) != len(weights) :
        print('input-data1 and weights data are of different length')
        print(colored('        ERROR','red',attrs=['bold']))
        exit()

    if ('-q' in arguments):
        operation_type2=operation_type2.upper()
        if operation_type2 == 'MEAN-DIVIDE':
            if np.nanmean(weights) != 0:
                weights=weights/np.nanmean(weights)
            else:
                print('Mean of weights is zero. Cannot divide by zero')
                print(colored('        ERROR','red',attrs=['bold']))
                exit()
        elif operation_type2 == 'MEAN-SUBTRACT':
            weights=weights - np.nanmean(weights)
        elif operation_type2 == 'MEDIAN-DIVIDE':
            if np.nanmedian(weights) != 0:
                weights=weights/np.nanmedian(weights)
            else:
                print('Median of weights is zero. Cannot divide by zero')
                print(colored('        ERROR','red',attrs=['bold']))
                exit()
        elif operation_type2 == 'MEDIAN-SUBTRACT':
            weights=weights - np.nanmedian(weights)
        elif operation_type2 == 'MIN-DIVIDE':
            if np.nanmin(weights) != 0:
                weights=weights/np.nanmin(weights) 
            else:
                print('Min of weights is zero. Cannot divide by zero')
                print(colored('        ERROR','red',attrs=['bold']))
                exit()
        elif operation_type2 == 'MIN-SUBTRACT':
            weights=weights - np.nanmin(weights)
        elif operation_type2 == 'MAX-DIVIDE':
            if np.nanmax(weights) != 0:
                weights=weights/np.nanmax(weights)
            else:
                print('Max of weights is zero. Cannot divide by zero')
                print(colored('        ERROR','red',attrs=['bold']))
                exit()
        elif operation_type2 == 'MAX-SUBTRACT':
            weights=weights - np.nanmax(weights)
        elif operation_type2 == 'SUM-DIVIDE':
            if np.nansum(weights) != 0:
                weights=weights/np.nansum(weights)
            else:
                print('SUM of weights is zero. Cannot divide by zero')
                print(colored('        ERROR','red',attrs=['bold']))
                exit()
        elif operation_type2 == 'SUM-SUBTRACT':
            weights=weights - np.nansum(weights)
        elif operation_type2 == 'FACTOR-DIVIDE':
            if ('-v' not in arguments)==True:
                print('Input factor not given (-v option)')
                print(colored('        ERROR','red',attrs=['bold']))
                exit()
            else:
                if value1 != 0:
                    weights=weights/value1
                else:
                    zero_divide_error()
        elif operation_type2 == 'FACTOR-SUBTRACT':
            if ('-v' not in arguments)==True:
                print('Input factor not given (-v option)')
                print(colored('        ERROR','red',attrs=['bold']))
                exit()
            else:
                weights=weights - value1
        else:
            print('Operation-type2 not recognized')
            print(colored('        ERROR','red',attrs=['bold']))
            exit()

    weighted_data=data1*weights
    total_weights=np.nansum(weights)
    if ('-p' not in arguments)==True:
        if total_weights == 0:
            print('Total weights equal zero.. Cannot divide by zero')
            print(colored('        ERROR','red',attrs=['bold']))
            exit()
        print(what,':   ',np.nansum(weighted_data)/total_weights)
    else:
        operation_type1=operation_type1.upper()
        if operation_type1 == 'BOOTSTRAP':
            if ('-b' not in arguments)==True:
                print('Bootstrap Value not provided (-b option)')
                print(colored('        ERROR','red',attrs=['bold']))
                exit()
            else:
                def weighted_bootstrap(wx,w,btv):
                    means=[]
                    for i in range(btv):
                        random_array=np.random.randint(len(wx),size=len(wx))
                        random_data=np.array([wx[j] for j in random_array])
                        random_weights=np.array([w[j] for j in random_array])
                        if np.nansum(random_weights) == 0:
                            print('Weights has zero values: Cannot divide by zero')
                            print(colored('        ERROR','red',attrs=['bold']))
                            exit()
                        means.append(np.nansum(random_data)/np.nansum(random_weights))
                    return means
                print('WEIGHTED-BOOTSTRAPED-MEAN:  ',np.nanmean(weighted_bootstrap(weighted_data,weights,operational_value2)))
        else:
            if operation_type1 == 'CUMULATIVE':
                def weighted_cumulative(wx,w):
                    av=[]
                    av.append(wx[0])
                    for i in range(1,len(wx)):
                        if np.nansum(w[:i+1]) == 0:
                            print('Weights has zero values: Cannot divide by zero')
                            print(colored('        ERROR','red',attrs=['bold']))
                            exit()
                        av.append(np.nansum(wx[:i+1])/np.nansum(w[:i+1]))
                    return av
                out=weighted_cumulative(weighted_data,weights)
                tout=times1
                final_out=np.column_stack((tout,out))
                cline='#REF-COLUMN   WEIGHTED-CUMULATIVE-MEAN  \n'
            elif (operation_type1 not in ['CUMULATIVE','RUNNING','ROLLIN','BLOCK'])==True:
                print('Operation-type1 not recognized (-p option)')
                print(colored('    Use -p bootstrap/cumulative/running/rolling/block','green',attrs=['bold']))
                print(colored('        ERROR','red',attrs=['bold']))
                exit()
            else:
                if ('-r' not in arguments)==True:
                    print('Operational-value not provided')
                    print(colored('    Use -r option','green',attrs=['bold']))
                    exit()
                else:
                    if operational_value1 > len(weighted_data):
                        print('Operational-value is greater than total length of input-data1')
                        print('    ',colored('CAN BE A SOURCE OF ERROR','red',attrs=['underline']))
                    if (operation_type1 in ['RUNNING','ROLLING']):
                        def weighted_running(wx,w,r):
                            av=[]
                            for i in range(0,len(wx)-r+1):
                                if np.nansum(w[i:i+r-1]) == 0 :
                                    print('Weights has zero values: Cannot divide by Zero')
                                    print(colored('        ERROR','red',attrs=['bold']))
                                    exit()
                                av.append(np.nansum(wx[i:i+r-1])/np.nansum(w[i:i+r-1]))
                            return av
                        out=weighted_running(weighted_data,weights,operational_value1)
                        tout=times1[operational_value1-1:]
                        final_out=np.column_stack((tout,out))
                        cline='#REF-COLUMN   WEIGHTED-RUNNING-MEAN  \n'
                    elif operation_type1 == 'BLOCK':
                        def weighted_block(wx,w,r):
                            i=0
                            j=r-1
                            av=[]
                            tav=[]
                            while j < len(wx):
                                if np.nansum(w[i:j]) == 0:
                                    print('Weights has zero values: Cannot divide by Zero')
                                    print(colored('        ERROR','red',attrs=['bold']))
                                    exit()
                                av.append(np.nansum(wx[i:j])/np.nansum(w[i:j]))
                                tav.append([times1[i],times1[j]])
                                i=i+r
                                j=j+r
                            if j-r+1 < len(wx):
                                if np.nansum(w[i:j]) == 0:
                                    print('Weights has zero values: Cannot divide by Zero')
                                    print(colored('        ERROR','red',attrs=['bold']))
                                    exit()
                                av.append(np.nansum(wx[i:])/np.nansum(w[i:]))
                                tav.append([times1[i],times1[-1]])
                            return tav, av
                        tout,out=weighted_block(weighted_data,weights,operational_value1)
                        final_out=np.column_stack((tout,out))
                        cline='#FROM  TO    WEIGHTED-BLOCK-MEAN  \n'

            if ('-o' in arguments):
                outfile=output_file
            else:
                outfile='sahil.out'
                print('No output file is provided. Output in file: ',outfile)
                print(colored('    Use -o outfile','green',attrs=['bold']))
            with open(outfile,'a') as f:
                f.write(cline)
                np.savetxt(f,final_out,fmt='%1.4f')
#========================================================================================
#---------------------------------------------------------------------------------------
#========================================================================================
elif what == 'BMEAN':
    proceed=0
    for i in arguments:
        if i == '-b':
            proceed=1
            break
    if proceed == 0:
        print('Bootstrap Value not provided (-b option)')
        print(colored('        ERROR','red',attrs=['bold']))
        exit()
    print(what,':   ',np.nanmean(bootstrap(data1)))
#========================================================================================
#---------------------------------------------------------------------------------------
#========================================================================================
elif what == 'STD':
    print(what,':   ',np.nanstd(data1))
#========================================================================================
#---------------------------------------------------------------------------------------
#========================================================================================
elif what == 'SEM':
    print(what,':   ',np.nanstd(data1)/(np.sqrt(np.size(data1)-1)))
#========================================================================================
#---------------------------------------------------------------------------------------
#========================================================================================
elif what == 'BSTD':
    if ('-b' not in arguments) == True:
        print('Bootstrap Value not provided (-b option)')
        print(colored('        ERROR','red',attrs=['bold']))
        exit()
    else: 
        print(what,':   ',np.nanstd(bootstrap(data1)))
#========================================================================================
#---------------------------------------------------------------------------------------
#========================================================================================
elif what == 'ROW-MEAN':
    if ('-o' in arguments):
        outfile=output_file
    else:
        outfile='sahil.out'
        print('No output file is provided. Output in file: ',outfile)
        print(colored('    Use -o outfile','green',attrs=['bold']))
    if raw_data1.ndim == 1:
        print('The input data has only one column.')
        print(colored('        ERROR','red',attrs=['bold']))
        exit()
    elif raw_data1.ndim == 2:
        if len(raw_data1[1]) == 2:
            out=[]
            for i in range(len(raw_data1)):
                out.append(np.nanmean(raw_data1[i]))
            with open(outfile,'a') as f:
                print('#The input data has only two columns... Using both of them.\n')
                np.savetxt(f,out,fmt='%1.4f')
        elif len(raw_data1[1]) > 2:
            if ('-p' in arguments):
                if operation_type1.upper() == 'ALL-COLS':
                    print('Using all rows:')
                    data_to_use=raw_data1
                elif operation_type1.upper() == 'EXCEPT-REF-COL':
                    data_to_use=rest_data1
                    outs='stacked'
                    print('Using all except ref column')
                else:
                    print('Invalid argument for -p')
                    print(colored('    -p all-cols / except-ref-col','green',attrs=['bold']))
                    exit()
            else:
                data_to_use=rest_data1
                outs='stacked'
            out=[]
            for i in range(len(data_to_use)):
                out.append(np.nanmean(data_to_use[i]))
            if outs == 'stacked':
                out=np.column_stack((times1,out))
            with open(outfile,'a') as f:
                np.savetxt(f,out,fmt='%1.4f')
#========================================================================================
#---------------------------------------------------------------------------------------
#========================================================================================
elif what == 'ROW-MEDIAN':
    if ('-o' in arguments):
        outfile=output_file
    else:
        outfile='sahil.out'
        print('No output file is provided. Output in file: ',outfile)
        print(colored('    Use -o outfile','green',attrs=['bold']))
    if raw_data1.ndim == 1:
        print('The input data has only one column.')
        print(colored('        ERROR','red',attrs=['bold']))
        exit()
    elif raw_data1.ndim == 2:
        if len(raw_data1[1]) == 2:
            out=[]
            for i in range(len(raw_data1)):
                out.append(np.nanmedian(raw_data1[i]))
            with open(outfile,'a') as f:
                print('#The input data has only two columns... Using both of them.\n')
                np.savetxt(f,out,fmt='%1.4f')
        elif len(raw_data1[1]) > 2:
            if ('-p' in arguments):
                if operation_type1.upper() == 'ALL-COLS':
                    print('Using all rows:')
                    data_to_use=raw_data1
                elif operation_type1.upper() == 'EXCEPT-REF-COL':
                    data_to_use=rest_data1
                    outs='stacked'
                    print('Using all except ref column')
                else:
                    print('Invalid argument for -p')
                    print(colored('    -p all-cols / except-ref-col','green',attrs=['bold']))
                    exit()
            else:
                data_to_use=rest_data1
                outs='stacked'
            out=[]
            for i in range(len(data_to_use)):
                out.append(np.nanmedian(data_to_use[i]))
            if outs == 'stacked':
                out=np.column_stack((times1,out))
            with open(outfile,'a') as f:
                np.savetxt(f,out,fmt='%1.4f')
    elif raw_data1.ndim > 2:
        print('Higher order data:::---!')
        print(colored('    this program is for 2-D data only','green',attrs=['bold']))
#========================================================================================
#---------------------------------------------------------------------------------------
#========================================================================================
elif what == 'NORMALIZE':
    if ('-p' in arguments):
        if operation_type1.upper() == 'MEAN':
            norm_factor=np.nanmean(data1)
        elif (operation_type1.upper() in ['TOTAL','SUM']):
            norm_factor=np.nansum(data1)
        elif operation_type1.upper() == 'MEDIAN':
            norm_factor=np.nanmedian(data1)
        elif operation_type1.upper() == 'MIN':
            norm_factor=np.nanmin(data1)
        elif operation_type1.upper() == 'MAX':
            norm_factor=np.nanmax(data1)
        elif operation_type1.upper() == 'factor':
            if ('-v' not in arguments)==True:
                print('The input-factor not provided (-v option)')
                print(colored('        ERROR','red',attrs=['bold']))
                exit()
            else:
                norm_factor = value1
        else:
            print('Operation_type1 not recognize')
            print(colored('    -p mean/sum/median....','green',attrs=['bold']))
            print(colored('        ERROR','red',attrs=['bold']))
            exit()
    else:
        norm_factor=np.nanmean(data1)

    if ('-q' in arguments):
        if (operation_type2.upper() in ['NORMALIZE','DIVIDE']):        
            if norm_factor != 0:
                out=data1/norm_factor
            else:
                print('Normalization-factor is 0.  Cannot divide by zero.')
                print(colored('        ERROR','red',attrs=['bold']))
                exit()
        elif operation_type2.upper() == 'SUBTRACT':
            out = data1 - norm_factor
        else:
            print('Operation_type2 not recognize')
            print(colored('    -p divide/subtract','green',attrs=['bold']))
            print(colored('        ERROR','red',attrs=['bold']))
            exit()
    else:
        if norm_factor != 0:
            out=data1/norm_factor
        else:
            print('Normalization-factor is 0.  Cannot divide by zero.')
            print(colored('        ERROR','red',attrs=['bold']))
            exit()

    final_out=np.column_stack((times1,out))

    if ('-o' in arguments):
        outfile=output_file
    else:
        outfile='sahil.out'
        print('No output file is provided. Output in file: ',outfile)
        print(colored('    Use -o outfile','green',attrs=['bold']))

    with open(outfile,'a') as f:
        np.savetxt(f,final_out,fmt='%1.4f')
#========================================================================================
#---------------------------------------------------------------------------------------
#========================================================================================
elif what == 'CORRELATION':
    if ('-g' in arguments):
        pass
    else:
        try:
            data2=raw_data1[:,column2]
        except:
            print('Data2 couldnot be read from input-file1')
            print(colored('    Use -y to define data2 column','green',attrs=['bold']))
            print(colored('        ERROR','red',attrs=['bold']))
            exit()

    if len(data1) != len(data2) :
        print('input-data1 and weights data are of different length')
        print(colored('        ERROR','red',attrs=['bold']))
        exit()

    if ('-p' not in arguments)==True:
        print('Provide type of correlation to calculate')
        print(colored('    Use -p option','green',attrs=['bold']))
        print(colored('        ERROR','red',attrs=['bold']))
        exit()
    else:
        operation_type1=operation_type1.upper()
        if operation_type1 == 'PEARSON':
            print('LINEAR-PEARSON-CORRELATION-COEFICIENT:  ',np.corrcoef(data1,data2)[0,1])
        else:
            print('Correlation type not identified')
            print(colored('        ERROR','red',attrs=['bold']))
            exit()
#========================================================================================
#---------------------------------------------------------------------------------------
#========================================================================================
elif what == 'BINDING-TIME':
    if ('-v' not in arguments):
        print('Binding cutoff not provided ')
        print(colored('    Use -v option ','green',attrs=['bold']))
        print(colored('        ERROR','red',attrs=['bold']))
        exit()
    else:
        cutoff=value1
        if ('-r' in arguments):
            if operational_value1 == 0:
                print('Operational value cannot be zero::  Taking it 1')
                operational_value1=1
            stable_pose_cutoff=operational_value1
        else:
            print(colored('    Use -r to define minimum events to be true simultenously for succesfull event occurence','green',attrs=['bold']))
            print(colored('     Usefull in discriminating the transient events specially for open/outer binding pockets','green',attrs=['bold']))
            print(colored('     For a carefully choosen cutoff, -r did not matter','green',attrs=['bold']))
            print(colored('      The default is 5 values','green',attrs=['bold']))
            stable_pose_cutoff=5

        if ('-p' in arguments):
            operation_type1=operation_type1.upper()
            if operation_type1 == 'UNBINDING':
                print('\n Looking for unbinding time \n')
                op1='data1[i] >= cutoff'
                op2='x >= cutoff'
            else:
                print('Operation-type1 not recognized.')
                print(colored('    Use -p unbinding (if looking for unbinding)','green',attrs=['bold']))
                exit()
        else:
            op1='data1[i] <= cutoff'
            op2='x <= cutoff'

        found=False
        for i in range(len(data1)):
            if eval(op1):
                dnext=[data1[j] for j in range(i,i+stable_pose_cutoff)]
                if all(eval(op2) for x in dnext) == True:
                    print('Event occured::    ',times1[i],'\t',data1[i])
                    found=True
                    break
                else:
                    print('Transient event::  ',times1[i],'\t',data1[i])

        if found == False:
            print('Event not occured based on the given criteria')
#========================================================================================
#---------------------------------------------------------------------------------------
#========================================================================================
