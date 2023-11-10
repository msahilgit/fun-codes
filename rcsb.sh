#!/bin/bash
usage=$(echo $(tput bold)$(tput setaf 3)"Usage:   "$(tput setaf 6)"rcsb pdb_code name     ||  without '.pdb' extension"$(tput sgr0) )
if [ "$1" = "" ]; then
  echo $(tput bold)"NO pdb code is provided"
  echo ${usage}
  proceed=0
else
  pdb=`echo $1 | tr '[a-z]' '[A-Z]'`
  proceed=1
  if [ "$2" = "" ] ; then
    name=$1
  else
    name=$2
    if [ -f ${name}.pdb ] ; then
      echo $(tput bold)$(tput setaf 1)'Warning:  '$(tput setaf 6)"file ${name}.pdb already present"
    fi
  fi
fi
#
if [ ${proceed} -eq 0 ] ; then
  exit 1
fi
#
wget https://www.rcsb.org/pdb/files/${pdb}.pdb > /dev/null 2>&1 & 
PID=$!
bar='|/-\'
echo -n $(tput bold)$(tput setaf 5)"Downloading $1  "$(tput sgr0)
while [ -d /proc/$PID ]
do
  echo -ne $(tput bold)"\b"${bar:i++%${#bar}:1}
  sleep 0.2
done
echo ' '
#
if [ -f ${pdb}.pdb ] ; then
  mv ${pdb}.pdb ${name}.pdb
  echo 'DONE' $(tput sgr0) 
  ls ${name}.pdb
else
  echo "      "$(tput bold)$(tput setaf 1)"ERROR:: "$(tput setaf 6)"Structure ${pdb}.pdb not found at RCSB"$(tput sgr0)
  echo ""
  echo ${usage}
  echo ""
fi



