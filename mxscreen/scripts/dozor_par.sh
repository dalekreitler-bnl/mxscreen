#!/bin/bash
# dozor_par, Script to run dozor_no_omp in parallel
#  (c) Copyright 2017 Herbert J. Bernstein 
#      yayahjb@gmail.com, 29 Jun 2017

#***** EDIT TO ENSURE besthome is defined in the environment
#***** and trhe dozor programs and scripts are in the PATH
if [ "xx${besthome}" == "xx" ] ; then
export besthome=/usr/local/crys-prod/dozor_20Jul2017
export PATH=$besthome:$PATH
fi

intre='^[0-9]+$'
last_frame="-1"
nimages="-1"
onedashargs=" "
twodashargs=" "
nodashargs=" "
maxblock=4
maxthreads=108


if [ "${1}xx" == "--helpxx" ]
  then
  echo "dozor_par first_frame last_frame [options]  dozor_args"
  echo "dozor_par last_frame [options]  dozor_args"
  echo "dozor_par [options] dozor_args"
  echo   "first_frame last_frame  -- frames numbered from 1"
  echo   "first_frame defaults to 1"
  echo   "last_frame defaults to the number of frames reported by eiger2cbf"
  echo "optionally followed by"
  echo "    --maxthreads mthreads    -- limit the threads to mthreads"
  echo "    --maxblock kimages       -- limit the blocks to kimages"
  echo "    followed by dozor_args -- the command line arguments for dozor"
  /usr/local/crys-local/dozor_20160517_rev_nsls_ii_07Nov17/dozor_no_omp --help
  exit
else
dozor_tmp=/tmp/dozor_tmp$$
mkdir -p $dozor_tmp
date > $dozor_tmp/date$$
if [[ $1 =~ $intre ]] ; then
   first_frame=$1
   shift
   if [[ $1 =~ $intre ]] ; then
     last_frame=$1
     shift
   else
     last_frame=first_frame
     first_frame=1
   fi
else
   first_frame=1
fi
#
# search arguments for frames
#
activearg="0"
for i in `seq $#` ; do
    #echo "activearg: $activearg"
    j=`expr $i + 1`
    if [ "$activearg" == "1" ] ; then
      activearg="0"
      #echo "skipping i: $i"
      continue
    fi
    #echo processing i: $i, j: $j ${@:$i:1} ${@:$j:1}

    option="${@:$i:1}"
    value="${@:$j:1}"
    # check for --first  or --first_image_number or
    #           --images or --number_images
    #           --maxthreads
    #           --maxblock  

    if [ "xx${option:0:2}" == "xx--" ] ; then
      #echo "processing two dash argument $option $value"
      if [ "${option}" != "--maxthreads" ] \
        && [ "${option}" != "--maxblock" ] \
        &&  [ "${option}" != "--images" ] \
        &&  [ "${option}" != "--first_image_number" ] \
        &&  [ "${option}" != "--images" ] \
        &&  [ "${option}" != "--number_images" ] ; then
        twodashargs="$twodashargs $option $value "
        #echo twodashargs: $twodashargs
      fi
      activearg="1"
      if [ "${first_frame}" == "-1" ] ; then
        if [ "${option}" == "--first" ] || [ "${option}" == "--first_image_number" ] ; then
          first_frame=$value
          twodashargs="$twodashargs --first_image_number $value "
          #echo twodashargs: $twodashargs
          continue
        fi
      fi
      if [ "${last_frame}" == "-1" ] ; then
        if [ "${option}" == "--images" ] || [ "${option}" == "--number_images" ] ; then
          nimages=$value
          twodashargs="$twodashargs --number_images $value "
          #echo twodashargs: $twodashargs
          continue
        fi
      fi
      if [  "${option}" == "--maxthreads" ]; then
        maxthreads=${value}
        continue;
      fi 
      if [  "${option}" == "--maxblock" ]; then
        maxblock=${value}
        continue;
      fi 
      if [ "$nimages" == "-1" ] ; then
        if [ "${option}" == "--name_template_image" ] && [ -f "$value" ] ; then
           #echo "processing $option $value"
           nimages=`eiger2cbf ${value}`
           echo nimages: $nimages
           twodashargs="$twodashargs $option $value "
           #echo "$twodashargs:  $twodashargs"
        fi 
      fi
    elif [ "xx${option:0:1}" == "xx-" ] ; then
      activearg="0"
      onedashargs="$onedashargs $option "
      continue
    else
      activearg="0"
      nodashargs="$nodashargs $option "
      #echo "$option nodashargs: $nodashargs$"
      if [ -f "${option}" ] ; then
        template=`grep "name_template_image " $option | cut -d " " -f 2-`
        if [ -f "${template}" ] ; then
          nimages=`eiger2cbf ${template}`
          #echo nimages: $nimages
        fi
      fi
    fi
