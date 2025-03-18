import streamlit as st
import google.generativeai as genai
from datetime import date

# Configure the Gemini API key
genai.configure(api_key="AIzaSyA7tnL0yYx08hGAR56qYU1_JfI-qnjvTB4")

# Streamlit layout
c1, c2 = st.columns([30, 50])
c2.title("AI-Powered Crop Selection and Rotation Planner")
c1.image("C:/Users/KALPESH/Downloads/logo-removebg-preview.png")

def create_gen_model():
    return genai.GenerativeModel('models/gemini-1.5-pro')

def main():
    st.write("Optimize crop selection and rotation strategies with AI-driven insights.")

    # Inputs for soil data
    soil_type = st.selectbox(
        "Select Soil Type:",
        ["Sandy", "Clayey", "Loamy", "Silty", "Peaty", "Chalky"],
        help="Choose the type of soil for your land."
    )
    soil_pH = st.number_input("Enter Soil pH Level:", min_value=0.0, max_value=14.0, step=0.1, help="Ideal range is 6.0-7.5.")
    nitrogen = st.number_input("Enter Nitrogen Content (ppm):", min_value=0.0, step=0.1)
    phosphorus = st.number_input("Enter Phosphorus Content (ppm):", min_value=0.0, step=0.1)
    potassium = st.number_input("Enter Potassium Content (ppm):", min_value=0.0, step=0.1)

    # Inputs for climate data
    climate_zone = st.selectbox(
        "Select Climate Zone:",
        ["Tropical", "Dry", "Temperate", "Continental", "Polar"],
        help="Choose the climate zone of your farm."
    )
    avg_temp = st.number_input("Enter Average Temperature (°C):", min_value=-50.0, max_value=50.0, step=0.1)
    annual_rainfall = st.number_input("Enter Annual Rainfall (mm):", min_value=0.0, step=0.1)

    # Inputs for historical crop data
    previous_crops = st.text_area(
        "Enter Previous Crops Grown (separate by commas):",
        help="Provide the names of crops grown on this land in the last 3 seasons."
    )

    # Language input
    language = st.text_input("Enter the language for the response (e.g., English, Hindi):", value="English")

    if st.button("Get Crop Recommendations"):
        model = create_gen_model()

        # Query for crop recommendations
        prompt = f"""
        Analyze the following data and recommend the best crops to grow and an effective crop rotation plan in {language}. Include:
        - Suitable crops based on soil type, pH, and nutrient levels
        - Recommendations for sustainable crop rotation to maintain soil health and prevent pest buildup
        - Tips for managing the selected crops in the given climate zone

        Soil Data:
        - Soil Type: {soil_type}
        - pH: {soil_pH}
        - Nitrogen: {nitrogen} ppm
        - Phosphorus: {phosphorus} ppm
        - Potassium: {potassium} ppm

        Climate Data:
        - Climate Zone: {climate_zone}
        - Average Temperature: {avg_temp}°C
        - Annual Rainfall: {annual_rainfall} mm

        Historical Data:
        - Previous Crops: {previous_crops}
        """
        response = model.generate_content(prompt)

        # Display the results
        if response and response.candidates:
            candidate = response.candidates[0]  # Access the first candidate
            if hasattr(candidate, 'text') and candidate.text:
                st.subheader(f"Crop Selection and Rotation Plan ({language})")
                st.write(candidate.text)
            else:
                st.write(response.text)
        else:
            st.write("No response received. Please try again.")

if __name__ == "__main__":
    main()
