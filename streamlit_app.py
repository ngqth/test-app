import streamlit as st
import pandas as pd
import io

# Streamlit app title
st.title("Excel Data Transformer")

# Step 1: Upload the Excel file
uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx", "xls"])

# Function to process the Excel file
def process_data(df):
    # Example transformation: Add a new column with doubled values of the first numeric column
    # This is just a placeholder; modify it as needed for your transformation logic
    df['Processed'] = df.iloc[:, 0] * 2
    return df

# Step 2: If a file is uploaded, process the file
if uploaded_file is not None:
    try:
        # Read the uploaded Excel file into a DataFrame
        df = pd.read_excel(uploaded_file)

        # Display the original data (first 10 rows)
        st.subheader("Original Data (First 10 Rows)")
        st.write(df.head(10))

        # Step 3: Process the data (transform the data)
        processed_df = process_data(df)

        # Display the transformed data (first 10 rows)
        st.subheader("Transformed Data (First 10 Rows)")
        st.write(processed_df.head(10))

        # Step 4: Download the transformed data as an Excel file
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            processed_df.to_excel(writer, index=False)

        # Step 5: Provide a download button for the transformed Excel file
        st.download_button(
            label="Download Transformed Excel File",
            data=output.getvalue(),
            file_name="transformed_data.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    except Exception as e:
        st.error(f"Error processing file: {e}")
else:
    st.info("Please upload an Excel file to proceed.")
