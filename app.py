import streamlit as st
import ctypes
import os
import sys
import random

# --- 0. BỘ TỪ ĐIỂN ĐA NGÔN NGỮ (I18N) ---
UI = {
    'vi': {
        'title': "✨ Trắc nghiệm tính cách OCEAN",
        'setup': "Chào mừng bạn! Hãy thiết lập bài test của mình.",
        'num_q': "Chọn số lượng câu hỏi:",
        'universe': "Chọn vũ trụ bạn muốn so sánh:",
        'start': "🚀 Bắt đầu làm bài!",
        'progress': "Đang làm bài test...",
        'guide': "💡 **Hướng dẫn:** Kéo thanh trượt để chọn mức độ đồng tình. (1 = Rất không đồng ý ➡️ 5 = Rất đồng ý).",
        'rate': "Đánh giá",
        'submit': "✅ Nộp bài và Xem kết quả",
        'analyzing': "C++ Engine đang phân tích...",
        'result_title': "Tadaaaa! Kết quả của bạn đây:",
        'you_are': "Bạn chính là",
        'why': "Vì sao lại là",
        'raw_score': "📊 **Bảng điểm thô của bạn:**",
        'retry': "🔄 Làm lại bài test",
        'error': "🚨 C++ Engine báo lỗi: Không tìm thấy file",
        'traits': {
            'O': "có tư duy cởi mở, sáng tạo vô tận và luôn thích bứt phá (Openness) 🌌!",
            'C': "cực kỳ kỷ luật, tận tâm và luôn hướng tới sự hoàn hảo (Conscientiousness) 🎯!",
            'E': "tràn đầy năng lượng, hướng ngoại và luôn biết cách tỏa sáng (Extraversion) 🔥!",
            'A': "rất dễ chịu, thân thiện và luôn mang lại 'vibe' tích cực (Agreeableness) 💖!",
            'N': "có một nội tâm sâu sắc, nhạy cảm và đầy cảm xúc mãnh liệt (Neuroticism) 🌪️!"
        }
    },
    'en': {
        'title': "✨ OCEAN Personality Quiz",
        'setup': "Welcome! Let's set up your test.",
        'num_q': "Select number of questions:",
        'universe': "Select the universe to compare with:",
        'start': "🚀 Start the Quiz!",
        'progress': "Taking the test...",
        'guide': "💡 **Guide:** Use the slider to rate your agreement. (1 = Strongly Disagree ➡️ 5 = Strongly Agree).",
        'rate': "Rate",
        'submit': "✅ Submit and View Results",
        'analyzing': "C++ Engine is analyzing...",
        'result_title': "Tadaaaa! Here is your result:",
        'you_are': "You are",
        'why': "Why",
        'raw_score': "📊 **Your raw scores:**",
        'retry': "🔄 Take the test again",
        'error': "🚨 C++ Engine Error: Cannot find file",
        'traits': {
            'O': "have a highly open, creative mind and love exploring new ideas (Openness) 🌌!",
            'C': "are very disciplined, dedicated, and always strive for perfection (Conscientiousness) 🎯!",
            'E': "are full of energy, outgoing, and love to shine in a crowd (Extraversion) 🔥!",
            'A': "are very agreeable, friendly, and always bring positive vibes (Agreeableness) 💖!",
            'N': "have a complex inner world, deep sensitivity, and intense emotions (Neuroticism) 🌪️!"
        }
    },
    'de': {
        'title': "✨ OCEAN Persönlichkeitstest",
        'setup': "Willkommen! Lass uns deinen Test einrichten.",
        'num_q': "Anzahl der Fragen wählen:",
        'universe': "Wähle das Universum zum Vergleichen:",
        'start': "🚀 Test Starten!",
        'progress': "Test läuft...",
        'guide': "💡 **Anleitung:** Benutze den Schieberegler für deine Zustimmung. (1 = Stimme gar nicht zu ➡️ 5 = Stimme voll zu).",
        'rate': "Bewerten",
        'submit': "✅ Einreichen und Ergebnisse sehen",
        'analyzing': "C++ Engine analysiert...",
        'result_title': "Tadaaaa! Hier ist dein Ergebnis:",
        'you_are': "Du bist",
        'why': "Warum",
        'raw_score': "📊 **Deine Rohwerte:**",
        'retry': "🔄 Test wiederholen",
        'error': "🚨 C++ Engine Fehler: Datei nicht gefunden",
        'traits': {
            'O': "offen, kreativ und lieben es, neue Ideen zu erforschen (Openness) 🌌!",
            'C': "sehr diszipliniert, engagiert und streben immer nach Perfektion (Conscientiousness) 🎯!",
            'E': "voller Energie, extrovertiert und stehen gerne im Mittelpunkt (Extraversion) 🔥!",
            'A': "sehr umgänglich, freundlich und bringen immer positive Vibes (Agreeableness) 💖!",
            'N': "haben eine komplexe innere Welt, tiefe Sensibilität und intensive Emotionen (Neuroticism) 🌪️!"
        }
    }
}

