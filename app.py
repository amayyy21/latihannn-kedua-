import streamlit as st
import pandas as pd
import plotly.express as px

# ================================
#       KONFIGURASI HALAMAN
# ================================
st.set_page_config(
    page_title="May Money App",
    page_icon="💰",
    layout="wide"
)

# ================================
#          STYLE CSS
# ================================
st.markdown("""
    <style>
        .title { 
            font-size: 40px; 
            font-weight: bold; 
            color: #ff4b4b; 
            text-align: center;
        }
        .subtitle {
            font-size: 18px;
            color: #555;
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)

# ================================
#       DATA (SESSION STATE)
# ================================
if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame({
        "Tanggal": [],
        "Kategori": [],
        "Jenis": [],
        "Nominal": []
    })

# ================================
#          SIDEBAR
# ================================
st.sidebar.title("✨ Menu Utama")
menu = st.sidebar.radio("Pilih menu", ["Dashboard", "Input Transaksi", "Catatan Transaksi"])

# ================================
#          DASHBOARD
# ================================
if menu == "Dashboard":
    st.markdown("<div class='title'>📊 May Money Dashboard</div>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>Pantau keuangan pribadimu setiap hari</p>", unsafe_allow_html=True)
    
    if len(st.session_state.data) == 0:
        st.info("Belum ada data transaksi. Silahkan tambah di menu *Input Transaksi*.")
    else:
        df = st.session_state.data
        
        total_pemasukan = df[df["Jenis"] == "Pemasukan"]["Nominal"].sum()
        total_pengeluaran = df[df["Jenis"] == "Pengeluaran"]["Nominal"].sum()
        saldo = total_pemasukan - total_pengeluaran
        
        col1, col2, col3 = st.columns(3)
        col1.metric("💵 Total Pemasukan", f"Rp {total_pemasukan:,.0f}")
        col2.metric("💸 Total Pengeluaran", f"Rp {total_pengeluaran:,.0f}")
        col3.metric("💰 Saldo Akhir", f"Rp {saldo:,.0f}")

        fig = px.line(df, x="Tanggal", y="Nominal", color="Jenis", title="Grafik Keuangan")
        st.plotly_chart(fig, use_container_width=True)

# ================================
#       INPUT TRANSAKSI
# ================================
elif menu == "Input Transaksi":
    st.markdown("<div class='title'>📝 Input Transaksi</div>", unsafe_allow_html=True)
    
    tanggal = st.date_input("Tanggal")
    jenis = st.radio("Jenis", ["Pemasukan", "Pengeluaran"])
    kategori = st.selectbox("Kategori", ["Gaji", "Belanja", "Makanan", "Transport", "Hiburan", "Lainnya"])
    nominal = st.number_input("Nominal (Rp)", min_value=0)
    
    if st.button("Simpan"):
        new_data = pd.DataFrame({
            "Tanggal": [tanggal],
            "Kategori": [kategori],
            "Jenis": [jenis],
            "Nominal": [nominal]
        })
        st.session_state.data = pd.concat([st.session_state.data, new_data], ignore_index=True)
        st.success("Transaksi berhasil ditambahkan!")

# ================================
#      CATATAN TRANSAKSI
# ================================
elif menu == "Catatan Transaksi":
    st.markdown("<div class='title'>📂 Catatan Transaksi</div>", unsafe_allow_html=True)

    if len(st.session_state.data) == 0:
        st.info("Belum ada data transaksi.")
    else:
        st.dataframe(st.session_state.data, use_container_width=True)
