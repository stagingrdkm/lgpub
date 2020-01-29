#!/bin/sh
LOOPDEV=$(losetup -f)
echo Using $LOOPDEV
losetup -v $LOOPDEV rootfs.sqsh.verity

source ./verity.conf
echo Running veritysetup 
veritysetup -v --debug create vencrootfs $LOOPDEV $LOOPDEV ${root_hash} --hash-offset=${hash_offset}
if [ $? != 0 ];then
  echo ERROR: veritysetup failed. Probably bad hash or hash offset. Does verity.conf match with rootfs.sqsh.verity?
  exit 1
fi

#for this demo we assume a fixed shared secret key
echo Running cryptsetup
DEMO_KEY="76f37ef456af7094a245c4f55d66bbd56651a8d78d97a198d864d8e04c24572fa9c1eebfc3c7e92fc1678f01d6dd7d0d425e69886a2f649313f95e5e2e7f8795"
echo $DEMO_KEY | cryptsetup -v --debug luksOpen /dev/mapper/vencrootfs vrootfs
if [ $? != 0 ];then
  echo ERROR: cryptsetup failed. Probably a bad key
  exit 1
fi

mkdir rootfs
mount -v /dev/mapper/vrootfs rootfs
