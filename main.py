import streamlit as st
import pandas as pd

# Create a form
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
    if age:
      try:
          age = int(age)
      except:
          col1.error("Enter a number")
    else:
        age = 0
    
                   
    Gender = col2.radio("Gender", ["Male", "Female"], horizontal=True)

    cholesterol = col2.text_input("", placeholder="Cholesterol")
    if cholesterol:
      try:
          cholesterol = float(cholesterol)
      except:
          col2.error("Enter a number")
    else:
        cholesterol = 0
    

    bp = col1.number_input("Blood Pressure")

    
    exercise_habit = col1.selectbox("Exercise habit", ["High", "Medium", "Low"])

    smokes = col2.radio("Smoking", ["Yes", "No"], horizontal=True)

    family_hrt_ds = col1.radio("Family Heart Disease", ["Yes", "No"], horizontal=True)

    diabetes = col2.radio("Diabetes", ["Yes", "No"], horizontal=True)

    bmi = col1.text_input("", placeholder="BMI")
    if bmi:
        try:
            bmi = float(bmi)
        except ValueError:
            col1.error("Enter a valid value")
    else: bmi=0

    
    sugar_con = col1.selectbox("Sugar Consumption", ["High", "Medium", "Low"])
    stress_lv = col2.selectbox("Stress Level", ["High", "Medium", "Low"])
    # Add a submit button
    p1, p2, p3 = st.columns([2,1,2])
    
    submitted = p2.form_submit_button("Submit")

if submitted:
    # Create a dictionary of the inputs
    input_data = {
        "age": age,
        "Gender": Gender,
        "bp": bp,
        "cholesterol": cholesterol,
        "exercise_habit": exercise_habit,
        "smokes": smokes,
        "family_hrt_ds": family_hrt_ds,
        "diabetes": diabetes,
        "bmi": bmi,
        "stress_lv": stress_lv,
        "sugar_con": sugar_con
    }

    # st.write("Collected Input Data:")
    # st.json(input_data)


    input_df = pd.DataFrame([input_data])
    st.write("DataFreme ready for Model")
    st.dataframe(input_df)


# Outside the form
# if submitted:
#     st.write(f"Hello {name}, age {age}, you are feeling {age}.")


# st.write("Hello world")
# st.markdown("Hello **World**")
# st.header("This is a header! ")
# st.badge("New")
# st.caption("This is a caption")
# with st.echo():
#     st.write("This code will be printed")

# st.divider()

# prompt = st.chat_input("Say something")
# if (prompt):
#     st.write(f"User has send prompt {prompt}")

#st.form_submit_button("submit")

# status = st.radio("Select Gender: ", ['Male', 'Female'])
# col1, col2 = st.columns(2)

# clicked = st.button("Click me")
# dropdown = st.link_button("Kishan", url="youtube.com")
# selected = st.checkbox("I Agree", key="Yes")
# settt = st.multiselect("Buy", ["milk", "apple", "car"], width=100)
# col2.selectbox("How would you like to be contacted?", 
#              ("Emali", "Phone", "WhatsApp"), index=None, accept_new_options=True,
#                placeholder="Select a saved email or add a new", width=300)
# st.feedback("faces")
# color = st.color_picker("Pick a color")
# st.radio("Filter", ["open", "closed", "All"])
# st.select_slider("Select size", ["S", "M", "L", "XL"])
# st.toggle("Activate")
# number = st.slider("Pick the value", 0, 100, width=200)

# with st.expander("Open to see more"):
#     st.text("""More expanded
#             The more you expand, the more you get,
#             the more you can seee""")

# tab1, tab2 = st.tabs(["Tab1", "Tab2"])
# tab1.write("This is tab 1")
# tab2.write("This is tab2222")

# col1.write("Column 1")
# col2.write("Column 2")
# if (status == 'Male'):
#     st.success("Male")
# else:
#     st.success("Female")

# st.write("Hello kishan how are you")