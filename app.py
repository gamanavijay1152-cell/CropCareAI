import streamlit as st
from PIL import Image
from gtts import gTTS
from datetime import datetime
import tempfile
import csv
import io

# ---------------- PAGE SETTINGS ----------------

st.set_page_config(
    page_title="CropCare AI",
    page_icon="🌱",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #f0fdf4, #ffffff);
}
.main-title {
    color: #166534;
    font-size: 42px;
    font-weight: 800;
    text-align: center;
}
.subtitle {
    color: #4b5563;
    text-align: center;
    font-size: 17px;
}
div.stButton > button {
    background-color: #15803d;
    color: white;
    border-radius: 12px;
    border: none;
    padding: 10px 20px;
    font-weight: bold;
}
div.stButton > button:hover {
    background-color: #166534;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# ---------------- LANGUAGES ----------------

TEXT = {
    "English": {
        "title": "CropCare AI",
        "subtitle": "Smarter crop care. Healthier harvests.",
        "location": "Farm location",
        "farmer": "Farmer Mode",
        "worker": "Agriculture Worker Mode",
        "crop": "Select crop",
        "upload": "Upload a crop photo",
        "symptoms": "Select visible symptoms",
        "yellow": "Yellow leaves",
        "spots": "Brown or black spots",
        "wilt": "Wilting leaves",
        "pests": "Visible insects or pests",
        "other": "Other damage",
        "check": "Check Crop",
        "advice": "Recommended next steps",
        "history": "Recent reports",
        "save": "Save report",
        "voice": "Voice result",
        "download": "Download reports as CSV",
        "healthy": "Possible healthy crop",
        "early": "Possible early blight",
        "late": "Possible late blight",
        "warning": "DEMO MODE: This version does not diagnose disease using a trained AI model.",
        "empty": "Upload a photo before checking the crop.",
        "saved": "Report saved for this session.",
        "symptom_advice": "Record the symptoms and consult a local agriculture officer if the damage continues.",
        "healthy_advice": "The image has received a demo result only. Continue monitoring the crop.",
        "early_advice": "Early blight is only a possibility, not a confirmed diagnosis. Ask an agriculture expert to inspect the plant.",
        "late_advice": "Late blight is only a possibility, not a confirmed diagnosis. Seek expert advice promptly if damage spreads."
    },
    "తెలుగు": {
        "title": "CropCare AI",
        "subtitle": "తెలివైన పంట సంరక్షణ. ఆరోగ్యకరమైన దిగుబడి.",
        "location": "పొలం ఉన్న ప్రదేశం",
        "farmer": "రైతు మోడ్",
        "worker": "వ్యవసాయ కార్యకర్త మోడ్",
        "crop": "పంటను ఎంచుకోండి",
        "upload": "పంట ఫోటోను అప్‌లోడ్ చేయండి",
        "symptoms": "కనిపిస్తున్న లక్షణాలను ఎంచుకోండి",
        "yellow": "పసుపు ఆకులు",
        "spots": "గోధుమ లేదా నల్ల మచ్చలు",
        "wilt": "వాడిపోతున్న ఆకులు",
        "pests": "పురుగులు కనిపిస్తున్నాయి",
        "other": "ఇతర నష్టం",
        "check": "పంటను పరిశీలించండి",
        "advice": "తదుపరి సూచనలు",
        "history": "ఇటీవలి నివేదికలు",
        "save": "నివేదికను సేవ్ చేయండి",
        "voice": "ఫలితాన్ని వినండి",
        "download": "నివేదికలను CSVగా డౌన్‌లోడ్ చేయండి",
        "healthy": "పంట ఆరోగ్యంగా ఉండవచ్చు",
        "early": "ఎర్లీ బ్లైట్ వచ్చే అవకాశం",
        "late": "లేట్ బ్లైట్ వచ్చే అవకాశం",
        "warning": "డెమో మోడ్: ఈ వెర్షన్ శిక్షణ పొందిన AIతో వ్యాధిని నిర్ధారించదు.",
        "empty": "ముందుగా పంట ఫోటోను అప్‌లోడ్ చేయండి.",
        "saved": "ఈ సెషన్‌లో నివేదిక సేవ్ చేయబడింది.",
        "symptom_advice": "లక్షణాలను నమోదు చేసి, సమస్య కొనసాగితే స్థానిక వ్యవసాయ అధికారిని సంప్రదించండి.",
        "healthy_advice": "ఇది డెమో ఫలితం మాత్రమే. పంటను క్రమం తప్పకుండా పరిశీలించండి.",
        "early_advice": "ఇది ఎర్లీ బ్లైట్ అని నిర్ధారణ కాదు. వ్యవసాయ నిపుణుడితో మొక్కను పరిశీలించండి.",
        "late_advice": "ఇది లేట్ బ్లైట్ అని నిర్ధారణ కాదు. నష్టం పెరిగితే వెంటనే నిపుణుడి సలహా తీసుకోండి."
    },
    "हिन्दी": {
        "title": "CropCare AI",
        "subtitle": "बेहतर फसल देखभाल। स्वस्थ पैदावार।",
        "location": "खेत का स्थान",
        "farmer": "किसान मोड",
        "worker": "कृषि कार्यकर्ता मोड",
        "crop": "फसल चुनें",
        "upload": "फसल की फोटो अपलोड करें",
        "symptoms": "दिखने वाले लक्षण चुनें",
        "yellow": "पीली पत्तियाँ",
        "spots": "भूरे या काले धब्बे",
        "wilt": "मुरझाई पत्तियाँ",
        "pests": "कीड़े या कीट दिखाई दे रहे हैं",
        "other": "अन्य नुकसान",
        "check": "फसल की जाँच करें",
        "advice": "अगले कदम",
        "history": "हाल की रिपोर्ट",
        "save": "रिपोर्ट सेव करें",
        "voice": "परिणाम सुनें",
        "download": "रिपोर्ट CSV में डाउनलोड करें",
        "healthy": "फसल स्वस्थ हो सकती है",
        "early": "अर्ली ब्लाइट की संभावना",
        "late": "लेट ब्लाइट की संभावना",
        "warning": "डेमो मोड: यह संस्करण प्रशिक्षित AI से रोग का निदान नहीं करता।",
        "empty": "पहले फसल की फोटो अपलोड करें।",
        "saved": "इस सेशन में रिपोर्ट सेव हो गई।",
        "symptom_advice": "लक्षण दर्ज करें और समस्या जारी रहने पर स्थानीय कृषि अधिकारी से सलाह लें।",
        "healthy_advice": "यह केवल डेमो परिणाम है। फसल की नियमित निगरानी करें।",
        "early_advice": "यह पक्की बीमारी की पहचान नहीं है। कृषि विशेषज्ञ से पौधे की जाँच करवाएँ।",
        "late_advice": "यह पक्की बीमारी की पहचान नहीं है। नुकसान फैलने पर तुरंत विशेषज्ञ से सलाह लें।"
    }
}

# ---------------- SESSION DATA ----------------

if "reports" not in st.session_state:
    st.session_state.reports = []

if "latest_result" not in st.session_state:
    st.session_state.latest_result = None

# ---------------- HEADER ----------------

language = st.sidebar.selectbox(
    "🌐 Language / భాష / भाषा",
    ["English", "తెలుగు", "हिन्दी"]
)

t = TEXT[language]

st.markdown(
    f'<div class="main-title">🌱 {t["title"]}</div>',
    unsafe_allow_html=True
)

st.markdown(
    f'<div class="subtitle">{t["subtitle"]}</div>',
    unsafe_allow_html=True
)

st.write("")

st.warning(t["warning"])

# ---------------- SIDEBAR ----------------

st.sidebar.header("🌾 CropCare Menu")

mode = st.sidebar.radio(
    "Choose access mode",
    [t["farmer"], t["worker"]]
)

location = st.sidebar.text_input(
    t["location"],
    placeholder="e.g. Guntur"
)

st.sidebar.info(
    "Designed for farmers, agriculture workers, "
    "and users who prefer local-language support."
)

# ---------------- DASHBOARD CARDS ----------------

c1, c2, c3 = st.columns(3)

with c1:
    st.metric("🌱 Project", "CropCare AI")

with c2:
    st.metric("🗣️ Languages", "3")

with c3:
    st.metric(
        "📋 Session Reports",
        len(st.session_state.reports)
    )

st.divider()

# ---------------- MAIN TABS ----------------

tab1, tab2, tab3 = st.tabs([
    "📸 Crop Check",
    "🩺 Symptom Guide",
    "📊 Reports"
])

# ---------------- CROP CHECK ----------------

with tab1:

    st.subheader("📸 Crop Health Check")

    if mode == t["worker"]:
        st.info(
            "Worker mode: take the photo with the farmer's "
            "permission and explain the result in their language."
        )

    crop_options = [
    "Tomato",
    "Rice",
    "Cotton",
    "Potato",
    "Chilli",
    "Maize",
    "Groundnut",
    "Mango",
    "Black Gram",
    "Green Gram"
]

crop = st.selectbox("🌱 Select your crop", crop_options)

photo = st.file_uploader(
        t["upload"],
        type=["jpg", "jpeg", "png"]
    )

if photo:
        image = Image.open(photo).convert("RGB")

        st.image(
            image,
            caption="Uploaded crop photo",
            width=450
        )

        st.caption(
            f"Image size: {image.width} × {image.height}"
        )

symptoms = st.multiselect(
        t["symptoms"],
        [
            t["yellow"],
            t["spots"],
            t["wilt"],
            t["pests"],
            t["other"]
        ]
    )

if st.button(t["check"], use_container_width=True):

        if not photo:
            st.error(t["empty"])

        else:
            # DEMO ONLY — NOT A REAL AI CLASSIFIER.
            # Replace this logic after training and connecting a model.
            demo_classes = [
                ("Healthy", t["healthy"], t["healthy_advice"]),
                ("Early Blight", t["early"], t["early_advice"]),
                ("Late Blight", t["late"], t["late_advice"])
            ]

            demo_index = (
                image.width + image.height
            ) % len(demo_classes)

            class_name, display_name, advice = demo_classes[demo_index]

            if symptoms:
                advice = t["symptom_advice"]

            result = {
                "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "location": location or "Not provided",
                "crop": crop,
                "result": display_name,
                "symptoms": ", ".join(symptoms) or "None selected",
                "advice": advice
            }

            st.session_state.latest_result = result

            st.success("### " + display_name)

            st.write("**" + t["advice"] + "**")
            st.write(advice)

            st.info(
                "This is a demonstration result. Do not use it "
                "to decide pesticide application or treatment."
            )

    # Voice is outside the Check button so it remains usable
    # after Streamlit reruns the page.
if st.session_state.latest_result:

        result = st.session_state.latest_result

        st.subheader("🔊 " + t["voice"])

        if st.button("Generate voice"):
            language_codes = {
                "English": "en",
                "తెలుగు": "te",
                "हिन्दी": "hi"
            }

            try:
                speech_text = (
                    result["result"] + ". " + result["advice"]
                )

                with tempfile.NamedTemporaryFile(
                    suffix=".mp3",
                    delete=False
                ) as audio_file:

                    audio_path = audio_file.name

                gTTS(
                    text=speech_text,
                    lang=language_codes[language]
                ).save(audio_path)

                with open(audio_path, "rb") as f:
                    st.audio(f.read(), format="audio/mp3")

            except Exception as error:
                st.error(
                    "Voice generation failed. Check your "
                    "internet connection and try again."
                )

        if st.button(t["save"], use_container_width=True):

            st.session_state.reports.append(
                st.session_state.latest_result.copy()
            )

            st.success(t["saved"])

# ---------------- SYMPTOM GUIDE ----------------

with tab2:

    st.subheader("🩺 Simple Symptom Guide")

    st.write(
        "Select the symptom you can see on the plant. "
        "This guide helps you record observations; it does "
        "not confirm a disease."
    )

    st.markdown("### 🍃 Yellow leaves")
    st.write(
        "Possible causes include nutrient problems, watering "
        "stress, pests, or disease."
    )

    st.markdown("### 🟤 Brown or black spots")
    st.write(
        "Spots can have several causes. Photograph both sides "
        "of the leaf and seek expert advice if they spread."
    )

    st.markdown("### 🥀 Wilting")
    st.write(
        "Check soil moisture and inspect the plant. Wilting "
        "can be caused by water stress or disease."
    )

    st.markdown("### 🐛 Visible pests")
    st.write(
        "Take a clear close-up photo and record which part of "
        "the plant is affected."
    )

    st.warning(
        "Do not apply pesticides based only on these symptoms. "
        "Confirm the cause with a qualified agriculture expert."
    )

# ---------------- REPORTS ----------------

with tab3:

    st.subheader("📊 " + t["history"])

    reports = st.session_state.reports

    if reports:

        st.dataframe(
            reports,
            use_container_width=True,
            hide_index=True
        )

        output = io.StringIO()

        fieldnames = [
            "time",
            "location",
            "crop",
            "result",
            "symptoms",
            "advice"
        ]

        writer = csv.DictWriter(
            output,
            fieldnames=fieldnames
        )

        writer.writeheader()
        writer.writerows(reports)

        st.download_button(
            label=t["download"],
            data=output.getvalue(),
            file_name="cropcare_reports.csv",
            mime="text/csv",
            use_container_width=True
        )

        if st.button("Clear session reports"):
            st.session_state.reports = []
            st.session_state.latest_result = None
            st.rerun()

    else:
        st.info(
            "No reports saved yet. Check a crop and select "
            "'Save report' to add one."
        )

# ---------------- FOOTER ----------------

st.divider()

st.markdown(
    "<center>🌱 CropCare AI | SIH26131 | "
    "Early Detection and Management of Crop Diseases</center>",
    unsafe_allow_html=True
)