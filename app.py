import streamlit as st
import cv2
import pandas as pd
from deepface import DeepFace
import os
from mark_attendance import mark_attendance_camera

st.set_page_config(page_title="Face Attendance System", layout="centered")
st.title("📸 Face Attendance System")

st.sidebar.title("Instructions")
st.sidebar.info("Click 'Start Camera' to begin face detection and log attendance.\nClick 'Show Attendance' to view today's log.")

if st.button("Start Camera"):
    st.info("Starting camera... Press 'q' to quit.")
    mark_attendance_camera()

if st.button("Show Attendance"):
    try:
        df = pd.read_csv("attendance/attendance.csv")
        st.dataframe(df)
    except FileNotFoundError:
        st.warning("No attendance file found.")

st.markdown("---")
st.caption("Built by Keerthi • Ethical, resilient, and demo-ready")
