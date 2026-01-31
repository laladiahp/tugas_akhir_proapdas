import streamlit as st

# Setup Halaman
st.set_page_config(page_title="Kasir Cloud UMKM", layout="wide")

# Memori Penyimpanan (Session State)
if 'keranjang' not in st.session_state:
    st.session_state.keranjang = []

st.title("🏪 Sistem Kasir Sederhana")
st.markdown("---")

# Layouting: Sidebar untuk Input
with st.sidebar:
    st.header("🛒 Input Transaksi")
    nama_barang = st.text_input("Nama Produk")
    harga_barang = st.number_input("Harga (Rp)", min_value=0, step=500)
    qty = st.number_input("Jumlah Beli", min_value=1, value=1)
    
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("Tambah ➕"):
            if nama_barang and harga_barang > 0:
                st.session_state.keranjang.append({
                    "Produk": nama_barang,
                    "Harga": harga_barang,
                    "Qty": qty,
                    "Subtotal": harga_barang * qty
                })
                st.success("Ditambah!")
    with col_btn2:
        if st.button("Reset Transaksi 🗑️"):
            st.session_state.keranjang = []
            st.rerun()

# Layouting: Halaman Utama
c1, c2 = st.columns([2, 1])

with c1:
    st.subheader("📄 Daftar Belanja (Struk)")
    if st.session_state.keranjang:
        st.table(st.session_state.keranjang)
        total_kotor = sum(item['Subtotal'] for item in st.session_state.keranjang)
        st.write(f"**Total Item:** {len(st.session_state.keranjang)}")
    else:
        st.info("Belum ada transaksi.")

with c2:
    st.subheader("💳 Pembayaran")
    if st.session_state.keranjang:
        total_kotor = sum(item['Subtotal'] for item in st.session_state.keranjang)
        diskon = st.slider("Diskon (%)", 0, 100, 0)
        
        # Rumus Aritmatika
        potongan = total_kotor * (diskon / 100)
        total_akhir = total_kotor - potongan
        
        st.metric("Total Bayar", f"Rp {total_akhir:,.0f}")
        
        bayar = st.number_input("Uang Yang Dibayar (Rp)", min_value=0)
        if bayar >= total_akhir:
            st.success(f"Kembalian: Rp {bayar - total_akhir:,.0f}")
        else:
            st.error("Uang tidak cukup")
