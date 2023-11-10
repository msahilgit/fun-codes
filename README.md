# fun-codes
Welcome to my small and fun codes, written during my initial learning period as part of coding practice. These codes can serve as quick analysis as these run directly from terminal like commands.



**STATISTICS**
> If you are starting Molecular Dynamics career using GROMACS and do not use python yet, this code can perform some of the statistical analysis on gromacs generated xvg files.
> Syntax of this code is similar to gromacs,
        Statistics sub_command -f ... options
        list of sub_commands are available like bootstrapped mean, binding time etc
        like gromacs, it does not overwrite, instead backed up the files
        in addition to gromacs, if sub_command has some alphabetical error, it also suggest the correct names.

USAGE
> put this code in any of your BASH PATH and modify python path (first line in statistics.py)
> just write statistics in terminal, it should print usage.
>  for any help, just like gromacs, write
        statistics sub_command -h



**PAIR_MAKER**



