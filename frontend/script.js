
const API_URL = "http://127.0.0.1:5000";

// Load dropdown options
async function loadOptions() {
    try {
        const response = await fetch(`${API_URL}/api/options`);

        if (!response.ok) {
            throw new Error("Could not load dropdown options");
        }

        const options = await response.json();

        const dropdowns = {
            airline: options.airlines,
            source_city: options.source_cities,
            destination_city: options.destination_cities,
            travel_class: options.classes,
            departure_time: options.departure_times,
            arrival_time: options.arrival_times,
            stops: options.stops
        };

        for (const [id, values] of Object.entries(dropdowns)) {
            const select = document.getElementById(id);

            if (!select) {
                console.error(`Dropdown not found: ${id}`);
                continue;
            }

            values.forEach(value => {
                const option = document.createElement("option");
                option.value = value;
                option.textContent = value;
                select.appendChild(option);
            });
        }

        console.log("Dropdown options loaded successfully!");

    } catch (error) {
        console.error("Dropdown loading error:", error);
        alert("Unable to load flight options. Check backend connection.");
    }
}

// Handle prediction form
document.getElementById("predictionForm").addEventListener("submit", async (event) => {
    event.preventDefault();

    const form = event.target;

    const data = {
        airline: form.elements["airline"].value,
        source_city: form.elements["source_city"].value,
        destination_city: form.elements["destination_city"].value,
        travel_class: form.elements["travel_class"].value,
        departure_time: form.elements["departure_time"].value,
        arrival_time: form.elements["arrival_time"].value,
        stops: form.elements["stops"].value,
        duration: form.elements["duration"].value,
        days_left: form.elements["days_left"].value
    };

    try {
        const response = await fetch(`${API_URL}/api/predict`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.error || "Prediction failed");
        }

        document.getElementById("predictedPrice").textContent =
            "₹ " + Number(result.predicted_price).toLocaleString("en-IN");

        document.getElementById("result").style.display = "block";

    } catch (error) {
        console.error("Prediction error:", error);
        alert(error.message);
    }
});

// Initialize
loadOptions();
