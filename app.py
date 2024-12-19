import pandas as pd  # Used for handling and manipulating tabular data.
import streamlit as st # Create web apps
import xml.etree.ElementTree as ET # To parse and extract data from XML files.
import csv # For reading and writing CSV

# Page configuration
st.set_page_config(
    page_title="Personal App",
    page_icon="favicon.ico",
    layout="wide"
)

# Styling the app
st.markdown("""
    <style>
        /* Add your custom CSS here */
        h1 {
            font-size: 3em;
            color: #273746;
            margin-bottom: 20px;
            font-weight: 900;
            text-align: center;
        }
        p {
            font-size: 1.1em;
            color: #A0A9B7;
            margin-bottom: 30px;
        }
            
        .css-1awe9bt:hover {
            background-color: #357ABD;
            cursor: pointer;
        }

        .css-1v3fvcr {
            width: 90% !important;
            margin: 0 auto;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
            background-color: #FFFFFF;
        }

        .css-1v3fvcr table {
            border-collapse: separate;
            border-spacing: 0;
            width: 100%;
        }

        .css-1v3fvcr th,
        .css-1v3fvcr td {
            padding: 12px 15px;
            text-align: left;
            font-size: 1em;
        }

        .css-1v3fvcr th {
            background-color: #4A90E2;
            color: white;
            font-size: 1.1em;
        }

        .css-1v3fvcr tr:nth-child(even) {
            background-color: #F1F4F9;
        }

        .css-1v3fvcr tr:nth-child(odd) {
            background-color: #FFFFFF;
        }

        .css-1v3fvcr tr:hover {
            background-color: #D1D9E6;
        }

        .css-14xtv0n {
            font-size: 1.2em;
            font-weight: 500;
            color: #4A90E2;
        }
            
        .st-emotion-cache-le7ohw p {
            word-break: break-word;
            margin-bottom: 0px;
            font-size: 14px;
            color: #41464d;
            font-weight: bold !important;
        }
        
        .st-emotion-cache-nrabgc p {
            word-break: break-word;
            font-size: 1.1em;
            color: #646568;
            margin-bottom: 25px;
            font-weight: bold;
        }
            
        .st-cp {
            width: 1.5rem;
        }
            
        .st-cn {
            fill: #506a58;
        }
            
        .st-emotion-cache-1rrh444{
            font-size: 2.25rem;
            color: #57b603;
            font-weight:bold;
            border-bottom: 2px solid #000;
        }
        
        .st-emotion-cache-16f4bz0 ,th{
            border: 1px solid #000000;
            vertical-align: middle;
            text-align: center;
            padding: 0.25rem 0.375rem;
            font-weight: 400;
            color: #000000;
        }
            
        .st-emotion-cache-6nj7z3 {
            border: 1px solid #000000;
            vertical-align: middle;
            padding: 0.25rem 0.375rem;
            font-weight: 400;
        }
        .st-emotion-cache-o3y40v { 
            display: flex;
            -webkit-box-align: center;
            align-items: center;
            -webkit-box-pack: center;
            justify-content: center;
            font-weight: 400;
            padding: 0.25rem 0.75rem;
            border-radius: 0.5rem;
            min-height: 2.5rem;
            margin: 0px;
            line-height: 1.6;
            color: inherit;
            width: auto;
            cursor: pointer;
            user-select: none;
            background-color: rgb(249, 249, 251);
            border: 1px solid rgba(38, 39, 48, 0.2);
        }
        .st-emotion-cache-v9anok p {
            word-break: break-word;
            margin-bottom: 0px;
            color : #000000;
        }
            
        .st-cp {
            width: auto;
        }
            
    </style>
""", unsafe_allow_html=True)

# Welcome Header
with st.container():
    st.markdown('<h1>Welcome to Your Personal App</h1>', unsafe_allow_html=True)
st.write("This tool allows you to upload and convert XML job data file. You can filter and download the data for easy analysis and reporting. With its simple, interactive interface, it's perfect for job management, system monitoring, and data analysis tasks.")

# Function to load data
def loaddata(path):
    return pd.read_csv(path)  # Read the CSV file

