import streamlit as st
import pandas as pd
import io

# Streamlit app title
st.title("Excel Data Transformer - Single Process, Dual Output")
st.markdown(
    """
    ### Instructions:
    Please upload 2 files to transform the data. The app will double the first numeric column in the first file and triple the first numeric column in the second file.

    ### Contact:
    If you have any questions or feedback, please contact the developer at [ngquocthang@gmail.com](mailto:ngqquocthang@gmail.com).
    """
)
with st.sidebar:
    st.header("Customize Graph")
    with st.form("graph_parameters"):
        layout_spacing = st.slider("Layout Spacing", 0.1, 1.0, 0.5)
        color_scheme = st.selectbox(
            "Color Scheme",
            [
                "pinkyl",
                "piyg",
                "plasma",
                "plotly3",
                "portland",
                "prgn",
                "pubu",
                "pubugn",
                "puor",
                "purd",
                "purp",
                "purples",
                "purpor",
                "rainbow",
                "rdbu",
                "rdgy",
                "rdpu",
                "rdylbu",
                "rdylgn",
                "redor",
                "reds",
                "solar",
                "spectral",
                "speed",
                "sunset",
                "sunsetdark",
                "teal",
                "tealgrn",
                "tealrose",
                "tempo",
                "temps",
                "thermal",
                "tropic",
                "turbid",
                "turbo",
                "twilight",
                "viridis",
                "ylgn",
                "ylgnbu",
                "ylorbr",
                "ylorrd",
            ],
            index=91,
        )
        show_labels = st.checkbox("Show Node Labels", value=True)
        show_labels_on_hover = st.checkbox("Show Labels on Hover", value=False)
        node_size = st.slider("Node Size", 1, 100, 10)
        edge_thickness = st.slider("Edge Thickness", 0.1, 5.0, 0.5)
        node_shape = st.selectbox(
            "Node Shape",
            [
                "circle",
                "square",
                "diamond",
                "cross",
                "x",
                "triangle-up",
                "triangle-down",
                "pentagon",
                "hexagon",
                "octagon",
                "star",
                "hexagram",
            ],
            index=0,
        )
        edge_color = st.color_picker("Edge Color", "#888")
        apply_changes = st.form_submit_button("Apply Changes")

# Step 1: Upload the first Excel file
uploaded_file1 = st.file_uploader("Upload your first Excel file", type=["xlsx", "xls"], key="file1")

# Step 2: Upload the second Excel file
uploaded_file2 = st.file_uploader("Upload your second Excel file", type=["xlsx", "xls"], key="file2")

# Function to process the two Excel files and output two transformed files
def process_data(production, sales):
    # Example transformation for the first file
    numeric_cols_1 = production.select_dtypes(include='number').columns
    if not numeric_cols_1.empty:
        production['Doubled'] = production[numeric_cols_1[0]] * 2

    # Example transformation for the second file
    numeric_cols_2 = sales.select_dtypes(include='number').columns
    if not numeric_cols_2.empty:
        sales['Tripled'] = sales[numeric_cols_2[0]] * 3

    # Return the two transformed DataFrames
    return production, sales

# Step 3: If both files are uploaded, process the files
if uploaded_file1 is not None and uploaded_file2 is not None:
    try:
        # Read the uploaded Excel files into DataFrames
        df1 = pd.read_excel(uploaded_file1)
        df2 = pd.read_excel(uploaded_file2)

        # Display the original data (first 10 rows) from both files
        st.subheader("Original Data from File 1 (First 10 Rows)")
        st.write(df1.head(10))

        st.subheader("Original Data from File 2 (First 10 Rows)")
        st.write(df2.head(10))

        # Step 4: Process the data (transform the data based on both files)
        processed_df1, processed_df2 = process_data(df1, df2)

        # Display the transformed data (first 10 rows) from both files
        st.subheader("Transformed Data from File 1 (First 10 Rows)")
        st.write(processed_df1.head(10))

        st.subheader("Transformed Data from File 2 (First 10 Rows)")
        st.write(processed_df2.head(10))

        # Step 5: Prepare to download both transformed files

        # Convert the first processed DataFrame to an Excel file in memory
        output1 = io.BytesIO()
        with pd.ExcelWriter(output1, engine='openpyxl') as writer:
            processed_df1.to_excel(writer, index=False)

        # Convert the second processed DataFrame to an Excel file in memory
        output2 = io.BytesIO()
        with pd.ExcelWriter(output2, engine='openpyxl') as writer:
            processed_df2.to_excel(writer, index=False)

        # Step 6: Provide download buttons for both Excel files (in the same processing step)
        st.download_button(
            label="Download 'Summary' File",
            data=output1.getvalue(),
            file_name="transformed_data_file1.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

        st.download_button(
            label="Download 'Sold' File",
            data=output2.getvalue(),
            file_name="transformed_data_file2.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    except Exception as e:
        st.error(f"Error processing files: {e}")
else:
    st.info("Please upload both Excel files to proceed.")
