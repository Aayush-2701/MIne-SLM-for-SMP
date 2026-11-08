"""
Multilingual Support Module for Indian Mining Workforce (Section 2.2.5).
Provides localized prompts, system terminology mapping, and translation support
for Hindi, Bengali, Odia, Telugu, Kannada, and Marathi.
"""
from typing import Dict, Any

# Mining regulatory terms dictionary across languages
MINING_GLOSSARY = {
    "safety_management_plan": {
        "hi": "सुरक्षा प्रबंधन योजना (SMP)",
        "bn": "নিরাপত্তা ব্যবস্থাপনা পরিকল্পনা (SMP)",
        "or": "ସୁରକ୍ଷା ପରିଚାଳନା ଯୋଜନା (SMP)",
        "te": "భద్రతా నిర్వహణ ప్రణాళిక (SMP)",
        "kn": "ಸುರಕ್ಷತಾ ನಿರ್ವಹಣಾ ಯೋಜನೆ (SMP)",
        "mr": "सुरक्षा व्यवस्थापन योजना (SMP)"
    },
    "hazard_identification": {
        "hi": "जोखिम पहचान (Hazard Identification)",
        "bn": "ঝুঁকি শনাক্তকরণ",
        "or": "ବିପଦ ଚିହ୍ନଟ",
        "te": "ప్రమాద గుర్తింపు",
        "kn": "ಅಪಾಯ ಗುರುತಿಸುವಿಕೆ",
        "mr": "धोका ओळख"
    },
    "risk_assessment": {
        "hi": "जोखिम मूल्यांकन (HIRA)",
        "bn": "ঝুঁকি মূল্যায়ন",
        "or": "ବିପଦ ମୂଲ୍ୟାଙ୍କନ",
        "te": "ప్రమాద అంచనా",
        "kn": "ಅಪಾಯ ಮೌಲ್ಯಮಾಪನ",
        "mr": "जोखीम मूल्यांकन"
    },
    "haul_road": {
        "hi": "हॉल रोड (परिवहन मार्ग)",
        "bn": "পরিবহন রাস্তা (Haul Road)",
        "or": "ପରିବହନ ରାସ୍ତା",
        "te": "రవాణా రహదారి",
        "kn": "ಸಾಗಣೆ ರಸ್ತೆ",
        "mr": "वाहतूक रस्ता"
    },
    "bench_stability": {
        "hi": "बेंच स्थिरता (खदान की सीढ़ियों की सुरक्षा)",
        "bn": "বেঞ্চ স্থায়িত্ব",
        "or": "ବେଞ୍ଚ ସ୍ଥିରତା",
        "te": "బెంచ్ స్థిరత్వం",
        "kn": "ಬೆಂಚ್ ಸ್ಥಿರತೆ",
        "mr": "बेंच स्थिरता"
    },
    "blasting_danger_zone": {
        "hi": "विस्फोट खतरा क्षेत्र (500 मीटर डेंजर ज़ोन)",
        "bn": "বিস্ফোরণ বিপদ অঞ্চল (৫০০ মিটার)",
        "or": "ବିସ୍ଫୋରଣ ବିପଦ କ୍ଷେତ୍ର (୫୦୦ ମିଟର)",
        "te": "పేలుడు ప్రమాద ప్రాంతం (500 మీటర్లు)",
        "kn": "ಸ್ಫೋಟದ ಅಪಾಯದ ವಲಯ (500 ಮೀಟರ್)",
        "mr": "स्फोटक धोका क्षेत्र (५०० मीटर)"
    },
    "ventilation_standards": {
        "hi": "वायुसंचार मानक (Ventilation Standards)",
        "bn": "বায়ু চলাচল মানদণ্ড",
        "or": "ବାୟୁ ଚଳାଚଳ ମାନକ",
        "te": "గాలి ప్రసరణ ప్రమాణాలు",
        "kn": "ಗಾಳಿ ಪ್ರಸರಣ ಮಾನದಂಡಗಳು",
        "mr": "हवा खेळती राहण्याचे निकष"
    }
}

