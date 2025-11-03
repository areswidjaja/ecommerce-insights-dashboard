# ==========================================================
# STREAMLIT DASHBOARD - ECOMMERCE INSIGHTS DASHBOARD
# ==========================================================
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")

# ==========================================================
# PAGE CONFIG
# ==========================================================
st.set_page_config(
    page_title="E-Commerce Analytics Dashboard",
    page_icon="🛍️",
    layout="wide"
)

# ==========================================================
# LOAD DATA
# ==========================================================
@st.cache_data
def load_data():
    sales_by_category = pd.read_csv("sales_by_category.csv")
    seller_summary = pd.read_csv("seller_summary.csv")
    payment_summary = pd.read_csv("payment_summary.csv")
    installment_summary = pd.read_csv("installment_summary.csv")
    review_summary = pd.read_csv("review_summary.csv")
    monthly_sales = pd.read_csv("monthly_sales.csv")
    monthly_sales["order_month"] = pd.to_datetime(monthly_sales["order_month"])
    return sales_by_category, seller_summary, payment_summary, installment_summary, review_summary, monthly_sales

sales_by_category, seller_summary, payment_summary, installment_summary, review_summary, monthly_sales = load_data()

# Pastikan tipe data numerik
sales_by_category["total_revenue"] = pd.to_numeric(sales_by_category["total_revenue"], errors="coerce")
sales_by_category["total_transactions"] = pd.to_numeric(sales_by_category["total_transactions"], errors="coerce")

