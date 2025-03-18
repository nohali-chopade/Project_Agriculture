import streamlit as st
import google.generativeai as genai

# Configure the Gemini API key
genai.configure(api_key="AIzaSyAZg8o4JMY_84zyHsHhVbsDeFg46tmA3CE")

c1, c2 = st.columns([30, 50])
c2.title("AI-Powered Crop Yield Prediction")
c1.image("logo.png")


def create_gen_model():
    return genai.GenerativeModel('models/gemini-1.5-pro')

def main():
    st.write("Predict crop yields based on historical data, climate conditions, and crop state.")
    # Inputs for historical data
    crop_name = st.text_input("Enter Crop Name:", help="E.g., Wheat, Rice, Maize")
    planting_date = st.date_input("Planting Date:", help="Select the planting date.")
    farm_size = st.number_input("Farm Size (in hectares):", min_value=0.1, step=0.1, help="Enter the size of your farm.")

    # Inputs for climate conditions
    avg_temp = st.number_input("Average Temperature During Growing Period (°C):", min_value=-10.0, max_value=50.0, step=0.1)
    rainfall = st.number_input("Total Rainfall During Growing Period (mm):", min_value=0.0, step=0.1)
    soil_moisture = st.number_input("Current Soil Moisture Level (%):", min_value=0.0, max_value=100.0, step=0.1)

    # Inputs for current crop state
    growth_stage = st.selectbox(
        "Current Growth Stage of the Crop:",
        ["Seedling", "Vegetative", "Reproductive", "Maturity"],
        help="Select the current growth stage."
    )
    pest_disease_level = st.slider(
        "Pest/Disease Infestation Level (0 = None, 10 = Severe):", 0, 10, step=1
    )

    # Language selection
    language = st.text_input("Enter the language for the response (e.g., English, Hindi):", value="English")

    # Predict yield
    if st.button("Predict Crop Yield"):
        model = create_gen_model()

        # Create the query for AI
        prompt = f"""
        Based on the following input data, predict the crop yield and provide recommendations for optimizing the yield in {language}. Include:
        - Estimated crop yield in metric tons per hectare.
        - Challenges and possible risks during the remaining growth stages.
        - Suggestions for improving yield based on current conditions.

        Input Data:
        - Crop Name: {crop_name}
        - Planting Date: {planting_date}
        - Farm Size: {farm_size} hectares
        - Average Temperature: {avg_temp}°C
        - Total Rainfall: {rainfall} mm
        - Soil Moisture Level: {soil_moisture}%
        - Current Growth Stage: {growth_stage}
        - Pest/Disease Infestation Level: {pest_disease_level}
        """

        # Get response from AI
        response = model.generate_content(prompt)

        # Display the results
        if response and response.candidates:
            candidate = response.candidates[0]  # Access the first candidate
            if hasattr(candidate, 'text') and candidate.text:
                st.subheader(f"Crop Yield Prediction ({language}):")
                st.write(candidate.text)
            else:
                st.write(response.text)
        else:
            st.write("No response received. Please try again.")

if __name__ == "__main__":
    main()
