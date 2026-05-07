# Step 2 Static Structure Analysis - WAGO PFC100/200

## Input Firmware

- Vendor: WAGO
- Device family: PFC100/200 G2
- Firmware package: Firmware PFC100/200 4.9.1(31)
- File: Firmware_PFC100_PFC200_040901_31.zip

## Package Structure

The downloaded ZIP contains two artifacts:

1. `PFC-G2-Linux_sd_V040901_31_r9d0900aaed.img`
   - SD-card firmware image
   - DOS/MBR boot sector with two partitions

2. `PFC-G2-Linux_update_V040901_31_r9d0900aaed.wup`
   - ZIP-based WAGOupload update package
   - Contains `package-info.xml` and a `.raucb` RAUC bundle

## Update Package Structure

The `.wup` file contains:

- `package-info.xml`
- `PFC-G2-Linux_update_V040901_31_r9d0900aaed.raucb`

The `.raucb` file is a SquashFS filesystem and contains a RAUC update bundle.

## Firmware Metadata

From `package-info.xml`:

- System: PFC-Linux
- Firmware revision: 4.9.1
- Release index: 31
- Supported article numbers include 0750-8110, 0750-8111, 0750-8112, and 0750-8210 through 0750-8217 variants.

## Root Filesystem

The RAUC bundle contains `root.tar.gz`, which expands into a Linux root filesystem.

OS identity:

- OS/build system: PTXdist
- Version: 2024.12.0
- Pretty name: PTXdist / WAGO-PFC
- BSP vendor: WAGO
- BSP name: PFC
- Platform: wago-pfcXXX
- Build date: 2026-04-29T14:22:45+0000

## Architecture

The kernel file is:

- U-Boot legacy uImage
- Linux kernel version: Linux-6.6.94-rt56-w05.08.02
- Architecture: Linux/ARM

Device tree files indicate AM335x-based WAGO PFC devices, including 750-811x and 750-821x models.

## Step 2 Status

Static structure analysis smoke test completed successfully.
