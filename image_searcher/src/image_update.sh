#!/bin/bash
dt=`date "+%Y%m%d" -d last-day`
echo $dt " begin to update the index"
HOME_OFFLINE=/home/admin/projectspace/offline_image_search/tujing/
HOME_IS_ONLINE=/home/admin/projectspace/image_search_app/image_searcher/

# step 1. check done
checkdone_file=$HOME_OFFLINE/output/$dt.done
echo $dt " to check configfile " $checkdone_file
if [ ! -f "$checkdone_file" ]; then
   echo $dt $checkdone_file " not exists!"
   exit -1
fi 
echo $dt $checkdone_file " ready and to update"

# step 2. copy the config file
# step 2.1 backup the old config in case that the new config is not workable
cp $HOME_IS_ONLINE/conf/offline_config.json $HOME_IS_ONLINE/conf/offline_config.json.$dt
mv $HOME_IS_ONLINE/conf/offline_config.json $HOME_IS_ONLINE/conf/offline_config.json.bak
cp $HOME_OFFLINE/output/offline_config.json $HOME_IS_ONLINE/conf/offline_config.json

# step 3. restart the is process
cd $HOME_IS_ONLINE/src
source /home/admin/.bash_local
pyenv_is_enable
# step 3.1 test the config
python is_server_test_config.py
if [ $? -eq 0 ]; then
    # kill current is process
    ps xuf | grep is_server_grpc | awk -F " " '{print $2}' | xargs kill -9
    # restart the is process
    echo "nohup python is_server_grpc.py > $HOME_IS_ONLINE/src/nohup_is.out 2>&1&"
    nohup python is_server_grpc.py > $HOME_IS_ONLINE/src/nohup_is.out 2>&1&
    sleep 5
    echo $dt " restart okay. config file " $checkdone_file
    echo $dt " ====  restart successfully ==== "
    exit 0
fi 

# step 4. roll back
cp $HOME_IS_ONLINE/conf/offline_config.json $HOME_IS_ONLINE/conf/offline_config.json.failed.$dt
echo $dt " ERROR: maybe config is not correct. pls check file " $HOME_IS_ONLINE/conf/offline_config.json.failed.$dt 
mv $HOME_IS_ONLINE/conf/offline_config.json.bak $HOME_IS_ONLINE/conf/offline_config.json 
echo $dt " ERROR: restart failed. The index is not update today!!!!!!!"
exit -1




