import streamlit as st
import random
import time
import streamlit.components.v1 as components

# --- CONFIGURATION & THEME ---
st.set_page_config(page_title="Bollywood Bidding Dashboard", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Bungee&display=swap');
    .main { background-color: #0e1117; }
    .stHeader { font-family: 'Bungee', cursive; color: #FFD700; text-align: center; }
    .briefcase-box {
        background: linear-gradient(145deg, #2c3e50, #000000);
        border: 3px solid #FFD700;
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        box-shadow: 0px 10px 20px rgba(0,0,0,0.5);
    }
    .money-val { font-size: 45px; color: #00FF00; font-weight: bold; font-family: 'Courier New', monospace; }
    .coin-icon { color: #FFD700; font-size: 24px; }
    </style>
    """, unsafe_allow_html=True)

# --- SESSION STATE ---
TEAMS = ["Tech Trio", "Badmaash Company", "Sassy Sakhis", "Bollywood Pitch Squad"]
if 'balances' not in st.session_state:
    st.session_state.balances = {team: 0 for team in TEAMS}
if 'active_teams' not in st.session_state:
    st.session_state.active_teams = {team: True for team in TEAMS}
if 'shields' not in st.session_state:
    st.session_state.shields = {team: False for team in TEAMS}
if 'last_result' not in st.session_state:
    st.session_state.last_result = "SPIN TO START"
if 'last_val' not in st.session_state:
    st.session_state.last_val = 0

# --- THE ANIMATED WHEEL (HTML/JS) ---
# This creates a visual pie chart wheel that actually spins and slows down.
wheel_options = ["₹100", "₹500", "₹1000", "BANKRUPT", "₹200", "SHIELD", "₹800", "STEAL", "JACKPOT", "₹300"]
colors = ["#f1c40f", "#e67e22", "#e74c3c", "#2c3e50", "#9b59b6", "#3498db", "#27ae60", "#d35400", "#c0392b", "#16a085"]

wheel_html = f"""
<div style="display: flex; flex-direction: column; align-items: center; justify-content: center; color: white; font-family: sans-serif;">
    <div id="wrapper" style="position: relative; width: 300px; height: 300px;">
        <div id="pin" style="position: absolute; top: -10px; left: 50%; transform: translateX(-50%); width: 0; height: 0; 
            border-left: 15px solid transparent; border-right: 15px solid transparent; border-top: 30px solid #FF0000; z-index: 10;"></div>
        <canvas id="wheel" width="300" height="300" style="transform: rotate(0deg); transition: transform 4s cubic-bezier(0.15, 0, 0.15, 1);"></canvas>
    </div>
    <button id="spinBtn" style="margin-top: 20px; padding: 10px 30px; font-size: 20px; cursor: pointer; background: #FFD700; border: none; border-radius: 5px; font-weight: bold;">SPIN THE WHEEL 🎰</button>
</div>

<script>
    const canvas = document.getElementById('wheel');
    const ctx = canvas.getContext('2d');
    const options = {wheel_options};
    const colors = {colors};
    const arc = 2 * Math.PI / options.length;

    function drawWheel() {{
        options.forEach((opt, i) => {{
            const angle = i * arc;
            ctx.fillStyle = colors[i];
            ctx.beginPath();
            ctx.moveTo(150, 150);
            ctx.arc(150, 150, 140, angle, angle + arc);
            ctx.fill();
            ctx.save();
            ctx.translate(150 + Math.cos(angle + arc/2) * 100, 150 + Math.sin(angle + arc/2) * 100);
            ctx.rotate(angle + arc/2 + Math.PI/2);
            ctx.fillStyle = "white";
            ctx.font = "bold 14px Arial";
            ctx.fillText(opt, -ctx.measureText(opt).width/2, 0);
            ctx.restore();
        }});
    }}
    drawWheel();

    let currentRotation = 0;
    document.getElementById('spinBtn').onclick = () => {{
        const addRotation = 1440 + Math.floor(Math.random() * 360);
        currentRotation += addRotation;
        canvas.style.transform = `rotate(${{currentRotation}}deg)`;
    }};
</script>
"""

# --- UI LAYOUT ---
st.markdown('<h1 class="stHeader">💰 BOLLYWOOD BIDDING WAR 💰</h1>', unsafe_allow_html=True)

# Sidebar for Attendance
with st.sidebar:
    st.header("🎟️ Attendance")
    for team in TEAMS:
        st.session_state.active_teams[team] = st.checkbox(f"{team} Present", value=True)
    st.divider()
    st.write("CFO Console: Adjust total prizes or tax rates here.")

# Top Section: The Wheel
col_w, col_ctrl = st.columns([1, 1])

with col_w:
    components.html(wheel_html, height=420)

with col_ctrl:
    st.write("### 🎛️ Host Controls")
    res = st.selectbox("Last Wheel Landing:", wheel_options)
    if st.button("Confirm Result & Lock Value"):
        st.session_state.last_result = res
        # Extract value
        if "₹" in res:
            val = int(res.replace("₹", ""))
            st.session_state.last_val = val
        elif "JACKPOT" in res:
            st.session_state.last_val = 2000
        else:
            st.session_state.last_val = 0
    
    st.info(f"Current Value per Letter: **₹{st.session_state.last_val}**")

st.divider()

# Team Section
active_list = [t for t in TEAMS if st.session_state.active_teams[t]]
cols = st.columns(len(active_list))

for i, team in enumerate(active_list):
    with cols[i]:
        st.markdown(f"""
            <div class="briefcase-box">
                <p style="color: #FFD700; font-weight: bold;">💼 {team}</p>
                <p class="money-val">₹{st.session_state.balances[team]}</p>
                {'<p style="color:#3498db;">🛡️ SHIELDED</p>' if st.session_state.shields[team] else ''}
            </div>
        """, unsafe_allow_html=True)
        
        # Action Buttons
        st.write("")
        if st.button(f"Add Letter (₹{st.session_state.last_val})", key=f"add_{team}"):
            st.session_state.balances[team] += st.session_state.last_val
        
        c1, c2 = st.columns(2)
        if c1.button("Vowel -₹200", key=f"v_{team}"):
            st.session_state.balances[team] -= 200
        if c2.button("Buy Shield", key=f"s_{team}"):
            st.session_state.balances[team] -= 400
            st.session_state.shields[team] = True
            
        if st.button("🔥 BANKRUPT 🔥", key=f"b_{team}"):
            if st.session_state.shields[team]:
                st.session_state.shields[team] = False
                st.toast(f"{team} used their shield!")
            else:
                st.session_state.balances[team] = 0
                st.error(f"{team} lost everything!")

        with st.expander("Bidding / Edit"):
            amt = st.number_input("Amount", key=f"edit_{team}", step=100)
            if st.button("Finalize Bid", key=f"bid_{team}"):
                st.session_state.balances[team] -= amt

st.markdown("---")
st.caption("E-Cell Yukta | MKSSS's Cummins College of Engineering for Women")
