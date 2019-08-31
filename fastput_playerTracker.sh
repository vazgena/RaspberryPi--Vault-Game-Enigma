CMD="mysql -u 'game' --database=game --disable-column-names -B  -ph95d3T7SXFta  -e \"select ipaddress  from station_ips  WHERE station not in \
    	('WATCH1WIN', 'WATCH2WIN', 'MIRROR1WIN', 'MIRROR2WIN', 'MiddleOneLights',\
	 'CAMERA1-2', 'CAMERA2-2', 'CAMERA2-1','CAMERA3-1' , 'CAMERA4-1' ) \"  " 
echo "CMD=\"" $CMD "\""
#exit
rv=eval $CMD
for i in `$CMD` ; do
	echo "machine" $i ;
	#sshpass -p '1qaz2wsx' scp www/playerTracking.py pi@${i}: ;
done
