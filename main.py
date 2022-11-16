import streamlit as st
from tabula import read_pdf
import pandas as pd
import numpy as np
#reads table from pdf file
# df = read_pdf("abc.pdf",pages="all") #address of pdf file
# print(tabulate(df))
header = lambda df:df.rename(columns=df.iloc[0]).drop(df.index[0]).reset_index(drop=True)

st.title("VIT grade sheet to US 4 point scale converter")
st.write("will convert grade sheet provided on VTOP")
agree = st.checkbox('drop all failed/withdrawn/incomplete courses')
st.write("Ignores all NC(Non Credit Course) Option")
gradeScale = pd.read_csv("grade.csv")
grade_to_gpa = dict(gradeScale[['Grade','Scale']].values)
grade_to_us = dict(gradeScale[['Grade','US Grade Points']].values)

uploaded_file = st.file_uploader("Upload your grade sheet")
if uploaded_file is not None:
    dfs = read_pdf(uploaded_file,pages="all")
    dfs = dfs[:-3]
    nd = []
    for df in dfs:
        nd.append(header(df))
    data = pd.concat(nd,ignore_index=True).drop(columns=['Sl.No'])
    if(agree):
        idx = data[(data["Grade"]=="F") | (data["Grade"].str.startswith("N")) | (data["Grade"]=="Y") | (data["Grade"]=="W")].index
        data.drop(idx , inplace=True)
        data.reset_index(inplace=True)
    data["10 Scale"] = data["Grade"].replace(grade_to_gpa)
    data["4 Scale"] = data["Grade"].replace(grade_to_us)
    data["Final Credits"] = np.where(data['Course\rOption'] == 'NC',0,data['Credits'])
    data['10 scale weights'] = data['10 Scale'].astype(float)*data['Final Credits'].astype(float)
    data['4 scale weights'] = data['4 Scale'].astype(float)*data['Final Credits'].astype(float)
    st.write(data)
    
    col1, col2,col3 = st.columns(3)
    col3.metric("Total credits Earned",round(np.sum(data["Final Credits"].astype(float).values)))
    col1.metric("VIT CGPA",round(data['10 scale weights'].astype(float).sum()/data["Final Credits"].astype(float).sum(),2))
    col2.metric("USA CGPA",round(data['4 scale weights'].astype(float).sum()/data["Final Credits"].astype(float).sum(),2))
st.write("Grade Scale : ")
st.write(header(gradeScale.transpose()))
st.write("source https://www.scholaro.com/gpa-calculator/ select India , All , Vellore Instituite of Technology")