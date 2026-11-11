
import math


def analyze_soil(N, P, K, ph):

    # Validate inputs
    values = [N, P, K, ph]

    if not all(math.isfinite(value) for value in values):
        raise ValueError("Please enter valid finite numbers.")

    if N < 0 or P < 0 or K < 0:
        raise ValueError("NPK values cannot be negative.")

    if not 0 <= ph <= 14:
        raise ValueError("Soil pH must be between 0 and 14.")

    # Analyze soil pH
    if ph < 5.5:
        condition = "Strongly acidic"
        suggestion = (
            "Consider a soil test to check acidity. "
            "Liming may be appropriate based on the test."
        )

    elif ph < 6.5:
        condition = "Slightly acidic"
        suggestion = (
            "Many crops tolerate this range. "
            "Choose crops according to local soil conditions."
        )

    elif ph <= 7.5:
        condition = "Near neutral"
        suggestion = (
            "This pH range is suitable for many crops. "
            "Continue regular soil monitoring."
        )

    elif ph <= 8.5:
        condition = "Alkaline"
        suggestion = (
            "Check nutrient availability through a soil test "
            "before choosing any soil treatment."
        )

    else:
        condition = "Strongly alkaline"
        suggestion = (
            "Get a soil test to identify the cause and "
            "appropriate soil management practices."
        )

    # Prepare analysis report
    result = {
        "nitrogen": N,
        "phosphorus": P,
        "potassium": K,
        "ph": ph,
        "condition": condition,
        "suggestion": suggestion,
        "npk_note": (
            "NPK values recorded. Their adequacy depends on "
            "soil units, crop requirements and laboratory results."
        )
    }

    return result
