"""
Risk Assessment and Principal Mining Hazards (PMH) Module.
Implements ISO 31000:2009, DGMS (Tech) Circular No. 02 of 2020, and Figure 3.4.
5x5 Risk Matrix: Likelihood (1-5) x Consequence (1-5) = Risk Score (1-25).
"""
from typing import List, Dict, Any

LIKELIHOOD_LABELS = {
    1: "1 - Rare (Once in 10+ years)",
    2: "2 - Unlikely (Once in 3 to 10 years)",
    3: "3 - Possible (Once in 1 to 3 years)",
    4: "4 - Likely (Several times a year)",
    5: "5 - Almost Certain (Weekly or ongoing)"
}

CONSEQUENCE_LABELS = {
    1: "1 - Insignificant (First aid, no lost work time)",
    2: "2 - Minor (Lost time injury < 20 days)",
    3: "3 - Moderate (Reportable serious injury, localized damage)",
    4: "4 - Major (Permanent disability, single fatality, extensive stoppage)",
    5: "5 - Catastrophic (Multiple fatalities, mine-wide destruction)"
}

def calculate_risk_level(score: int) -> Dict[str, str]:
    """Classifies risk score into DGMS risk category, color code, and action protocol."""
    if score >= 16:
        return {
            "level": "Critical / Extreme",
            "color": "#e53e3e",
            "action": "INTOLERABLE: Work must cease immediately. Immediate engineering controls and re-assessment required before restart."
        }
    elif score >= 10:
        return {
            "level": "High",
            "color": "#dd6b20",
            "action": "UNACCEPTABLE: Action plan must be executed within 7 days. Escalated senior management inspection mandated."
        }
    elif score >= 5:
        return {
            "level": "Medium",
            "color": "#d69e2e",
            "action": "TOLERABLE: Specific Standard Operating Procedures (SOPs) and weekly supervisor audit required."
        }
    else:
        return {
            "level": "Low",
            "color": "#38a169",
            "action": "ACCEPTABLE: Manage by routine procedures, training, and continuous safety awareness."
        }

DEFAULT_HAZARDS = [
    {
        "id": "HAZ-001",
        "category": "Slope & Ground Stability",
        "description": "Highwall slope failure, bench collapse, or rock-fall during excavation",
        "likelihood": 3,
        "consequence": 5,
        "controls": [
            "Maintain bench height <= machine reach per CMR Reg 106",
            "Install continuous Slope Stability Radar (SSR) for pits > 100m (DGMS Circ 06/2021)",
            "Weekly tension crack dilation monitoring; TARP trigger at 5mm/day",
            "Establish safety berms and clear accumulated talus from benches"
        ],
        "regulation": "CMR 2017 Reg 106 & DGMS Tech Circ 06/2021"
    },
    {
        "id": "HAZ-002",
        "category": "Haul Road & Mobile Plant",
        "description": "Heavy dumper collision, runaway truck, or dumper tipping over bench edge",
        "likelihood": 4,
        "consequence": 4,
        "controls": [
            "Maintain haul road gradient <= 1 in 16 (CMR Reg 83/84)",
            "Construct continuous earthen berms >= tyre diameter of 240T dumper (2.7m)",
            "Enforce 3x dumper width on two-way traffic routes",
            "Fit proximity detection systems and rear-view cameras on all haul trucks"
        ],
        "regulation": "CMR 2017 Reg 83/84 & DGMS Circ 09/2008"
    },
    {
        "id": "HAZ-003",
        "category": "Explosives & Blasting",
        "description": "Flyrock projection outside blast boundary, ground vibration exceeding structural limits",
        "likelihood": 2,
        "consequence": 5,
        "controls": [
            "Strict evacuation of 500m danger zone with manned red flag sentries (CMR Reg 171)",
            "Three-stage blasting siren protocol (10 min, 2 min, all-clear)",
            "Deploy electronic delay detonators and conveyor belt wire-mesh muffling for controlled blasts",
            "Monitor Peak Particle Velocity (PPV <= 10 mm/s) at nearby structures"
        ],
        "regulation": "CMR 2017 Reg 171 & 186"
    },
    {
        "id": "HAZ-004",
        "category": "Inundation & Water Inrush",
        "description": "Sudden breaching of waterlogged old workings or surface river inundation",
        "likelihood": 2,
        "consequence": 5,
        "controls": [
            "Maintain 60m barrier from waterlogged workings without DGMS approval (CMR Reg 149)",
            "Drive 3-metre advance exploratory boreholes and 30-degree flank holes at 4.5m spacing",
            "Construct peripheral diversion bunds and check monsoon sump pumping capacity"
        ],
        "regulation": "CMR 2017 Reg 149"
    },
    {
        "id": "HAZ-005",
        "category": "Ventilation & Mine Gases",
        "description": "Accumulation of methane (CH4) leading to flammable gas ignition or asphyxiation",
        "likelihood": 3,
        "consequence": 5,
        "controls": [
            "Maintain minimum 6.0 m3/min airflow per person in largest shift (CMR Reg 153)",
            "Continuous telemetric monitoring of CH4 at face and returns",
            "Automatic power shutoff calibrated when CH4 reaches 1.25%",
            "Deploy flameproof apparatus and carry Self-Contained Self-Rescuers (SCSR)"
        ],
        "regulation": "CMR 2017 Reg 153 & 155"
    }
]

class RiskMatrixManager:
    def __init__(self, hazards: List[Dict[str, Any]] = None):
        self.hazards = hazards or [dict(h) for h in DEFAULT_HAZARDS]
        self._calculate_all_scores()

    def _calculate_all_scores(self):
        for h in self.hazards:
            score = h["likelihood"] * h["consequence"]
            h["risk_score"] = score
            level_info = calculate_risk_level(score)
            h["risk_level"] = level_info["level"]
            h["color"] = level_info["color"]
            h["action_protocol"] = level_info["action"]

    def add_custom_hazard(self, category: str, description: str, likelihood: int, consequence: int, controls: List[str], regulation: str):
        new_id = f"HAZ-{len(self.hazards) + 1:03d}"
        entry = {
            "id": new_id,
            "category": category,
            "description": description,
            "likelihood": likelihood,
            "consequence": consequence,
            "controls": controls,
            "regulation": regulation
        }
        self.hazards.append(entry)
        self._calculate_all_scores()
        return entry
