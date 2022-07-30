#!/bin/bash
gluster volume create gvol replica 3 gfs-223:/opt/gfs/bk1 gfs-222:/opt/gfs/bk1 gfs-224:/opt/gfs/bk1 gfs-223:/opt/gfs/bk2 gfs-222:/opt/gfs/bk2 gfs-224:/opt/gfs/bk2 gfs-223:/opt/gfs/bk3 gfs-222:/opt/gfs/bk3 gfs-224:/opt/gfs/bk3

if [ $? -eq 0 ];then
    gluster volume start gvol
fi
if [ $? -eq 0 ];then
    mount -t glusterfs gfs-224:/gvol /home/wgq/gfs_cli/
else
   echo "mount gluster client error" $?
fi
