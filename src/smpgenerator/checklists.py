"""
Operational Safety Checklists & Audit Forms (Section 3.3.6).
Provides structured, actionable checklists for statutory mine personnel
(Mine Manager, Safety Officer, Overman, Mining Sirdar, Blasting Officer).
"""
from typing import List, Dict, Any

STANDARD_CHECKLISTS = {
    "bench_stability": {
        "title": "Pre-Shift Opencast Bench & Slope Stability Checklist",
        "role": "Mining Sirdar / Overman",
        "statutory_ref": "CMR 2017 Regulation 106 & DGMS Circular 06/2021",
        "items": [
            {"id": "BS-1", "question": "Are all bench heights within the certified digging reach of active shovels/excavators?", "standard": "<= 15.0m in hard rock, <= 3.0m in alluvium"},
            {"id": "BS-2", "question": "Is the active bench floor width at least equal to bench height plus 3x machine width?", "standard": ">= 35m for 240T dumpers"},
            {"id": "BS-3", "question": "Are highwalls free from loose boulders, undercuts, and overhangs?", "standard": "No loose overhangs permitted"},
            {"id": "BS-4", "question": "Has tension crack inspection been conducted along the pit crest?", "standard": "Dilation < 5 mm/day on SSR / GPS markers"},
            {"id": "BS-5", "question": "Are toe drains cleared to prevent water saturation at the base of slopes?", "standard": "Effective positive drainage maintained"}
        ]
    },
    "haul_road_audit": {
        "title": "Haul Road, Dumper & Berm Safety Audit",
        "role": "Safety Officer / Mechanical Engineer",
        "statutory_ref": "CMR 2017 Regulation 83 & 84, DGMS Circular 09/2008",
        "items": [
            {"id": "HR-1", "question": "Is the haul road gradient maintained at 1 in 16 or flatter?", "standard": "<= 1 in 16 (short ramps <= 1 in 10)"},
            {"id": "HR-2", "question": "Are continuous earthen berms maintained along drop-off edges (> 2m)?", "standard": "Height >= Wheel diameter of 240T dumper (2.7m)"},
            {"id": "HR-3", "question": "Is the haul road width at least 3 times the width of the widest truck?", "standard": ">= 30-35m for 240T heavy dumpers"},
            {"id": "HR-4", "question": "Are dust suppression water tankers spraying at scheduled 45-min intervals?", "standard": "Adequate visibility maintained, zero hydroplaning"},
            {"id": "HR-5", "question": "Are retro-reflective signboards and speed limit markers (max 30 km/h) legible?", "standard": "Full visibility day & night"}
        ]
    },
    "blasting_protocol": {
        "title": "Shotfiring & Blasting Danger Zone Clearance Protocol",
        "role": "Blasting Officer / Shotfirer",
        "statutory_ref": "CMR 2017 Regulation 171 & 186",
        "items": [
            {"id": "BL-1", "question": "Has the 500-metre radial danger zone been completely cleared of personnel?", "standard": "Strict 500m radius evacuation"},
            {"id": "BL-2", "question": "Are all entrance roads blocked and red-flag sentries stationed with VHF radios?", "standard": "100% barricaded access"},
            {"id": "BL-3", "question": "Was the 1st warning siren sounded 10 minutes prior to blast?", "standard": "Continuous 2-minute siren"},
            {"id": "BL-4", "question": "Was the 2nd warning siren sounded 2 minutes prior to firing?", "standard": "Intermittent 1-minute alert"},
            {"id": "BL-5", "question": "Was post-blast examination completed and no misfires detected before all-clear?", "standard": "Statutory inspection per Reg 186"}
        ]
    },
    "underground_ventilation": {
        "title": "Underground Ventilation & Hazardous Gas Monitoring Checklist",
        "role": "Ventilation Officer / Overman",
        "statutory_ref": "CMR 2017 Regulation 153 & 155",
        "items": [
            {"id": "UG-1", "question": "Is air quantity at least 6.0 m3/min per person or 2.5 m3/min per daily tonne?", "standard": "Complies with Reg 153 standard"},
            {"id": "UG-2", "question": "Is Methane (CH4) below 0.75% in general body and below 1.25% in return?", "standard": "<= 0.75% district return, <= 1.25% main return"},
            {"id": "UG-3", "question": "Is Carbon Monoxide (CO) within permissible limits (< 50 ppm)?", "standard": "Norm < 25-50 ppm; zero spontaneous heating"},
            {"id": "UG-4", "question": "Are automatic power cutoff sensors functional at working faces?", "standard": "Calibrated trip at 1.25% CH4"},
            {"id": "UG-5", "question": "Do 100% of underground personnel have functional Self-Contained Self-Rescuers?", "standard": "SCSR verified prior to man-riding"}
        ]
    }
}
