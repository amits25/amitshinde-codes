####################################################################################################
	#Author:: Amit Shinde
	#DSC   :: This script will show size of individual file/DIr and also show total size in GB
	#ARG   :: This Script need DIR path as ARG($1)
###################################################################################################

#!/bin/bash
rm -rf /home/kpit/Desktop/140493/linux/Size_DIR/size.txt
cd $1
for data in *
do


    sudo du -hs $data |awk '{print $1}' >>/home/kpit/Desktop/140493/linux/Size_DIR/size.txt
     sudo du -hs $data 



done

echo "END" >>/home/kpit/Desktop/140493/linux/Size_DIR/size.txt
sudo /home/kpit/Desktop/140493/linux/Size_DIR/sizeCount.sh $1             #for total size In GB


# amit path_to_calculate_size    // here amit is command to run shell script

