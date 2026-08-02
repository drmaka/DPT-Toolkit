"""Operational anchors for Discovery Complexity.

Anchors are explicit, auditable defaults—not natural laws. Projects should adapt
and preregister them where domain conditions differ materially.
"""
from __future__ import annotations

COMPONENTS = ("time", "concept", "search", "experiment", "compute", "coordination")

ANCHORS = {
"time": [
 {"score":0,"label":"Negligible","anchor":"<= 1 working day to make the question available","evidence":"dated notes or existing artefact"},
 {"score":1,"label":"Low","anchor":">1 day to 4 weeks","evidence":"work plan or retrospective timeline"},
 {"score":2,"label":"Moderate","anchor":">1 to 6 months","evidence":"milestones and staff allocation"},
 {"score":3,"label":"High","anchor":">6 to 24 months","evidence":"project records or historical reconstruction"},
 {"score":4,"label":"Very high","anchor":">24 months, or duration cannot be bounded without a major programme","evidence":"programme-level plan or primary historical sources"}],
"concept": [
 {"score":0,"label":"Negligible","anchor":"Direct restatement inside existing terminology; no new relation or category"},
 {"score":1,"label":"Low","anchor":"One familiar relation transferred within the same subfield"},
 {"score":2,"label":"Moderate","anchor":"Combines multiple known constructs or crosses adjacent subfields"},
 {"score":3,"label":"High","anchor":"Requires a new abstraction, mechanism, ontology link, or substantial reframing"},
 {"score":4,"label":"Very high","anchor":"Requires new foundational categories or challenges prevailing explanatory structure"}],
"search": [
 {"score":0,"label":"Negligible","anchor":"Target and evidence already identified; <= 10 relevant items or <= 20 candidate states"},
 {"score":1,"label":"Low","anchor":"11-50 relevant items or 21-100 candidate states"},
 {"score":2,"label":"Moderate","anchor":"51-250 relevant items or 101-1,000 candidate states"},
 {"score":3,"label":"High","anchor":"251-1,000 relevant items or 1,001-100,000 candidate states"},
 {"score":4,"label":"Very high","anchor":">1,000 relevant items, >100,000 states, open-ended search, or no defensible finite bound"}],
"experiment": [
 {"score":0,"label":"Negligible","anchor":"No new experiment; uses existing observations or purely analytic reasoning"},
 {"score":1,"label":"Low","anchor":"Single pilot, simulation, archival extraction, or routine laboratory procedure"},
 {"score":2,"label":"Moderate","anchor":"Multiple runs/sites or specialised equipment with standard approvals"},
 {"score":3,"label":"High","anchor":"Longitudinal, multi-site, rare sample, custom instrument, or substantial regulatory burden"},
 {"score":4,"label":"Very high","anchor":"Unique facility, hazardous/mission-critical setting, very rare event, or international trial-scale programme"}],
"compute": [
 {"score":0,"label":"Negligible","anchor":"Spreadsheet/hand calculation or <1 CPU-hour; <1 GB working data"},
 {"score":1,"label":"Low","anchor":"1-100 CPU-hours; no accelerator required; <=100 GB"},
 {"score":2,"label":"Moderate","anchor":"101-10,000 CPU-hours or <=1,000 GPU-hours; <=10 TB"},
 {"score":3,"label":"High","anchor":"10,001-1,000,000 CPU-hours or 1,001-100,000 GPU-hours; distributed infrastructure"},
 {"score":4,"label":"Very high","anchor":">1,000,000 CPU-hours, >100,000 GPU-hours, exascale/special-purpose compute, or presently unavailable capability"}],
"coordination": [
 {"score":0,"label":"Negligible","anchor":"One investigator; no external approval or dependency"},
 {"score":1,"label":"Low","anchor":"2-5 people in one unit; <=1 routine approval"},
 {"score":2,"label":"Moderate","anchor":"6-20 people or 2-3 units/institutions; multiple scheduled dependencies"},
 {"score":3,"label":"High","anchor":"21-100 people, 4-10 institutions, or complex ethics/regulatory/data agreements"},
 {"score":4,"label":"Very high","anchor":">100 people, >10 institutions/countries, mission-level governance, or unresolved legal/sovereign dependencies"}]
}

DOMAIN_NOTES = {
 "generic":"Use quantitative evidence where available; use the highest applicable anchor when indicators disagree, then record why.",
 "medicine":"Treat participant risk, ethics approval, recruitment rarity and clinical-site dependencies as experiment/coordination evidence; never replace ethical review with DPT.",
 "physics":"Record facility scarcity, beam/instrument time, detector construction, compute and collaboration scale separately.",
 "ai":"Record data acquisition, benchmark leakage controls, accelerator hours, model/API dependence, and reproducibility constraints.",
 "economics":"Record data access/licensing, identification strategy, institutional heterogeneity, longitudinal coverage, and stakeholder coordination.",
 "social_science":"Record sampling access, fieldwork duration, translation/cultural adaptation, ethics, and multi-site coordination."
}

def score_from_indicator(component: str, value: float) -> int:
    """Deterministic numeric helper for components with numeric anchors.

    Value semantics: time=days, search=item/state count (items preferred), compute=CPU-hours,
    coordination=people. Experiment and concept require anchored human coding.
    """
    if component == 'time':
        return 0 if value <= 1 else 1 if value <= 28 else 2 if value <= 183 else 3 if value <= 730 else 4
    if component == 'search':
        return 0 if value <= 10 else 1 if value <= 50 else 2 if value <= 250 else 3 if value <= 1000 else 4
    if component == 'compute':
        return 0 if value < 1 else 1 if value <= 100 else 2 if value <= 10000 else 3 if value <= 1_000_000 else 4
    if component == 'coordination':
        return 0 if value <= 1 else 1 if value <= 5 else 2 if value <= 20 else 3 if value <= 100 else 4
    raise ValueError(f"No purely numeric auto-anchor for {component}; use evidence-based coding.")
