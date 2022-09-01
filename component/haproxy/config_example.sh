
config_file=/opt/config/haproxoy_example.cfg
zk="127.0.0.1:2181@127.0.0.1:2182"
if [ ! x"$zk" = x ];then
	###zk####
	zk_ha_port=2183
	# bind-process 4\n
	zk_proxy="listen zk_bc_resource:${zk_ha_port}\nbind :::${zk_ha_port} v4v6\nmode tcp\nbalance roundrobin\noption httpchk HEAD /zk HTTP/1.1\\\r\\\nHost:\\\ www\n"

	array=(${zk//,/ })
	length=${#array[@]}
	for ((i=0; i<$length; i++))
	do
		check_port=$(echo ${array[i]} | awk -F"@" '{print $2}' | awk -F":" '{print $NF}')
		check_addr=$(echo ${array[i]} | awk -F"@" '{print $2}' | sed "s/\:${check_port}$//")
		server_port=$(echo ${array[i]} | awk -F"@" '{print $1}' | awk -F":" '{print $NF}')
		server_addr=$(echo ${array[i]} | awk -F"@" '{print $1}' | sed "s/\:${server_port}$//")
		if [[ ${check_addr} =~ ":" ]];then
			server_host=$(echo ${check_addr//::/:} | sed "s/\:/-/g")
			zk_proxy1=$zk_proxy1"server s$server_host [${server_addr}]:${server_port} check addr [${check_addr}] check port ${check_port} inter 5s rise 1 fall 3 on-marked-down shutdown-sessions\n"
		else
			server_host=$(echo ${check_addr} | sed "s/\./-/g" )
			zk_proxy1=$zk_proxy1"server s$server_host ${server_addr}:${server_port} check addr ${check_addr} check port ${check_port} inter 5s rise 1 fall 3 on-marked-down shutdown-sessions\n"
		fi
	done
	zk_proxy=$zk_proxy$zk_proxy1

	sed -i "/^listen zk_bc_resource:${zk_ha_port}/,/^#End the zk proxy./d" $config_file
	sed -i "$ a  $zk_proxy"  $config_file
	sed -i "$ a  #End the zk proxy." $config_file
fi