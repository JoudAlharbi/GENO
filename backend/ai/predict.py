from typing import Dict, List
try:
    from cyvcf2 import VCF
    HAS_CYVCF2 = True
except Exception:
    HAS_CYVCF2 = False
from .snp_panel import SNP_PANEL

def _fallback_parse(file_path: str):
    seen = set()
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            if line.startswith("#"): continue
            cols = line.strip().split()
            if len(cols) >= 3:
                seen.add(cols[2])  # rsID
    return seen

def run_analysis_with_model(file_path: str) -> Dict:
    rsids = set()
    if HAS_CYVCF2:
        for rec in VCF(file_path):
            if rec.ID: rsids.add(rec.ID)
    else:
        rsids = _fallback_parse(file_path)

    markers: List[Dict] = []
    count = 0
    for item in SNP_PANEL:
        if item["rsid"] in rsids:
            count += 1
            markers.append({
                "gene": item["gene"], "locus": item["locus"],
                "variant": item["rsid"], "acmg": item.get("acmg","N/A"),
                "evidence": item.get("evidence","N/A")
            })
    prob = count / max(len(SNP_PANEL), 1)
    risk = "Low" if prob < 0.33 else ("Moderate" if prob < 0.66 else "High")
    return {"risk_level": risk, "score": round(float(prob), 3), "markers": markers}