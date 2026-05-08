# Step 3 Dependency Structure Extraction - WAGO PFC100/200

## Input

Extracted WAGO PFC100/200 root filesystem from:

- Firmware package: Firmware PFC100/200 4.9.1(31)
- File: Firmware_PFC100_PFC200_040901_31.zip
- Root filesystem payload: root.tar.gz

## Method

The firmware root filesystem was scanned for shared libraries using filename patterns:

- `*.so`
- `*.so.*`

Each discovered library was checked with `file`, and dynamic dependency metadata was extracted with `greadelf -d`.

## Results

- Shared library files found: 453
- ELF shared libraries: 453
- Total `NEEDED` dependency references: 1259
- Unique dependency names: 105

## Top Referenced Libraries

The most frequently referenced libraries include:

- `libc.so.6`
- `libxtables.so.12`
- `libm.so.6`
- `libglib-2.0.so.0`
- `libgcc_s.so.1`
- `libstdc++.so.6`
- `ld-linux-armhf.so.3`
- `libcrypto.so.3`
- `libssl.so.3`
- `libdbus-1.so.3`

## Initial Observation

The firmware has a substantial Linux dependency surface, including core runtime libraries, networking/firewall libraries, cryptographic libraries, IPC/system-service libraries, and WAGO-specific libraries.
