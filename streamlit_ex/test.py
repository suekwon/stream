import streamlit as st
import pandas as pd

st.title("Hello, Streamlit!!")
st.write("Welcome to your first Streamlit app.")

dt = {
    'first column': [1, 2, 3, 4],
    'second column': [10, 20, 30, 40]
}
df = pd.DataFrame(dt)
df = pd.DataFrame(
    {
    'first column': [1, 2, 3, 4],
    'second column': [10, 20, 30, 40]
    }
)
df