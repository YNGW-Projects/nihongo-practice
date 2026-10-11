import streamlit as st

# ==========================================
# ページ設定
# ==========================================
st.set_page_config(
    page_title="Nihongo Practice",
    page_icon="🇯🇵",
    layout="wide"
)

# ==========================================
# デザイン
# ==========================================
st.markdown("""
<style>
.stApp {
    background: #F6F8FC;
}
.block-container {
    max-width: 1000px;
    padding-top: 2rem;
}
.hero {
    background: linear-gradient(120deg, #16345C, #3467A5);
    color: white;
    border-radius: 18px;
    padding: 28px;
    margin-bottom: 20px;
}
.hero h1 {
    color: white;
    margin: 0;
}
.hero p {
    color: #E2EAF5;
    margin-bottom: 0;
}
.lesson {
    background: white;
    border-radius: 14px;
    padding: 20px;
    border: 1px solid #E2E8F0;
    margin-bottom: 12px;
}
.dialogue {
    background: #EAF1FB;
    padding: 18px;
    border-radius: 12px;
    margin-bottom: 12px;
    color: #172033;
}
.dialogue strong {
    color: #16345C;
}
.dialogue .jp {
    font-size: 22px;
    font-weight: 650;
    margin: 8px 0;
}
.dialogue .translation {
    font-size: 14px;
    color: #526174;
}
.stButton button {
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3言語設定
# ==========================================
LANGS = {
    "日本語": "ja",
    "English": "en",
    "ภาษาไทย": "th"
}

WORDS = {
    "title": {
        "ja": "日本語を、使える力に。",
        "en": "Japanese for Real Life",
        "th": "เรียนภาษาญี่ปุ่นเพื่อใช้ในชีวิตจริง"
    },
    "subtitle": {
        "ja": "JLPT × 実践日本語会話",
        "en": "JLPT × Practical Japanese",
        "th": "JLPT × ภาษาญี่ปุ่นเพื่อการสื่อสาร"
    },
    "level": {
        "ja": "JLPTレベル",
        "en": "JLPT Level",
        "th": "ระดับ JLPT"
    },
    "lesson": {
        "ja": "レッスンを選択",
        "en": "Choose a lesson",
        "th": "เลือกบทเรียน"
    },
    "conversation": {
        "ja": "会話練習",
        "en": "Conversation practice",
        "th": "ฝึกบทสนทนา"
    },
    "quiz": {
        "ja": "会話クイズ",
        "en": "Conversation quiz",
        "th": "แบบทดสอบบทสนทนา"
    },
    "question": {
        "ja": "この場面で適切な日本語は？",
        "en": "Which Japanese expression fits this situation?",
        "th": "ควรใช้ประโยคภาษาญี่ปุ่นใดในสถานการณ์นี้"
    },
    "check": {
        "ja": "答え合わせ",
        "en": "Check answer",
        "th": "ตรวจคำตอบ"
    },
    "correct": {
        "ja": "正解！",
        "en": "Correct!",
        "th": "ถูกต้อง!"
    },
    "wrong": {
        "ja": "もう一度確認しよう。",
        "en": "Let's review the answer.",
        "th": "มาทบทวนคำตอบกัน"
    },
    "explanation": {
        "ja": "解説",
        "en": "Explanation",
        "th": "คำอธิบาย"
    },
    "completed": {
        "ja": "回答済み",
        "en": "Completed",
        "th": "ทำแล้ว"
    },
    "accuracy": {
        "ja": "正答率",
        "en": "Accuracy",
        "th": "อัตราตอบถูก"
    },
    "reset": {
        "ja": "学習記録をリセット",
        "en": "Reset progress",
        "th": "รีเซ็ตผลการเรียน"
    }
}

def tr(key, lang):
    return WORDS[key][lang]

# ==========================================
# レッスンデータ
# ==========================================
LESSONS = [
    {
        "id": "N5-01",
        "level": "N5",
        "title": {
            "ja": "あいさつ",
            "en": "Greetings",
            "th": "การทักทาย"
        },
        "dialogue": [
            {
                "speaker": "A",
                "jp": "おはようございます。",
                "en": "Good morning.",
                "th": "สวัสดีตอนเช้า"
            },
            {
                "speaker": "B",
                "jp": "おはようございます。お元気ですか。",
                "en": "Good morning. How are you?",
                "th": "สวัสดีตอนเช้า สบายดีไหม"
            }
        ],
        "situation": {
            "ja": "朝、先生に会いました。",
            "en": "You meet your teacher in the morning.",
            "th": "คุณพบคุณครูในตอนเช้า"
        },
        "choices": [
            "こんばんは。",
            "おはようございます。",
            "おやすみなさい。"
        ],
        "answer": 1,
        "explain": {
            "ja": "朝の丁寧なあいさつは「おはようございます」です。",
            "en": "Ohayou gozaimasu is a polite morning greeting.",
            "th": "おはようございます เป็นคำทักทายสุภาพในตอนเช้า"
        }
    },
    {
        "id": "N5-02",
        "level": "N5",
        "title": {
            "ja": "レストラン",
            "en": "Restaurant",
            "th": "ร้านอาหาร"
        },
        "dialogue": [
            {
                "speaker": "店員",
                "jp": "ご注文はお決まりですか。",
                "en": "Are you ready to order?",
                "th": "พร้อมสั่งอาหารหรือยัง"
            },
            {
                "speaker": "客",
                "jp": "カレーを一つください。",
                "en": "One curry, please.",
                "th": "ขอแกงกะหรี่หนึ่งที่"
            }
        ],
        "situation": {
            "ja": "カレーを一つ注文したいです。",
            "en": "You want to order one curry.",
            "th": "คุณต้องการสั่งแกงกะหรี่หนึ่งที่"
        },
        "choices": [
            "カレーを一つください。",
            "カレーはどこですか。",
            "カレーがありません。"
        ],
        "answer": 0,
        "explain": {
            "ja": "注文するときは「〜をください」が使えます。",
            "en": "Use ~ o kudasai to order something.",
            "th": "ใช้ ～をください เมื่อต้องการสั่งอาหารหรือสิ่งของ"
        }
    },
    {
        "id": "N5-03",
        "level": "N5",
        "title": {
            "ja": "買い物",
            "en": "Shopping",
            "th": "การซื้อของ"
        },
        "dialogue": [
            {
                "speaker": "客",
                "jp": "これはいくらですか。",
                "en": "How much is this?",
                "th": "อันนี้ราคาเท่าไร"
            },
            {
                "speaker": "店員",
                "jp": "千円です。",
                "en": "It is 1,000 yen.",
                "th": "หนึ่งพันเยน"
            }
        ],
        "situation": {
            "ja": "商品の値段を知りたいです。",
            "en": "You want to know the price.",
            "th": "คุณต้องการทราบราคาสินค้า"
        },
        "choices": [
            "これは何時ですか。",
            "これは誰ですか。",
            "これはいくらですか。"
        ],
        "answer": 2,
        "explain": {
            "ja": "値段を聞くときは「いくらですか」を使います。",
            "en": "Ikura desu ka means 'How much is it?'",
            "th": "いくらですか ใช้ถามราคาสินค้า"
        }
    },
    {
        "id": "N5-04",
        "level": "N5",
        "title": {
            "ja": "道を聞く",
            "en": "Asking directions",
            "th": "การถามทาง"
        },
        "dialogue": [
            {
                "speaker": "A",
                "jp": "すみません。駅はどこですか。",
                "en": "Excuse me. Where is the station?",
                "th": "ขอโทษ สถานีอยู่ที่ไหน"
            },
            {
                "speaker": "B",
                "jp": "あそこです。",
                "en": "It is over there.",
                "th": "อยู่ตรงโน้น"
            }
        ],
        "situation": {
            "ja": "駅の場所を聞きたいです。",
            "en": "You want to ask where the station is.",
            "th": "คุณต้องการถามว่าสถานีอยู่ที่ไหน"
        },
        "choices": [
            "駅は何時ですか。",
            "駅はどこですか。",
            "駅はいくらですか。"
        ],
        "answer": 1,
        "explain": {
            "ja": "場所を聞くときは「どこですか」を使います。",
            "en": "Doko desu ka is used to ask where something is.",
            "th": "どこですか ใช้ถามสถานที่"
        }
    },
    {
        "id": "N4-01",
        "level": "N4",
        "title": {
            "ja": "学校で質問する",
            "en": "Asking at school",
            "th": "การถามคำถามที่โรงเรียน"
        },
        "dialogue": [
            {
                "speaker": "学生",
                "jp": "先生、質問してもいいですか。",
                "en": "May I ask a question?",
                "th": "คุณครู ขอถามคำถามได้ไหม"
            },
            {
                "speaker": "先生",
                "jp": "はい、いいですよ。",
                "en": "Yes, of course.",
                "th": "ได้เลย"
            }
        ],
        "situation": {
            "ja": "先生に質問する許可をもらいたいです。",
            "en": "You want permission to ask a question.",
            "th": "คุณต้องการขออนุญาตถามคำถาม"
        },
        "choices": [
            "質問してもいいですか。",
            "質問しなければなりません。",
            "質問したことがあります。"
        ],
        "answer": 0,
        "explain": {
            "ja": "「〜てもいいですか」は許可を求める表現です。",
            "en": "~te mo ii desu ka is used to ask permission.",
            "th": "～てもいいですか ใช้ขออนุญาต"
        }
    },
    {
        "id": "N4-02",
        "level": "N4",
        "title": {
            "ja": "体調が悪い",
            "en": "Feeling sick",
            "th": "เมื่อรู้สึกไม่สบาย"
        },
        "dialogue": [
            {
                "speaker": "A",
                "jp": "どうしたんですか。",
                "en": "What's wrong?",
                "th": "เป็นอะไรหรือเปล่า"
            },
            {
                "speaker": "B",
                "jp": "頭が痛いので、早く帰りたいです。",
                "en": "I have a headache, so I want to go home early.",
                "th": "ปวดหัว เลยอยากกลับบ้านเร็ว"
            }
        ],
        "situation": {
            "ja": "頭痛が理由で早く帰りたいです。",
            "en": "You want to go home early because of a headache.",
            "th": "คุณอยากกลับบ้านเร็วเพราะปวดหัว"
        },
        "choices": [
            "頭が痛いのに、早く帰ります。",
            "頭が痛くても、早く帰ります。",
            "頭が痛いので、早く帰りたいです。"
        ],
        "answer": 2,
        "explain": {
            "ja": "「〜ので」は理由を説明するときに使います。",
            "en": "~node explains a reason.",
            "th": "ので ใช้อธิบายเหตุผล"
        }
    },
    {
        "id": "N4-03",
        "level": "N4",
        "title": {
            "ja": "アルバイト",
            "en": "Part-time work",
            "th": "งานพาร์ตไทม์"
        },
        "dialogue": [
            {
                "speaker": "店長",
                "jp": "明日、働けますか。",
                "en": "Can you work tomorrow?",
                "th": "พรุ่งนี้มาทำงานได้ไหม"
            },
            {
                "speaker": "学生",
                "jp": "すみません。明日は予定があります。",
                "en": "Sorry, I have plans tomorrow.",
                "th": "ขอโทษ พรุ่งนี้มีธุระ"
            }
        ],
        "situation": {
            "ja": "明日は予定があるので仕事を断りたいです。",
            "en": "You cannot work tomorrow because you have plans.",
            "th": "คุณทำงานพรุ่งนี้ไม่ได้เพราะมีธุระ"
        },
        "choices": [
            "明日は予定があります。",
            "明日は予定がありません。",
            "明日は働きたいです。"
        ],
        "answer": 0,
        "explain": {
            "ja": "「予定があります」は先約があることを伝えます。",
            "en": "Yotei ga arimasu means you already have plans.",
            "th": "予定があります หมายถึงมีนัดหรือมีแผนอยู่แล้ว"
        }
    },
    {
        "id": "N4-04",
        "level": "N4",
        "title": {
            "ja": "友達を誘う",
            "en": "Inviting a friend",
            "th": "การชวนเพื่อน"
        },
        "dialogue": [
            {
                "speaker": "A",
                "jp": "週末、一緒に映画を見ませんか。",
                "en": "Would you like to watch a movie this weekend?",
                "th": "สุดสัปดาห์นี้ไปดูหนังด้วยกันไหม"
            },
            {
                "speaker": "B",
                "jp": "いいですね。行きましょう。",
                "en": "Sounds good. Let's go.",
                "th": "ดีเลย ไปกันเถอะ"
            }
        ],
        "situation": {
            "ja": "友達を映画に誘いたいです。",
            "en": "You want to invite your friend to a movie.",
            "th": "คุณต้องการชวนเพื่อนไปดูหนัง"
        },
        "choices": [
            "映画を見てはいけません。",
            "一緒に映画を見ませんか。",
            "映画を見ることができます。"
        ],
        "answer": 1,
        "explain": {
            "ja": "「〜ませんか」は相手を丁寧に誘う表現です。",
            "en": "~masen ka is a polite way to invite someone.",
            "th": "～ませんか ใช้ชวนผู้อื่นอย่างสุภาพ"
        }
    }
]

# ==========================================
# サイドバー
# ==========================================
with st.sidebar:
    st.header("🇯🇵 Nihongo Practice")

    language_name = st.selectbox(
        "Language / 言語 / ภาษา",
        list(LANGS.keys())
    )
    lang = LANGS[language_name]

    level = st.selectbox(
        tr("level", lang),
        ["N5", "N4"]
    )

    if "results" not in st.session_state:
        st.session_state.results = {}

    if st.button(tr("reset", lang)):
        st.session_state.results = {}
        st.rerun()

# ==========================================
# トップ画面
# ==========================================
st.markdown(
    f"""
    <div class="hero">
        <h1>{tr("title", lang)}</h1>
        <p>{tr("subtitle", lang)}</p>
    </div>
    """,
    unsafe_allow_html=True
)

# ==========================================
# 成績表示
# ==========================================
results = st.session_state.results
completed = len(results)
correct = sum(results.values())
accuracy = round(correct / completed * 100) if completed else 0

c1, c2, c3 = st.columns(3)

c1.metric(tr("completed", lang), f"{completed}/{len(LESSONS)}")
c2.metric("Score", correct)
c3.metric(tr("accuracy", lang), f"{accuracy}%")

st.progress(completed / len(LESSONS))
st.divider()

# ==========================================
# レッスン選択
# ==========================================
available = [x for x in LESSONS if x["level"] == level]

options = [
    f'{x["id"]} | {x["title"][lang]}'
    for x in available
]

selected = st.selectbox(tr("lesson", lang), options)
lesson = available[options.index(selected)]

st.subheader(lesson["title"][lang])
st.caption(f'JLPT {level} | {lesson["id"]}')

# ==========================================
# 会話表示
# ==========================================
st.markdown(f'### {tr("conversation", lang)}')

for line in lesson["dialogue"]:
    translation = line[lang] if lang != "ja" else ""

    st.markdown(
        f"""
        <div class="dialogue">
            <strong>{line["speaker"]}</strong>
            <div class="jp">{line["jp"]}</div>
            <div class="translation">{translation}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

# ==========================================
# クイズ
# ==========================================
st.divider()
st.markdown(f'### {tr("quiz", lang)}')
st.write(tr("question", lang))
st.info(lesson["situation"][lang])

lesson_id = lesson["id"]

answer = st.radio(
    tr("question", lang),
    lesson["choices"],
    index=None,
    key=f"choice_{lesson_id}",
    label_visibility="collapsed",
    disabled=lesson_id in st.session_state.results
)

if lesson_id not in st.session_state.results:
    if st.button(
        tr("check", lang),
        type="primary",
        disabled=answer is None
    ):
        selected_index = lesson["choices"].index(answer)
        st.session_state.results[lesson_id] = (
            selected_index == lesson["answer"]
        )
        st.rerun()

# ==========================================
# 採点結果
# ==========================================
if lesson_id in st.session_state.results:
    if st.session_state.results[lesson_id]:
        st.success(tr("correct", lang))
    else:
        st.error(tr("wrong", lang))

    correct_answer = lesson["choices"][lesson["answer"]]
    st.write("**Answer:**", correct_answer)
    st.write(
        f'**{tr("explanation", lang)}:** '
        f'{lesson["explain"][lang]}'
    )

st.divider()
st.caption(
    "Nihongo Practice | JLPT × Practical Japanese"
)
st.caption(
    "JLPTレベルを参考にした独自教材です。公式試験問題ではありません。"
)
