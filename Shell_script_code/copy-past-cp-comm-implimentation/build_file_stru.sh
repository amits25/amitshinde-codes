
#!/bin/bash
line=$(head -n 1 /home/kpit/Desktop/trial/source1.txt)
echo $line
bsNa=$(echo "$line" | cut -d " " -f2) 
baseDIR=$(basename $bsNa)
#echo $baseDIR
cd $1
mkdir -p $baseDIR
#cat /home/kpit/Desktop/trial/source1.txt > /home/kpit/Desktop/trial/source2.txt 
sed -i 's/'$baseDIR'/,/g' /home/kpit/Desktop/trial/source1.txt
toPath=$1/$baseDIR
cd $toPath
#echo $pwd
cat /home/kpit/Desktop/trial/source1.txt |
while read data             #line by line
do
line=$data
 type=$(echo "$line" | cut -d " " -f1) 
 bsNa=$(echo "$line" | cut -d " " -f2) 
 if [[ $type ==  "D" ]];then
       nextPath=$(echo "$bsNa" | cut -d "," -f2)
       #echo $nextPath
       mkdir -p $toPath/$nextPath

elif [[ $type ==  "F" ]];then
      nextPath=$(echo "$bsNa" | cut -d "," -f2)
      #echo $nextPath"****"
      touch $toPath$nextPath   #to path
      #echo $2$nextPath         #from path
      cat $2$nextPath > $toPath$nextPath      
fi
done
