
from src.soil_analysis import analyze_soil

result = analyze_soil(90, 42, 43, 6.8)

print("AGRI NOVA - SOIL ANALYSIS")
print("------------------------")

print("Nitrogen:", result["nitrogen"])
print("Phosphorus:", result["phosphorus"])
print("Potassium:", result["potassium"])
print("Soil pH:", result["ph"])

print("Soil Condition:", result["condition"])
print("Suggestion:", result["suggestion"])
print("NPK Note:", result["npk_note"])
