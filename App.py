import streamlit as st
import pandas as pd
import numpy as np

# Konfiguracja strony
st.set_page_config(
    page_title="Smart Warehouse & Logistics Analytics",
    page_icon="📦",
    layout="wide"
)

# Nagłówek główny
st.title("📦 Inteligentny System Analityczny w Logistyce Magazynowej")
st.markdown("""
Aplikacja realizuje kompleksowy proces przetwarzania danych w oparciu o **trzy poziomy analityki**:
1. **Deskryptywna** (Co się stało?) – raportowanie danych historycznych i wskaźników KPI.
2. **Predykcyjna** (Co się może wydarzyć?) – wykrywanie anomalii i szacowanie ryzyka opóźnień.
3. **Preskryptywna** (Co powinniśmy zrobić?) – automatyczne rekomendacje optymalizacyjne i alokacja zasobów.
""")

# Generowanie profesjonalnego, spójnego zestawu danych (Dataset)
@st.cache_data
def load_warehouse_data():
    np.random.seed(42)
    n_rows = 50
    ids = [1000 + i for i in range(n_rows)]
    pracownicy = ['Jan Kowalski', 'Anna Nowak', 'Piotr Zieliński', 'Katarzyna Wójcik', 'Michał Lewandowski', 'Magda Dąbrowska']
    
    data = pd.DataFrame({
        'ID_Zamowienia': ids,
        'Pracownik': np.random.choice(pracownicy, n_rows),
        'Waga_kg': np.round(np.random.uniform(1.0, 25.0, n_rows), 2),
        'Czas_Pakowania_min': np.random.randint(10, 45, n_rows),
        'Liczba_Bledow': np.random.choice([0, 1, 2, 3], n_rows, p=[0.7, 0.2, 0.08, 0.02]),
        'Priorytet': np.random.choice(['Normalny', 'Wysoki', 'Pilny'], n_rows, p=[0.6, 0.3, 0.1])
    })
    return data

df = load_warehouse_data()

# Zakładki systemowe
tab1, tab2, tab3 = st.tabs([
    "📊 1. Analityka Deskryptywna", 
    "🔮 2. Analityka Predykcyjna", 
    "⚙️ 3. Analityka Preskryptywna"
])

# --- ZAKŁADKA 1: ANALIZA DESKRYPTYWNA ---
with tab1:
    st.header("Analiza Deskryptywna: Raportowanie i Statystyki Historyczne")
    st.write("Moduł agreguje dane historyczne z operacji magazynowych, prezentując kluczowe wskaźniki efektywności (KPI).")
    
    # Filtry interaktywne
    selected_priority = st.selectbox("Filtruj według priorytetu zamówienia:", ['Wszystkie'] + list(df['Priorytet'].unique()))
    filtered_df = df if selected_priority == 'Wszystkie' else df[df['Priorytet'] == selected_priority]
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Łączna liczba zamówień", len(filtered_df))
    col2.metric("Średni czas pakowania", f"{filtered_df['Czas_Pakowania_min'].mean():.1f} min")
    col3.metric("Suma wykrytych błędów", int(filtered_df['Liczba_Bledow'].sum()))
    col4.metric("Średnia waga paczki", f"{filtered_df['Waga_kg'].mean():.2f} kg")
    
    st.subheader("Pełna baza danych operacyjnych")
    st.dataframe(filtered_df, use_container_width=True)
    
    st.subheader("Wizualizacja: Czas pakowania w zależności od pracownika")
    chart_data = filtered_df.groupby('Pracownik')['Czas_Pakowania_min'].mean()
    st.bar_chart(chart_data)

# --- ZAKŁADKA 2: ANALIZA PREDYKCYJNA ---
with tab2:
    st.header("Analiza Predykcyjna: Wykrywanie Ryzyka i Anomalii")
    st.write("Wykorzystanie modeli regułowych do prognozowania opóźnień na podstawie wagi, czasu i priorytetu.")
    
    # Model predykcyjny (algorytm oceny ryzyka)
    pred_df = df.copy()
    # Reguła predykcyjna: ryzyko rośnie, gdy czas pakowania przekracza 30 min lub waga jest duża przy wysokim priorytecie
    pred_df['Wskaznik_Ryzyka'] = (pred_df['Czas_Pakowania_min'] * 0.6) + (pred_df['Waga_kg'] * 0.4)
    sredni_prog_ryzyka = pred_df['Wskaznik_Ryzyka'].mean()
    
    pred_df['Status_Ryzyka'] = pred_df['Wskaznik_Ryzyka'].apply(
        lambda x: 'Wysokie Ryzyko 🔴' if x > (sredni_prog_ryzyka * 1.2) else 'Stabilnie 🟢'
    )
    
    st.dataframe(pred_df[['ID_Zamowienia', 'Pracownik', 'Priorytet', 'Wskaznik_Ryzyka', 'Status_Ryzyka']], use_container_width=True)
    
    wysokie_ryzyko_count = len(pred_df[pred_df['Status_Ryzyka'] == 'Wysokie Ryzyko 🔴'])
    if wysokie_ryzyko_count > 0:
        st.warning(f"⚠️ **Alarm predykcyjny:** Wykryto {wysokie_ryzyko_count} zamówień zagrożonych opóźnieniem w realizacji.")
    else:
        st.success("✅ Brak zagrożeń krytycznych w bieżącym harmonogramie.")

# --- ZAKŁADKA 3: ANALIZA PRESKRYPTYWNA ---
with tab3:
    st.header("Analiza Preskryptywna: System Rekomendacji i Optymalizacji")
    st.write("Moduł generujący automatyczne decyzje menedżerskie w celu optymalizacji przepustowości procesów.")
    
    # Obliczenia optymalizacyjne
    wydajnosc_pracownikow = df.groupby('Pracownik').agg(
        Sredni_Czas=('Czas_Pakowania_min', 'mean'),
        Suma_Bledow=('Liczba_Bledow', 'sum'),
        Liczba_Zadan=('ID_Zamowienia', 'count')
    ).reset_index()
    
    # Najlepszy pracownik (najkrótszy średni czas i najmniej błędów)
    najlepszy = wydajnosc_pracownikow.sort_values(by=['Sredni_Czas', 'Suma_Bledow']).iloc[0]
    
    # Pracownik wymagający wsparcia
    wymagajacy_wsparcia = wydajnosc_pracownikow.sort_values(by='Suma_Bledow', ascending=False).iloc[0]
    
    st.subheader("🎯 Automatyczne rekomendacje optymalizacyjne systemu:")
    
    st.success(f"""
    * **Optymalizacja alokacji zadań pilnych:** 
      Najbardziej efektywny pracownik w systemie to **{najlepszy['Pracownik']}** 
      (średni czas realizacji: **{najlepszy['Sredni_Czas']:.1f} min**). 
      Zaleca się skierowanie go do obsługi zamówień o priorytecie *Pilnym*.
    """)
    
    st.info(f"""
    * **Korekta jakościowa procesu:** 
      Pracownik **{wymagajacy_wsparcia['Pracownik']}** generuje najwięcej odchyłek 
      (łączna liczba błędów: **int({wymagajacy_wsparcia['Suma_Bledow']})**). 
      Rekomenduje się przeprowadzenie krótkiego instruktażu stanowiskowego.
    """)
    
    st.write("### Ranking efektywności zespołu:")
    st.dataframe(wydajnosc_pracownikow, use_container_width=True)
