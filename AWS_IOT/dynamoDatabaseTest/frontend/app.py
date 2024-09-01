import streamlit as st
import datetime
import time
import pandas as pd

# Initialize session state
if 'alarms' not in st.session_state:
    st.session_state.alarms = []

def main():
    st.title("Alarm App")

    # Sidebar for navigation
    page = st.sidebar.selectbox("Choose a page", ["Set Alarm", "Alarm List", "Settings", "Analytics"])

    if page == "Set Alarm":
        set_alarm_page()
    elif page == "Alarm List":
        alarm_list_page()
    elif page == "Settings":
        settings_page()
    elif page == "Analytics":
        analytics_page()

def set_alarm_page():
    st.header("Set New Alarm")
    alarm_time = st.time_input("Set alarm time")
    alarm_name = st.text_input("Alarm name")
    if st.button("Set Alarm"):
        new_alarm = {"time": alarm_time, "name": alarm_name}
        st.session_state.alarms.append(new_alarm)
        st.success(f"Alarm set for {alarm_time}")

def alarm_list_page():
    st.header("Your Alarms")
    for idx, alarm in enumerate(st.session_state.alarms):
        st.write(f"{alarm['name']} - {alarm['time']}")
        if st.button(f"Delete Alarm {idx}"):
            st.session_state.alarms.pop(idx)
            st.experimental_rerun()

def settings_page():
    st.header("Settings")
    st.write("(Placeholder for settings)")

def analytics_page():
    st.header("Analytics")
    if st.session_state.alarms:
        df = pd.DataFrame(st.session_state.alarms)
        st.write("Alarm Statistics:")
        st.write(f"Total Alarms: {len(df)}")
        st.write(f"Earliest Alarm: {df['time'].min()}")
        st.write(f"Latest Alarm: {df['time'].max()}")
    else:
        st.write("No alarms set yet.")

if __name__ == "__main__":
    main()
