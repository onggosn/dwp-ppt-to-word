"""Formal web front end for the PPTX -> Word pipeline.   Run:  streamlit run app.py"""
import os
import tempfile
from pathlib import Path

import streamlit as st

from pipeline import convert_presentation

st.set_page_config(page_title="Presentation to Word Converter", layout="centered")

st.markdown(
    """
    <style>
      #MainMenu, footer {visibility: hidden;}
      html, body, [class*="css"] {font-family: "Segoe UI", Arial, sans-serif;}
      .block-container {max-width: 760px; padding-top: 2rem;}
      .app-header {background: #1F3A5F; color: #fff; padding: 1.4rem 1.6rem;
                   border-radius: 4px; margin-bottom: 1.5rem;}
      .app-header h1 {color: #fff; font-size: 1.5rem; margin: 0 0 .3rem 0; padding: 0;}
      .app-header p {color: #D6E0EE; margin: 0; font-size: .95rem;}
      .stButton > button, .stDownloadButton > button {
          background: #1F3A5F; color: #fff; border: 0; border-radius: 4px;
          padding: .55rem 1.4rem; font-weight: 600;}
      .stButton > button:hover, .stDownloadButton > button:hover {background: #2B4F80; color: #fff;}
      .stButton > button:disabled {background: #B8C2D0; color: #fff;}
      .step-label {color: #1F3A5F; font-weight: 600; margin: 1.2rem 0 .3rem 0;}
    </style>
    <div class="app-header">
      <h1>Presentation to Word Converter</h1>
      <p>Upload a PowerPoint file and download an editable Word document.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

PROVIDERS = {"None (no text refinement)": "none", "Ollama (local)": "ollama", "Gemini (cloud)": "gemini"}
DEFAULT_MODELS = {"ollama": "qwen2.5-coder:7b", "gemini": "gemini-2.5-flash"}

# ---- Step 1: upload -------------------------------------------------------
st.markdown('<div class="step-label">1. Select presentation</div>', unsafe_allow_html=True)
uploaded = st.file_uploader("PowerPoint file (.pptx)", type=["pptx"], label_visibility="collapsed")

# ---- Step 2: settings -----------------------------------------------------
st.markdown('<div class="step-label">2. Options</div>', unsafe_allow_html=True)
with st.expander("Text refinement and style", expanded=False):
    provider_label = st.radio("Text refinement", list(PROVIDERS), horizontal=True,
                              help="An AI model can merge broken lines and fix typos. "
                                   "Images and text content are never removed.")
    provider = PROVIDERS[provider_label]
    model, api_key, reference = "", None, None

    if provider != "none":
        model = st.text_input("Model", value=DEFAULT_MODELS[provider], key=f"model_{provider}")
    if provider == "gemini":
        if os.environ.get("GOOGLE_API_KEY"):
            st.caption("Using the GOOGLE_API_KEY environment variable.")
        else:
            api_key = st.text_input("Google AI Studio API key", type="password")
        st.caption("Slide text is sent to Google when Gemini is selected.")
    if provider != "none":
        reference = st.file_uploader("Reference HTML for style (optional)", type=["html", "htm"])

# ---- Step 3: convert ------------------------------------------------------
st.markdown('<div class="step-label">3. Convert</div>', unsafe_allow_html=True)
go = st.button("Convert to Word", disabled=uploaded is None)

if go and uploaded is not None:
    st.session_state.pop("result", None)
    work = Path(tempfile.mkdtemp(prefix="pptx2docx_"))
    pptx_path = work / Path(uploaded.name).name
    pptx_path.write_bytes(uploaded.getvalue())
    ref_path = None
    if reference is not None:
        ref_path = work / "reference.html"
        ref_path.write_bytes(reference.getvalue())
    docx_path = work / (pptx_path.stem + ".docx")

    bar = st.progress(0.0, text="Starting")

    def on_progress(fraction: float, message: str) -> None:
        bar.progress(min(max(fraction, 0.0), 1.0), text=message)

    try:
        stats = convert_presentation(pptx_path, docx_path, provider=provider, model=model,
                                     api_key=api_key, reference_html=ref_path,
                                     work_dir=work / "build", progress=on_progress)
        st.session_state["result"] = {"name": docx_path.name, "data": docx_path.read_bytes(),
                                      "stats": stats}
    except Exception as exc:
        bar.empty()
        st.error(f"The conversion could not be completed: {exc}")

# ---- Result ---------------------------------------------------------------
result = st.session_state.get("result")
if result:
    stats = result["stats"]
    st.success("The Word document is ready.")
    cols = st.columns(3)
    cols[0].metric("Images", stats.get("images", 0))
    if "chunks" in stats:
        cols[1].metric("Sections refined", f'{stats["refined"]} / {stats["chunks"]}')
        cols[2].metric("Kept as original", stats["kept_original"])
        if stats["kept_original"]:
            st.caption("Sections kept as original were left unchanged because the refined version "
                       "lost text or an image, or the model could not be reached.")
    st.download_button(
        "Download Word document", data=result["data"], file_name=result["name"],
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    )