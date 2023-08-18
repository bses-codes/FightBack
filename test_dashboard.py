import streamlit as st
import pandas as pd
df = pd.read_csv("Dataa.csv",index_col=0)
st.dataframe(df)