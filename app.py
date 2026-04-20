import yfinance as yf
import pandas as pd
import streamlit as st
from ta.momentum import RSIIndicator

st.title("📈 Screener Saham IHSG (Simple)")

saham_list = ["BBCA.JK", "BBRI.JK", "TLKM.JK"]

hasil = []

for saham in saham_list:
    try:
        data = yf.download(saham, period="5d", interval="15m")

        # CEK kalau data kosong
        if data.empty or len(data) < 20:
            continue

        data['MA20'] = data['Close'].rolling(20).mean()

        rsi = RSIIndicator(close=data['Close'], window=14)
        data['RSI'] = rsi.rsi()

        last = data.iloc[-1]
        avg_volume = data['Volume'].mean()

        if (
            last['Close'] > last['MA20'] and
            last['Volume'] > avg_volume * 1.5 and
            50 < last['RSI'] < 70
        ):
            hasil.append({
                "Saham": saham,
                "Harga": round(last['Close'], 2),
                "RSI": round(last['RSI'], 2)
            })

    except Exception as e:
        st.write(f"Error di {saham}: {e}")

df = pd.DataFrame(hasil)

st.subheader("🔥 Kandidat")
st.dataframe(df)
