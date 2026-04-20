import yfinance as yf
import pandas as pd
import streamlit as st
from ta.momentum import RSIIndicator

st.title("📈 Screener Saham IHSG (Fix Total)")

saham_list = ["BBCA.JK", "BBRI.JK", "TLKM.JK"]

hasil = []

for saham in saham_list:
    try:
        data = yf.download(saham, period="5d", interval="15m", auto_adjust=True)

        if data.empty or len(data) < 20:
            continue

        # Flatten kolom kalau multi-index
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.get_level_values(0)

        # Pastikan numeric
        data = data.astype(float)

        # MA20
        data['MA20'] = data['Close'].rolling(20).mean()

        # RSI
        close = data['Close']
        rsi = RSIIndicator(close=close, window=14).rsi()
        data['RSI'] = rsi

        # Ambil nilai terakhir (PAKSA FLOAT)
        last_close = float(data['Close'].iloc[-1])
        last_ma20 = float(data['MA20'].iloc[-1])
        last_rsi = float(data['RSI'].iloc[-1])
        last_volume = float(data['Volume'].iloc[-1])
        avg_volume = float(data['Volume'].mean())

        # LOGIKA
        if (
            last_close > last_ma20 and
            last_volume > avg_volume * 1.5 and
            50 < last_rsi < 70
        ):
            hasil.append({
                "Saham": saham,
                "Harga": round(last_close, 2),
                "RSI": round(last_rsi, 2)
            })

    except Exception as e:
        st.write(f"Error di {saham}: {e}")

df = pd.DataFrame(hasil)

st.subheader("🔥 Kandidat Potensi Naik")
st.dataframe(df)
