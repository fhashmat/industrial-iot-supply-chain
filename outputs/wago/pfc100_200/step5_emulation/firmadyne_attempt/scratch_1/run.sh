#!/bin/bash

set -u

ARCHEND=armel
IID=1

if [ -e ./firmadyne.config ]; then
    source ./firmadyne.config
elif [ -e ../firmadyne.config ]; then
    source ../firmadyne.config
elif [ -e ../../firmadyne.config ]; then
    source ../../firmadyne.config
else
    echo "Error: Could not find 'firmadyne.config'!"
    exit 1
fi

IMAGE=`get_fs ${IID}`
KERNEL=`get_kernel ${ARCHEND}`
QEMU=`get_qemu ${ARCHEND}`
QEMU_MACHINE=`get_qemu_machine ${ARCHEND}`
QEMU_ROOTFS=`get_qemu_disk ${ARCHEND}`
WORK_DIR=`get_scratch ${IID}`



function cleanup {
    pkill -P $$
    
}

trap cleanup EXIT

echo "Starting firmware emulation... use Ctrl-a + x to exit"
sleep 1s

QEMU_AUDIO_DRV=none ${QEMU} -m 256 -M ${QEMU_MACHINE} -kernel ${KERNEL} \
    -drive if=none,file=${IMAGE},format=raw,id=rootfs -device virtio-blk-device,drive=rootfs -append "root=${QEMU_ROOTFS} console=ttyS0 nandsim.parts=64,64,64,64,64,64,64,64,64,64 rdinit=/firmadyne/preInit.sh rw debug ignore_loglevel print-fatal-signals=1 user_debug=31 firmadyne.syscall=0" \
    -nographic \
    -device virtio-net-device,netdev=net1 -netdev socket,id=net1,listen=:2001 -device virtio-net-device,netdev=net2 -netdev socket,id=net2,listen=:2002 -device virtio-net-device,netdev=net3 -netdev socket,id=net3,listen=:2003 | tee ${WORK_DIR}/qemu.final.serial.log
