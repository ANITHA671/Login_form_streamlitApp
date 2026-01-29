import streamlit as st

#header for the app
st.header("Registration")

#Title of the app
st.title("Student CRUD Application")

#Sub header for the app
st.subheader("Manage student records with efficiently and effectively")
st.markdown("----------------------------------------------------------------------------")

#text method to display information
st.text("This application allows to perform CRUD operation on student records using a MySql database")

#write method to provide additional information
st.write("Hello Streamlit")
st.write(123)
st.write([1,2,3])
st.write({"name":"Anitha","role":"Trainer"})

#markdown method to format text
st.markdown("### Features of the Application")
st.markdown("***Bold Text***")
st.markdown("_Italic Text_")
st.markdown("- Item 1\n- Item 2")
st.markdown("<h3 style-color:red'>Done Students</h3>",unsafe_allow_html=True)

# caption method toa dd captions
st.caption ("This is a caption for the student management system.")

#code method to display code snippets
st.code("""
        def add(a,b):
        return a+b
        """,language='python')

#latex method to display mathematical expressions
st.latex(r'''
         a^2+b^2=c^2
         ''')

#divider method to separate sections
st.divider()

#button method to create a button
if st.button("Click Me"):
    st.write("Button Clicked!")
    st.success("Operation Successful")
    st.balloons()
    st.snow()
else:
    st.write("Button Not Clicked Yet")
    st.error("Operation Failed")

#text input method to get user input
name = st.text_input("Enter Student Name")
if name=="":
    st.warning("Name cannot be empty")
elif not name.isalpha():
    st.error("Invalid input please enter only alphabets(no numbers or symbols)")
else:
    st.success(f"Welcome,{name}!")
feedback=st.text_area("enter your feedback")
st.write(feedback)

#checkbox method to create a checkbox
if st.checkbox("I agree to the terms and conditions"):
    st.write("Thank you for agreeing!")

#Radio button method to create radio buttons
gender=st.radio("select your gender:",("Male","Female","Other"))
st.write(f"You selected:{gender}")

#seelctbox method to create a dropdown menu
country=st.selectbox("select your country:",["USA","Canada","UK","Australia","India "])
st.write(f"You selected:{country}")

#multiselect method to create a multi-select dropdown
skills=st.multiselect("select your skills:",["Python","Java","C++","JavaScript","SQL"])
st.write(f"skills:{skills}")

#slider method to create a slider
age=st.slider("select your age:",0,100,25)
st.write(f"Your age is:{age}")

#file uploader method to upload files
upload=st.file_uploader("choose a file:")
if upload is not None:
    st.success("File uploaded successfully!")
    st.write(f"File name:{upload.name}")
#form method to create a form
with st.form("my_form"):
    name=st.text_input("Name:")
    age=st.number_input("Age:",0,100)
    submit=st.form_submit_button("Submit")

    if submit:
        st.write(name,age)

#form submit button method to create a submit button for the form
with st.form("login"):
    user=st.text_input("Username:")
    password=st.text_input("Password:",type="password")
    login=st.form_submit_button("Login")
if login:
    st.success("login successful!")


#columns method to create columns
st.subheader("Dashboard")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Students", 120)

with col2:
    st.metric("Courses", 6)

with col3:
    st.metric("Active", 98)

#divider to separate sections
st.divider()
#container method to create a container
container=st.container()
container.button("Click")

#table method to display data in tabular format
data={
    'Name':['Anurag','Bharath','Chitra'],
    'Age':[23,22,24],   
    'Course':['Python','Java','C++']
}
st.table(data)
#sidebar method to create a sidebar
st.sidebar.title("Menu")
option =st.sidebar.selectbox("Select Option:",["Home","Add Student","View Students","Settings"])
st.sidebar.write(f"You selected:{option}")
st.divider()
