# WAGO Firmware Smoke Test Summary

## Scope

This smoke test validates the first end-to-end pipeline on one Set A vendor/device family.

- Vendor: WAGO
- Device family: PFC100/200 G2
- Firmware: Firmware PFC100/200 4.9.1(31)
- File: Firmware_PFC100_PFC200_040901_31.zip
- Release date: 2026-05-05
- SHA256: 01e1329dc89cabe2985ca6c3c757952f2e75b8b86eb84d2f9fe505d6390cf939

## Step 1: Firmware Acquisition and Curation

The WAGO firmware package was downloaded from the public WAGO Download Center. Metadata, file size, release date, and SHA256 hash were recorded.

Output:
- data/set_a/wago_firmware_inventory.csv

## Step 2: Static Structure Analysis

The firmware ZIP contained:

- SD-card image: PFC-G2-Linux_sd_V040901_31_r9d0900aaed.img
- Update package: PFC-G2-Linux_update_V040901_31_r9d0900aaed.wup

The .wup file contained:

- package-info.xml
- RAUC bundle: PFC-G2-Linux_update_V040901_31_r9d0900aaed.raucb

The RAUC bundle contained:

- manifest.raucm
- root.tar.gz
- bootloader-related files
- update hooks

The extracted root filesystem identified itself as:

- PTXdist / WAGO-PFC
- PTXdist version: 2024.12.0
- Kernel: Linux-6.6.94-rt56-w05.08.02
- Architecture: Linux/ARM

Output:
- outputs/wago/pfc100_200/step2_static_structure/

## Step 3: Dependency Structure Extraction

The extracted root filesystem was scanned for shared libraries.

Results:

- Shared library files found: 453
- ELF shared libraries: 453
- Total NEEDED dependency references: 1259
- Unique dependency names: 105

Top dependencies included libc, libxtables, libm, glib, OpenSSL, D-Bus, zlib, libxml2, and WAGO-specific libraries.

Output:
- outputs/wago/pfc100_200/step3_dependency_structure/

## Step 4: SWSC Characterization and CVE Candidate Mapping

Three components were manually versioned for the smoke test:

| Component | Version | Evidence |
|---|---:|---|
| OpenSSL | 3.2.4 | strings from libcrypto.so.3 |
| zlib | 1.3.1 | library filename libz.so.1.3.1 |
| libxml2 | 2.13.8 | library filename libxml2.so.2.13.8 |

The CVE mapping script scanned the local cvelistV5 database.

Results:

- CVE JSON files scanned: 349,307
- Total candidate CVE matches: 42
- OpenSSL matches: 31
- libxml2 matches: 8
- zlib matches: 3

These are candidate CVE matches and require later validation against vendor patches, affected-version rules, and firmware build context.

Output:
- outputs/wago/pfc100_200/step4_swsc_characterization/

## Status

End-to-end smoke test completed successfully.
