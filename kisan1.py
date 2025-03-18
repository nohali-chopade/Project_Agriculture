import streamlit as st
import google.generativeai as genai

# Configure the Gemini API key
genai.configure(api_key="AIzaSyCwBC1Q0MG1d2lf1pulXxfXTmFDrlCkJi0")

# Streamlit layout
c1, c2 = st.columns([30, 50])
c2.title("AI-Powered Farm Equipment Management")
c1.image("logo.png")

def create_gen_model():
    return genai.GenerativeModel('models/gemini-1.5-pro')

def main():
    st.write("Optimize the management of your farm equipment with AI-driven insights.")

    # Inputs for equipment data
    equipment_name = st.text_input("Enter Equipment Name (e.g., Tractor, Harvester):")
    total_hours_used = st.number_input("Total Hours Used:", min_value=0, step=1, help="Enter the total hours the equipment has been in operation.")
    maintenance_schedule = st.text_area("Enter Maintenance Schedule (e.g., every 100 hours, quarterly):")
    last_service_date = st.date_input("Last Service Date:")
    reported_issues = st.text_area("Reported Issues or Faults (if any):", help="Briefly describe any known issues or faults.")

    # Language input
    language = st.text_input("Enter the language for the response (e.g., English, Hindi):", value="English")

    if st.button("Analyze Equipment Management"):
        model = create_gen_model()

        # Query for equipment management analysis
        prompt = f"""
        Analyze the following farm equipment management data and provide detailed insights in {language}. Include:
        - Current maintenance status
        - Recommendations for scheduling future maintenance
        - Suggestions to minimize downtime and optimize equipment usage
        - Tips to prolong the equipment's lifespan
        - Any critical concerns to address immediately

        Equipment Data:
        - Equipment Name: {equipment_name}
        - Total Hours Used: {total_hours_used} hours
        - Maintenance Schedule: {maintenance_schedule}
        - Last Service Date: {last_service_date}
        - Reported Issues: {reported_issues}
        """
        response = model.generate_content(prompt)

        # Display the results
        if response and response.candidates:
            candidate = response.candidates[0]  # Access the first candidate
            if hasattr(candidate, 'text') and candidate.text:
                st.subheader(f"Farm Equipment Management Report ({language})")
                st.write(candidate.text)
            else:
                st.write(response.text)
        else:
            st.write("No response received. Please try again.")

if __name__ == "__main__":
    main()
