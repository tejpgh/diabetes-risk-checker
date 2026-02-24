import streamlit as st
import numpy as np
import joblib

# Load the trained model
model = joblib.load('diabetes_model_v2.pkl')

# Page config
st.set_page_config(page_title="Diabetes Risk Checker", page_icon="🏥")

# Header
st.title("🏥 Early Diabetes Risk Checker")
st.write("Answer these simple questions to understand your diabetes risk.")
st.warning("⚠️ This tool is for awareness purposes only and is NOT a substitute for medical advice. Always consult a qualified doctor for proper diagnosis.")
st.info("⏱️ Takes less than 2 minutes to complete. No lab tests needed!")

# Personal details
st.subheader("👤 About You")
age = st.slider("What is your age?", min_value=1, max_value=100, value=30)
gender = st.radio("Gender", ["Male", "Female"])

# Key symptoms
st.subheader("🔍 Common Early Warning Signs")
st.write("Please answer honestly based on how you have been feeling over the last few weeks:")

polyuria = st.radio(
    "🚽 Do you urinate more frequently than usual, including waking up at night to urinate?",
    ["No", "Yes"],
    help="This is one of the strongest early signs of diabetes"
)

polydipsia = st.radio(
    "💧 Do you feel excessively thirsty most of the time even after drinking water?",
    ["No", "Yes"],
    help="Excessive thirst often goes hand in hand with frequent urination"
)

sudden_weight_loss = st.radio(
    "⚖️ Have you lost weight recently without dieting or exercising?",
    ["No", "Yes"],
    help="Unexplained weight loss can be an early sign of diabetes"
)

weakness = st.radio(
    "😴 Do you feel unusually tired or weak even after a good night's sleep?",
    ["No", "Yes"]
)

polyphagia = st.radio(
    "🍽️ Do you feel excessively hungry even shortly after eating a full meal?",
    ["No", "Yes"],
    help="Feeling hungry all the time even after eating is a common diabetes symptom"
)

# Secondary symptoms
st.subheader("🔎 Other Possible Symptoms")
st.write("Have you noticed any of the following?")

genital_thrush = st.radio(
    "🔄 Do you get recurring fungal or yeast infections that keep coming back?",
    ["No", "Yes"],
    help="Recurring infections can be caused by high blood sugar levels"
)

visual_blurring = st.radio(
    "👁️ Has your vision become blurry or harder to focus recently?",
    ["No", "Yes"]
)

itching = st.radio(
    "🤚 Do you experience unusual itching especially on your hands or feet?",
    ["No", "Yes"]
)

irritability = st.radio(
    "😤 Do you feel unusually irritable or have sudden mood changes?",
    ["No", "Yes"]
)

delayed_healing = st.radio(
    "🩹 Do cuts or wounds on your body take longer than usual to heal?",
    ["No", "Yes"],
    help="Slow wound healing is a common sign of high blood sugar"
)

partial_paresis = st.radio(
    "🦵 Do you experience numbness, tingling or weakness in your hands or feet?",
    ["No", "Yes"],
    help="This can be an early sign of nerve damage caused by high blood sugar"
)

muscle_stiffness = st.radio(
    "💪 Do you experience unusual muscle stiffness or cramps?",
    ["No", "Yes"]
)

alopecia = st.radio(
    "💇 Have you noticed unusual or excessive hair loss recently?",
    ["No", "Yes"]
)

obesity = st.radio(
    "⚖️ Would you describe yourself as overweight or obese?",
    ["No", "Yes"],
    help="Being overweight significantly increases diabetes risk"
)

# Convert inputs
def yes_no(val):
    return 1 if val == "Yes" else 0

def gender_val(val):
    return 1 if val == "Male" else 0

