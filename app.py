import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


st.set_page_config(
    page_title="Titanic EDA",
    layout="wide"
)


st.title("Exploratory Data Analysis Interface")
st.write("Upload a CSV dataset and explore its structure, statistics, and visual patterns.")



st.sidebar.header("EDA Controls")

uploaded_file = st.sidebar.file_uploader(
    "Upload CSV File",
    type=["csv"]
)



if uploaded_file is not None:

    try:

    
        df = pd.read_csv(uploaded_file)

        st.sidebar.success("CSV file loaded successfully.")


        st.header("Dataset Preview")

        st.dataframe(df.head())


        st.header("Dataset Dimensions")

        rows, columns = df.shape

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Number of Rows", rows)

        with col2:
            st.metric("Number of Columns", columns)

        st.header("Column Data Types")

        dtype_df = pd.DataFrame({
            "Column": df.columns,
            "Data Type": df.dtypes.astype(str)
        })

        st.dataframe(dtype_df)

   

        st.header("Missing Values")

        missing_df = pd.DataFrame({
            "Column": df.columns,
            "Missing Values": df.isnull().sum()
        })

        st.dataframe(missing_df)


        st.header("Numerical Statistics")

        numerical_columns = df.select_dtypes(
            include="number"
        ).columns

        if len(numerical_columns) > 0:

            statistics = pd.DataFrame({
                "Mean": df[numerical_columns].mean(),
                "Median": df[numerical_columns].median(),
                "Minimum": df[numerical_columns].min(),
                "Maximum": df[numerical_columns].max()
            })

            st.dataframe(statistics)

        else:

            st.write("No numerical attributes found.")

   

        st.sidebar.header("Attribute Selection")

        selected_column = st.sidebar.selectbox(
            "Select a column for analysis",
            df.columns
        )


        if pd.api.types.is_numeric_dtype(df[selected_column]):

            attribute_type = "Numerical"

        else:

            attribute_type = "Categorical"

        st.subheader("Selected Attribute")

        st.write("Column:", selected_column)
        st.write("Attribute Type:", attribute_type)


        st.header("Visualization")

        if attribute_type == "Numerical":

            st.subheader(
                f"Distribution of {selected_column}"
            )

            fig, ax = plt.subplots()

            ax.hist(
                df[selected_column].dropna(),
                bins=20
            )

            ax.set_xlabel(selected_column)
            ax.set_ylabel("Frequency")
            ax.set_title(
                f"Histogram of {selected_column}"
            )

            st.pyplot(fig)

        else:

            st.subheader(
                f"Frequency of {selected_column}"
            )

            counts = df[selected_column].value_counts()

            fig, ax = plt.subplots()

            counts.plot(
                kind="bar",
                ax=ax
            )

            ax.set_xlabel(selected_column)
            ax.set_ylabel("Frequency")
            ax.set_title(
                f"Frequency of {selected_column}"
            )

            plt.xticks(rotation=45)

            st.pyplot(fig)

    except Exception as e:

        st.error(
            "The uploaded file could not be read as a valid CSV file."
        )

        st.write("Error:", e)

else:

    st.info(
        "Please upload a CSV file from the sidebar to begin."
    )
