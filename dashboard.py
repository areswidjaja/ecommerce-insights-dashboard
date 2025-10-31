# ==========================================================
# STREAMLIT DASHBOARD FOR E-COMMERCE INSIGHTS
# ==========================================================
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import warnings
warnings.filterwarnings("ignore")


# ==========================================================
#  SETUP & THEME CONFIGURATION
# ==========================================================
st.set_page_config(
    page_title="E-Commerce Insights Dashboard",
    page_icon="🛍️",
    layout="wide"
)

# ---------- LOAD DATA ----------
@st.cache_data
def load_data():
    sales_by_category = pd.read_csv("sales_by_category.csv")
    seller_summary = pd.read_csv("seller_summary.csv")
    payment_summary = pd.read_csv("payment_summary.csv")
    installment_summary = pd.read_csv("installment_summary.csv")
    review_summary = pd.read_csv("review_summary.csv")
    monthly_sales = pd.read_csv("monthly_sales.csv")
    monthly_sales['order_month'] = pd.to_datetime(monthly_sales['order_month'])
    return sales_by_category, seller_summary, payment_summary, installment_summary, review_summary, monthly_sales

sales_by_category, seller_summary, payment_summary, installment_summary, review_summary, monthly_sales = load_data()

# ==========================================================
#  CUSTOM STYLE
# ==========================================================
st.markdown("""
<style>
/* --- GLOBAL --- */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #F8FAFC, #E8F0F8);
}
h1, h2, h3 {
    color: #0F172A;
    font-weight: 700;
}
hr {
    border: none;
    height: 1px;
    background-color: #E2E8F0;
    margin: 1.5rem 0;
}
div[data-testid="stMetricValue"] {
    color: #1E3A8A;
    font-weight: bold;
    font-size: 1.3rem;
}
div[data-testid="stMetricLabel"] {
    color: #64748B;
    font-size: 14px;
}
/* --- HEADER --- */
#main-header {
    text-align: center;
    background: linear-gradient(90deg, #1E3A8A, #2563EB);
    color: white;
    padding: 1.2rem;
    border-radius: 12px;
    margin-bottom: 2rem;
    box-shadow: 0 3px 8px rgba(0,0,0,0.1);
}
#main-header h1 {
    font-size: 1.8rem;
    margin: 0;
    color: #FFF;
    letter-spacing: 0.5px;
}
/* --- DARK MODE SUPPORT --- */
[data-theme="dark"] #main-header {
    background: linear-gradient(90deg, #334155, #1E293B);
}
</style>
""", unsafe_allow_html=True)

# ==========================================================
#  HEADER
# ==========================================================
st.markdown('<div id="main-header"><h1>🛒 E-Commerce Insights Dashboard</h1></div>', unsafe_allow_html=True)

# ==========================================================
#  SIDEBAR
# ==========================================================
st.sidebar.header("⚙️ Navigation Panel")
menu = st.sidebar.radio(
    "Pilih Analisis:",
    [
        "1️⃣ Penjualan per Kategori Produk",
        "2️⃣ Kinerja Penjual",
        "3️⃣ Metode Pembayaran",
        "4️⃣ Kepuasan Pelanggan",
        "5️⃣ Tren Penjualan Bulanan"
    ]
)
st.sidebar.markdown("---")
theme = st.sidebar.selectbox("🎨 Pilih Tema Tampilan", ["Light Mode", "Dark Mode"])
if theme == "Dark Mode":
    plt.style.use("dark_background")
    sns.set_theme(style="darkgrid")
else:
    sns.set_theme(style="whitegrid")

# ==========================================================
#  HELPER FUNCTION
# ==========================================================
def divider():
    st.markdown("<hr/>", unsafe_allow_html=True)

def fmt(x):
    return f"{x:,.0f}".replace(",", ".")

