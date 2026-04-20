import yfinance as yf
import pandas as pd
import streamlit as st
from ta.momentum import RSIIndicator

st.title("📈 Screener Saham IHSG (Stable Version)")

saham_list = ["BBCA.JK", "BBRI.JK", "TLKM.JK"]

hasil = []

for saham in saham_list:
    try:
        data = yf.download(saham, period="5d", interval="15m")

        if data.empty or len(data) < 20:
            continue

        # RESET INDEX biar aman
        data = data.reset_index()

        # MA20
        data['MA20'] = data['Close'].rolling(20).mean()

        # FIX CLOSE
        close = data['Close']
        if isinstance(close, pd.DataFrame):
            close = close.squeeze()

        # HITUNG RSI
        rsi = RSIIndicator(close=close, window=14).rsi()

        # PAKSA SEJAJAR
        data['RSI'] = rsi.values

        last = data.iloc[-1]
        avg_volume = data['Volume'].mean()

        if (
            last['Close'] > last['MA20'] and
            last['Volume'] > avg_volume * 1.5 and
            50 < last['RSI'] < 70
        ):
            hasil.append({
                "Saham": saham,
                "Harga": round(float(last['Close']), 2),
                "RSI": round(float(last['RSI']), 2)
            })

    except Exception as e:
        st.write(f"Error di {saham}: {e}")

df = pd.DataFrame(hasil)

st.subheader("🔥 Kandidat Potensi Naik")
st.dataframe(df)
