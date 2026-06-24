import streamlit as st
import pandas as pd

# =============================
# PAGE SETUP
# =============================
st.set_page_config(page_title="ARK Shop Rechner", layout="wide")

# =============================
# ITEMS
# =============================
ITEM_PRICES = {
    "armor": 1500,
    "tek": 3000,
    "saddle": 2000,
    "weapon": 2500
}

# =============================
# TIERS
# =============================
TIER = {
    "Schultertier": {
        "rate": 20,
        "essence": 30000,
        "note": "Schultertiere"
    },

    "Companion": {
        "rate": 40,
        "essence": 40000,
        "note": "Companions / Begleiter"
    },

    "Normale Dino": {
        "rate": 80,
        "essence": 50000,
        "note": "Standard-Dinos"
    },

    # 🟡 BOSSE
    "Boss-Tier": {
        "rate": 110,
        "essence": 70000,
        "note": "Ossidon / Rex / Megatherium / Therizino / Deinosuchus / Spino"
    },

    # 🥚 EIER
    "Eier-Dino": {
        "rate": 120,
        "essence": 80000,
        "note": "Deinonychus / Aureliax / Wyvern / Rock Drake"
    },

    # 🔥 SPEZIAL
    "Spezial-Tier": {
        "rate": 150,
        "essence": 90000,
        "note": "Carcha / Giga / Reaper / Rhynio / Dreadnought"
    }
}

# =============================
# SESSION STATE
# =============================
if "animals" not in st.session_state:
    st.session_state.animals = []

# =============================
# HELPERS
# =============================
def fmt(x):
    return f"{int(x):,}".replace(",", ".") + " SP"

def calc_items(a, t, s, w):
    return (
        a * ITEM_PRICES["armor"] +
        t * ITEM_PRICES["tek"] +
        s * ITEM_PRICES["saddle"] +
        w * ITEM_PRICES["weapon"]
    )

def calc_animal(an):
    cfg = TIER[an["cat"]]

    if an["essence"]:
        value = cfg["essence"]
        label = f"🧬 {an['cat']} Essenz"
    else:
        value = an["level"] * cfg["rate"]
        label = f"🦖 {an['cat']} Lvl {an['level']}"

        if an["shiny"]:
            value += 30000
            label += " ✨"

        if an["castrated"]:
            value *= 0.25
            label += " ✂️"

    return label, value

# =============================
# HEADER
# =============================
st.title("🦖 ARK Shop Rechner")
st.caption("Shopwert & Tierberechnung in Echtzeit")

st.divider()

# =============================
# LAYOUT
# =============================
col1, col2 = st.columns(2)

# -----------------------------
# 🛡️ ITEMS
# -----------------------------
with col1:
    st.subheader("🛡️ Gegenstände")

    armor = st.number_input("Rüstungsteile", min_value=0, step=1)
    tek = st.number_input("Tek-Rüstung", min_value=0, step=1)
    saddle = st.number_input("Sättel", min_value=0, step=1)
    weapon = st.number_input("Waffen", min_value=0, step=1)

    item_total = calc_items(armor, tek, saddle, weapon)

    st.metric("🧾 Gegenstände", fmt(item_total))

# -----------------------------
# 🦖 TIERE
# -----------------------------
with col2:
    st.subheader("🦖 Tier Builder")

    cat = st.selectbox("Kategorie", list(TIER.keys()))
    st.caption(TIER[cat]["note"])

    level = st.number_input("Level", min_value=1, step=1)

    shiny = st.checkbox("✨ Shiny (+30.000)")
    essence = st.checkbox("🧬 Essenz (Fixwert)")
    castrated = st.checkbox("✂️ Kastriert (25%)")

    if st.button("➕ Tier hinzufügen"):
        st.session_state.animals.append({
            "cat": cat,
            "level": level,
            "shiny": shiny,
            "essence": essence,
            "castrated": castrated
        })

        st.toast("Tier hinzugefügt 🦖✨")
        st.balloons()

st.divider()

# =============================
# 📋 TIER LISTE
# =============================
st.subheader("📋 Tiere")

rows = []
animal_total = 0

for i, a in enumerate(st.session_state.animals):
    label, value = calc_animal(a)
    animal_total += value

    rows.append({
        "Tier": label,
        "Wert": fmt(value),
        "Index": i
    })

df = pd.DataFrame(rows)

if not df.empty:
    st.dataframe(df, use_container_width=True)

    if st.button("🗑️ Letztes Tier löschen"):
        st.session_state.animals.pop()
        st.rerun()
else:
    st.info("Noch keine Tiere hinzugefügt")

# =============================
# 💰 TOTAL
# =============================
total = item_total + animal_total

st.divider()

st.subheader("💰 Gesamtwert")

st.metric("🏆 TOTAL", fmt(total))

st.success("Berechnung aktuell")

# =============================
# 📋 EXPORT
# =============================
export = "🦖 ARK SHOP RECHNER\n\n"

export += f"🛡️ Items: {fmt(item_total)}\n"
export += f"🦖 Tiere: {fmt(animal_total)}\n"
export += f"🏆 Gesamt: {fmt(total)}\n\n"

for a in st.session_state.animals:
    label, value = calc_animal(a)
    export += f"- {label}: {fmt(value)}\n"

st.download_button(
    "📋 Export (Discord / Text)",
    export,
    file_name="ark_shop.txt"
)