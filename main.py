import numpy as np
import pandas as pd
from pandas_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report
import streamlit as st
import sys, os

st.set_page_config(
    page_title="Data Profile",
    layout="wide",
)


def get_file_size(file):
    size_bytes = sys.getsizeof(file)
    return size_bytes / (1024**2)


def validate_file(file):
    name, ext = os.path.splitext(file.name)
    if ext in (".xlsx", ".csv"):
        return ext
    else:
        return False


with st.sidebar:
    uploaded_file = st.file_uploader(
        "Upload .csv, .xlx files not exceeding 10MB.",
        type=["csv", "xlsx"],
    )
    if uploaded_file is not None:
        st.write("Modes of Operation")
        minimal = st.checkbox("Do you want minimal report?")
        display_mode = st.radio(
            "Display Mode",
            options=("Primary", "Dark", "Orange"),
        )

        if display_mode == "Dark":
            dark_mode = True
            orange_mode = False
        elif display_mode == "Orange":
            dark_mode = False
            orange_mode = True
        else:
            dark_mode = False
            orange_mode = False

if uploaded_file is not None:
    ext = validate_file(uploaded_file)
    if ext:
        filesize = get_file_size(uploaded_file)
        if filesize < 10:
            if ext == ".csv":
                df = pd.read_csv(uploaded_file)
            else:
                xl_file = pd.ExcelFile(uploaded_file, engine="openpyxl")
                sheet_tuple = tuple(xl_file.sheet_names)
                sheet_name = st.sidebar.selectbox("Select the sheet name", sheet_tuple)
                df = xl_file.parse(sheet_name)
        else:
            st.error("File is is too big to be handeled.")
    else:
        st.error("Something went wrong while reading the file")

    # st.dataframe(df)
    # generate report
    with st.spinner("Generating report. Please be patient."):
        pr = ProfileReport(
            df,
            minimal=minimal,
            dark_mode=dark_mode,
            orange_mode=orange_mode,
        )

    st_profile_report(pr)
else:
    st.title("Data Profiler")
    st.info("Upload your data in the left sidebar to generate profilling.")
