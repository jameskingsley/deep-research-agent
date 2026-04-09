import streamlit as st
import requests
import json
from fpdf import FPDF
from datetime import datetime

# Page config
st.set_page_config(
    page_title="Deep Research Agent", 
    layout="wide"
)

# PDF Generation Helper
def create_pdf(text, topic):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, f"Research Report: {topic}", ln=True, align='C')
    pdf.set_font("Arial", size=10)
    pdf.cell(0, 10, f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}", ln=True, align='C')
    pdf.ln(10)
    
    pdf.set_font("Arial", size=11)
    # multi_cell handles line breaks and long text
    # encoding 'latin-1' helps prevent issues with special characters in PDF
    pdf.multi_cell(0, 8, txt=text.encode('latin-1', 'replace').decode('latin-1'))
    return pdf.output(dest='S').encode('latin-1')

# Custom Styling 
st.markdown("""
    <style>
    .report-container {
        padding: 20px;
        border-radius: 5px;
        background-color: #ffffff;
        border: 1px solid #e6e9ef;
        color: #31333F;
    }
    .stButton>button {
        width: 100%;
        background-color: #333333;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# Sidebar 
with st.sidebar:
    st.title("Agent Control")
    st.write("Infrastructure: Groq + Tavily")
    st.divider()
    st.info("System uses iterative autonomous search. Initial queries are refined automatically based on data density.")
    if st.button("Clear Session"):
        st.rerun()

# Main UI 
st.title("Deep Research Agent")
st.caption("Professional Multi-Agent Research Framework")

topic = st.text_input("Research Topic:", placeholder="Enter your research query here")

if st.button("Execute Research"):
    if topic:
        with st.spinner("Processing research iterations..."):
            try:
                # API Call to FastAPI backend
                res = requests.post(
                    "https://deep-research-agent-3nl8.onrender.com/research", 
                    json={"topic": topic},
                    timeout=300
                )
                
                if res.status_code == 200:
                    report_data = res.json()["data"]
                    
                    st.success("Analysis Complete")
                    
                    # Layout columns
                    col1, col2 = st.columns([4, 1])
                    
                    with col1:
                        st.markdown("### Analysis Report")
                        st.markdown(f'<div class="report-container">{report_data}</div>', unsafe_allow_html=True)
                    
                    with col2:
                        st.write("### Exports")
                        # Export as Text
                        st.download_button(
                            label="Download TXT",
                            data=report_data,
                            file_name=f"research_{datetime.now().strftime('%Y%m%d')}.txt",
                            mime="text/plain"
                        )
                        
                        # Export as PDF
                        try:
                            pdf_bytes = create_pdf(report_data, topic)
                            st.download_button(
                                label="Download PDF",
                                data=pdf_bytes,
                                file_name=f"research_{datetime.now().strftime('%Y%m%d')}.pdf",
                                mime="application/pdf"
                            )
                        except Exception as e:
                            st.error(f"Export Error: {e}")

                else:
                    st.error(f"Status Code: {res.status_code}")
                    st.write(res.text)
            except Exception as e:
                st.error("Connection Failed. Verify FastAPI service is active.")
                st.exception(e)
    else:
        st.warning("Input required.")

# --- Footer ---
st.divider()
st.caption("Technical Research Framework. Built for academic and professional documentation.")