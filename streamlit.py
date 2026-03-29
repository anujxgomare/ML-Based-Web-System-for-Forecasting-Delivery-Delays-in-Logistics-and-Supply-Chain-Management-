import streamlit as st
import pickle
import pandas as pd
import os

# ===============================
# Page Configuration
# ===============================
st.set_page_config(
    page_title="Supply Chain Delay Prediction",
    layout="centered"
)

st.title("🚚 Supply Chain Delay Prediction")
st.markdown("### Enter shipment details")

# ===============================
# Load Model
# ===============================
MODEL_PATH = os.path.join(os.path.dirname(__file__), "model.pkl")

if not os.path.exists(MODEL_PATH):
    st.error("❌ model.pkl not found in the project folder")
    st.stop()

model = pickle.load(open(MODEL_PATH, "rb"))

# ===============================
# Encoded Mappings
# ===============================
vendors = {"Vendor A": 0, "Vendor B": 1, "Vendor C": 2, "Vendor D": 3}
vehicle_types = {"Truck": 0, "Van": 1, "Bike": 2}
cities = {"Mumbai": 0, "Delhi": 1, "Pune": 2, "Bangalore": 3, "Chennai": 4}
traffic_conditions = {"Low": 0, "Medium": 1, "High": 2, "Severe": 3}
order_priorities = {"Low": 0, "Medium": 1, "High": 2, "Urgent": 3}
road_types = {"Highway": 0, "City Road": 1, "Rural": 2, "Mountain": 3}

# ===============================
# Distance Map (KM)
# ===============================
distance_map = {
    ("Mumbai", "Delhi"): 1400,
    ("Mumbai", "Pune"): 150,
    ("Mumbai", "Bangalore"): 980,
    ("Mumbai", "Chennai"): 1030,

    ("Delhi", "Mumbai"): 1400,
    ("Delhi", "Pune"): 1450,
    ("Delhi", "Bangalore"): 2150,
    ("Delhi", "Chennai"): 2200,

    ("Pune", "Mumbai"): 150,
    ("Pune", "Delhi"): 1450,
    ("Pune", "Bangalore"): 840,
    ("Pune", "Chennai"): 910,

    ("Bangalore", "Mumbai"): 980,
    ("Bangalore", "Delhi"): 2150,
    ("Bangalore", "Pune"): 840,
    ("Bangalore", "Chennai"): 350,

    ("Chennai", "Mumbai"): 1030,
    ("Chennai", "Delhi"): 2200,
    ("Chennai", "Pune"): 910,
    ("Chennai", "Bangalore"): 350,
}

# ===============================
# User Inputs
# ===============================
vendor = st.selectbox("Vendor", vendors.keys())
vehicle = st.selectbox("Vehicle Type", vehicle_types.keys())
origin = st.selectbox("Origin City", cities.keys())
destination = st.selectbox("Destination City", cities.keys())

# Auto distance calculation
if origin == destination:
    distance = 0
    st.warning("⚠️ Origin and destination are the same. Distance set to 0 km.")
else:
    distance = distance_map.get((origin, destination), 0)
    st.info(f"📍 Estimated Distance: **{distance} km**")

traffic = st.selectbox("Traffic Condition", traffic_conditions.keys())

vendor_delay_score = st.slider(
    "Vendor Delay Score (Historical)", 0.0, 1.0, 0.3
)

hour = st.slider("Hour of Day", 0, 23, 12)
day = st.slider("Day of Week (1 = Monday)", 1, 7, 3)

holiday_ui = st.radio("Is it a Holiday?", ["No", "Yes"], horizontal=True)
holiday_flag = 1 if holiday_ui == "Yes" else 0

pickup_delay = st.number_input("Pickup Delay (minutes)", min_value=0, value=5)
driver_rating = st.slider("Driver Rating", 1.0, 5.0, 3.5)
vehicle_age = st.number_input("Vehicle Age (years)", min_value=0, value=3)

order_weight = st.number_input("Order Weight (kg)", min_value=0.1, value=50.0)
num_packages = st.number_input("Number of Packages", min_value=1, value=3)

priority = st.selectbox("Order Priority", order_priorities.keys())
road = st.selectbox("Road Type", road_types.keys())

# ===============================
# Weather (Hidden)
# ===============================
weather_condition = 0  # Clear weather

# ===============================
# Delay Estimation + Explanation
# ===============================
def estimate_delay_hours_and_reasons(row):
    delay = 0
    reasons = []

    if row["traffic_condition"] >= 2:
        delay += 2
        reasons.append("High traffic conditions")

    if row["pickup_delay_minutes"] > 15:
        delay += 1
        reasons.append("Pickup delay at source")

    if row["distance_km"] > 300:
        delay += 3
        reasons.append("Long-distance route")

    if row["holiday_flag"] == 1:
        delay += 1
        reasons.append("Holiday-related slowdown")

    if delay == 0:
        delay = 1
        reasons.append("Minor operational delays")

    return delay, reasons

# ===============================
# Run Prediction
# ===============================
st.markdown("### 🚀 Run Prediction")

predict_clicked = st.button(
    "🚚 Predict Shipment Delay",
    use_container_width=True
)

if predict_clicked:
    input_df = pd.DataFrame([{
        "vendor": vendors[vendor],
        "vehicle_type": vehicle_types[vehicle],
        "origin_city": cities[origin],
        "destination_city": cities[destination],
        "distance_km": distance,
        "weather_condition": weather_condition,
        "traffic_condition": traffic_conditions[traffic],
        "vendor_delay_score": vendor_delay_score,
        "hour_of_day": hour,
        "day_of_week": day,
        "holiday_flag": holiday_flag,
        "pickup_delay_minutes": pickup_delay,
        "driver_rating": driver_rating,
        "vehicle_age_years": vehicle_age,
        "order_weight_kg": order_weight,
        "num_packages": num_packages,
        "order_priority": order_priorities[priority],
        "road_type": road_types[road]
    }])

    probability = model.predict_proba(input_df)[0][1]
    prob_percent = round(probability * 100, 2)

    st.markdown("---")
    st.subheader("📊 Prediction Result")

    if probability >= 0.30:
        delay_hours, reasons = estimate_delay_hours_and_reasons(input_df.iloc[0])

        st.error("🚨 **Shipment Likely Delayed**")
        st.markdown(f"🔴 **Delay Probability:** **{prob_percent}%**")
        st.markdown(f"⏱️ **Estimated Delay:** **{delay_hours} hours**")

        st.markdown("### 🔍 Reason for Delay")
        for reason in reasons:
            st.write(f"• {reason}")
    else:
        st.success("✅ **Shipment Likely On Time**")
        st.markdown(f"🟢 **Delay Probability:** **{prob_percent}%**")
