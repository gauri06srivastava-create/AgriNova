
# AgriNova - Farming Knowledge Hub

crop_knowledge = {

    "Rice": {
        "season": "Kharif",
        "soil": "Clayey and loamy soil",
        "water": "Requires regular water supply. Avoid uncontrolled waterlogging.",
        "irrigation": "Maintain suitable field moisture and follow local irrigation schedules.",
        "fertilizer": "Use nitrogen, phosphorus and potassium based on soil test results.",
        "tips": [
            "Use healthy and certified seeds.",
            "Monitor weeds regularly.",
            "Check crops for pests and diseases."
        ]
    },

    "Wheat": {
        "season": "Rabi",
        "soil": "Well-drained loamy soil",
        "water": "Requires timely irrigation, especially during critical growth stages.",
        "irrigation": "Monitor soil moisture and irrigate according to crop stage.",
        "fertilizer": "Apply balanced nutrients based on soil testing.",
        "tips": [
            "Use quality certified seeds.",
            "Maintain proper spacing.",
            "Monitor for rust and other diseases."
        ]
    },

    "Maize": {
        "season": "Kharif, Rabi and other suitable seasons",
        "soil": "Well-drained fertile loamy soil",
        "water": "Needs adequate moisture during flowering and grain formation.",
        "irrigation": "Avoid water stress during important growth stages.",
        "fertilizer": "Use balanced NPK according to soil test recommendations.",
        "tips": [
            "Avoid waterlogging.",
            "Control weeds during early growth.",
            "Monitor for fall armyworm."
        ]
    },

    "Tomato": {
        "season": "Can be grown in suitable seasons depending on region.",
        "soil": "Well-drained sandy loam or loamy soil",
        "water": "Needs consistent soil moisture.",
        "irrigation": "Prefer drip irrigation and avoid excessive watering.",
        "fertilizer": "Use balanced nutrients based on soil testing and crop stage.",
        "tips": [
            "Provide proper plant spacing.",
            "Remove diseased plant parts.",
            "Monitor for fruit borer and leaf diseases."
        ]
    },

    "Potato": {
        "season": "Mainly Rabi in many Indian regions",
        "soil": "Loose, well-drained sandy loam soil",
        "water": "Requires adequate moisture without waterlogging.",
        "irrigation": "Maintain uniform soil moisture during tuber development.",
        "fertilizer": "Apply nutrients according to soil testing.",
        "tips": [
            "Use certified disease-free seed tubers.",
            "Earth up plants when appropriate.",
            "Monitor for late blight."
        ]
    }
}


def get_all_crops():
    return list(crop_knowledge.keys())


def get_crop_details(crop_name):
    return crop_knowledge.get(crop_name)
