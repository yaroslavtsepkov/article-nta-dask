import pandas as pd
import streamlit as st
import altair as alt

st.set_page_config(
    page_title="Experiment report",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded")
    
def main():
	    
	df = pd.read_csv("report.csv", sep=",", dtype={
	"timestamp":float,
	"tool":str,
	"filesize(mb/s)":str,
	"os":str,
	"ram(gb)":str,
	"drive type":str,
	"process(mb/s)":float,
	"researcher":str
	})
	with st.container():
		st.title("Интерактивный отчет, сравнение Dask и Pandas")
		st.markdown("На данном отчете вы можете посмотреть взаимось любых данных нашего экспереминта")
		with st.expander("Нажать для просмотра всех данных"):
			st.dataframe(df)
	col1, col2 = st.columns(2)
	with col1:
		st.markdown("Результаты эксперементов. Исследователь Цепков Я.А.")
		temp = df.query("researcher == 'y.tsepkov'")
#		st.altair_chart(
#			alt.chart(temp).mark_boxplot().encode(
#			x = "filesize(mb):q", y = "process(mb/s)",\
#			use_container_width=true)

	with col2:
		st.markdown("Результаты эксперементов. Исследователь Поручиков М.А.")
		temp = df.query("researcher == 'm.poruchikov'")
		st.altair_chart(
			alt.Chart(temp).mark_line().encode(
			x = "filesize(mb):Q", y = "process(mb/s)",color="tool", size="ram(gb)"),\
			use_container_width=True)
			
	with st.container():
		temp = df.groupby(["filesize(mb)","ram(gb)","os","drive type", "researcher"]).agg({"process(mb/s)":"mean"}).reset_index()
		st.altair_chart(
			alt.Chart(temp).mark_bar().encode(x="ram(gb)", y="mean(process(mb/s))",\
		color="researcher"), use_container_width=False)
		st.altair_chart(
			alt.Chart(temp).mark_bar().encode(
				x="os", y="mean(process(mb/s))",color="ram(gb)",column="researcher"),use_container_width=False)
		with col3:
			st.altair_chart(
				alt.Chart(temp).mark_bar().encode(
					x="drive type", y="mean(process(mb/s))",color="ram(gb)", column="researcher"), use_container_width=True)

if __name__ == "__main__":
    main()
