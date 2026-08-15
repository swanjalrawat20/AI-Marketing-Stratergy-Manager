from app.tools.campaign_data import analyze_campaign_data


print("=" * 40)
print("CAMPAIGN DATA TOOL TEST")
print("=" * 40)

print("\nStarting Campaign Data Tool...")

result = analyze_campaign_data(
    "sample_campaign_data.csv"
)

print("\n==============================")
print("CAMPAIGN DATA RESULT")
print("==============================")

print(result)
