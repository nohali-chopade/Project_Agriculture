import streamlit as st
import google.generativeai as genai

# Configure the Gemini API key
genai.configure(api_key="AIzaSyCW2lmwmiT18AI7Zaw5s1rnhg3-UMp6o4o")

# Streamlit layout
c1, c2 = st.columns([30, 50])
c2.title("AI-Powered Soil Health Monitoring")
c1.image("logo.png")


def create_gen_model():
    return genai.GenerativeModel('models/gemini-1.5-pro')


def main():
    st.write("Analyze your soil's health and get actionable insights.")

    # Inputs
    soil_pH = st.number_input("Enter Soil pH Level:", min_value=0.0, max_value=14.0, step=0.1,
                              help="Ideal range is 6.0-7.5.")
    moisture_level = st.slider("Select Soil Moisture Level (%):", 0, 100, step=1, help="Percentage of soil moisture.")
    nitrogen = st.number_input("Enter Nitrogen Content (ppm):", min_value=0.0, step=0.1)
    phosphorus = st.number_input("Enter Phosphorus Content (ppm):", min_value=0.0, step=0.1)
    potassium = st.number_input("Enter Potassium Content (ppm):", min_value=0.0, step=0.1)

    # Language input
    language = st.text_input("Enter the language for the response (e.g., English, Hindi):", value="English")

    if st.button("Analyze Soil Health"):
        model = create_gen_model()

        # Query for soil health analysis
        prompt = f"""
        Analyze the following soil data and provide a detailed report in {language}. Include:
        - Current soil health status
        - Recommendations for soil improvement
        - Suitable fertilizers
        - Suggested crops based on soil conditions
        - Crop rotation strategies to enhance long-term sustainability

        Soil Data:
        - pH: {soil_pH}
        - Moisture Level: {moisture_level}%
        - Nitrogen: {nitrogen} ppm
        - Phosphorus: {phosphorus} ppm
        - Potassium: {potassium} ppm
        """
        response = model.generate_content(prompt)

        # Display the results
        if response and response.candidates:
            candidate = response.candidates[0]  # Access the first candidate
            if hasattr(candidate, 'text') and candidate.text:
                st.subheader(f"Soil Health Analysis Report ({language})")
                st.write(candidate.text)
            else:
                st.write(response.text)
        else:
            st.write("No response received. Please try again.")


if __name__ == "__main__":
    main()
