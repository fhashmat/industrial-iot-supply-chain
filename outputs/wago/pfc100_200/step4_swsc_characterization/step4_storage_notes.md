# Step 4 SWSC Characterization Storage Notes

Step 4 reuses the SecElf Stage B/B1/C logic, but firmware analysis requires an adapter.

The original SecElf Stage B resolves packages using host package managers such as rpm or dpkg. This is suitable for installed Linux tools, but not directly suitable for an extracted ARM firmware root filesystem on macOS.

For the WAGO smoke test, Step 4 is organized into:

- inputs: dependency evidence from Step 3
- stageB_component_mapping: library-to-component mapping
- stageB1_dependency_metadata: SecElf-compatible dependency metadata
- stageC_cve_mapping: CVE mapping outputs
- results: final SWSC profile and CVE summary
- logs: execution logs

Current file:

- stageB1_dependency_metadata/dependency_risk_metadata_initial.csv

This file is an initial SecElf-compatible placeholder. Version extraction is pending.