# ==========================================================
# STYLE CONFIGURATION
# ==========================================================
st.markdown("""
<style>
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}
#MainMenu, footer, header {visibility: hidden;}
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #F9FAFB, #EEF2F7);
}
h1, h2, h3 {
    color: #0F172A;
    font-weight: 700;
}
div[data-testid="stMetricValue"] {
    color: #1E3A8A;
    font-weight: bold;
    font-size: 1.4rem;
}
div[data-testid="stMetricLabel"] {
    color: #475569;
    font-size: 14px;
}
hr {
    border: none;
    height: 1px;
    background-color: #E2E8F0;
    margin: 1.5rem 0;
}
#main-header {
    text-align: center;
    background: linear-gradient(90deg, #1E3A8A, #2563EB);
    color: white;
    padding: 1.2rem;
    border-radius: 12px;
    margin-bottom: 2rem;
    box-shadow: 0 3px 8px rgba(0,0,0,0.1);
}
/* Judul expander jadi bold dan ada efek hover */
details > summary {
    font-weight: 700 !important;
    font-size: 1.05rem !important;
    color: #0F172A !important;
}
details > summary:hover {
    color: #2563EB !important;
    cursor: pointer;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div id="main-header"><h1>🛒 E-Commerce Insights Dashboard</h1></div>', unsafe_allow_html=True)

# ==========================================================
# SIDEBAR FILTERS
# ==========================================================
st.sidebar.header("⚙️ Filter Global")

# Rentang waktu otomatis dibatasi berdasarkan dataset
min_date, max_date = monthly_sales["order_month"].min(), monthly_sales["order_month"].max()

st.sidebar.subheader("🗓️ Rentang Waktu Analisis")
date_range = st.sidebar.date_input(
    "Pilih Rentang Waktu",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
    help="Data hanya dapat dipilih dalam rentang waktu yang tersedia di dataset."
)
filtered_monthly = monthly_sales.query("@date_range[0] <= order_month <= @date_range[1]")

# ==========================================================
# FILTER KATEGORI PRODUK (DENGAN PILIH SEMUA)
# ==========================================================
st.sidebar.subheader("📦 Filter Kategori Produk")
categories = sorted(sales_by_category["product_category_name_english"].unique())
select_all_categories = st.sidebar.checkbox("Pilih Semua Kategori", value=False)

if select_all_categories:
    selected_categories = st.sidebar.multiselect("Pilih Kategori Produk", options=categories, default=categories)
else:
    selected_categories = st.sidebar.multiselect("Pilih Kategori Produk", options=categories, default=categories[:5])

filtered_sales = (
    sales_by_category[sales_by_category["product_category_name_english"].isin(selected_categories)]
    if selected_categories else pd.DataFrame()
)

# ==========================================================
# FILTER METODE PEMBAYARAN (DENGAN PILIH SEMUA)
# ==========================================================
st.sidebar.subheader("💳 Filter Metode Pembayaran")
methods = sorted(payment_summary["payment_type"].unique())
select_all_methods = st.sidebar.checkbox("Pilih Semua Metode Pembayaran", value=False)

if select_all_methods:
    selected_methods = st.sidebar.multiselect("Pilih Metode Pembayaran", options=methods, default=methods)
else:
    selected_methods = st.sidebar.multiselect("Pilih Metode Pembayaran", options=methods, default=methods[:2])

filtered_payment = (
    payment_summary[payment_summary["payment_type"].isin(selected_methods)]
    if selected_methods else pd.DataFrame()
)

# ==========================================================
# HELPER FUNCTIONS
# ==========================================================
def fmt(x): 
    try:
        return f"{x:,.0f}".replace(",", ".")
    except:
        return "-"

def divider(): 
    st.markdown("<hr/>", unsafe_allow_html=True)

sns.set_theme(style="whitegrid", palette="pastel")

# ==========================================================
# SUMMARY HEADER (EXECUTIVE OVERVIEW)
# ==========================================================
st.subheader("📊 Ringkasan Kinerja Utama")

total_revenue = filtered_sales["total_revenue"].sum() if not filtered_sales.empty else sales_by_category["total_revenue"].sum()
total_orders = filtered_monthly["total_orders"].sum() if not filtered_monthly.empty else monthly_sales["total_orders"].sum()
avg_review = review_summary["avg_review_score"].mean() if not review_summary.empty else "-"
top_category = filtered_sales.nlargest(1, "total_revenue")["product_category_name_english"].iloc[0] if not filtered_sales.empty else "Tidak Ada Data"

col1, col2, col3, col4 = st.columns(4)
col1.metric("💰 Total Revenue (BRL)", fmt(total_revenue))
col2.metric("📦 Total Orders", fmt(total_orders))
col3.metric("⭐ Avg Review Score", f"{avg_review:.2f}" if avg_review != "-" else "-")
col4.metric("🏆 Top Category", top_category)

divider()

# ==========================================================
# SECTION 1 - PENJUALAN PER KATEGORI PRODUK
# ==========================================================
with st.expander("📦 Penjualan per Kategori Produk", expanded=True):
    if filtered_sales.empty:
        st.info("Tidak ada data untuk kategori yang dipilih.")
    else:
        n_top = st.slider("Tampilkan Top-N Kategori", 5, 15, 10, key="cat_slider")
        col1, col2 = st.columns(2)
        col1.metric("💰 Total Revenue (BRL)", fmt(filtered_sales["total_revenue"].sum()))
        col2.metric("🛍️ Total Transactions", fmt(filtered_sales["total_transactions"].sum()))

        top_rev = filtered_sales.nlargest(n_top, "total_revenue")
        top_trans = filtered_sales.nlargest(n_top, "total_transactions")

        if top_rev.empty or top_trans.empty:
            st.warning("⚠️ Tidak ada data valid untuk kategori yang dipilih.")
        else:
            col3, col4 = st.columns(2)
            with col3:
                fig, ax = plt.subplots(figsize=(8, 5))
                sns.barplot(data=top_rev, y="product_category_name_english", x="total_revenue", palette="Blues_r", ax=ax)
                ax.set_title("Top Kategori Berdasarkan Revenue", fontsize=12, weight='bold')
                ax.set_xlabel("Total Revenue (BRL)")
                ax.set_ylabel("")
                st.pyplot(fig)
            with col4:
                fig, ax = plt.subplots(figsize=(8, 5))
                sns.barplot(data=top_trans, y="product_category_name_english", x="total_transactions", palette="Greens_r", ax=ax)
                ax.set_title("Top Kategori Berdasarkan Jumlah Transaksi", fontsize=12, weight='bold')
                ax.set_xlabel("Total Transactions")
                ax.set_ylabel("")
                st.pyplot(fig)
            st.success(f"Kategori dengan revenue tertinggi: **{top_rev.iloc[0]['product_category_name_english']}**.")

divider()

# ==========================================================
# SECTION 2 - KINERJA PENJUAL
# ==========================================================
with st.expander("👨‍💼 Analisis Kinerja Penjual", expanded=False):
    if seller_summary.empty:
        st.info("Data penjual tidak tersedia.")
    else:
        top_n = st.slider("Top-N Seller", 5, 20, 10, key="seller_slider")
        col1, col2, col3 = st.columns(3)
        col1.metric("💰 Avg Revenue/Seller", fmt(seller_summary["total_revenue"].mean()))
        col2.metric("📦 Total Orders", fmt(seller_summary["total_orders"].sum()))
        col3.metric("⭐ Avg Review Score", f"{seller_summary['avg_review_score'].mean():.2f}")

        col4, col5 = st.columns(2)
        with col4:
            fig, ax = plt.subplots(figsize=(8, 5))
            sns.barplot(data=seller_summary.nlargest(top_n, "total_revenue"), y="seller_id", x="total_revenue", palette="Blues_r", ax=ax)
            ax.set_title("Top Seller Berdasarkan Revenue", fontsize=12, weight='bold')
            st.pyplot(fig)
        with col5:
            fig, ax = plt.subplots(figsize=(8, 5))
            sns.barplot(data=seller_summary.nlargest(top_n, "total_orders"), y="seller_id", x="total_orders", palette="Greens_r", ax=ax)
            ax.set_title("Top Seller Berdasarkan Jumlah Order", fontsize=12, weight='bold')
            st.pyplot(fig)

        fig, ax = plt.subplots(figsize=(10, 5))
        sns.scatterplot(data=seller_summary, x="total_orders", y="avg_review_score", alpha=0.7, color="#2563EB", s=60)
        sns.regplot(data=seller_summary, x="total_orders", y="avg_review_score", scatter=False, color="#F59E0B")
        ax.set_title("Hubungan antara Jumlah Order dan Skor Review", fontsize=12, weight='bold')
        st.pyplot(fig)
        st.info("Kualitas layanan relatif stabil di berbagai tingkat volume penjualan.")

divider()

# ==========================================================
# SECTION 3 - METODE PEMBAYARAN
# ==========================================================
with st.expander("💳 Analisis Metode Pembayaran", expanded=False):
    if filtered_payment.empty:
        st.info("Tidak ada data untuk metode pembayaran yang dipilih.")
    else:
        col1, col2 = st.columns(2)
        col1.metric("💰 Total Payment Value", fmt(filtered_payment["total_payment_value"].sum()))
        col2.metric("💳 Metode Dominan", filtered_payment.loc[filtered_payment["total_payment_value"].idxmax(), "payment_type"])

        col3, col4 = st.columns(2)
        with col3:
            fig, ax = plt.subplots(figsize=(8, 5))
            sns.barplot(data=filtered_payment.sort_values(by="total_payment_value", ascending=False),
                        y="payment_type", x="total_payment_value", palette="Blues_r", ax=ax)
            ax.set_title("Nilai Pembayaran per Metode", fontsize=12, weight='bold')
            st.pyplot(fig)
        with col4:
            fig, ax = plt.subplots(figsize=(8, 5))
            sns.barplot(data=installment_summary.sort_values(by="total_orders", ascending=False).head(10),
                        y="payment_installments", x="total_orders", palette="Greens_r", ax=ax)
            ax.set_title("Distribusi Jumlah Order Berdasarkan Cicilan", fontsize=12, weight='bold')
            st.pyplot(fig)

divider()

# ==========================================================
# SECTION 4 - KEPUASAN PELANGGAN
# ==========================================================
with st.expander("⭐ Kepuasan Pelanggan per Kategori Produk", expanded=False):
    if review_summary.empty:
        st.info("Data ulasan pelanggan tidak tersedia.")
    else:
        top_n_rev = st.slider("Top-N Kategori", 5, 15, 10, key="review_slider")
        col1, col2 = st.columns(2)
        col1.metric("⭐ Avg Review Score", f"{review_summary['avg_review_score'].mean():.2f}")
        col2.metric("💬 Total Reviews", fmt(review_summary["total_reviews"].sum()))

        col3, col4 = st.columns(2)
        with col3:
            fig, ax = plt.subplots(figsize=(8, 5))
            sns.barplot(data=review_summary.nlargest(top_n_rev, "avg_review_score"),
                        y="product_category_name_english", x="avg_review_score", palette="Blues_r", ax=ax)
            ax.set_title("Kategori dengan Skor Review Tertinggi", fontsize=12, weight='bold')
            st.pyplot(fig)
        with col4:
            fig, ax = plt.subplots(figsize=(8, 5))
            sns.barplot(data=review_summary.nsmallest(top_n_rev, "avg_review_score"),
                        y="product_category_name_english", x="avg_review_score", palette="Reds_r", ax=ax)
            ax.set_title("Kategori dengan Skor Review Terendah", fontsize=12, weight='bold')
            st.pyplot(fig)
        st.info("Produk anak-anak dan buku memiliki skor ulasan tertinggi.")

divider()

# ==========================================================
# SECTION 5 - TREN PENJUALAN BULANAN
# ==========================================================
with st.expander("📈 Tren Penjualan Bulanan", expanded=False):
    if filtered_monthly.empty:
        st.info("Tidak ada data penjualan untuk rentang waktu yang dipilih.")
    else:
        months = st.slider("Tampilkan N Bulan Terakhir", 6, 18, 12, key="trend_slider")
        df_monthly = filtered_monthly.tail(months)
        col1, col2 = st.columns(2)
        col1.metric("📦 Total Orders", fmt(df_monthly["total_orders"].sum()))
        col2.metric("💰 Total Revenue", fmt(df_monthly["total_revenue"].sum()))

        fig, ax1 = plt.subplots(figsize=(12, 6))
        sns.lineplot(data=df_monthly, x="order_month", y="total_revenue", color="#2563EB", marker="o", linewidth=2.5, ax=ax1, label="Revenue")
        ax2 = ax1.twinx()
        sns.lineplot(data=df_monthly, x="order_month", y="total_orders", color="#16A34A", marker="o", linewidth=2.5, ax=ax2, label="Orders")
        ax1.set_title("Tren Penjualan Bulanan: Revenue vs Jumlah Order", fontsize=12, weight='bold')
        plt.xticks(rotation=45)
        fig.tight_layout()
        st.pyplot(fig)
        st.success("Puncak penjualan terjadi pada Black Friday 2017 dengan tren stabil setelahnya.")
