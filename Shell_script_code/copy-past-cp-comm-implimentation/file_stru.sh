#!/bin/bash
# $1:filepath & $2 word
# this code scan directory recursivly to search specific word from any type of file
my_function()
{
	#echo $1 
	cd $1
    #echo "@" $1 >>/home/kpit/Desktop/trial/source1.txt
	#ls
for directory in *
	do
			if [ -f $directory ]; then 
				echo -e "F $PWD/"$directory >>/home/kpit/Desktop/trial/source1.txt
			elif [ -d $directory ]; then 
			   cd $1/$directory	
				for file in $1/$directory*
				   do
   					if [ -f $file ]; then 
       			 			echo -e "F $PWD/"$directory >>/home/kpit/Desktop/trial/source1.txt
    					elif [ -d $file ];then
                             echo -e "D $PWD/" >>/home/kpit/Desktop/trial/source1.txt
						    my_function $1/$directory $2 
					fi
               
		     			 cd $1
				done 			
fi
cd $1
 done  
	
}
rm -rf /home/kpit/Desktop/trial/source1.txt
export MY_PATH=$1
echo -e "D $1">>/home/kpit/Desktop/trial/source1.txt
my_function ${MY_PATH} $2

echo "completed"
