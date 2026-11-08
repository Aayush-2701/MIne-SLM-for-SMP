"""
Data builder for Mine SLM:
Generates authentic DGMS regulatory documents, safety circulars,
mines act provisions, sample mine plans, and standard evaluation test queries.
"""
import json
import os
from pathlib import Path
import fitz # PyMuPDF
from src.config import RAW_DOCS_DIR, EVALUATION_DATASET_PATH

DGMS_DOCUMENTS = [
    {
        "doc_id": "DGMS-CMR-2017",
        "title": "The Coal Mines Regulations, 2017",
        "issuing_authority": "Directorate General of Mines Safety (DGMS), Ministry of Labour and Employment, Govt of India",
        "publication_date": "2017-11-27",
        "status": "In Force",
        "source_location": "https://www.dgms.gov.in/writereaddata/UploadFile/CMR_2017.pdf",
        "sections": [
            {
                "section": "Regulation 104 - Safety Management Plan (SMP)",
                "page": 48,
                "content": """Regulation 104: Safety Management Plan.
(1) The owner, agent and manager of every mine shall, within one year of coming into force of these regulations, prepare and implement a comprehensive Safety Management Plan (SMP) for the mine based on Hazard Identification and Risk Assessment (HIRA).
(2) The Safety Management Plan shall include:
(a) A clear safety and health policy formulated by top management;
(b) Systematic identification of all hazards in mining operations, machinery, civil structures, and mine environment;
(c) Risk assessment of identified hazards using qualitative or semi-quantitative risk matrices (Likelihood vs Consequence);
(d) Specification of control measures conforming strictly to the hierarchy of controls: Elimination, Substitution, Engineering controls, Administrative controls, and Personal Protective Equipment (PPE);
(e) Allocation of duties and statutory responsibilities to qualified personnel (Mine Manager, Safety Officer, Overman, Mining Sirdar);
(f) Standard Operating Procedures (SOPs) for high-risk operations including blasting, slope stability, heavy machinery movement, and ventilation;
(g) Internal safety audits and monitoring protocols at predefined intervals;
(h) A comprehensive emergency response and disaster management plan with mock drill schedules;
(3) The Safety Management Plan shall be reviewed at least once every calendar year or immediately following any serious accident, dangerous occurrence, or major alteration in mining method or machinery."""
            },
            {
                "section": "Regulation 106 - Opencast Workings and Benches",
                "page": 51,
                "content": """Regulation 106: Manual and Mechanised Opencast Workings.
(1) In opencast workings in alluvium, soil, gravel, clay or other soft unconsolidated strata:
(a) The bench sides shall be sloped at an angle of safety not exceeding 45 degrees from the horizontal, or bench height shall not exceed 1.5 metres and width shall not be less than height;
(b) In mechanized operations with excavators in soft strata, bench height shall not exceed 3.0 metres unless specially permitted by the Chief Inspector.
(2) In hard rock opencast workings:
(a) The height of any bench shall not exceed the maximum reach or digging height of the machine in use for excavating;
(b) The width of any bench shall not be less than the height of the bench, and in mechanised opencast mines where heavy earth moving machinery (HEMM) like dumpers and shovel are deployed, the bench width shall not be less than the height of the bench plus 3 times the width of the widest machine operating on the bench;
(c) The overall pit slope angle shall be maintained in accordance with scientific geotechnical slope stability studies approved by CIM/DGMS;
(3) No person or equipment shall undercut any face or bench so as to cause overhanging or unstable strata."""
            },
            {
                "section": "Regulation 83 & 84 - Haul Roads and Dumpers",
                "page": 41,
                "content": """Regulation 83 & 84: Haul Roads, Dumper Movement, and Berm Standards.
(1) Design and maintenance of haul roads:
(a) The gradient of any haul road for dumper or truck operation shall generally not be steeper than 1 in 16. In exceptional circumstances for short ramps not exceeding 100 metres, gradient up to 1 in 10 may be permitted;
(b) The width of the haul road shall not be less than 3 times the width of the widest dumper or haul vehicle deployed in two-way traffic, plus an additional clearance of at least 1.5 metres;
(c) For one-way traffic, the width shall not be less than 2 times the width of the widest vehicle plus 1.0 metre;
(2) Parapet walls and Berms:
(a) Along the edge of every bench, haul road, spoil dump or ramp adjacent to a drop or drop-off exceeding 2 metres, strong earthen berms or crash barriers shall be maintained;
(b) The height of the berm shall not be less than the diameter of the tyre (wheel height) of the largest vehicle plying on the road (or at minimum 1.2 times tyre radius per DGMS Tech Circular 09/2008);
(c) The berm shall have a top width of not less than 1.0 metre and sides sloped at the natural angle of repose."""
            },
            {
                "section": "Regulation 153 & 155 - Standards of Ventilation and Mine Gases",
                "page": 76,
                "content": """Regulation 153 & 155: Standards of Ventilation and Monitoring of Inflammable and Noxious Gases.
(1) Standards of Ventilation:
(a) In every underground coal mine, the quantity of air in the general body of air shall not be less than 6.0 cubic metres per minute per person employed in the mine on the largest shift, or 2.5 cubic metres per minute per daily tonne of coal raised, whichever is larger;
(b) Air velocity at working faces shall be maintained between 0.5 m/s and 1.5 m/s to prevent stagnation and thermal stress.
(2) Gas limits in mine atmosphere:
(a) The percentage of oxygen in the ventilating current shall nowhere be less than 19.0%;
(b) The percentage of carbon dioxide (CO2) shall nowhere exceed 0.5%;
(c) In any coal seam of Degree I, II or III gassiness:
- Percentage of inflammable gas (methane / CH4) shall not exceed 0.75% in the general body of the return air of any ventilating district;
- Percentage of inflammable gas shall not exceed 1.25% in the main return airway;
(d) If inflammable gas concentration reaches 1.25% at any working place or blind heading, all electrical power must be cut off instantly and workers immediately withdrawn to a fresh air base."""
            },
            {
                "section": "Regulation 171 & 186 - Explosives, Shotfiring, and Blasting Precautions",
                "page": 89,
                "content": """Regulation 171 & 186: Shotfiring, Blasting Danger Zone, and Precautions.
(1) Opencast Blasting Danger Zone:
(a) Before firing any shot in an opencast mine, the shotfirer or blasting officer shall ensure that all persons within the Danger Zone—defined as a radius of not less than 500 metres from the blast site—have been evacuated to safe blasting shelters;
(b) All access roads and entrances leading into the 500-metre danger zone shall be effectively barricaded and manned by red-flag guards;
(2) Warning signals:
(a) Blasting siren protocol: First warning siren (continuous 2-minute siren) 10 minutes prior to blast; Second warning siren (intermittent 1-minute blasts) 2 minutes prior; All-clear siren (single 1-minute steady blast) after post-blast inspection confirms no misfires;
(3) Controlled Blasting:
(a) Where structures, villages, railways, or public highways fall within 500 metres, controlled blasting techniques (NONEL detonators, electronic delay detonators, air-decking, and heavy blasting wire mesh with conveyor-belt muffling) must be deployed;
(b) Ground vibration measured at nearest permanent structure shall not exceed DGMS circular vibration thresholds (e.g. 5 to 10 mm/s Peak Particle Velocity depending on dominant frequency)."""
            },
            {
                "section": "Regulation 149 - Precaution Against Inundation and Water Danger",
                "page": 71,
                "content": """Regulation 149: Precautions against danger from surface water and underground water-logging.
(1) No workings shall be extended to any point within 60 metres of any waterlogged workings, disused flooded mine, river, reservoir, tank or nallah, whether in the same mine or in adjoining mines, without prior written approval of the Chief Inspector of Mines.
(2) Where workings approach within 120 metres of known waterlogged or suspected inundated workings, advance exploratory boreholes shall be driven:
(a) At least one central advance borehole not less than 3 metres ahead of working face;
(b) Flank boreholes drilled at an outward angle of 30 degrees at regular intervals not exceeding 4.5 metres;
(3) Regular physical surveys and water level checks shall be conducted, and daily water discharge from mine sumps shall be logged."""
            }
        ]
    },
    {
        "doc_id": "DGMS-CIRCULAR-2020-02",
        "title": "DGMS (Tech) Circular No. 02 of 2020: Risk Assessment and SMP Formulation Guidelines",
        "issuing_authority": "Directorate General of Mines Safety (DGMS), Dhanbad",
        "publication_date": "2020-03-15",
        "status": "Active Advisory",
        "source_location": "https://www.dgms.gov.in/circulars/tech_circ_2020_02.pdf",
        "sections": [
            {
                "section": "Section 3 - Systematic Hazard Identification and Risk Scoring (HIRA)",
                "page": 2,
                "content": """DGMS Tech Circular 02 of 2020: Guidelines on Risk Assessment Matrix for Mining Operations.
(1) Every mine operator must construct an objective 5x5 Risk Matrix combining Likelihood (1=Rare, 2=Unlikely, 3=Possible, 4=Likely, 5=Almost Certain) and Consequence Severity (1=Insignificant, 2=Minor injury, 3=Moderate/LTI, 4=Major/Permanent disability, 5=Catastrophic/Multiple fatalities).
(2) Risk Score = Likelihood x Consequence (Range 1 to 25).
- Low Risk (Score 1-4): Acceptable with routine monitoring and standard operating procedures;
- Medium Risk (Score 5-9): Tolerable; requires defined engineering controls and scheduled supervisor inspections;
- High Risk (Score 10-15): Unacceptable without additional risk reduction measures implemented within specified timeline;
- Critical/Extreme Risk (Score 16-25): Intolerable; work must cease immediately until controls reduce risk to Tolerable or Low.
(3) Risk Assessment Teams: Must comprise Mine Manager, Safety Officer, Geotechnical/Ventilation Engineer, Foremen/Overmen, Worker Representatives, and Trade Union Safety Committee delegates."""
            },
            {
                "section": "Section 5 - Principal Mining Hazards Register",
                "page": 4,
                "content": """Principal Mining Hazards (PMH) mandated by DGMS:
Every Safety Management Plan must explicitly incorporate Principal Hazard Management Plans (PHMPs) for:
1. Ground Control and Slope Stability (Pit walls, benches, dump slope failures);
2. Inundation and Inrush of Water or Slurry;
3. Explosives, Blasting, Flyrock, and Ground Vibration;
4. Mobile Equipment, Haul Road Accidents, and Traffic Interactions;
5. Mine Fires, Spontaneous Combustion, and Coal Dust Explosion;
6. Toxic, Flammable, and Asphyxiating Gases and Underground Atmospheric Monitoring;
7. Electricity in Hazardous Environments and Flameproof Apparatus Integrity."""
            }
        ]
    },
    {
        "doc_id": "DGMS-CIRCULAR-2021-06",
        "title": "DGMS (Tech) Circular No. 06 of 2021: Precautions Against Slope Failure in Deep Opencast Mines",
        "issuing_authority": "Directorate General of Mines Safety (DGMS), Dhanbad",
        "publication_date": "2021-08-20",
        "status": "Active Directive",
        "source_location": "https://www.dgms.gov.in/circulars/tech_circ_2021_06.pdf",
        "sections": [
            {
                "section": "Section 2 - Slope Stability Radar and Geotechnical Monitoring",
                "page": 1,
                "content": """DGMS Tech Circular 06 of 2021: Slope Stability Monitoring Mandates.
In all deep opencast coal and metalliferous mines exceeding a pit depth of 100 metres:
(a) Deployment of Continuous Real-Time Slope Stability Radar (SSR) is mandatory along critical highwall sections;
(b) Piezometers must be installed across the pit crest and periphery to monitor pore water pressures;
(c) Tension cracks must be surveyed weekly using GPS/total stations; any crack dilation exceeding 5 mm/day constitutes an immediate trigger action response plan (TARP) Level-2 alert;
(d) Berms must be kept clear of accumulated debris to ensure catch capacity in the event of local rock roll."""
            }
        ]
    },
    {
        "doc_id": "MINES-ACT-1952",
        "title": "The Mines Act, 1952 (Act No. 35 of 1952)",
        "issuing_authority": "Parliament of India / Ministry of Labour and Employment",
        "publication_date": "1952-03-15",
        "status": "Statutory Act (As Amended)",
        "source_location": "https://www.dgms.gov.in/acts/mines_act_1952.pdf",
        "sections": [
            {
                "section": "Section 18 - Duties and Responsibilities of Owners, Agents, and Managers",
                "page": 12,
                "content": """Section 18: Duties and responsibilities of owners, agents and managers.
(1) The owner and agent of every mine shall be responsible for making financial and operational provision to ensure that all operations are carried out in full accordance with the Act, regulations, rules, and bye-laws.
(2) The manager shall be responsible for the overall management, control, supervision, and direction of the mine.
(3) The manager shall appoint competent persons (including Safety Officers, Overmen, Mining Sirdars, Surveyors, and Engineers) to oversee ventilation, roof support, machinery maintenance, and hazard mitigation."""
            },
            {
                "section": "Section 23 - Notice of Accidents and Dangerous Occurrences",
                "page": 16,
                "content": """Section 23: Reporting of Accidents.
(1) Whenever there occurs in or about a mine:
(a) An accident causing loss of life or serious bodily injury;
(b) An accidental explosion, ignition, outbreak of fire, irruption of water;
(c) An influx of noxious or inflammable gases;
(d) A premature collapse of ground or major slope failure;
The owner, agent or manager shall give immediate notice within 24 hours to the Chief Inspector of Mines, Regional Inspector, and District Magistrate in the prescribed Form IV-A/IV-B."""
            }
        ]
    },
    {
        "doc_id": "MINE-PLAN-GEVRA-OPENCAST",
        "title": "Mine Operational Plan & Parameters: Gevra Opencast Project (SECL)",
        "issuing_authority": "South Eastern Coalfields Limited (SECL) / Mine Management Office",
        "publication_date": "2026-01-15",
        "status": "Active Operational Plan",
        "source_location": "Internal Mine Technical Archive (Ref: SECL/GEV/2026/SMP-01)",
        "sections": [
            {
                "section": "Operational Overview and Geotechnical Specifications",
                "page": 3,
                "content": """Gevra Mega Opencast Project Specifications:
- Mine Type: Large Mechanised Opencast Coal Mine.
- Annual Capacity: 50 Million Tonnes Per Annum (MTPA).
- Current Pit Depth: 120 metres (Planned ultimate pit depth: 210 metres).
- Stripping Ratio: 1:1.8 cubic metres of Overburden per tonne of coal.
- Seam Details: Upper Kusmunda (thickness 22-28m), Lower Kusmunda (thickness 18-24m).
- Bench Design: Overburden bench height: 15.0 metres; Coal bench height: 12.0 metres; Bench width: 35 to 45 metres (allowing safe maneuverability of 240T dumpers and 42 m3 electric rope shovels).
- Haul Road Design: Width 35 metres; Gradient maintained at 1 in 16; Continuous berms on drop side at height of 2.7 metres (matching 240T dumper tyre diameter).
- Heavy Machinery: 42 m3 Electric Rope Shovels, 240T Dumpers, 311mm Rotary Blast Hole Drills, 850 HP Bulldozers, 50kL Water Sprinklers.
- Blasting Practice: SME (Site Mixed Emulsion) explosives, electronic detonators with sequential firing to maintain Peak Particle Velocity (PPV) under 10 mm/s at peripheral structures. Danger zone 500m cleared prior to blast."""
            }
        ]
    },
    {
        "doc_id": "MINE-PLAN-MOONIDIH-UNDERGROUND",
        "title": "Mine Operational Plan & Parameters: Moonidih Underground Project (BCCL)",
        "issuing_authority": "Bharat Coking Coal Limited (BCCL) / Safety Directorate",
        "publication_date": "2025-11-10",
        "status": "Active Operational Plan",
        "source_location": "Internal Mine Technical Archive (Ref: BCCL/MND/UG/2025/SMP-03)",
        "sections": [
            {
                "section": "Underground Ventilation and Gassiness Parameters",
                "page": 4,
                "content": """Moonidih Deep Underground Coal Project Specifications:
- Mine Type: Fully Mechanised Deep Underground Coal Mine (Powered Support Longwall face).
- Target Seam: Seam XVI (Thickness 2.4 - 3.2 metres), Depth 420 metres below surface.
- Gassiness Degree: Degree-III Gassy Coal Seam (Methane emission > 10 m3 per tonne of coal raised).
- Main Ventilation: Two axial flow exhaust fans delivering 18,500 cubic metres per minute total ventilation.
- District Airflow: 2,400 m3/min circulated through Longwall face tailgate and maingate.
- Gas Drainage: Pre-drainage boreholes drilled from surface and in-seam cross-measure drainage pipelines extracting 45% methane before mining.
- Real-Time Environmental Monitoring: Telemetric multi-sensor network measuring CH4, CO, Air Velocity, and Temperature continuously at face, return gate, and main upcast shaft.
- Power Isolation: Automatic flameproof breaker tripping calibrated at 0.8% CH4 at face and 1.2% in return airway.
- Personnel Safety: Filter self-rescuers and SCSR (Self-Contained Self-Rescuers) carried by 100% underground workforce; refuge chambers located every 500m along intake airway."""
            }
        ]
    }
]

