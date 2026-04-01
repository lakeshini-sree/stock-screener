// --------------------
// QUERY FUNCTION
// --------------------
async function runQuery() {
    const query = document.getElementById("queryInput").value;
    const message = document.getElementById("message");
    const resultsDiv = document.getElementById("results");

    message.innerHTML = "";
    resultsDiv.innerHTML = "";

    try {
        const response = await fetch("http://localhost:8000/query", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ query: query })
        });

        const data = await response.json();

        if (data.status === "error") {
            message.innerHTML = "⚠️ Invalid query. Please try again.";
            return;
        }

        const results = data.data.results;

        if (results.length === 0) {
            message.innerHTML = "No results found.";
            return;
        }

        let table = "<table border='1'><tr><th>Company</th><th>Price</th></tr>";

        results.forEach(r => {
            table += `<tr><td>${r.company}</td><td>${r.price}</td></tr>`;
        });

        table += "</table>";
        resultsDiv.innerHTML = table;

    } catch (error) {
        message.innerHTML = "⚠️ Server error. Please check connection.";
    }
}


// --------------------
// CREATE ALERT
// --------------------
async function createAlert() {
    const symbol = document.getElementById("symbol").value.toUpperCase();
    const condition = document.getElementById("condition").value.toLowerCase();
    const value = document.getElementById("value").value;
    const msg = document.getElementById("alertMessage");

    msg.innerHTML = "";

    if (!symbol || !condition || !value) {
        msg.innerHTML = "⚠️ Please fill all fields.";
        return;
    }

    try {
        const res = await fetch("http://localhost:8000/alerts", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                user_id: "user1",
                alert_type: "metric",
                stock_symbol: symbol,
                condition: condition,
                value: parseFloat(value)
            })
        });

        const data = await res.json();

        if (data.status === "error") {
            msg.innerHTML = "⚠️ Failed to create alert.";
            return;
        }

        msg.innerHTML = "✅ Alert created successfully!";

    } catch (error) {
        msg.innerHTML = "⚠️ Unable to connect to server.";
    }
}


// --------------------
// CHECK ALERTS
// --------------------
async function checkAlerts() {
    const div = document.getElementById("alerts");
    div.innerHTML = "";

    try {
        const res = await fetch("http://localhost:8000/alerts/check");
        const data = await res.json();

        const alerts = data.triggered_alerts;

        if (!alerts || alerts.length === 0) {
            div.innerHTML = "<p>No alerts triggered.</p>";
            return;
        }

        alerts.forEach(a => {
            div.innerHTML += `<p>🚨 ${a[1]} triggered at ₹${a[2]}</p>`;
        });

    } catch (error) {
        div.innerHTML = "<p>⚠️ Failed to fetch alerts.</p>";
    }
}