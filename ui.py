import streamlit as st
import pandas as pd
import scheduling
import memory
import features
import system_calls
import synchronization
import commands

def home():
    st.markdown("""
    <div style='display: flex; align-items: center; justify-content: space-between;'>
        <div>
            <h1 style='font-size: 80px'>OpenBSD</h1>
            <h2 style='font-size: 45px'>Done by Group 13</h2>
            <ul style='list-style-type: none; padding: 0;'>
                <li style='font-size: 20px'><strong>Jaideep P</strong>: CB.EN.U4CSE22563</li>
                <li style='font-size: 20px'><strong>Sudhakar KS</strong>: CB.EN.U4CSE22550</li>
                <li style='font-size: 20px'><strong>Suren Adithiya B</strong>: CB.EN.U4CSE22551</li>
                <li style='font-size: 20px'><strong>Praysun Raja M</strong>: CB.EN.U4CSE22537</li>
            </ul>
        </div>
        <div>
            <img src="https://upload.wikimedia.org/wikipedia/en/8/83/OpenBSD_Logo_-_Cartoon_Puffy_with_textual_logo_below.svg" style='width: 300px; height: auto;'/>
        </div>
    </div>
    """, unsafe_allow_html=True)




page_element="""
<style>
[data-testid="stAppViewContainer"]{
  background-image: url("https://e0.pxfuel.com/wallpapers/157/770/desktop-wallpaper-minimalism-gradient-background-fou3ie-dark-purple-gradient.jpg");
  background-size: cover;
}
</style>
"""

st.markdown(page_element, unsafe_allow_html=True)

# Sidebar for navigation
st.sidebar.title("Dashboard Navigation")
option = st.sidebar.selectbox("Choose a feature", ["Home", "OpenBSD Features", "Commands", "System Calls", "ULE Scheduler", "Buddy Allocator", "Synchronization"])

# Display selected feature
if option == "Home":
    home()
elif option == "OpenBSD Features":
    features.main()
elif option == "Commands":
    commands.main()
elif option == "System Calls":
    system_calls.main()
elif option == "Buddy Allocator":
    memory.main()
elif option == "ULE Scheduler":
    scheduling.main()
elif option == "Synchronization":
    synchronization.main()
