N = int(input("Enter Nitrogen (N): "))
P = int(input("Enter Phosphorus (P): "))
K = int(input("Enter Potassium (K): "))

pH = float(input("Enter Soil pH: "))
rainfall = float(input("Enter Rainfall (mm): "))

print("\n----- AgriNova Soil Details -----")

print("Nitrogen:", N)
print("Phosphorus:", P)
print("Potassium:", K)
print("Soil pH:", pH)
print("Rainfall:", rainfall, "mm")

if pH<7:
    print("Soil type : Acidic")
elif pH==7:
    print("Soil type : Neutral")
else:
    print("Soil type : Alkaline")