#!/usr/bin/env python3

"""
Step 4 - CVE Mapping Smoke Test

Input:
- CVE-ready component CSV from Step 4 SWSC characterization
- Local cvelistV5 database

Output:
- CSV of matched CVEs for the smoke-test components
"""

import csv
import json
import re
from pathlib import Path

try:
    from tqdm import tqdm
except ImportError:
    tqdm = None


def iter_with_progress(items, desc="Processing CVEs"):
    if tqdm is not None:
        return tqdm(items, desc=desc, unit="file")

    total = len(items)

    def generator():
        for i, item in enumerate(items, 1):
            if i == 1 or i % 1000 == 0 or i == total:
                pct = (i / total) * 100 if total else 100
                print(f"[PROGRESS] {i}/{total} CVE files ({pct:.1f}%)", flush=True)
            yield item

    return generator()


INPUT_CSV = Path("outputs/wago/pfc100_200/step4_swsc_characterization/stageC_cve_mapping/cve_input_smoke_test_from_script.csv")
CVE_ROOT = Path("cvelistV5/cves")
OUT_CSV = Path("outputs/wago/pfc100_200/step4_swsc_characterization/stageC_cve_mapping/cve_matches_smoke_test.csv")


def norm(s):
    return (s or "").strip().lower()


def version_token(v):
    m = re.search(r"\d+(?:\.\d+)+", str(v or ""))
    return m.group(0) if m else norm(v)


def version_parts(v):
    return [int(x) for x in re.findall(r"\d+", version_token(v))]


def compare_versions(a, b):
    pa, pb = version_parts(a), version_parts(b)
    n = max(len(pa), len(pb))
    pa += [0] * (n - len(pa))
    pb += [0] * (n - len(pb))
    return (pa > pb) - (pa < pb)


def product_matches(dep_project, affected_item):
    candidates = [
        affected_item.get("product", ""),
        affected_item.get("packageName", ""),
        affected_item.get("vendor", ""),
    ]
    candidates = [norm(x) for x in candidates if x]

    aliases = {
        "openssl": ["openssl"],
        "zlib": ["zlib"],
        "libxml2": ["libxml2", "libxml"],
    }

    for alias in aliases.get(dep_project, [dep_project]):
        if alias in candidates:
            return True
    return False


def version_matches(dep_version, version_info):
    status = norm(version_info.get("status", ""))
    if status == "unaffected":
        return False

    v = version_token(version_info.get("version", ""))
    less_than = version_token(version_info.get("lessThan", ""))
    less_than_eq = version_token(version_info.get("lessThanOrEqual", ""))

    dep_v = version_token(dep_version)

    if v and dep_v == v:
        return True

    if less_than and compare_versions(dep_v, less_than) < 0:
        return True

    if less_than_eq and compare_versions(dep_v, less_than_eq) <= 0:
        return True

    if status == "affected" and not v and not less_than and not less_than_eq:
        return True

    return False


def extract_cve_id(data):
    return data.get("cveMetadata", {}).get("cveId", "")


def extract_published(data):
    return data.get("cveMetadata", {}).get("datePublished", "").split("T")[0]


def extract_title(data):
    return data.get("containers", {}).get("cna", {}).get("title", "")


def extract_description(data):
    descs = data.get("containers", {}).get("cna", {}).get("descriptions", [])
    for d in descs:
        if norm(d.get("lang", "")).startswith("en"):
            return d.get("value", "")
    return ""


def extract_cvss(data):
    cna = data.get("containers", {}).get("cna", {})
    metrics = cna.get("metrics", []) or []
    for metric in metrics:
        for key in ["cvssV4_0", "cvssV3_1", "cvssV3_0", "cvssV2_0"]:
            if key in metric:
                return metric[key].get("baseScore", "")
    return ""


def load_dependencies():
    deps = []
    with INPUT_CSV.open(newline="", errors="ignore") as f:
        reader = csv.DictReader(f)
        for row in reader:
            project = norm(row.get("UpstreamProject"))
            version = norm(row.get("VersionOnly"))
            if project and version:
                deps.append(row)
    return deps


def main():
    deps = load_dependencies()
    print(f"[INFO] Dependencies loaded: {len(deps)}")

    cve_files = list(CVE_ROOT.rglob("CVE-*.json"))
    print(f"[INFO] CVE files discovered: {len(cve_files)}")

    results = []

    for cve_path in iter_with_progress(cve_files):
        try:
            data = json.loads(cve_path.read_text(errors="ignore"))
        except Exception:
            continue

        affected = data.get("containers", {}).get("cna", {}).get("affected", []) or []

        for dep in deps:
            dep_project = norm(dep.get("UpstreamProject"))
            dep_version = norm(dep.get("VersionOnly"))

            for item in affected:
                if not product_matches(dep_project, item):
                    continue

                for ver_info in item.get("versions", []) or []:
                    if version_matches(dep_version, ver_info):
                        results.append({
                            "Tool": dep.get("Tool", ""),
                            "ToolVersion": dep.get("Version", ""),
                            "UpstreamProject": dep_project,
                            "DependencyVersion": dep_version,
                            "LibraryEvidence": dep.get("LibraryEvidence", ""),
                            "CVE ID": extract_cve_id(data),
                            "Published Date": extract_published(data),
                            "CVSS Score": extract_cvss(data),
                            "Title": extract_title(data),
                            "Description": extract_description(data),
                            "AffectedProduct": item.get("product", ""),
                            "AffectedVendor": item.get("vendor", ""),
                            "AffectedVersionRule": json.dumps(ver_info),
                            "CVEFile": str(cve_path),
                        })
                        break

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = [
        "Tool",
        "ToolVersion",
        "UpstreamProject",
        "DependencyVersion",
        "LibraryEvidence",
        "CVE ID",
        "Published Date",
        "CVSS Score",
        "Title",
        "Description",
        "AffectedProduct",
        "AffectedVendor",
        "AffectedVersionRule",
        "CVEFile",
    ]

    with OUT_CSV.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    print(f"[OK] Matches found: {len(results)}")
    print(f"[OK] Wrote: {OUT_CSV}")


if __name__ == "__main__":
    main()
