import streamlit as st
import pandas as pd
import numpy as np

# Konfiguracja strony
st.set_page_config(page_title="System Analityki Magazynowej", page_icon="📦", layout="wide")

st.title("📦 Inteligentny System Analityczny w Logistyce")
st.markdown("Świadome opracowanie projektu: aplikacja analityczna z możliwością wpisania własnych danych.")

# --- PANEL BOCZNY: WPROWADZANIE DANYCH PRZEZ UŻYTKOWNIKA ---
st.sidebar.header("📝 Wprowadź własne dane do analizy")
st.sidebar.markdown("Dostosuj parametry symulacji procesów magazynowych:")

# Pola do wpisywania danych przez użytkownika
imie_pracownika = st.sidebar.text_input("Imię pracownika:", value="Jan Kowalski")
czas_pakowania = st.sidebar.number_input("Czas pakowania (w minutach):", min_value=1, max_value=120, value=18)
liczba_bledow = st.sidebar.number_input("Liczba popełnionych błędów:", min_value=0, max_value=10, value=0)
priorytet_zamowienia = st.sidebar.selectbox("Priorytet zamówienia:", ["Normalny", "Wysoki", "Pilny"])

# Instrukcja dla użytkownika wchodzącego na stronę
st.info("""
👋 **Witaj w aplikacji analitycznej!** 
**Instrukcja korzystania:**
1. W panelu po lewej stronie wpisz imię pracownika, czas pakowania, liczbę błędów oraz priorytet.
2. Aplikacja automatycznie przeliczy dane i przedstawi wyniki w poniższych trzech zakładkach (zgodnie z wymogami analityki).
""")

# Tworzenie dynamicznego DataFrame na bazie wpisanych danych
user_df = pd.DataFrame({
    'Zamówienie': [101, 102, 103],
    'Pracownik': [imie_pracownika, 'Anna Nowak', 'Piotr Zieliński'],
    'Czas (min)': [czas_pakowania, 22, 12],
    'Błędy': [liczba_bledow, 1, 0],
    'Priorytet': [priorytet_zamowienia, 'Wysoki', 'Niski']
})

# --- ZAKŁADKI ANALITYCZNE ---
tab1, tab2, tab3 = st.tabs(["📊 1. Analiza Deskryptywna", "🔮 2. Analiza Predykcyjna", "⚙️ 3. Analiza Preskryptywna"])

with tab1:
    st.subheader("1. Analiza Deskryptywna (Co się stało?)")
    st.markdown("**• Wejście:** Wprowadzone parametry zamówień oraz dane operacyjne.")
    st.markdown("**• Wyjście:** Zestawienie tabelaryczne i podsumowanie wskaźników.")
    
    col1, col2 = st.columns(2)
    col1.metric("Średni czas pakowania", f"{user_df['Czas (min)'].mean():.1f} min")
    col2.metric("Suma błędów w systemie", int(user_df['Błędy'].sum()))
    
    st.dataframe(user_df, use_container_width=True)

with tab2:
    st.subheader("2. Analiza Predykcyjna (Co się może wydarzyć?)")
    st.markdown("**• Wejście:** Czas realizacji wpisany przez użytkownika.")
    st.markdown("**• Wyjście:** Ocena ryzyka opóźnień i anomalií.")
    
    pred_df = user_df.copy()
    pred_df['Ryzyko opóźnienia'] = pred_df['Czas (min)'].apply(lambda x: '⚠️ Wysokie Ryzyko' if x > 20 else '✅ Stabilnie')
    
    st.dataframe(pred_df[['Zamówienie', 'Pracownik', 'Czas (min)', 'Ryzyko opóźnienia']], use_container_width=True)
    
    if czas_pakowania > 20:
        st.warning(f"⚠️ **Alarm predykcyjny:** Wprowadzony czas ({czas_pakowania} min) dla pracownika {imie_pracownika} przekracza normę i grozi opóźnieniem!")
    else:
        st.success(f"✅ Proces dla pracownika {imie_pracownika} przebiega bezpiecznie.")

with tab3:
    st.subheader("3. Analiza Preskryptywna (Co powinniśmy zrobić?)")
    st.markdown("**• Wejście:** Wyniki predykcji oraz wskaźniki błędów.")
    st.markdown("**• Wyjście:** Rekomendacje optymalizacyjne dla menedżera.")
    
    st.success("✅ **Automatyczna rekomendacja menedżerska:**")
    if liczba_bledow > 0:
        st.info(f"• **Działanie naprawcze:** Zauważono {liczba_bledow} błędów u pracownika **{imie_pracownika}**. Zaleca się skierowanie go na dodatkowe szkolenie stanowiskowe.")
    else:
        st.info(f"• **Optymalizacja zasobów:** Pracownik **{imie_pracownika}** nie popełnia błędów. Zaleca się przydzielanie mu zadań o priorytecie *Pilnym*.")
