
import streamlit as st
import math
from datetime import date, time

# =====================================================
# 1. KONFIGURASI
# =====================================================

st.set_page_config(
    page_title="Solar Position Calculator",
    page_icon="☀️",
    layout="wide"
)

# =====================================================
# 2. CUSTOM CSS
# =====================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Comic+Neue:wght@400;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Comic Sans MS', 'Comic Neue', cursive !important;
}

.stApp {
    background: linear-gradient(135deg, #FFF8EF, #FFE9D2, #FFF3E7);
}

.block-container {
    max-width: 1150px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

h1, h2, h3 {
    color: #A94F20 !important;
    font-family: 'Comic Sans MS', 'Comic Neue', cursive !important;
    font-weight: bold !important;
}

p, label {
    color: #87451F;
}

div[data-testid="stWidgetLabel"] p {
    color: #87451F !important;
    font-weight: bold !important;
}

.stNumberInput input,
.stDateInput input,
.stTimeInput input {
    background-color: #FFFCF8 !important;
    color: #75401F !important;
    border: 2px solid #FFD0A6 !important;
    border-radius: 12px !important;
}

/* Tombol plus dan minus */
div[data-testid="stNumberInput"] button {
    background-color: #FFE4CC !important;
    color: #A94F20 !important;
    border: 1px solid #FFD0A6 !important;
    border-radius: 8px !important;
    opacity: 1 !important;
    cursor: pointer !important;
}

div[data-testid="stNumberInput"] button:hover {
    background-color: #FFC18F !important;
    color: #873D16 !important;
}

.stSelectbox div[data-baseweb="select"] {
    background-color: #FFFCF8 !important;
    border-radius: 12px !important;
}

div.stButton > button {
    width: 100%;
    min-height: 52px;
    background: linear-gradient(90deg, #FF9D50, #F47B35);
    color: white !important;
    border: none !important;
    border-radius: 15px !important;
    font-family: 'Comic Sans MS', 'Comic Neue', cursive !important;
    font-size: 18px !important;
    font-weight: bold !important;
    transition: 0.2s;
}

div.stButton > button:hover {
    background: #E96C2C !important;
    transform: translateY(-2px);
}

div[data-testid="stMetric"] {
    background-color: #FFF9F2;
    border: 2px solid #FFD3AE;
    padding: 20px;
    border-radius: 18px;
}

div[data-testid="stMetricLabel"] {
    color: #A65B2D !important;
    font-weight: bold;
}

div[data-testid="stMetricValue"] {
    color: #E87532 !important;
    font-weight: bold;
}

div[data-testid="stAlert"] {
    border-radius: 14px;
}

hr {
    border-color: #FFD3AE !important;
}

</style>
""", unsafe_allow_html=True)


# =====================================================
# 3. HEADER
# =====================================================

st.write("")

with st.container(border=True):
    st.markdown(
        "<h1 style='text-align:center;'>☀️</h1>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<h1 style='text-align:center;'>Solar Position Calculator</h1>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<p style='text-align:center;'>Let's Explore the Position of the Sun! 🌻</p>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<p style='text-align:center;'>Calculate the Azimuth and Elevation of the Sun Based on Geographic Location</p>",
        unsafe_allow_html=True
    )

st.write("")


# =====================================================
# 4. INPUT DATA
# =====================================================

st.subheader("🌍 Data Pengamatan Matahari")

col1, col2 = st.columns(2)

with col1:
    tanggal = st.date_input(
        "📅 Tanggal Pengamatan",
        value=date.today()
    )

    latitude = st.number_input(
        "📍 Latitude (°)",
        min_value=-90.0,
        max_value=90.0,
        value=4.1445,
        step=0.0001,
        format="%.4f"
    )

    waktu = st.time_input(
        "⏰ Waktu Pengamatan",
        value=time(12, 0)
    )

with col2:
    longitude = st.number_input(
        "🌐 Longitude (°)",
        min_value=-180.0,
        max_value=180.0,
        value=96.1289,
        step=0.0001,
        format="%.4f"
    )

    zona_waktu = st.selectbox(
        "🕒 Zona Waktu",
        ["WIB (UTC+7)", "WITA (UTC+8)", "WIT (UTC+9)"]
    )


# =====================================================
# 5. KARAKTER MATAHARI
# =====================================================

with st.container(border=True):
    st.markdown(
        "<h2 style='text-align:center;'>🌞 🌻 🌤️</h2>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<p style='text-align:center;'>Enter your observation data and let's calculate!</p>",
        unsafe_allow_html=True
    )

st.divider()


# =====================================================
# 6. PERHITUNGAN POSISI MATAHARI
# =====================================================

if st.button("☀️ HITUNG POSISI MATAHARI", type="primary"):

    # Hari dalam satu tahun
    day_of_year = tanggal.timetuple().tm_yday

    jam = waktu.hour + waktu.minute / 60

    # UTC Offset
    if zona_waktu == "WIB (UTC+7)":
        utc_offset = 7
    elif zona_waktu == "WITA (UTC+8)":
        utc_offset = 8
    else:
        utc_offset = 9

    # Fractional Year
    days_in_year = (
        366 if (
            tanggal.year % 4 == 0
            and (
                tanggal.year % 100 != 0
                or tanggal.year % 400 == 0
            )
        )
        else 365
    )

    gamma = (2 * math.pi / days_in_year) * (
        day_of_year - 1 + (jam - 12) / 24
    )

    # Equation of Time
    equation_of_time = 229.18 * (
        0.000075
        + 0.001868 * math.cos(gamma)
        - 0.032077 * math.sin(gamma)
        - 0.014615 * math.cos(2 * gamma)
        - 0.040849 * math.sin(2 * gamma)
    )

    # Deklinasi Matahari
    declination = (
        0.006918
        - 0.399912 * math.cos(gamma)
        + 0.070257 * math.sin(gamma)
        - 0.006758 * math.cos(2 * gamma)
        + 0.000907 * math.sin(2 * gamma)
        - 0.002697 * math.cos(3 * gamma)
        + 0.00148 * math.sin(3 * gamma)
    )

    # True Solar Time
    local_time = (
        waktu.hour * 60
        + waktu.minute
        + waktu.second / 60
    )

    time_correction = (
        equation_of_time
        + 4 * longitude
        - 60 * utc_offset
    )

    true_solar_time = (
        local_time + time_correction
    ) % 1440

    # Hour Angle
    hour_angle = (true_solar_time / 4) - 180

    # Sudut Zenith
    lat_rad = math.radians(latitude)
    dec_rad = declination
    hour_angle_rad = math.radians(hour_angle)

    cos_zenith = (
        math.sin(lat_rad) * math.sin(dec_rad)
        + math.cos(lat_rad)
        * math.cos(dec_rad)
        * math.cos(hour_angle_rad)
    )

    cos_zenith = max(-1, min(1, cos_zenith))

    zenith = math.degrees(math.acos(cos_zenith))

    # Elevasi Matahari
    elevation = 90 - zenith

    # Azimuth Matahari
    azimuth = (
        math.degrees(
            math.atan2(
                math.sin(hour_angle_rad),
                math.cos(hour_angle_rad) * math.sin(lat_rad)
                - math.tan(dec_rad) * math.cos(lat_rad)
            )
        ) + 180
    ) % 360


    # =================================================
    # 7. HASIL PERHITUNGAN
    # =================================================

    st.success("🎉 Perhitungan berhasil diselesaikan!")

    st.subheader("🌞 Hasil Posisi Matahari")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "🧭 Azimuth Matahari",
            f"{azimuth:.2f}°"
        )

    with col2:
        st.metric(
            "📐 Elevasi Matahari",
            f"{elevation:.2f}°"
        )


    # =================================================
    # 8. MENENTUKAN ARAH MATAHARI
    # =================================================

    if azimuth >= 337.5 or azimuth < 22.5:
        arah = "Utara"
    elif azimuth < 67.5:
        arah = "Timur Laut"
    elif azimuth < 112.5:
        arah = "Timur"
    elif azimuth < 157.5:
        arah = "Tenggara"
    elif azimuth < 202.5:
        arah = "Selatan"
    elif azimuth < 247.5:
        arah = "Barat Daya"
    elif azimuth < 292.5:
        arah = "Barat"
    else:
        arah = "Barat Laut"

    st.info(f"🧭 Arah Matahari: **{arah}**")


    # =================================================
    # 9. KONDISI MATAHARI
    # =================================================

    if elevation > 0:
        st.success("🌞 Matahari berada di atas horizon.")
        karakter = "😎 ☀️"
        pesan = "The sun is shining! Have a sunny day!"

    elif elevation == 0:
        st.warning("🌅 Matahari berada tepat pada garis horizon.")
        karakter = "🌅"
        pesan = "The sun is touching the horizon!"

    else:
        st.warning("🌙 Matahari berada di bawah horizon.")
        karakter = "🌙 💤"
        pesan = "The sun is resting below the horizon!"

    with st.container(border=True):
        st.markdown(
            f"<h1 style='text-align:center;'>{karakter}</h1>",
            unsafe_allow_html=True
        )

        st.markdown(
            f"<p style='text-align:center;'>{pesan}</p>",
            unsafe_allow_html=True
        )


    # =================================================
    # 10. DETAIL PERHITUNGAN
    # =================================================

    st.divider()

    st.subheader("📊 Detail Perhitungan")

    with st.container(border=True):
        st.write(f"📅 **Tanggal:** {tanggal}")
        st.write(f"⏰ **Waktu:** {waktu}")
        st.write(f"📍 **Latitude:** {latitude}°")
        st.write(f"🌐 **Longitude:** {longitude}°")
        st.write(f"🕒 **Zona Waktu:** {zona_waktu}")

        st.write(
            f"🌞 **Deklinasi Matahari:** "
            f"{math.degrees(declination):.2f}°"
        )

        st.write(
            f"🧭 **Hour Angle:** {hour_angle:.2f}°"
        )

        st.write(
            f"📐 **Zenith:** {zenith:.2f}°"
        )


# =====================================================
# 11. FOOTER
# =====================================================

st.divider()

st.markdown(
    "<h2 style='text-align:center;'>🌻 ☀️ 🌻</h2>",
    unsafe_allow_html=True
)

st.markdown(
    "<p style='text-align:center;'>"
    "<b>Solar Position Calculator</b><br>"
    "Made with Streamlit | Group 4"
    "</p>",
    unsafe_allow_html=True
)
