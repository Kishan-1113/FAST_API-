import streamlit as st
import pandas as pd
import requests

# Create a form
is_valid = False
with st.form("my_form"):
    st.markdown("  **Model Prediction input data form**")

    col1,spacer, col2 = st.columns([1, 0.2, 1])
   
    first_name = col1.text_input("",
                         placeholder="First name",
                         help="First name")
    last_name = col2.text_input("",
                         placeholder="Last name",
                         help="Last name")
    # Add input widgets
   
    age = col1.text_input("Age", placeholder="Age")
    
    Gender = col2.radio("Gender", ["Male", "Female"], horizontal=True)

    cholesterol = col2.text_input("", placeholder="Cholesterol")
    
    bp = col1.number_input("Blood Pressure", min_value=1.0)

    exercise_habit = col1.selectbox("Exercise habit", ["High", "Medium", "Low"])

    smokes = col2.radio("Smoking", ["Yes", "No"], horizontal=True)

    family_hrt_ds = col1.radio("Family Heart Disease", ["Yes", "No"], horizontal=True)

    diabetes = col2.radio("Diabetes", ["Yes", "No"], horizontal=True)

    weight = col1.number_input("Weight", placeholder="Weight in kg")
    
    sugar_consumption = col1.selectbox("Sugar Consumption", ["High", "Medium", "Low"])
    stress_level = col2.selectbox("Stress Level", ["High", "Medium", "Low"])

    height = col2.number_input("Height", placeholder="Height in feet")

    # Add a submit button
    p1, p2, p3 = st.columns([2,1,2])
    
    submitted = p2.form_submit_button("Submit")


if submitted:
    is_valid = True
    # Age check
    if age:
      try:
          age = int(age)
      except:
          col1.error("Enter a number")
    else:
        col1.error("Enter Age")
        is_valid = False

    # Cholesterol check
    if cholesterol:
      try:
          cholesterol = float(cholesterol)
      except:
          col2.error("Enter a number")
    else:
        col2.error("Enter Cholesterol")
        is_valid =False
    
    # BP Check
    if (bp==0.00) or (not bp):
        is_valid = False
        col1.error("BP can't be zero")
    
    # Weight check
    if weight:
        try:
            weight = float(weight)
        except ValueError:
            col1.error("Enter a valid value")
    else:
        is_valid = False
        col1.error("Enter weight")
    
    # Height check
    if height and height>0 and height<9:
        
        height = float(height)
        height = height * 0.3048
        
    else:
        is_valid = False
        col2.error("Enter valid height")



if is_valid:
    if (height>0):
        bmi = weight/(height)**2
    else: bmi = 0
    
    input_data = {
        "Age": age,
        "Gender": Gender,
        "bp": bp,
        "cholesterol": cholesterol,
        "exercise_habit": exercise_habit,
        "smokes": smokes,
        "family_hrt_ds": family_hrt_ds,
        "diabetes": diabetes,
        "bmi": bmi,
        "stress_level": stress_level,
        "sugar_consumption": sugar_consumption
    }

    input_df = pd.DataFrame([input_data])
    st.write("DataFreme ready for Model")
    st.dataframe(input_df)

    response = requests.post("http://127.0.0.1:8000/predict", json=input_data)


    col1,col2,col3=st.columns(3)

    if response.status_code == 200:
        result = response.json()
        if (result['prediction'] == 0):
            col2.markdown(
            "<h3 style='text-align: center; color: green;'>✅ Safe</h3>",
            unsafe_allow_html=True)
        
        else:
            col2.markdown(
            "<h3 style='text-align: center; color: green;'>❌ Unsafe</h3>",
            unsafe_allow_html=True)

        # col2.success(f"Prediction: {result['prediction']}")
    
    elif response.status_code == 500:
        st.error('Internal Server error')

    elif response.status_code == 422:
        st.error("Unprocessable entity")
    else:
        st.error("Error: could not get prediction.")