class MultilingualHandler:
    def __init__(self):
        pass

    def detect_language(self, text: str) -> str:
        """Heuristically detects Devanagari (Hindi/Marathi), Bengali, Odia, Telugu, Kannada or English."""
        for char in text:
            code = ord(char)
            if 0x0900 <= code <= 0x097F:
                return "hi"  # Hindi / Devanagari
            elif 0x0980 <= code <= 0x09FF:
                return "bn"  # Bengali
            elif 0x0B00 <= code <= 0x0B7F:
                return "or"  # Odia
            elif 0x0C00 <= code <= 0x0C7F:
                return "te"  # Telugu
            elif 0x0C80 <= code <= 0x0CFF:
                return "kn"  # Kannada
        return "en"

    def get_system_prompt_language_instructions(self, target_lang: str) -> str:
        """Generates instruction clause to enforce response in the selected Indian language."""
        if target_lang == "hi":
            return (
                "भाषा निर्देश: उत्तर पूर्णतः स्पष्ट, प्रामाणिक और पेशेवर हिन्दी में दें। "
                "तकनीकी शब्दावली और सांविधिक नियमों (जैसे CMR 2017 Regulation 104, DGMS Circulars, 500m, 1 in 16, HIRA) "
                "को कोष्ठक में अंग्रेजी संदर्भ सहित स्पष्ट रखें।"
            )
        elif target_lang == "bn":
            return (
                "ভাষা নির্দেশাবলী: সম্পূর্ণ উত্তরটি স্পষ্ট এবং নির্ভুল বাংলায় প্রদান করুন। "
                "ডিজিএমএস বিধিবিধান এবং আইনি রেফারেন্সগুলি (যেমন CMR 2017, Regulation 104) স্পষ্টভাবে বজায় রাখুন।"
            )
        elif target_lang == "or":
            return (
                "ଭାଷା ନିର୍ଦ୍ଦେଶ: ଉତ୍ତରଟି ସମ୍ପୂର୍ଣ୍ଣ ସ୍ପଷ୍ଟ ଏବଂ ପ୍ରାମାଣିକ ଓଡ଼ିଆ ଭାଷାରେ ପ୍ରଦାନ କରନ୍ତୁ। "
                "ଖଣି ନିରାପତ୍ତା ସମ୍ପର୍କିତ ନିୟମାବଳୀ (CMR 2017, DGMS Regulations) ସଠିକ୍ ରଖନ୍ତୁ।"
            )
        elif target_lang == "te":
            return (
                "భాషా సూచనలు: సమాధానాన్ని స్పష్టమైన మరియు ప్రామాణికమైన తెలుగులో అందించండి. "
                "డీజీఎమ్ఎస్ నిబంధనలు మరియు చట్టబద్ధమైన ప్రమాణాలు (CMR 2017, DGMS) ఖచ్చితంగా ఉంచండి."
            )
        elif target_lang == "kn":
            return (
                "ಭಾಷಾ ಸೂಚನೆಗಳು: ಉತ್ತರವನ್ನು ಸ್ಪಷ್ಟ ಮತ್ತು ನಿಖರವಾದ ಕನ್ನಡದಲ್ಲಿ ಒದಗಿಸಿ. "
                "ಡಿಜಿಎಂಎಸ್ ಶಾಸನಬದ್ಧ ನಿಯಮಗಳನ್ನು (CMR 2017, DGMS) ಯಥಾವತ್ತಾಗಿ ಕಾಪಾಡಿಕೊಳ್ಳಿ."
            )
        elif target_lang == "mr":
            return (
                "भाषा सूचना: उत्तर स्पष्ट आणि प्रामाणिक मराठीत द्या. "
                "खान सुरक्षा नियम आणि वैधानिक संदर्भ (CMR 2017, DGMS Circulars) जसेच्या तसे ठेवा."
            )
        return "Language Instructions: Provide the response in clear, professional English with precise statutory citations."
