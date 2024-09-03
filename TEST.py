import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from datetime import datetime, timedelta
from matplotlib.patches import FancyBboxPatch

# Título de la aplicación
st.title("Análisis de Retornos YTD de CEDEARs")

# Lista de tickers de CEDEARs
tickers = ["CVH.BA", "EDLH.BA", "EDSH.BA", "INAG.BA", "VALO.BA", "SAMI.BA", "REGE.BA",
           "SUPV.BA", "MORI.BA", "LOMA.BA", "SEMI.BA", "CGPA2.BA", "HAVA.BA", "MOLI.BA",
           "PAMP.BA", "FIPL.BA", "MOLA.BA", "CTIO.BA", "CEPU.BA", "LONG.BA", "AGRO.BA",
           "TECO2.BA", "COME.BA", "METR.BA", "MIRG.BA", "CRES.BA", "BBAR.BA", "GGAL.BA",
           "BMA.BA", "CECO2.BA", "BHIP.BA", "TGNO4.BA", "CAPX.BA", "BPAT.BA", "YPFD.BA",
           "TGSU2.BA", "AUSO.BA", "INVJ.BA", "TRAN.BA", "FERR.BA", "BYMA.BA", "DGCE.BA",
           "ALUA.BA", "HARG.BA", "LEDE.BA", "CELU.BA", "BOLT.BA", "TXAR.BA", "IRSA.BA",
           "HSAT.BA", "GCDI.BA", "DGCU2.BA", "DYCA.BA", "ROSE.BA", "POLL.BA", "GARO.BA",
           "CARC.BA", "GCLA.BA", "RIGO.BA", "CADO.BA", "GBAN.BA", "DOME.BA", "PATA.BA",
           "EDN.BA", "RICH.BA", "OEST.BA", "GRIM.BA", "INTR.BA"]

# Obtener el último día hábil del año previo
def get_last_business_day_of_last_year():
    today = datetime.now()
    last_year = today.year - 1
    last_day_of_last_year = datetime(last_year, 12, 29)

    # Ajustar si el último día del año es fin de semana
    while last_day_of_last_year.weekday() >= 5:  # 5: Saturday, 6: Sunday
        last_day_of_last_year -= timedelta(days=1)

    return last_day_of_last_year

# Calcular el rendimiento desde el último día hábil del año previo
def calculate_year_to_date_returns(tickers):
    start_date = get_last_business_day_of_last_year()
    end_date = datetime.now()
    returns = {}

    for ticker in tickers:
        try:
            data = yf.download(ticker, start=start_date, end=end_date)
            if not data.empty:
                initial_price = data.iloc[0]['Adj Close']
                latest_price = data.iloc[-1]['Adj Close']
                ytd_return = (latest_price - initial_price) / initial_price * 100
                returns[ticker] = ytd_return
        except Exception as e:
            st.error(f"Error con {ticker}: {e}")

    return returns

# Calcular rendimientos
ytd_returns = calculate_year_to_date_returns(tickers)

# Convertir los resultados a un DataFrame y seleccionar las 10 empresas con mayores variaciones positivas
df_returns = pd.DataFrame(list(ytd_returns.items()), columns=['Ticker', 'YTD Return'])
top_10_positive_returns = df_returns[df_returns['YTD Return'] > -30].nlargest(10, 'YTD Return')

# Eliminar la extensión ".BA" de los tickers
tickers = top_10_positive_returns['Ticker'].str.replace('.BA', '')

# Crear el gráfico
plt.style.use('dark_background')
fig, ax = plt.subplots(figsize=(12, 8))

# Ajuste del ancho de las barras y espacio entre ellas
bar_width = 0.4  # más estrecho
bars = ax.bar(tickers, top_10_positive_returns['YTD Return'], width=bar_width, color=['#FF5733', '#33FF57', '#5733FF', '#FF33A1', '#33FFF0', '#FF8C00', '#8CFF00', '#00FF8C', '#8C00FF', '#FF00C4'])

# Crear borde redondeado en las barras
for bar in bars:
    x, y = bar.get_xy()
    width = bar.get_width()
    height = bar.get_height()
    bbox = FancyBboxPatch((x, y), width, height, boxstyle="round,pad=0.05", edgecolor='none', facecolor=bar.get_facecolor())
    ax.add_patch(bbox)
    bar.set_alpha(0)  # Hacer invisible la barra original

# Agregar la línea horizontal para la inflación acumulada
inflation_value = 91
ax.axhline(y=inflation_value, color='white', linestyle='--', linewidth=1.5)
ax.text(x=len(top_10_positive_returns) - 1, y=inflation_value, s='Inflación acumulada 2024', color='white', ha='right', va='bottom')

# Establecer límites y etiquetas
ax.set_ylabel('Retorno (%)')
ax.set_title('Retornos YTD')

# Quitar líneas verticales de la grilla
ax.grid(True, axis='y', linestyle='--', alpha=0.5)  # Solo grilla horizontal

# Etiquetas del eje X en vertical
plt.xticks(rotation=90)
plt.tight_layout()

# Mostrar el gráfico en Streamlit
st.pyplot(fig)

