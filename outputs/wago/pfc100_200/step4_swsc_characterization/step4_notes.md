# Step 4 SWSC Characterization - WAGO PFC100/200

## Goal

Characterize the firmware software supply chain surface using dependency and binary metadata from Step 3.

## Inputs

- shared_libraries.txt
- unique_needed_libraries.txt
- needed_library_frequency_top30.txt
- readelf_needed_soname.txt

## Planned Process

1. Identify third-party/open-source components from library evidence.
2. Extract or infer component versions where possible.
3. Classify components by function, such as crypto, networking, IPC, compression, parsing, and vendor-specific libraries.
4. Reuse or adapt the SecElf CVE mapping script for known component-to-CVE matching.
5. Produce SWSC profile and CVE mapping outputs.

## Current Status

Initial SWSC profile created manually from Step 3 dependency evidence. CVE mapping script integration is pending.
