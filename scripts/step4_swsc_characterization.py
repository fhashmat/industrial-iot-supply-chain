#!/usr/bin/env python3

"""
Step 4 - SWSC Characterization

Smoke-test version.

Current purpose:
- Store manually verified component/version evidence for WAGO PFC100/200.
- Write a CVE-ready CSV.

Future purpose:
- Read Step 3 dependency outputs.
- Map library names to upstream components.
- Extract versions automatically from filenames, metadata, and strings.
- Produce full SWSC and CVE input tables.
"""

import csv
from pathlib import Path

OUT = Path("outputs/wago/pfc100_200/step4_swsc_characterization/stageC_cve_mapping/cve_input_smoke_test_from_script.csv")
OUT.parent.mkdir(parents=True, exist_ok=True)

rows = [
    {
        "Tool": "WAGO-PFC100-200",
        "Version": "4.9.1(31)",
        "BinaryPackage": "openssl",
        "SourcePackage": "openssl",
        "UpstreamProject": "openssl",
        "VersionOnly": "3.2.4",
        "LibraryCategory": "Crypto/Security",
        "LibraryEvidence": "libcrypto.so.3 / libssl.so.3",
        "Status": "VersionExtracted",
        "Notes": "OpenSSL version extracted from libcrypto string",
    },
    {
        "Tool": "WAGO-PFC100-200",
        "Version": "4.9.1(31)",
        "BinaryPackage": "zlib",
        "SourcePackage": "zlib",
        "UpstreamProject": "zlib",
        "VersionOnly": "1.3.1",
        "LibraryCategory": "Compression",
        "LibraryEvidence": "libz.so.1.3.1",
        "Status": "VersionExtracted",
        "Notes": "zlib version inferred from library filename",
    },
    {
        "Tool": "WAGO-PFC100-200",
        "Version": "4.9.1(31)",
        "BinaryPackage": "libxml2",
        "SourcePackage": "libxml2",
        "UpstreamProject": "libxml2",
        "VersionOnly": "2.13.8",
        "LibraryCategory": "Parsing",
        "LibraryEvidence": "libxml2.so.2.13.8",
        "Status": "VersionExtracted",
        "Notes": "libxml2 version inferred from library filename",
    },
]

fieldnames = [
    "Tool",
    "Version",
    "BinaryPackage",
    "SourcePackage",
    "UpstreamProject",
    "VersionOnly",
    "LibraryCategory",
    "LibraryEvidence",
    "Status",
    "Notes",
]

with OUT.open("w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f"[OK] Wrote {OUT}")
