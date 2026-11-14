# Smart-werehouse-logistics
Aplikacja logistyczna z analizą deskryptywną, predykcyjną i perspektywną
# 📦 Smart Warehouse & Logistics Intelligence System

Projekt zaliczeniowy z zakresu sztucznej inteligencji i zaawansowanej analityki w procesach logistycznych.

## 🎯 Cel projektu
Aplikacja wspomaga zarządzanie procesem pakowania paczek oraz alokacją pracowników w magazynie, wykorzystując trzy poziomy analityki danych: deskryptywną, predykcyjną oraz preskryptywną.

---

## 📊 1. Analiza deskryptywna (Descriptive Analytics) – *Co się stało?*
* **Opis:** Zbieranie, porządkowanie i prezentacja danych historycznych dotyczących operacji magazynowych.
* **Wejście (Input):** Plik `data.csv` zawierający historyczne dane o spakowanych paczkach, czasach realizacji oraz liczbie błędów.
* **Wyjście (Output):** Statystyki ogólne (np. całkowita liczba paczek, średni czas pakowania) oraz wykresy w dashboardzie.

## 🔮 2. Analiza predykcyjna (Predictive Analytics) – *Co się może wydarzyć?*
* **Opis:** Wykorzystanie modeli do przewidywania przyszłych zdarzeń i ryzyka.
* **Wejście (Input):** Bieżący stan zamówień, obciążenie pracowników w czasie rzeczywistym.
* **Wyjście (Output):** Alerty i prognozy (np. ostrzeżenie: *"Zamówienie #104 ma wysokie ryzyko opóźnienia"*, przewidywane przeciążenie sekcji pakowania w przyszłym kwartale).

## ⚙️ 3. Analiza preskryptywna (Prescriptive Analytics) – *Co powinniśmy zrobić?*
* **Opis:** System rekomendacyjny łączący predykcję z optymalizacją.
* **Wejście (Input):** Wyniki analizy predykcyjnej (wykryte wąskie gardła i opóźnienia) oraz lista dostępnych pracowników i ich kompetencji.
* **Wyjście (Output):** Konkretne rekomendacje decyzyjne (np. *"Aby uniknąć opóźnień, przydziel pracownika [Jan Kowalski] do zadania [Pakowanie pilne]"*).

---

## 🚀 Jak uruchomić aplikację?
1. Sklonuj repozytorium.
2. Zainstaluj wymagane biblioteki: `pip install -r requirements.txt`
3. Uruchom aplikację: `streamlit run app.py`
