#!/bin/bash
cd $1
Marray=()
Garray=()
Karray=()
Mcount=0
Gcount=0
Kcount=0
declare -i START=0
cat /home/kpit/Desktop/140493/linux/Size_DIR/size.txt | 
while read data 
do

#echo $data
if [[ $data ==  *K* ]];then
	#echo "K"
	NUM=$(echo "$data" | cut -d "K" -f1)
	Karray+=($NUM)
elif [[ $data ==  *M* ]];then
        NUM=$(echo "$data" | cut -d "M" -f1)
	Marray+=($NUM)
	#echo "M"
elif [[ $data ==  *G* ]];then
	#echo "G"
	NUM=$(echo "$data" | cut -d "G" -f1)
	Garray+=($NUM)
elif [[ $data ==  *END* ]];then
	len=${#Marray[@]}
	#echo $len "lenght"
        for (( c=$START; c<$len; c++  ))
  	do
	#echo ${Marray[$c]}
         Mcount=$(echo $Mcount + ${Marray[$c]} | bc)
	done
	#echo $Mcount "M size"
	MBNUM=$(echo "$Mcount" | cut -d "." -f1)
	MBsize=`expr $MBNUM / 1024` 
	#echo $MBsize "MB to GB"
######################################################
	lenG=${#Garray[@]}
	#echo $lenG "lenght"
	declare -i START=0
        for (( c=$START; c<$lenG; c++  ))
  	do
	#echo ${Garray[$c]}
         Gcount=$(echo $Gcount + ${Garray[$c]} | bc)
	done
	#echo $Gcount "G size"
##########################################################
	lenK=${#Karray[@]}
	#echo $lenK "lenght"
	declare -i START=0
        for (( c=$START; c<$lenK; c++  ))
  	do
	#echo ${Karray[$c]} 
         Kcount=$(echo $Kcount + ${Karray[$c]} | bc)
	done
	#echo $Kcount "K size"
	KBNUM=$(echo "$Kcount" | cut -d "." -f1)
	#echo $KBNUM "KB size"
	KB2size=`expr $KBNUM / 1024`
	#KB3size=`expr $KB2size / 1024`
	#echo $KB2size "KB to GB"
############################################################
	total=$(echo $MBsize + $Gcount | bc)
	total=$(echo $total + $KB2size | bc)
	echo "#Total Size::"$total" GB  For DIR::" $PWD
	echo "#Total Size:: " $total" GB  For DIR::" $PWD >>/home/kpit/Desktop/140493/linux/Size_DIR/size.txt
fi

done


