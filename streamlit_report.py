import pandas as pd
from pandas.io.pytables import ClosedFileError
import streamlit as st
import altair as alt

def main():
    st.set_page_config(
    page_title="Experiment report",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded")
    df = pd.read_csv("report.csv", sep=";")
    with st.beta_container():
        st.title("Интерактивный отчет, сравнение Dask и Pandas")
        st.markdown("На данном отчете вы можете посмотреть взаимось любых данных нашего экспереминта")
    xaxis = "filesize(mb)"
    yaxis = "process(mb/s)"
    varcolor = "tools"
    with st.beta_container():
        st.altair_chart(
        alt.Chart(df, width=512).mark_circle(size=60).encode(
            x=xaxis, y=yaxis, color=varcolor, tooltip=list(df)
        ).interactive(), False
        )
        st.altair_chart(
        alt.Chart(df, width=512).mark_line(size=3, interpolate=interpol).encode(
            x=xaxis,\
            y='{}({})'.format(agg,yaxis), color=varcolor
        ).interactive()
        )
    with st.sidebar:
        st.header("Тут вы можете изменить настройки графиков")
        xaxis = st.selectbox("Ось x",df.columns)
        yaxis = st.selectbox("Ось y",df.drop(columns=[xaxis]).columns)
        varcolor = st.selectbox("Как разделить наблюдения", df.drop(columns=[xaxis,yaxis]).columns)
        agg = st.selectbox("Агрегация", ["median", "mean"])
        interpol = st.selectbox("Интерполяция", ['basis', 'basis-open', 'basis-closed', 'bundle', 'cardinal', 'cardinal-open', 'cardinal-closed', 'catmull-rom', 'linear', 'linear-closed', 'monotone', 'natural', 'step', 'step-before', 'step-after'])
   
        with st.beta_expander("Набор данных"):
            st.dataframe(df)
            
                
                    


if __name__ == "__main__":
    main()