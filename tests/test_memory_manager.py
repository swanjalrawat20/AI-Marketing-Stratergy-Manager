from app.memory.memory_manager import MemoryManager


def test_campaign_round_trip(tmp_path):
    manager = MemoryManager(str(tmp_path / "test.db"))
    campaign_id = manager.save_campaign(
        campaign_name="Test Campaign",
        product="Test Product",
        target_audience="Students",
        marketing_goal="100 signups",
        budget="₹10,000",
        timeline="10 days",
        strategy="Initial strategy",
        status="Pending Review",
        approval_status="pending",
        performance_data={"actual": {"signups": 10}},
    )

    record = manager.get_campaign(campaign_id)
    assert record["campaign_name"] == "Test Campaign"
    assert record["performance_data"]["actual"]["signups"] == 10

    assert manager.update_campaign(
        campaign_id,
        status="Approved",
        approval_status="approved",
        strategy="Approved strategy",
    )

    updated = manager.get_campaign(campaign_id)
    assert updated["status"] == "Approved"
    assert updated["strategy"] == "Approved strategy"


def test_context_round_trip(tmp_path):
    manager = MemoryManager(str(tmp_path / "context.db"))
    manager.save_context("preferred_channels", ["Instagram", "Email"])
    assert manager.get_context("preferred_channels") == ["Instagram", "Email"]