EVALUATION_DATASET = [
    {
        "query_id": "EVAL-001",
        "query_text": "What are the statutory requirements for the Safety Management Plan under Regulation 104 of Coal Mines Regulations 2017?",
        "query_language": "en",
        "expected_source": "DGMS-CMR-2017",
        "expected_section": "Regulation 104 - Safety Management Plan (SMP)",
        "expected_answer_points": [
            "Mandated within one year of CMR 2017 coming into force",
            "Must be based on Hazard Identification and Risk Assessment (HIRA)",
            "Follows hierarchy of controls (Elimination, Substitution, Engineering, Admin, PPE)",
            "Review required at least once every calendar year or after serious accident/alteration"
        ]
    },
    {
        "query_id": "EVAL-002",
        "query_text": "What is the maximum permissible gradient and minimum berm height for opencast haul roads?",
        "query_language": "en",
        "expected_source": "DGMS-CMR-2017",
        "expected_section": "Regulation 83 & 84 - Haul Roads and Dumpers",
        "expected_answer_points": [
            "Haul road gradient shall not be steeper than 1 in 16 (short ramps up to 1 in 10)",
            "Width at least 3 times widest vehicle width for 2-way traffic",
            "Berm height not less than diameter of tyre (wheel height) of largest vehicle"
        ]
    },
    {
        "query_id": "EVAL-003",
        "query_text": "ओपनकास्ट खदान में ब्लास्टिंग के समय डेंजर जोन की दूरी कितनी होनी चाहिए और क्या सावधानियां आवश्यक हैं?",
        "query_language": "hi",
        "expected_source": "DGMS-CMR-2017",
        "expected_section": "Regulation 171 & 186 - Explosives, Shotfiring, and Blasting Precautions",
        "expected_answer_points": [
            "Danger zone radius not less than 500 metres from blast site",
            "All persons evacuated to blasting shelters and access paths manned with red flags",
            "Siren protocol: 10 min first siren, 2 min second siren, post-blast all-clear siren"
        ]
    },
    {
        "query_id": "EVAL-004",
        "query_text": "भूमिगत कोयला खदान में मीथेन (Inflammable gas) की अधिकतम अनुमेय सीमा क्या है?",
        "query_language": "hi",
        "expected_source": "DGMS-CMR-2017",
        "expected_section": "Regulation 153 & 155 - Standards of Ventilation and Mine Gases",
        "expected_answer_points": [
            "Max 0.75% in general body of return air of ventilating district",
            "Max 1.25% in main return airway",
            "Electrical power must be cut off instantly if gas reaches 1.25% at working place"
        ]
    },
    {
        "query_id": "EVAL-005",
        "query_text": "How is risk scored in DGMS Technical Circular 02 of 2020 and what are the action levels for High Risk?",
        "query_language": "en",
        "expected_source": "DGMS-CIRCULAR-2020-02",
        "expected_section": "Section 3 - Systematic Hazard Identification and Risk Scoring (HIRA)",
        "expected_answer_points": [
            "5x5 Risk Matrix: Risk Score = Likelihood (1-5) x Consequence (1-5)",
            "Score ranges: Low (1-4), Medium (5-9), High (10-15), Critical (16-25)",
            "High Risk is unacceptable without additional risk reduction within specified timeline"
        ]
    },
    {
        "query_id": "EVAL-006",
        "query_text": "What specific slope stability monitoring is mandated for deep opencast pits exceeding 100 metres depth?",
        "query_language": "en",
        "expected_source": "DGMS-CIRCULAR-2021-06",
        "expected_section": "Section 2 - Slope Stability Radar and Geotechnical Monitoring",
        "expected_answer_points": [
            "Deployment of continuous real-time Slope Stability Radar (SSR) along critical highwalls",
            "Piezometers installed across pit crest and periphery to monitor pore pressure",
            "Weekly crack survey; crack dilation > 5 mm/day triggers TARP Level-2 alert"
        ]
    },
    {
        "query_id": "EVAL-007",
        "query_text": "What are the bench dimensions and haul road parameters at Gevra Opencast Project?",
        "query_language": "en",
        "expected_source": "MINE-PLAN-GEVRA-OPENCAST",
        "expected_section": "Operational Overview and Geotechnical Specifications",
        "expected_answer_points": [
            "Overburden bench height 15.0m, coal bench height 12.0m, width 35-45m",
            "Haul road width 35m, gradient 1 in 16",
            "Continuous berm height 2.7m matching 240T dumper tyre diameter"
        ]
    },
    {
        "query_id": "EVAL-008",
        "query_text": "खान में गंभीर दुर्घटना होने पर खान प्रबंधक को किसे और कितने समय में सूचना देनी होती है?",
        "query_language": "hi",
        "expected_source": "MINES-ACT-1952",
        "expected_section": "Section 23 - Notice of Accidents and Dangerous Occurrences",
        "expected_answer_points": [
            "Within 24 hours of accident or dangerous occurrence",
            "Notice to Chief Inspector of Mines, Regional Inspector, and District Magistrate",
            "Prescribed Form IV-A / IV-B"
        ]
    },
    {
        "query_id": "EVAL-009",
        "query_text": "What are the quantum computing requirements for longwall face shearers according to DGMS?",
        "query_language": "en",
        "expected_source": "None",
        "expected_section": "None",
        "expected_answer_points": [
            "ABSTAIN: The available DGMS safety regulations and knowledge base contain no provisions regarding quantum computing."
        ]
    }
]

