"""
Automated Safety Management Plan (SMP) Generator.
Strictly implements the 10-Section structure defined in Appendix C of the Project Report.
Incorporates mine-specific operational inputs, hybrid-retrieved statutory clauses,
and Principal Mining Hazard risk registers.
"""
from typing import Dict, Any, List
from datetime import datetime
from src.smp_generator.risk_assessment import RiskMatrixManager

class SafetyManagementPlanGenerator:
    def __init__(self):
        self.risk_manager = RiskMatrixManager()

    def generate_plan(self, mine_params: Dict[str, Any], retrieved_statutory_chunks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generates the 10-Section statutory draft SMP document.
        """
        mine_name = mine_params.get("mine_name", "Gevra Opencast Coal Project")
        company = mine_params.get("company", "South Eastern Coalfields Limited (SECL)")
        mine_type = mine_params.get("mine_type", "Opencast Coal Mine")
        capacity = mine_params.get("capacity", "50.0 MTPA")
        pit_depth = mine_params.get("pit_depth", "120 metres")
        workforce = mine_params.get("workforce", "2,450 personnel")
        manager_name = mine_params.get("manager_name", "First Class Certified Mine Manager")
        safety_officer = mine_params.get("safety_officer", "Chief Safety Officer, Mining Engineering")
        date_str = datetime.now().strftime("%B %d, %Y")

        # Compile section references from retrieved chunks
        statutory_citations = []
        for c in retrieved_statutory_chunks:
            statutory_citations.append(f"- **{c.get('doc_id')}**: {c.get('doc_title')} ({c.get('section_clause')}, Page {c.get('page_number')})")
        citations_text = "\n".join(statutory_citations) if statutory_citations else "- DGMS The Coal Mines Regulations, 2017 (Regulation 104, 106, 83, 171, 153)\n- The Mines Act, 1952 (Sections 18, 23)\n- DGMS (Tech) Circular No. 02 of 2020 (HIRA Guidelines)"

        # Parse numeric depth safely
        import re
        depth_digits = re.search(r'\d+(\.\d+)?', str(pit_depth))
        depth_val = float(depth_digits.group(0)) if depth_digits else 100.0
        ultimate_depth = depth_val * 1.75

        # 1. Mine Identification
        sec1 = f"""### Section 1: Mine Identification and Operational Description
- **Mine Name:** {mine_name}
- **Operating Organization:** {company}
- **Mine Classification:** Large-scale Mechanised {mine_type}
- **Annual Production Capacity:** {capacity}
- **Current Working Depth:** {pit_depth} (Ultimate planned depth: {ultimate_depth:.1f} m)
- **Total Registered Workforce:** {workforce}
- **Primary Machinery Deployed:** Shovel-Dumper Combination (Electric Rope Shovels 42 m³, Rear Dumpers 240T capacity, Rotary Blast Hole Drills 311mm).
- **Geographical & Geotechnical Setting:** Gondwana Supergroup Coal Measures, stratified sandstone and shale overburden, sub-tropical monsoon region."""

        # 2. Scope and Objectives
        sec2 = f"""### Section 2: Scope and Objectives of the Safety Management Plan
- **Primary Goal:** Achieve Zero Harm and eliminate lost-time injuries (LTI) through systematic preventive safety engineering.
- **Operational Scope:** Encompasses all excavation benches, overburden spoil dumps, internal and arterial haul roads, magazine and blasting operations, electrical substations, maintenance workshops, and surface civil infrastructure.
- **Statutory Mandate:** Formulated in mandatory compliance with **Regulation 104 of The Coal Mines Regulations, 2017**, and DGMS (Tech) Circular No. 02 of 2020.
- **Target Performance Indicators:**
  - Zero fatal or reportable accidents;
  - 100% adherence to DGMS bench geometry and haul road berm specifications;
  - Zero unmonitored tension crack propagation on highwalls."""

        # 3. Applicable Statutory and Regulatory References
        sec3 = f"""### Section 3: Applicable Statutory and Regulatory References
The operations and safety protocols in this plan are strictly governed by:
{citations_text}
- **ISO 31000:2009 / ISO 45001:2018:** Principles of Occupational Health and Safety Management Systems."""

        # 4. Hazards and Risk Assessment
        hazards = self.risk_manager.hazards
        hazard_rows = []
        for h in hazards:
            hazard_rows.append(
                f"| `{h['id']}` | **{h['category']}** | {h['description']} | {h['likelihood']} | {h['consequence']} | **{h['risk_score']}** | <span style='color:{h['color']};font-weight:bold'>{h['risk_level']}</span> | {h['action_protocol']} |"
            )
        sec4 = f"""### Section 4: Mine-Specific Hazards and Risk Assessment (HIRA)
In accordance with DGMS (Tech) Circular 02 of 2020, risks have been evaluated using an objective 5x5 Likelihood vs Consequence matrix:

| Hazard ID | Category | Hazard Description | Likelihood (1-5) | Consequence (1-5) | Risk Score | Risk Category | Action Protocol |
|:---|:---|:---|:---:|:---:|:---:|:---|:---|
{chr(10).join(hazard_rows)}"""

        # 5. Proposed Preventive and Control Measures
        sec5 = f"""### Section 5: Proposed Preventive and Control Measures (Hierarchy of Controls)
1. **Slope Stability and Bench Controls (CMR Reg 106 & DGMS Circ 06/2021):**
   - Hard rock bench height strictly limited to maximum excavator digging reach (15.0m maximum);
   - Active bench floor width maintained at not less than 35m (bench height + 3x machine width);
   - Continuous real-time Slope Stability Radar (SSR) monitoring with automated TARP triggers;
   - Minimum catch berms cleaned weekly to prevent rolling rock hazards.
2. **Haul Road and Traffic Controls (CMR Reg 83/84 & DGMS Circ 09/2008):**
   - Maximum road gradient maintained at 1 in 16;
   - Strong continuous earthen berms constructed along all drop-offs at height >= tyre diameter (2.7m);
   - Segregated heavy dumper traffic from light vehicles with dedicated pedestrian walkways;
   - Anti-collision radar and fatigue monitoring systems active on 100% of haul trucks.
3. **Blasting and Explosives Controls (CMR Reg 171 & 186):**
   - Compulsory 500-metre radius danger zone evacuation verified by sentry checkpoints;
   - Electronic delay detonators with non-electric shocktube initiation;
   - Conveyor belt and steel-mesh muffling for blasts near periphery."""

        # 6. Roles and Responsibilities
        sec6 = f"""### Section 6: Statutory Roles and Key Responsibilities
- **Mine Manager ({manager_name}):** Overall statutory responsibility under Mines Act Section 18 for safety enforcement, resource allocation, and annual SMP review.
- **Safety Officer ({safety_officer}):** Formulation of HIRA, daily risk monitoring, incident investigation, internal safety audits, and DGMS liaison.
- **Overman / Foremen:** Direct shift supervision, verification of pre-shift bench stability, haul road condition inspections, and statutory logbook recording.
- **Mining Sirdar:** Pre-shift inspection of working faces, loose rock dressing, sentry posting during blasting, and immediate withdrawal of workers in unsafe conditions.
- **Blasting Officer:** Safe storage, transport, charging, danger zone clearance, and post-blast misfire examinations."""

        # 7. Emergency Preparedness and Response Arrangements
        sec7 = f"""### Section 7: Emergency Preparedness and Disaster Management Arrangements
- **Emergency Control Center (ECC):** Fully equipped round-the-clock control room with redundant VHF, cellular, and public address communication.
- **Trigger Action Response Plan (TARP):**
  - *Level 1 (Normal Operations):* Routine monitoring, crack dilation < 2 mm/day.
  - *Level 2 (Amber Alert):* Crack dilation 2-5 mm/day or abnormal gas spike -> Operations slowed, geotechnical re-survey ordered.
  - *Level 3 (Red Alert):* Crack dilation > 5 mm/day or heavy seepage -> Immediate siren sounding, complete bench evacuation within 10 minutes.
- **Medical & Rescue Services:** 2 Advanced Life Support ambulances stationed at pit-head, fully equipped Occupational Health Center, certified mine rescue brigade on stand-by.
- **Mock Drills:** Quarterly simulated disaster evacuations conducted and logged."""

        # 8. Inspection, Monitoring and Review Requirements
        sec8 = f"""### Section 8: Inspection, Monitoring, and Continual Review
- **Daily:** Mining Sirdar pre-shift inspection, dumper pre-start checklists, haul road dust suppression logs.
- **Weekly:** Joint safety committee inspections with trade union representatives; SSR data calibration.
- **Monthly:** Full Pit Safety Audit by Manager and Safety Officer; review of near-miss reporting.
- **Annual Statutory Review:** Mandatory comprehensive SMP re-evaluation under CMR 2017 Regulation 104(3)."""

        # 9. Source References and Document Traceability
        sec9 = f"""### Section 9: Source References and Knowledge Traceability
All control specifications, numerical thresholds, and hazard classifications are traced back to the following authoritative records:
{citations_text}"""

        # 10. Review and Approval Record
        sec10 = f"""### Section 10: Review and Approval Record

> [!WARNING]
> **STATUTORY DRAFT NOTICE:**
> This document is an AI-generated draft Safety Management Plan produced by the Mine SLM platform. Under the Mines Act, 1952 and Coal Mines Regulations, 2017 (Regulation 104), this document does not possess legal validity until thoroughly reviewed, verified, and officially signed by the certified Mine Manager and approved by the Internal Safety Committee.

| Role | Name & Designation | Statutory Certificate No. | Signature & Date |
|:---|:---|:---:|:---:|
| **Prepared By (Safety Officer)** | {safety_officer} | DGMS-SO-2024-889 | `[ Pending Verification ]` |
| **Reviewed By (Geotechnical Expert)** | Geotechnical Engineer | MHRD-GT-2022-104 | `[ Pending Verification ]` |
| **Approved By (Mine Manager)** | {manager_name} | FCC-1st-Class-Mining-451 | `[ Pending Final Approval ]` |

*Plan Generated on: {date_str} via Mine SLM Platform (NITK Surathkal)*"""

        full_markdown = "\n\n".join([
            f"# SAFETY MANAGEMENT PLAN (SMP)\n**{mine_name}**\n*Prepared pursuant to Regulation 104 of The Coal Mines Regulations, 2017*\n",
            sec1, sec2, sec3, sec4, sec5, sec6, sec7, sec8, sec9, sec10
        ])

        return {
            "title": f"Safety Management Plan: {mine_name}",
            "generated_at": date_str,
            "markdown": full_markdown,
            "sections": {
                "1_mine_identification": sec1,
                "2_scope_objectives": sec2,
                "3_statutory_references": sec3,
                "4_hazard_risk_assessment": sec4,
                "5_preventive_controls": sec5,
                "6_roles_responsibilities": sec6,
                "7_emergency_arrangements": sec7,
                "8_inspection_monitoring": sec8,
                "9_source_traceability": sec9,
                "10_review_approval": sec10
            }
        }