# Predict button
if st.button("Check My Risk 🔍"):
    input_data = np.array([[
        age,
        gender_val(gender),
        yes_no(polyuria),
        yes_no(polydipsia),
        yes_no(sudden_weight_loss),
        yes_no(weakness),
        yes_no(polyphagia),
        yes_no(genital_thrush),
        yes_no(visual_blurring),
        yes_no(itching),
        yes_no(irritability),
        yes_no(delayed_healing),
        yes_no(partial_paresis),
        yes_no(muscle_stiffness),
        yes_no(alopecia),
        yes_no(obesity)
    ]])

    prediction = model.predict(input_data)[0]
    probability = model.predict_proba(input_data)[0]
    risk_percentage = probability[1] * 100

    # Count how many symptoms user has
    symptoms = [
        yes_no(polyuria), yes_no(polydipsia), yes_no(sudden_weight_loss),
        yes_no(weakness), yes_no(polyphagia), yes_no(genital_thrush),
        yes_no(visual_blurring), yes_no(itching), yes_no(irritability),
        yes_no(delayed_healing), yes_no(partial_paresis), yes_no(muscle_stiffness),
        yes_no(alopecia), yes_no(obesity)
    ]
    symptom_count = sum(symptoms)

    # Collect which symptoms they have for explanation
    symptom_names = []
    if yes_no(polyuria): symptom_names.append("Frequent urination")
    if yes_no(polydipsia): symptom_names.append("Excessive thirst")
    if yes_no(sudden_weight_loss): symptom_names.append("Sudden weight loss")
    if yes_no(weakness): symptom_names.append("Unusual weakness or fatigue")
    if yes_no(polyphagia): symptom_names.append("Excessive hunger")
    if yes_no(genital_thrush): symptom_names.append("Recurring fungal infections")
    if yes_no(visual_blurring): symptom_names.append("Blurry vision")
    if yes_no(itching): symptom_names.append("Unusual itching")
    if yes_no(irritability): symptom_names.append("Unusual irritability")
    if yes_no(delayed_healing): symptom_names.append("Slow wound healing")
    if yes_no(partial_paresis): symptom_names.append("Numbness or tingling")
    if yes_no(muscle_stiffness): symptom_names.append("Muscle stiffness")
    if yes_no(alopecia): symptom_names.append("Unusual hair loss")
    if yes_no(obesity): symptom_names.append("Overweight or obese")

    # Adjust risk based on symptom count
    if symptom_count == 0:
        risk_percentage = min(risk_percentage, 20)
    elif symptom_count == 1:
        risk_percentage = min(risk_percentage, 40)
    elif symptom_count == 2:
        risk_percentage = min(risk_percentage, 60)

    st.subheader("📊 Your Results")

    # Risk meter
    st.write(f"**Your Diabetes Risk Score: {risk_percentage:.1f}%**")
    st.progress(int(risk_percentage))

    if risk_percentage >= 80:
        st.error("🔴 HIGH Risk — Please see a doctor as soon as possible!")
    elif risk_percentage >= 60:
        st.warning("🟡 MODERATE Risk — We recommend getting tested soon")
    else:
        st.success("🟢 LOW Risk — Keep maintaining a healthy lifestyle!")
    # Explain why
    st.subheader("📋 Why did you get this score?")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write(f"**Your age:** {age} years")
        st.write(f"**Your gender:** {gender}")
        st.write(f"**Number of symptoms:** {symptom_count} out of 14")
    
    with col2:
        if age >= 45:
            st.write("⚠️ Age above 45 increases diabetes risk")
        if gender == "Male":
            st.write("⚠️ Males are slightly more at risk")
        if yes_no(obesity):
            st.write("⚠️ Being overweight increases risk significantly")

    if symptom_count > 0:
        st.write("**Symptoms you reported:**")
        for symptom in symptom_names:
            st.write(f"- ⚠️ {symptom}")
        
        # Explain the two most important symptoms
        if yes_no(polyuria) and yes_no(polydipsia):
            st.warning("🔴 Frequent urination AND excessive thirst together are the two strongest warning signs of diabetes!")
        elif yes_no(polyuria):
            st.info("ℹ️ Frequent urination alone can have many causes but is worth monitoring")
        elif yes_no(polydipsia):
            st.info("ℹ️ Excessive thirst alone can have many causes but is worth monitoring")
    else:
        st.write("✅ You reported no symptoms which is a good sign!")
        if age >= 45:
            st.write("However your age puts you in a higher risk group — we still recommend an annual blood sugar test!")

    # Next steps
    st.subheader("👣 What Should You Do Next?")

    if prediction == 1:
        st.write("""
        Based on your symptoms we strongly recommend getting these tests done at your nearest diagnostic centre or doctor:

        **Essential Tests:**
        - 📌 **Fasting Blood Sugar Test** — Done after 8 hours of fasting. Most basic diabetes test.
        - 📌 **HbA1c Test** — Shows your average blood sugar over the last 3 months. No fasting needed.
        - 📌 **Oral Glucose Tolerance Test (OGTT)** — Most comprehensive diabetes test.

        **Additional Tests your doctor may recommend:**
        - 📌 **Fasting Insulin Test** — Checks insulin resistance
        - 📌 **Lipid Profile** — Checks cholesterol levels which are often affected by diabetes

        **Important:**
        👉 Don't panic — early detection means diabetes is completely manageable!
        👉 Many people live completely normal lives with proper management.
        👉 Please share these results with your doctor for proper evaluation.
        """)
    else:
        st.write("""
        Your symptoms suggest low diabetes risk. Here's how to stay healthy:

        **Lifestyle Tips:**
        - ✅ Exercise at least 30 minutes a day
        - ✅ Eat a balanced diet — reduce sugar and processed foods
        - ✅ Maintain a healthy weight
        - ✅ Stay hydrated — drink plenty of water
        - ✅ Get 7-8 hours of sleep every night

        **Still recommended:**
        👉 Get a routine fasting blood sugar test **once a year** especially if diabetes runs in your family!
        👉 Even with low risk, regular checkups are important.
        """)

    st.markdown("---")
    st.caption("⚠️ This tool is for awareness and educational purposes only. It is NOT a medical diagnosis. Please consult a qualified healthcare professional for proper evaluation and diagnosis.")