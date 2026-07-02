# IGCSE Mark Schemes - Subject Knowledge Base

MARK_SCHEMES = {
    "Biology": {
        "photosynthesis": {
            "definition": "Process by which plants convert light energy into chemical energy in glucose",
            "keywords": ["light-dependent reactions", "light-independent reactions", "chloroplast", "ATP", "NADPH", "glucose", "CO2", "H2O"],
            "common_errors": [
                "Confusing photosynthesis with respiration",
                "Forgetting the role of chlorophyll",
                "Not mentioning ATP production",
                "Incorrect products (should be glucose, not just sugars)"
            ]
        },
        "cellular_respiration": {
            "definition": "Process of releasing energy from glucose in cells",
            "keywords": ["aerobic respiration", "anaerobic respiration", "ATP", "mitochondria", "glucose", "oxygen", "CO2", "lactic acid", "ethanol"],
            "common_errors": [
                "Not distinguishing between aerobic and anaerobic",
                "Forgetting stages: glycolysis, Krebs cycle, electron transport chain",
                "Incorrect ATP yields",
                "Confusing products of different respiration types"
            ]
        },
        "enzyme_action": {
            "definition": "Proteins that catalyze biological reactions",
            "keywords": ["substrate", "active site", "enzyme-substrate complex", "denature", "cofactor", "coenzyme", "optimum temperature", "optimum pH"],
            "common_errors": [
                "Not mentioning active site specificity",
                "Forgetting that enzymes are reusable",
                "Incorrect explanation of denaturation",
                "Not linking pH/temperature to enzyme shape"
            ]
        },
        "dna_structure": {
            "definition": "Double helix structure containing genetic information",
            "keywords": ["nucleotide", "phosphate", "deoxyribose", "base pair", "complementary", "adenine", "thymine", "guanine", "cytosine", "semi-conservative replication"],
            "common_errors": [
                "Incorrect base pairing (A with T, G with C)",
                "Forgetting the role of DNA polymerase",
                "Not explaining semi-conservative replication",
                "Confusing DNA with RNA"
            ]
        }
    },
    "Physics": {
        "force_and_motion": {
            "definition": "Interaction that changes or tends to change the state of motion of an object",
            "keywords": ["Newton's first law", "Newton's second law", "Newton's third law", "F=ma", "acceleration", "friction", "mass", "weight"],
            "common_errors": [
                "Confusing mass with weight",
                "Forgetting that forces act in pairs",
                "Incorrect application of F=ma",
                "Not considering all forces acting on an object"
            ]
        },
        "energy": {
            "definition": "Capacity to do work; exists in various forms",
            "keywords": ["kinetic energy", "potential energy", "work", "power", "efficiency", "energy conservation", "J", "W"],
            "common_errors": [
                "Incorrect energy formulas",
                "Not accounting for all forms of energy",
                "Confusing work with force",
                "Wrong units (using kg instead of N for force)"
            ]
        },
        "waves": {
            "definition": "Disturbances that transfer energy without transferring matter",
            "keywords": ["wavelength", "frequency", "amplitude", "speed", "refraction", "diffraction", "interference", "transverse", "longitudinal"],
            "common_errors": [
                "Confusing wavelength with frequency",
                "Incorrect wave equation (v=fλ)",
                "Not distinguishing wave types",
                "Wrong explanation of wave phenomena"
            ]
        },
        "electricity": {
            "definition": "Flow of electrons through a circuit",
            "keywords": ["current", "voltage", "resistance", "Ohm's law", "V=IR", "circuit", "series", "parallel", "power"],
            "common_errors": [
                "Incorrect Ohm's law application",
                "Confusing series and parallel circuits",
                "Wrong power formula (P=IV)",
                "Not considering total resistance correctly"
            ]
        }
    },
    "Chemistry": {
        "atomic_structure": {
            "definition": "Arrangement of protons, neutrons, and electrons in an atom",
            "keywords": ["proton", "neutron", "electron", "nucleus", "atomic number", "mass number", "isotope", "electron shells"],
            "common_errors": [
                "Confusing atomic number with mass number",
                "Incorrect electron configuration",
                "Not understanding isotopes",
                "Wrong mass number calculations"
            ]
        },
        "bonding": {
            "definition": "Forces holding atoms together in molecules or structures",
            "keywords": ["ionic bond", "covalent bond", "metallic bond", "electron transfer", "electron sharing", "electronegativity", "valence electrons"],
            "common_errors": [
                "Not distinguishing between bond types",
                "Incorrect dot-and-cross diagrams",
                "Wrong electronegativity explanations",
                "Confusing structure with bonding"
            ]
        },
        "reactions": {
            "definition": "Process where substances change into different substances",
            "keywords": ["exothermic", "endothermic", "combustion", "oxidation", "reduction", "catalyst", "reversible", "displacement"],
            "common_errors": [
                "Not balancing chemical equations",
                "Confusing exothermic with endothermic",
                "Not identifying reaction types",
                "Incorrect state symbols (s, l, g, aq)"
            ]
        },
        "equilibrium": {
            "definition": "State where forward and backward reaction rates are equal",
            "keywords": ["dynamic equilibrium", "reversible reaction", "Le Chatelier's principle", "shift position", "concentration", "temperature", "pressure"],
            "common_errors": [
                "Not understanding dynamic nature",
                "Incorrect Le Chatelier predictions",
                "Forgetting all factors that affect equilibrium",
                "Confusing equilibrium with completion"
            ]
        }
    }
}

def get_mark_scheme_keywords(subject: str, topic: str = None) -> dict:
    """Retrieve mark scheme data for a subject or topic"""
    if subject not in MARK_SCHEMES:
        return {}
    
    if topic and topic in MARK_SCHEMES[subject]:
        return MARK_SCHEMES[subject][topic]
    
    return MARK_SCHEMES[subject]

def validate_response(response: str, subject: str, topic: str = None) -> dict:
    """Validate student response against mark scheme"""
    scheme = get_mark_scheme_keywords(subject, topic)
    
    if not scheme:
        return {"valid": False, "message": "Topic not found in mark scheme"}
    
    found_keywords = []
    for topic_name, topic_data in scheme.items() if not topic else [(topic, scheme)]:
        keywords = topic_data.get("keywords", [])
        for keyword in keywords:
            if keyword.lower() in response.lower():
                found_keywords.append(keyword)
    
    common_errors = []
    for topic_name, topic_data in scheme.items() if not topic else [(topic, scheme)]:
        for error in topic_data.get("common_errors", []):
            if any(keyword.lower() in response.lower() for keyword in error.split()):
                common_errors.append(error)
    
    return {
        "found_keywords": found_keywords,
        "possible_missing": get_missing_keywords(response, subject, topic),
        "common_errors_detected": common_errors,
        "completeness_score": len(found_keywords) / 5
    }

def get_missing_keywords(response: str, subject: str, topic: str = None) -> list:
    """Identify missing keywords from mark scheme"""
    scheme = get_mark_scheme_keywords(subject, topic)
    
    missing = []
    for topic_name, topic_data in scheme.items() if not topic else [(topic, scheme)]:
        keywords = topic_data.get("keywords", [])
        for keyword in keywords:
            if keyword.lower() not in response.lower():
                missing.append(keyword)
    
    return missing[:5]  # Return top 5 missing keywords