# ==========================================================
#  1️⃣ PENJUALAN PER KATEGORI PRODUK
# ==========================================================
if menu == "1️⃣ Penjualan per Kategori Produk":
    st.subheader("📦 Analisis Penjualan per Kategori Produk")

    n_top = st.slider("Tampilkan Top-N Kategori", 5, 15, 10)
    col1, col2 = st.columns(2)
    col1.metric("💰 Total Revenue (BRL)", fmt(sales_by_category['total_revenue'].sum()))
    col2.metric("🛍️ Total Transactions", fmt(sales_by_category['total_transactions'].sum()))
    divider()

    col3, col4 = st.columns(2)
    with col3:
        st.caption("Top kategori dengan total revenue tertinggi:")
        fig, ax = plt.subplots(figsize=(8, 5))
        top_rev = sales_by_category.nlargest(n_top, 'total_revenue')
        sns.barplot(data=top_rev, y="product_category_name_english", x="total_revenue", palette="Blues_r", ax=ax)
        ax.set_xlabel("Total Revenue (BRL)")
        ax.set_ylabel("")
        sns.despine()
        st.pyplot(fig)

    with col4:
        st.caption("Top kategori dengan jumlah transaksi terbanyak:")
        fig, ax = plt.subplots(figsize=(8, 5))
        top_trans = sales_by_category.nlargest(n_top, 'total_transactions')
        sns.barplot(data=top_trans, y="product_category_name_english", x="total_transactions", palette="Greens_r", ax=ax)
        ax.set_xlabel("Total Transactions")
        ax.set_ylabel("")
        sns.despine()
        st.pyplot(fig)

    st.success("""
    💡 **Insight:**  
    Kategori **health_beauty**, **watches_gifts**, dan **bed_bath_table** menjadi pendorong utama pendapatan.  
    Kombinasi produk **premium bernilai tinggi** dan **barang kebutuhan rutin** menjaga stabilitas bisnis.
    """)

# ==========================================================
#  2️⃣ KINERJA PENJUAL
# ==========================================================
elif menu == "2️⃣ Kinerja Penjual":
    st.subheader("👨‍💼 Analisis Kinerja Penjual")

    top_n = st.slider("Tampilkan Top-N Seller", 5, 20, 10)
    col1, col2, col3 = st.columns(3)
    col1.metric("💰 Rata-rata Revenue/Seller", fmt(seller_summary['total_revenue'].mean()))
    col2.metric("📦 Total Orders", fmt(seller_summary['total_orders'].sum()))
    col3.metric("⭐ Avg Review Score", f"{seller_summary['avg_review_score'].mean():.2f}")
    divider()

    col4, col5 = st.columns(2)
    with col4:
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.barplot(data=seller_summary.nlargest(top_n, "total_revenue"),
                    y="seller_id", x="total_revenue", palette="Blues_r", ax=ax)
        ax.set_title("Top Seller Berdasarkan Revenue", fontsize=13)
        sns.despine()
        st.pyplot(fig)
    with col5:
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.barplot(data=seller_summary.nlargest(top_n, "total_orders"),
                    y="seller_id", x="total_orders", palette="Greens_r", ax=ax)
        ax.set_title("Top Seller Berdasarkan Jumlah Pesanan", fontsize=13)
        sns.despine()
        st.pyplot(fig)

    divider()
    st.caption("Hubungan antara frekuensi penjualan dan rata-rata skor ulasan:")
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.scatterplot(data=seller_summary, x="total_orders", y="avg_review_score", alpha=0.7, color="#2E8B57")
    sns.regplot(data=seller_summary, x="total_orders", y="avg_review_score", scatter=False, color="#F59E0B")
    sns.despine()
    st.pyplot(fig)
    st.info("Korelasi ≈ -0.03 → tidak signifikan. Kualitas layanan tetap stabil di berbagai skala penjualan.")