# Function to write XML data to CSV file
def xml_to_csv(xml_file_path, csv_file_path):
    try:
        tree = ET.parse(xml_file_path)  # Parse XML file
        root = tree.getroot()  # Get the root element of the XML
        col_name = ["LastUpdated", "Source", "Target", "Triggered_By_Button", "Button_Location", "Description","IsScheduled", "Other Comments"]  # Column structure
        with open(csv_file_path, mode="w", newline="") as csv_file:  # Open a CSV file
            data = csv.writer(csv_file)  # Write into CSV file
            cols = ["Job Name", "Job Type", "ModifiedBy"] + col_name  # Header row of the CSV file
            data.writerow(cols)
            for job in root.findall(".//job"):  # Loop through each job element within the XML
                job_name = job.get("name")  # Get the job name
                job_type = job.get("type")  # Get the job type
                modifiedby = job.get("modifiedBy")  # Get the modifiedBy attribute
                comment_data = {field: "" for field in col_name[:-1]}  # Initialize empty dictionary for comments
                comment_data["Other Comments"] = ""  # Separate column for plain text
                comment = job.find("comment")  # Get the comment element inside the job
                if comment is not None:
                    comment_text = comment.text.strip()  # Retrieve the text within comment section
                    parts = comment_text.split("$")  # Split comment text by "$" to get each line separately
                    plain_text_found = False
                    for part in parts:
                        if ":" in part:  # Check for key-value pairs
                            key, value = part.split(":", 1)  # Split by ":" if found
                            key = key.strip()  # Remove whitespaces
                            value = value.strip()  # Remove whitespaces
                            if key in comment_data:
                                comment_data[key] = value
                        else:
                            plain_text_found = True
                            comment_data["Other Comments"] = part.strip()
                row = [job_name] + [job_type] + [modifiedby] + [comment_data[field] for field in col_name]  # Collect row data
                data.writerow(row)  # Write data into the CSV
        # print("Data has been written to", csv_file_path)
    except ET.ParseError as e:
        print("Parse Error: ", e)  # Exception handling

# File Upload Handling
uploaded_file = st.file_uploader("Upload an XML file", type=["xml"])  # Allow users to upload an XML file

# File Handling
if uploaded_file is not None:
    try:
        # Save the uploaded XML file temporarily
        xml_file_path = "uploaded_file.xml"  # Temporary path for the uploaded XML
        with open(xml_file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())  # Save the file in binary mode
        st.success("File uploaded successfully")  # Success message
        
        # Define the output CSV file path
        csvfilename = "extracted_jobs.csv"
        
        # Convert the XML file to CSV
        xml_to_csv(xml_file_path, csvfilename)
        
        # Load and display the data if the file is processed successfully
        df = loaddata(csvfilename)  # Load the CSV file into a DataFrame
        
        # Create filter interface
        left, right = st.columns(2)
        with left:
            col_name = st.selectbox("Select column to filter by", df.columns)  # Select column to filter by
        uniqueValues = df[col_name].unique().tolist()
        uniqueValues.insert(0, "All")
        with right:
            selected_Value = st.multiselect(f"Filter By {col_name}:", uniqueValues, default="All")  # Multi-select for filter options
        if "All" in selected_Value or not selected_Value:  # Default selection shows all records
            filter_table = df
        else:
            filter_table = df[df[col_name].isin(selected_Value)]  # Filter the data based on selected values
        record_count = len(filter_table)  # Get the number of records in the filtered table

        # To get the name of the project
        tree = ET.parse(xml_file_path) 
        root = tree.getroot()
        project_name = root.get('name')
        download_csv = f"{project_name}.csv"

        # For styling the metric area of the app
        col_1,col_2,col_3,col_4 = st.columns(4)
        with col_1:
            st.metric(label="Project Name: ", value=project_name)
        with col_2:
            st.metric(label="Number of Records Retrieved:", value=record_count)
        with col_3:
            st.metric(label="Category: ", value="Integration")
        csv_data = filter_table.to_csv(index=False)
        with col_4:
            st.download_button("Download",data=csv_data,file_name=download_csv,mime="text/csv",)
        
        # Display the filtered table
        st.write("Job Details Table:")
        st.table(filter_table)  # Display the filtered table

    except Exception as e:
        st.error(f"Error processing the uploaded file: {e}")
else:
    st.warning("Please upload an XML file to proceed.")