done

if [ "$last_frame" == "-1" ] && [ "$nimages" != "-1" ] ; then
    last_frame=`expr $first_frame + $nimages - 1 `
fi
#echo nimages: $nimages, first_frame: $first_frame, last_frame: $last_frame



iframe=$first_frame
nframes=`expr $last_frame - $first_frame + 1`

block_size=$maxblock
totframes=$(( $block_size * $maxthreads ))
#echo totframes: $totframes block_size: $block_size maxthreads: $maxthreads
while [ "${totframes}" -gt "${nframes}" ]; do
  block_size=$(( $block_size / 2 ))
  #echo block_size: $block_size
  if [ "${block_size}" -lt "3" ]; then
    block_size=1
    break
  fi
  totframes=$(( $block_size * $maxthreads ))
  #echo totframes: $totframes block_size: $block_size maxthreads: $maxthreads
done
                    
#echo block_size: $block_size, maxthreads: $maxthreads 
                    


running=0

#echo "onedashargs: $onedashargs"
#echo "nodashargs: $nodashargs"
#echo "twodashargs: $twodashargs"

while [ $iframe -le $last_frame ]; do
  block_end=`expr $iframe + $block_size - 1`
  if [ $block_end -gt $last_frame ]
    then block_end=$last_frame
  fi
  
  kframes=`expr $block_end - $iframe + 1`
  #echo  "(dozor_no_omp $onedashargs $nodashargs $twodashargs  --first $iframe --images $kframes  >> \
      #$dozor_tmp/dozor_out_$iframe 2>> $dozor_tmp/dozor_err_$iframe ; date &>> $dozor_tmp/dozor_err_$iframe) " 
  (/usr/local/crys-local/dozor_20160517_rev_nsls_ii_07Nov17/dozor_no_omp $onedashargs $nodashargs $twodashargs  --first
 $iframe --images $kframes  >> \
      $dozor_tmp/dozor_out_$iframe 2>> $dozor_tmp/dozor_err_$iframe ; date &>> $dozor_tmp/dozor_err_$iframe) & 
  running=$(( $running + 1 ))
    if [ $running -ge $maxthreads ]
      then
      wait
      running=0
    fi
                        
  iframe=`expr $block_end + 1
  `
done
wait

iframe=$first_frame
echo "NSLS-II LSBR dozor_par script, 17 Jul 2017, HJB"
head -6 $dozor_tmp/dozor_out_$iframe

while [ $iframe -le $last_frame ]; do
  block_end=`expr $iframe + $block_size - 1`
  if [ $block_end -gt $last_frame ]
    then block_end=$last_frame
  fi
  
  kframes=`expr $block_end - $iframe + 1`
  tail -n +7 $dozor_tmp/dozor_out_$iframe >> /tmp/dozor_out$$
  iframe=`expr $block_end + 1`
done

cat $dozor_tmp/dozor_err_* >> /tmp/dozor_err$$
grep -v "SPOTS" /tmp/dozor_out$$ | grep "|" | sort -u -g | grep -v intrefT
cat /tmp/dozor_err$$ |  grep ":" | sort -u  | grep -v IEEE  1>&2
echo ran from `cat $dozor_tmp/date$$` to `date` 1>&2
rm -rf $dozor_tmp
fi