# --- 1. KẾT NỐI VỚI C++ ENGINE ---
lib_ext = '.dll' if sys.platform == 'win32' else '.so'
lib_path = os.path.join(os.path.dirname(__file__), f'core_engine{lib_ext}')

try:
    engine = ctypes.CDLL(lib_path)
    engine.get_best_match_api.argtypes = [
        ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_char_p
    ]
    engine.get_best_match_api.restype = ctypes.c_char_p
except Exception as e:
    st.error(f"Lỗi tải C++ Engine: {e}")
    st.stop()

# --- 2. HÀM ĐỌC CÂU HỎI THEO NGÔN NGỮ ---
@st.cache_data
def load_questions(lang_code):
    questions = []
    filename = f"questions_{lang_code}.txt"
    try:
        with open(filename, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line: continue
                parts = line.split()
                q_text = []
                factors = {}
                for token in parts:
                    if ':' in token and any(c.isdigit() for c in token):
                        trait, val = token.split(':')
                        factors[trait] = int(val)
                    else:
                        q_text.append(token)
                questions.append({"text": " ".join(q_text), "factors": factors})
    except Exception as e:
        st.error(f"Không tìm thấy file {filename}!")
    return questions

# --- 3. QUẢN LÝ TRẠNG THÁI (STATE) ---
if 'step' not in st.session_state:
    st.session_state.step = 0
# CHỈ LƯU VỊ TRÍ (INDEX) CỦA CÂU HỎI, KHÔNG LƯU TEXT
if 'selected_indices' not in st.session_state:
    st.session_state.selected_indices = []

# --- 4. GIAO DIỆN NAVBAR & TIÊU ĐỀ ---
st.set_page_config(page_title="OCEAN Quiz", page_icon="🧠", layout="centered")

# -- CSS ÉP CỨNG ĐỘ RỘNG CHO DROPDOWN NGÔN NGỮ --
st.markdown("""
    <style>
    /* Tìm đúng cột số 2 (cột chứa ngôn ngữ) và ép cứng width của Selectbox */
    div[data-testid="column"]:nth-of-type(2) div[data-testid="stSelectbox"] {
        min-width: 145px !important;
        max-width: 145px !important;
        margin-left: auto; /* Đẩy hộp thoại sát sang mép phải cho sang trọng */
    }
    </style>
""", unsafe_allow_html=True)

# Chỉnh lại tỉ lệ cột (Nới cột phải ra một chút để chứa vừa đủ cái width 145px)
col_title, col_lang = st.columns([3.75, 1.25])

with col_lang:
    st.markdown("<br>", unsafe_allow_html=True) # Cân bằng chiều cao với Tiêu đề
    lang_choice = st.selectbox(
        "Language", 
        options=['vi', 'en', 'de'],
        format_func=lambda x: {'vi': '🇻🇳 Tiếng Việt', 'en': '🇬🇧 English', 'de': '🇩🇪 Deutsch'}[x],
        key="lang",
        label_visibility="collapsed"
    )

t = UI[lang_choice]
all_questions = load_questions(lang_choice)

with col_title:
    st.title(t['title'])

st.divider()

universes = {
    "Beatboxers": "Beatboxer.people",
    "Gen Alpha (Brainrot)": "Brainrot.people",
    "Baby Animals": "BabyAnimals.people",
    "Brooklyn 99": "Brooklyn99.people",
    "Disney": "Disney.people",
    "Hogwarts": "Hogwarts.people",
    "Star Wars": "StarWars.people",
}

# ==========================================
# MÀN HÌNH 0: SETUP
# ==========================================
if st.session_state.step == 0:
    st.info(t['setup'])
    
    num_q = st.number_input(f"{t['num_q']} (20 - {len(all_questions)}):", 
                            min_value=20, max_value=len(all_questions), value=20)
    
    universe_name = st.selectbox(t['universe'], list(universes.keys()))
    
    if st.button(t['start']):
        # Bốc random vị trí index thay vì bốc cả câu
        st.session_state.selected_indices = random.sample(range(len(all_questions)), num_q)
        st.session_state.universe_file = universes[universe_name]
        st.session_state.step = 1
        st.rerun()

# ==========================================
# MÀN HÌNH 1: KHẢO SÁT
# ==========================================
elif st.session_state.step == 1:
    st.progress(50, text=t['progress'])
    st.info(t['guide'])
    
    st.markdown("""
        <style>
        .question-text { text-align: center; font-size: 24px !important; font-weight: 600; margin: 20px 0; }
        </style>
    """, unsafe_allow_html=True)
    st.divider()
    
    with st.form("quiz_form"):
        answers = []
        # Duyệt qua các index đã lưu và lôi câu hỏi tương ứng trong ngôn ngữ hiện tại ra
        for i, q_idx in enumerate(st.session_state.selected_indices):
            q = all_questions[q_idx]
            
            st.markdown(f"<div class='question-text'>{q['text']}</div>", unsafe_allow_html=True)
            ans_val = st.select_slider(
                t['rate'], options=[1, 2, 3, 4, 5], value=3, key=f"q_{i}", label_visibility="collapsed"
            )
            answers.append((q, ans_val))
            st.write("---")
            
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submitted = st.form_submit_button(t['submit'], use_container_width=True)
        
        if submitted:
            scores = {'O': 0, 'C': 0, 'E': 0, 'A': 0, 'N': 0}
            for q, ans_val in answers:
                weight = ans_val - 3 
                for trait, factor_val in q['factors'].items():
                    scores[trait] += (weight * factor_val)
            st.session_state.final_scores = scores
            st.session_state.step = 2
            st.rerun()

# ==========================================
# MÀN HÌNH 2: KẾT QUẢ
# ==========================================
elif st.session_state.step == 2:
    scores = st.session_state.final_scores
    c_filepath = st.session_state.universe_file.encode('utf-8')
    
    with st.spinner(t['analyzing']):
        match_bytes = engine.get_best_match_api(
            scores['O'], scores['C'], scores['E'], scores['A'], scores['N'], c_filepath
        )
        match_name = match_bytes.decode('utf-8')
    
    if "Error" in match_name:
        st.error(f"{t['error']} `{st.session_state.universe_file}`!")
    else:
        st.progress(100, text="100%")
        st.balloons()
        st.success(t['result_title'])
        st.markdown(f"<h1 style='text-align: center; color: #ff4b4b;'>{t['you_are']} {match_name}!</h1>", unsafe_allow_html=True)
        
        best_trait = max(scores, key=scores.get)
        st.info(f"💡 **{t['why']} {match_name}?**\n\n{match_name} ({best_trait}): {t['traits'][best_trait]}")
        
        st.divider()
        st.write(f"{t['raw_score']} O: {scores['O']} | C: {scores['C']} | E: {scores['E']} | A: {scores['A']} | N: {scores['N']}")
        
        if st.button(t['retry']):
            st.session_state.step = 0
            st.rerun()