from alerts_service import evaluate_alerts

def test_alert_logic():
    triggered = evaluate_alerts()

    assert isinstance(triggered, list)