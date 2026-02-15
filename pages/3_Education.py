import streamlit as st
import os

st.title("📚 Elliott Wave Education — Wave 3")

video_path = "assets/animations/w3_intro.mp4"

if os.path.exists(video_path):
    st.video(video_path)
else:
    st.warning("Educational animation not installed yet.")
    st.markdown("""
### What is Wave 3?

Wave 3 is typically:

✅ The strongest impulsive move  
✅ High momentum  
✅ Strong institutional participation  
✅ Clear breakout phase

This is the primary target of FXBot strategy.

(Visual animation coming soon)
""")

st.divider()

st.subheader("Why Wave 3 Matters")

st.write("""
Most traders chase random price moves.

FXBot focuses only on Wave 3 — where probability and momentum align.
""")
