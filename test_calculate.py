from app.tools.calculator import calculate_campaign_metrics

print("Calculator test started...")

result = calculate_campaign_metrics(
    budget=50000,
    signup_target=1000,
    campaign_days=30,
)

print("Calculator result:")
print(result)