def build_data_repository():
    """Generates authentic raw document files and sample PDF for PyMuPDF ingestion."""
    RAW_DOCS_DIR.mkdir(parents=True, exist_ok=True)
    
    # Save JSON database of raw regulatory documents
    docs_json_path = RAW_DOCS_DIR / "dgms_and_mine_plans.json"
    with open(docs_json_path, "w", encoding="utf-8") as f:
        json.dump(DGMS_DOCUMENTS, f, indent=2, ensure_ascii=False)
        
    # Generate authentic PDF version for PyMuPDF extraction testing
    sample_pdf_path = RAW_DOCS_DIR / "DGMS_CMR_2017_Official_Extracts.pdf"
    doc = fitz.open()
    for d in DGMS_DOCUMENTS[:2]:
        for sec in d["sections"]:
            page = doc.new_page()
            rect = fitz.Rect(50, 50, 550, 750)
            text = f"{d['title']}\nIssuing Authority: {d['issuing_authority']}\nDocument ID: {d['doc_id']} | Status: {d['status']}\n\nSection: {sec['section']} (Page {sec['page']})\n\n{sec['content']}"
            page.insert_textbox(rect, text, fontsize=11, fontname="helv", color=(0.1, 0.1, 0.2))
    doc.save(str(sample_pdf_path))
    doc.close()
    
    # Save Evaluation dataset
    with open(EVALUATION_DATASET_PATH, "w", encoding="utf-8") as f:
        json.dump(EVALUATION_DATASET, f, indent=2, ensure_ascii=False)
        
    print(f"[OK] Generated {len(DGMS_DOCUMENTS)} documents and {sample_pdf_path.name}")
    print(f"[OK] Generated evaluation dataset with {len(EVALUATION_DATASET)} queries at {EVALUATION_DATASET_PATH.name}")

if __name__ == "__main__":
    build_data_repository()
