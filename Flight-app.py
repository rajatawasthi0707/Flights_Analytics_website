import streamlit as st
from dbhelper import DB
import plotly.graph_objects as go
import plotly.express as px

db = DB()

st.sidebar.title("Flights Analytics")
user_options = st.sidebar.selectbox('Menu', ['Select One', 'View Flights', 'Analytics'])

if user_options == 'View Flights':
    st.title('Check Flights')
    col1, col2 = st.columns(2)
    with col1:
        city = db.fetch_city_names()
        source=st.selectbox('Source', sorted(city))
    with col2:
        city = db.fetch_city_names()
        destination=st.selectbox('Destination', city)
    if st.button('Search'):
        results = db.fetch_all_flights(source, destination)
        if results:
            st.dataframe(results)
        else:
            st.write("No flights found for the selected source and destination.")
elif user_options == 'Analytics':
    airline, frequency = db.fetch_airline_frequency()
    fig = go.Figure(
        go.Pie(
            labels=airline,
            values=frequency,
            hoverinfo="label+percent",
            textinfo="value"
        ))
    st.header("Pie chart")
    st.plotly_chart(fig)

    city, frequency1 = db.busy_airport()
    fig = px.bar(
        x=city,
        y=frequency1
    )
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)
    date, frequency2 = db.daily_frequency()

    print(len(date))
    print(len(frequency2))
    fig = px.line(
        x=date,
        y=frequency2
    )

    st.plotly_chart(fig, theme="streamlit", use_container_width=True)
else:
    pass
