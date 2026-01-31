import streamlit as st

# Setup Halaman
st.set_page_config(page_title="Kasir Digital UMKM", layout="centered")

# Memori Penyimpanan (Session State)
if 'keranjang' not in st.session_state:
    st.session_state.keranjang = []

st.title("🏪 Sistem Kasir Digital")
st.write("Isi detail barang di bawah ini untuk memulai transaksi.")
st.markdown("---")

# --- BAGIAN INPUT (DI TENGAH) ---
with st.container():
    col_in1, col_in2 = st.columns(2)
    with col_in1:
        nama_barang = st.text_input("Nama Produk", placeholder="Contoh: Kopi")
    with col_in2:
        harga_barang = st.number_input("Harga Satuan (Rp)", min_value=0, step=500)
    
    col_in3, col_in4 = st.columns(2)
    with col_in3:
        qty = st.number_input("Jumlah Beli (Qty)", min_value=1, value=1)
    with col_in4:
        # Diskon ditulis manual (bukan slider)
        diskon_input = st.number_input("Input Diskon (%)", min_value=0, max_value=100, value=0)

    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("➕ TAMBAH BARANG", use_container_width=True, variant="primary"):
            if nama_barang and harga_barang > 0:
                st.session_state.keranjang.append({
                    "Produk": nama_barang,
                    "Harga": harga_barang,
                    "Qty": qty,
                    "Subtotal": harga_barang * qty
                })
                st.toast(f"{nama_barang} berhasil ditambahkan!")
    with col_btn2:
        if st.button("🗑️ RESET TRANSAKSI", use_container_width=True):
            st.session_state.keranjang = []
            st.rerun()

st.markdown("---")

# --- BAGIAN OUTPUT / STRUK ---
if st.session_state.keranjang:
    st.subheader("📄 Struk Belanja Sementara")
    st.table(st.session_state.keranjang)
    
    # Hitung Kalkulasi
    total_kotor = sum(item['Subtotal'] for item in st.session_state.keranjang)
    potongan = total_kotor * (diskon_input / 100)
    total_akhir = total_kotor - potongan
    
    col_res1, col_res2 = st.columns(2)
    with col_res1:
        st.metric("Total Belanja", f"Rp {total_kotor:,.0f}")
        st.metric("Potongan Diskon", f"Rp {potongan:,.0f}")
    with col_res2:
        st.metric("TOTAL BAYAR", f"Rp {total_akhir:,.0f}")
        
    st.markdown("---")
    
    # Bagian Kembalian
    uang_bayar = st.number_input("Uang Yang Dibayar (Rp)", min_value=0)
    if uang_bayar >= total_akhir and total_akhir > 0:
        kembalian = uang_bayar - total_akhir
        st.success(f"### 💰 Kembalian: Rp {kembalian:,.0f}")
    elif uang_bayar < total_akhir and uang_bayar > 0:
        st.error("Uang kurang!")
else:
    st.info("Belum ada data transaksi. Silakan masukkan barang.")
