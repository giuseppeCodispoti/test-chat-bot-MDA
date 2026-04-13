import pandas as pd
import re

def normalizza_testo(s):
    if s is None:
        return ""
    s = str(s).lower().strip()
    s = re.sub(r"[^a-z0-9 ]", "", s)
    s = re.sub(r"\s+", " ", s)
    return s


def info_locale(df, nome_locale):
    query = normalizza_testo(nome_locale)

    df["__locale_norm"] = df["Locale"].apply(normalizza_testo)
    match = df[df["__locale_norm"].str.contains(query, na=False)]

    if match.empty:
        return f"❌ Nessuna informazione trovata per il locale '{nome_locale}'."

    if len(match) > 1:
        nomi = match["Locale"].unique()[:10]
        elenco = "\n".join([f"- {n}" for n in nomi])
        return (
            f"⚠️ Ho trovato più locali simili a '{nome_locale}':\n"
            f"{elenco}\n\n"
            f"Scrivi il nome completo."
        )

    r = match.iloc[0]

    indirizzo = ""
    if "Address" in df.columns and pd.notna(r.get("Address")):
        indirizzo = r["Address"]
    elif "Indirizzo" in df.columns:
        indirizzo = r["Indirizzo"]

    risposta = [
        f"📍 Locale: {r['Locale']}",
        f"📌 Indirizzo: {indirizzo}",
    ]

    if "Partita Iva" in df.columns and pd.notna(r.get("Partita Iva")):
        risposta.append(f"🧾 Partita IVA: {r['Partita Iva']}")

    anni = [c for c in df.columns if str(c).isdigit()]
    if anni:
        risposta.append("\n📅 Stato per anno:")
        for a in sorted(anni):
            val = r[a]
            if pd.isna(val):
                risposta.append(f"❌ {a}: dato mancante")
            elif str(val).strip().lower() == "pag":
                risposta.append(f"✅ {a}: {val}")
            else:
                risposta.append(f"❌ {a}: {val}")

    return "\n".join(risposta)


def chatbot(domanda, df):
    # cerca la parola "locale" ignorando maiuscole/minuscole
    match = re.search(r"\blocale\b\s*(.*)", domanda, re.IGNORECASE)

    if match:
        nome_locale = match.group(1).strip()
        return info_locale(df, nome_locale)

    return "❓ Scrivi: Dammi informazioni sul locale XYZ"