# ==========================================================
#  3️⃣ METODE PEMBAYARAN
# ==========================================================
elif menu == "3️⃣ Metode Pembayaran":
    st.subheader("💳 Analisis Metode Pembayaran dan Jumlah Cicilan")

    col1, col2 = st.columns(2)
    col1.metric("💰 Total Payment Value", fmt(payment_summary['total_payment_value'].sum()))
    col2.metric("💳 Dominant Payment Type", payment_summary.loc[payment_summary['total_payment_value'].idxmax(), 'payment_type'])
    divider()

    col3, col4 = st.columns(2)
    with col3:
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.barplot(data=payment_summary.sort_values(by="total_payment_value", ascending=False),
                    y="payment_type", x="total_payment_value", palette="Blues_r", ax=ax)
        ax.set_title("Total Transaction Value by Payment Method", fontsize=13)
        sns.despine()
        st.pyplot(fig)

    with col4:
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.barplot(data=installment_summary.sort_values(by="total_orders", ascending=False).head(10),
                    y="payment_installments", x="total_orders", palette="Greens_r", ax=ax)
        ax.set_title("Most Used Installment Counts", fontsize=13)
        sns.despine()
        st.pyplot(fig)

    st.success("Mayoritas pelanggan menggunakan **credit_card (±9,45 juta BRL)** dengan **pembayaran 1x**. Ini menunjukkan perilaku konsumen yang mengutamakan efisiensi dan kenyamanan.")

# ==========================================================
#  4️⃣ KEPUASAN PELANGGAN
# ==========================================================
elif menu == "4️⃣ Kepuasan Pelanggan":
    st.subheader("⭐ Analisis Kepuasan Pelanggan per Kategori Produk")

    col1, col2 = st.columns(2)
    col1.metric("⭐ Avg Review Score", f"{review_summary['avg_review_score'].mean():.2f}")
    col2.metric("💬 Total Reviews", fmt(review_summary['total_reviews'].sum()))
    divider()

    top_n = st.slider("Tampilkan Top-N Kategori", 5, 15, 10)
    col3, col4 = st.columns(2)
    with col3:
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.barplot(data=review_summary.nlargest(top_n, "avg_review_score"),
                    y="product_category_name_english", x="avg_review_score", palette="Blues_r", ax=ax)
        ax.set_title("Top Categories by Review Score", fontsize=13)
        sns.despine()
        st.pyplot(fig)
    with col4:
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.barplot(data=review_summary.nsmallest(top_n, "avg_review_score"),
                    y="product_category_name_english", x="avg_review_score", palette="Reds_r", ax=ax)
        ax.set_title("Bottom Categories by Review Score", fontsize=13)
        sns.despine()
        st.pyplot(fig)

    st.info("Rata-rata skor ulasan pelanggan mencapai **4,04 dari 5**. Produk buku dan anak-anak mendapat ulasan tertinggi, sedangkan furniture & elektronik memerlukan peningkatan layanan.")

# ==========================================================
#  5️⃣ TREN PENJUALAN BULANAN
# ==========================================================
elif menu == "5️⃣ Tren Penjualan Bulanan":
    st.subheader("📈 Analisis Tren Penjualan Bulanan")

    months = st.slider("Tampilkan N Bulan Terakhir", 6, 18, 18)
    df_monthly = monthly_sales.tail(months)
    divider()

    col1, col2 = st.columns(2)
    col1.metric("📦 Total Orders", fmt(df_monthly['total_orders'].sum()))
    col2.metric("💰 Total Revenue", fmt(df_monthly['total_revenue'].sum()))
    divider()

    fig, ax1 = plt.subplots(figsize=(12, 6))
    sns.lineplot(data=df_monthly, x='order_month', y='total_revenue',
                 color='#2563EB', marker='o', linewidth=2.5, label='Revenue', ax=ax1)
    ax1.set_ylabel("Total Revenue (BRL)", color='#2563EB')
    ax2 = ax1.twinx()
    sns.lineplot(data=df_monthly, x='order_month', y='total_orders',
                 color='#16A34A', marker='o', linewidth=2.5, label='Orders', ax=ax2)
    ax2.set_ylabel("Total Orders", color='#16A34A')
    plt.xticks(rotation=45, ha='right')
    sns.despine()
    st.pyplot(fig)


    st.success("Puncak penjualan terjadi pada November 2017 (Black Friday). Setelahnya, performa stabil dan terus tumbuh, menandakan fondasi bisnis yang kuat.")
