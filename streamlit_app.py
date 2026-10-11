"""YNGW Japan Ready Passport — mobile-first, session-only demo.

No real student records, access control, or persistent storage.
Do not use for actual applicant records without a secure backend.
"""

from copy import deepcopy
from datetime import datetime, timezone
from html import escape

import streamlit as st

st.set_page_config(
    page_title="YNGW Japan Ready Passport",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
<style>
:root { --navy:#122B3A; --teal:#167D77; --ink:#193044; }
.stApp { background: #F6F8FA; }
.block-container { max-width: 1050px; padding-top: 1.2rem; padding-bottom: 4rem; }
[data-testid="stHeader"] { background: transparent; }
h1, h2, h3, p, label { color: var(--ink); }
.hero {
  padding: 27px 28px; border-radius: 20px;
  background: linear-gradient(125deg, #133044 0%, #167D77 100%);
  color: #fff; margin: 4px 0 22px;
}
.hero small { color:#D6F3EA; letter-spacing: 1.5px; font-weight: 650; }
.hero h1 { color:white; font-size: clamp(1.65rem, 4vw, 2.35rem); margin: 8px 0; }
.hero p { color:#E6F5F1; margin:0; font-size: .97rem; }
.section-title { font-size:1.15rem; font-weight:750; margin: 1rem 0 .6rem; }
.study-card {background:white; border:1px solid #E0E8EA; border-radius:16px;
  padding:19px 20px; margin:11px 0; box-shadow: 0 2px 10px #102D3909;}
.study-card .jp {font-size:1.25rem; font-weight:700; color:#1B3440; margin:8px 0 3px;}
.study-card .muted {color:#617482; font-size:.93rem;}
.eyebrow {color:#167D77; font-weight:750; font-size:.78rem; letter-spacing:.06em;}
.status {display:inline-block; padding:5px 11px; border-radius:100px;
  font-weight:700; font-size:.85rem; background:#E8F2F0; color:#136960; margin-right:6px;}
.notice {background:#EFF6F9;border:1px solid #DCE8F1;border-radius:12px;
  padding:12px 15px; color:#355064; font-size:.9rem;}
[data-testid="stMetric"] {background:white; border-radius:14px;
  padding:14px 16px; border:1px solid #E3E9ED;}
.stButton > button[kind="primary"] {background:#167D77;border-color:#167D77;}
.stButton > button {border-radius:11px; min-height:42px;}
[data-testid="stForm"] {background:white; padding:14px; border:1px solid #E3E9ED; border-radius:15px;}
@media (max-width: 640px) {
  .block-container { padding-left: .8rem; padding-right: .8rem; padding-top:.7rem; }
  .hero { padding:20px 18px; border-radius:16px; }
  .hero h1 { font-size: 1.8rem; }
  .study-card { padding:15px 14px; }
  .study-card .jp { font-size:1.16rem; }
}
</style>
""",
    unsafe_allow_html=True,
)

TRANSLATIONS = {
    "ja": {
        "intro": "留学前の準備を、見える化。",
        "subtitle": "日本語の基礎・実践会話・学校生活を確認する留学準備パスポート",
        "demo": "試作版：サンプル生徒5名／記録はこの画面内のみ。実際の個人情報は入力しないでください。",
        "learner": "生徒用", "admin": "学校管理（デモ）", "view": "画面を選択",
        "student": "生徒を選択", "track": "留学コース", "short": "短期留学", "long": "長期留学",
        "readiness": "Japan Ready Score", "basic": "基礎日本語", "speaking": "実践会話", "school": "学校生活",
        "admission": "受入審査", "departure": "渡日前修了", "pending": "審査中", "approved": "受入承認", "rejected": "受入不可",
        "passed": "修了", "waiting": "未修了", "study": "会話を学ぶ", "tests": "ミニ試験", "proof": "外部学習の記録",
        "score_note": "100点満点：基礎40点＋教員による会話評価40点＋学校生活20点。試験はデモ用です。",
        "test_basic": "基礎日本語テスト（4問・40点）", "test_school": "学校生活テスト（2問・20点）",
        "submit": "採点して記録する", "result": "今回の得点", "speak_note": "会話40点は選択式クイズでは判定せず、先生の面談後に入力します。",
        "evidence_title": "外部学習の修了・受講記録", "evidence_short": "短期：指定レッスンの学習記録", "evidence_long": "長期：指定コースの修了証",
        "upload": "証明画像またはPDFを選ぶ", "send": "提出を記録（デモ）", "upload_note": "デモではファイル本体を保存しません。ファイル名だけをこの画面内に記録します。",
        "evidence_none": "未提出", "evidence_submitted": "提出済み・学校確認待ち", "evidence_verified": "学校確認済み",
        "overview": "学習者一覧", "detail": "生徒別の評価・審査", "basic_edit": "基礎テスト結果", "school_edit": "学校生活テスト結果",
        "speaking_edit": "先生による会話面談の評価（0〜40点）", "proof_verify": "外部学習記録を確認済みにする",
        "decision": "受入審査の学校判断", "memo": "学校側メモ（デモ）", "save": "評価を保存",
        "finalize": "渡日前学習の修了を学校が承認", "undo": "修了承認を取り消す",
        "admit_target": "受入審査の参考点", "depart_target": "渡日前修了の目安点", "speaking_target": "必要な会話点",
        "criteria": "合格基準（変更可・デモ限定）", "threshold_warning": "合計点だけで受入は決まりません。受入は学校の承認が必要です。",
        "admission_ready": "審査参考基準", "departure_ready": "渡日前の要件", "met": "達成", "not_met": "未達成",
        "confirmed": "学校による修了承認済み", "not_confirmed": "学校の最終確認待ち",
        "reset": "デモデータを初期化", "retake": "再受験できます。最新の得点で更新されます。",
        "time": "最終更新", "no_results": "未実施", "student_no": "生徒番号",
    },
    "en": {
        "intro": "Get ready for Japan with confidence.",
        "subtitle": "A pre-arrival passport for Japanese, speaking and school-life readiness",
        "demo": "Demo: 5 sample students. Data only lasts in this session. Do not enter real personal data.",
        "learner": "Student view", "admin": "School admin (demo)", "view": "Select view",
        "student": "Choose student", "track": "Program", "short": "Short-term", "long": "Long-term",
        "readiness": "Japan Ready Score", "basic": "Basic Japanese", "speaking": "Speaking", "school": "School life",
        "admission": "Admissions", "departure": "Pre-departure", "pending": "Under review", "approved": "Approved", "rejected": "Not approved",
        "passed": "Completed", "waiting": "Not completed", "study": "Practice", "tests": "Mini tests", "proof": "External learning evidence",
        "score_note": "Out of 100: basic Japanese 40 + teacher-scored speaking 40 + school life 20. Tests are for demonstration.",
        "test_basic": "Basic Japanese (4 questions, 40 pts)", "test_school": "School life (2 questions, 20 pts)",
        "submit": "Mark and save", "result": "Latest score", "speak_note": "Speaking (40 pts) is assessed by a teacher, not automatically by multiple-choice questions.",
        "evidence_title": "External course completion evidence", "evidence_short": "Short-term: assigned lessons", "evidence_long": "Long-term: assigned course certificate",
        "upload": "Choose proof (PDF / image)", "send": "Record submission (demo)", "upload_note": "Demo only: file content is NOT saved. Only the filename is recorded in this session.",
        "evidence_none": "Not submitted", "evidence_submitted": "Submitted, awaiting verification", "evidence_verified": "Verified by school",
        "overview": "Student overview", "detail": "Student assessment", "basic_edit": "Basic test score", "school_edit": "School-life test score",
        "speaking_edit": "Teacher speaking assessment (0–40 pts)", "proof_verify": "Verify external learning record",
        "decision": "School admissions decision", "memo": "Teacher notes (demo)", "save": "Save assessment",
        "finalize": "Approve pre-departure completion", "undo": "Revoke final approval",
        "admit_target": "Admission reference", "depart_target": "Pre-departure benchmark", "speaking_target": "Speaking minimum",
        "criteria": "Benchmarks (editable demo)", "threshold_warning": "A test score does not automatically grant admission. School approval is required.",
        "admission_ready": "Admission benchmark", "departure_ready": "Departure requirements", "met": "Met", "not_met": "Not met",
        "confirmed": "Pre-departure approved by school", "not_confirmed": "Awaiting final school approval",
        "reset": "Reset demo data", "retake": "Retakes allowed. Latest scores replace previous scores.",
        "time": "Last updated", "no_results": "Not taken", "student_no": "Student ID",
    },
    "th": {
        "intro": "เตรียมความพร้อมก่อนเดินทางไปญี่ปุ่น",
        "subtitle": "พาสปอร์ตประเมินภาษาญี่ปุ่น การสนทนา และชีวิตในโรงเรียน",
        "demo": "เวอร์ชันทดลอง: นักเรียนตัวอย่าง 5 คน ข้อมูลอยู่เฉพาะหน้านี้ ห้ามใส่ข้อมูลจริง",
        "learner": "สำหรับนักเรียน", "admin": "สำหรับโรงเรียน (ทดลอง)", "view": "เลือกหน้าจอ",
        "student": "เลือกนักเรียน", "track": "หลักสูตร", "short": "ระยะสั้น", "long": "ระยะยาว",
        "readiness": "Japan Ready Score", "basic": "ภาษาญี่ปุ่นพื้นฐาน", "speaking": "การสนทนา", "school": "ชีวิตในโรงเรียน",
        "admission": "การพิจารณารับเข้า", "departure": "ก่อนเดินทาง", "pending": "กำลังพิจารณา", "approved": "อนุมัติ", "rejected": "ไม่อนุมัติ",
        "passed": "สำเร็จแล้ว", "waiting": "ยังไม่สำเร็จ", "study": "ฝึกบทสนทนา", "tests": "แบบทดสอบ", "proof": "หลักฐานการเรียนภายนอก",
        "score_note": "รวม 100 คะแนน: ภาษาพื้นฐาน 40 + ครูประเมินการสนทนา 40 + ชีวิตในโรงเรียน 20 (ข้อสอบทดลอง)",
        "test_basic": "ภาษาญี่ปุ่นพื้นฐาน (4 ข้อ / 40 คะแนน)", "test_school": "ชีวิตในโรงเรียน (2 ข้อ / 20 คะแนน)",
        "submit": "ตรวจและบันทึก", "result": "คะแนนล่าสุด", "speak_note": "คะแนนสนทนา 40 คะแนนประเมินโดยครูหลังสัมภาษณ์ ไม่ใช่ข้อสอบตัวเลือก",
        "evidence_title": "หลักฐานการเรียนจากหลักสูตรภายนอก", "evidence_short": "ระยะสั้น: บันทึกบทเรียนที่กำหนด", "evidence_long": "ระยะยาว: ใบรับรองหลักสูตรที่กำหนด",
        "upload": "เลือกไฟล์ PDF หรือรูปภาพ", "send": "บันทึกการส่ง (ทดลอง)", "upload_note": "เวอร์ชันทดลองไม่เก็บเนื้อหาไฟล์ เก็บเฉพาะชื่อไฟล์ชั่วคราว",
        "evidence_none": "ยังไม่ส่ง", "evidence_submitted": "ส่งแล้ว รอโรงเรียนตรวจ", "evidence_verified": "โรงเรียนตรวจแล้ว",
        "overview": "รายชื่อนักเรียน", "detail": "ประเมินรายบุคคล", "basic_edit": "คะแนนภาษาพื้นฐาน", "school_edit": "คะแนนชีวิตในโรงเรียน",
        "speaking_edit": "คะแนนสนทนาจากครู (0–40)", "proof_verify": "ตรวจสอบหลักฐานการเรียนแล้ว",
        "decision": "ผลการพิจารณาของโรงเรียน", "memo": "บันทึกของครู (ทดลอง)", "save": "บันทึกผล",
        "finalize": "รับรองการเตรียมพร้อมก่อนเดินทาง", "undo": "ยกเลิกการรับรอง",
        "admit_target": "เกณฑ์อ้างอิงรับเข้า", "depart_target": "เกณฑ์ก่อนเดินทาง", "speaking_target": "คะแนนสนทนาขั้นต่ำ",
        "criteria": "เกณฑ์คะแนน (ปรับได้เฉพาะเดโม)", "threshold_warning": "คะแนนสอบไม่ได้หมายถึงได้รับอนุมัติให้เข้าเรียน โรงเรียนต้องเป็นผู้อนุมัติ",
        "admission_ready": "เกณฑ์อ้างอิงรับเข้า", "departure_ready": "เงื่อนไขก่อนเดินทาง", "met": "ผ่าน", "not_met": "ไม่ผ่าน",
        "confirmed": "โรงเรียนรับรองแล้ว", "not_confirmed": "รอโรงเรียนรับรองขั้นสุดท้าย",
        "reset": "เริ่มข้อมูลทดลองใหม่", "retake": "สอบใหม่ได้ คะแนนล่าสุดจะแทนที่คะแนนก่อนหน้า",
        "time": "อัปเดตล่าสุด", "no_results": "ยังไม่สอบ", "student_no": "รหัสนักเรียน",
    },
}


def t(key):
    return TRANSLATIONS[st.session_state.lang][key]


def seed_students():
    return {
        "S001": {"name": "Student A", "track": "short", "basic": 20, "school": 10, "speaking": 20,
                 "evidence": "", "verified": False, "admission": "pending", "final": False, "note": "", "updated": "—"},
        "S002": {"name": "Student B", "track": "long", "basic": 40, "school": 20, "speaking": 32,
                 "evidence": "course-certificate-demo.pdf", "verified": True, "admission": "approved", "final": True, "note": "", "updated": "—"},
        "S003": {"name": "Student C", "track": "short", "basic": 40, "school": 20, "speaking": 30,
                 "evidence": "learning-record-demo.png", "verified": True, "admission": "approved", "final": False, "note": "", "updated": "—"},
        "S004": {"name": "Student D", "track": "long", "basic": 20, "school": 10, "speaking": 16,
                 "evidence": "", "verified": False, "admission": "pending", "final": False, "note": "", "updated": "—"},
        "S005": {"name": "Student E", "track": "short", "basic": 30, "school": 10, "speaking": 20,
                 "evidence": "", "verified": False, "admission": "pending", "final": False, "note": "", "updated": "—"},
    }


def seed_criteria():
    return {
        "short": {"admission": 60, "departure": 70, "admission_speak": 20, "departure_speak": 24},
        "long": {"admission": 70, "departure": 85, "admission_speak": 28, "departure_speak": 32},
    }


def init_state():
    if "students" not in st.session_state:
        st.session_state.students = seed_students()
    if "criteria" not in st.session_state:
        st.session_state.criteria = seed_criteria()
    if "lang" not in st.session_state:
        st.session_state.lang = "ja"
    if "attempts" not in st.session_state:
        st.session_state.attempts = []


def total(student):
    return student["basic"] + student["speaking"] + student["school"]


def flags(student):
    crit = st.session_state.criteria[student["track"]]
    admission_benchmark = (total(student) >= crit["admission"]
                           and student["speaking"] >= crit["admission_speak"])
    departure_requirements = (
        student["admission"] == "approved"
        and total(student) >= crit["departure"]
        and student["speaking"] >= crit["departure_speak"]
        and student["verified"]
        and bool(student["evidence"])
    )
    return admission_benchmark, departure_requirements


def mark_updated(student):
    student["updated"] = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


def metric_row(student):
    c1, c2, c3, c4 = st.columns(4)
    c1.metric(t("readiness"), f"{total(student)}/100")
    c2.metric(t("basic"), f"{student['basic']}/40")
    c3.metric(t("speaking"), f"{student['speaking']}/40")
    c4.metric(t("school"), f"{student['school']}/20")
    st.progress(min(total(student), 100) / 100)
    st.caption(t("score_note"))


def states(student):
    admission_benchmark, departure_requirements = flags(student)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"**{t('admission')}**")
        if student["admission"] == "approved":
            st.success(t("approved"))
        elif student["admission"] == "rejected":
            st.error(t("rejected"))
        else:
            st.info(t("pending"))
        st.caption(f"{t('admission_ready')}: {t('met') if admission_benchmark else t('not_met')}")
    with c2:
        st.markdown(f"**{t('departure')}**")
        if student["final"] and departure_requirements:
            st.success(t("confirmed"))
        else:
            st.info(t("not_confirmed"))
        st.caption(f"{t('departure_ready')}: {t('met') if departure_requirements else t('not_met')}")


SCENES = [
    {
        "title": {"ja": "01｜先生にあいさつ", "en": "01 | Greeting your teacher", "th": "01 | ทักทายคุณครู"},
        "lines": [
            ("先生", "おはようございます。", "Good morning.", "สวัสดีตอนเช้า"),
            ("生徒", "おはようございます。よろしくお願いします。", "Good morning. Nice to meet you.", "สวัสดีตอนเช้า ฝากเนื้อฝากตัวด้วยค่ะ/ครับ"),
        ],
    },
    {
        "title": {"ja": "02｜授業が分からない", "en": "02 | Asking for help", "th": "02 | ขอให้ครูอธิบายอีกครั้ง"},
        "lines": [
            ("生徒", "先生、もう一度お願いします。", "Could you say that again, please?", "คุณครู ช่วยพูดอีกครั้งได้ไหม"),
            ("先生", "はい。ゆっくり話しますね。", "Sure. I'll speak slowly.", "ได้เลย ครูจะพูดช้า ๆ นะ"),
        ],
    },
    {
        "title": {"ja": "03｜体調を伝える", "en": "03 | Explaining illness", "th": "03 | บอกว่าไม่สบาย"},
        "lines": [
            ("生徒", "すみません。頭が痛いです。", "Excuse me, I have a headache.", "ขอโทษค่ะ/ครับ ปวดหัว"),
            ("先生", "分かりました。保健室に行きましょう。", "Let's go to the nurse's office.", "เข้าใจแล้ว ไปห้องพยาบาลกันเถอะ"),
        ],
    },
]

BASIC_QUESTIONS = [
    {"prompt": {"ja": "朝、先生に会いました。何と言いますか？", "en": "You meet a teacher in the morning. What do you say?", "th": "พบคุณครูตอนเช้า ควรพูดอย่างไร"},
     "choices": ["こんばんは。", "おはようございます。", "おやすみなさい。"], "answer": 1},
    {"prompt": {"ja": "「わたし ___ 学生です。」に入る言葉は？", "en": "Complete: わたし ___ 学生です。", "th": "เติมคำในประโยค わたし ___ 学生です。"},
     "choices": ["は", "を", "に"], "answer": 0},
    {"prompt": {"ja": "水を注文したいときは？", "en": "How do you ask for water?", "th": "ต้องการขอน้ำ ควรพูดว่าอะไร"},
     "choices": ["水はどこですか。", "水をください。", "水がありません。"], "answer": 1},
    {"prompt": {"ja": "「学校」はどれですか？", "en": "Which word means school?", "th": "คำใดหมายถึงโรงเรียน"},
     "choices": ["がっこう", "ぎんこう", "くうこう"], "answer": 0},
]

SCHOOL_QUESTIONS = [
    {"prompt": {"ja": "先生の説明が分からないときは？", "en": "You didn't understand your teacher. What do you say?", "th": "ไม่เข้าใจที่คุณครูพูด ควรพูดอย่างไร"},
     "choices": ["もう一度お願いします。", "いくらですか。", "おやすみなさい。"], "answer": 0},
    {"prompt": {"ja": "学校の廊下ではどうしますか？", "en": "What should you do in a school hallway?", "th": "ควรปฏิบัติตัวอย่างไรในทางเดินโรงเรียน"},
     "choices": ["走ります。", "大きな声で歌います。", "歩きます。"], "answer": 2},
]


def render_quiz(sid, student, kind, questions, max_score):
    title = t("test_basic") if kind == "basic" else t("test_school")
    st.subheader(title)
    st.caption(t("retake"))
    with st.form(f"quiz_{sid}_{kind}"):
        answers = []
        for i, q in enumerate(questions):
            answers.append(st.radio(
                f"{i+1}. {q['prompt'][st.session_state.lang]}",
                q["choices"], index=None, key=f"q_{sid}_{kind}_{i}"
            ))
        submitted = st.form_submit_button(t("submit"), type="primary", use_container_width=True)
    if submitted:
        if any(answer is None for answer in answers):
            st.warning("全問回答してください / Please answer every question / กรุณาตอบทุกข้อ")
        else:
            correct = sum(q["choices"].index(a) == q["answer"] for q, a in zip(questions, answers))
            student[kind] = int(correct * max_score / len(questions))
            mark_updated(student)
            st.session_state.attempts.append({"student": sid, "exam": kind, "score": student[kind], "at": student["updated"]})
            # A changed score can invalidate an earlier sign-off.
            if not flags(student)[1]:
                student["final"] = False
            st.success(f"{t('result')}: {student[kind]} / {max_score}")
    st.caption(f"{t('result')}: {student[kind]} / {max_score}")


def learner_view():
    students = st.session_state.students
    sid = st.selectbox(t("student"), list(students.keys()),
                       format_func=lambda s: f"{s} · {students[s]['name']}")
    student = students[sid]
    st.markdown(f"**{t('student_no')}: {sid}**　｜　{t('track')}: {t(student['track'])}")
    metric_row(student)
    states(student)
    st.divider()
    tab1, tab2, tab3 = st.tabs([t("study"), t("tests"), t("proof")])
    with tab1:
        for scene in SCENES:
            title = escape(scene["title"][st.session_state.lang])
            html = f'<div class="study-card"><div class="eyebrow">{title}</div>'
            for speaker, jp, en, th in scene["lines"]:
                detail = "" if st.session_state.lang == "ja" else (en if st.session_state.lang == "en" else th)
                html += (f'<div class="jp">{escape(jp)}</div>'
                         f'<div class="muted">{escape(speaker)} · {escape(detail)}</div><br>')
            html += '</div>'
            st.markdown(html, unsafe_allow_html=True)
    with tab2:
        render_quiz(sid, student, "basic", BASIC_QUESTIONS, 40)
        st.divider()
        render_quiz(sid, student, "school", SCHOOL_QUESTIONS, 20)
        st.info(t("speak_note"))
    with tab3:
        st.subheader(t("evidence_title"))
        st.write(t("evidence_short") if student["track"] == "short" else t("evidence_long"))
        if student["verified"]:
            st.success(t("evidence_verified"))
        elif student["evidence"]:
            st.info(t("evidence_submitted"))
        else:
            st.warning(t("evidence_none"))
        if student["evidence"]:
            st.caption(escape(student["evidence"]))
        f = st.file_uploader(t("upload"), type=["pdf", "png", "jpg", "jpeg"],
                             key=f"evidence_{sid}")
        st.caption(t("upload_note"))
        if st.button(t("send"), disabled=f is None, type="primary"):
            student["evidence"] = f.name[:150]
            student["verified"] = False
            student["final"] = False
            mark_updated(student)
            st.rerun()


def admin_view():
    students = st.session_state.students
    rows = []
    for sid, s in students.items():
        admission_benchmark, departure_requirements = flags(s)
        rows.append({
            "ID": sid, "Name": s["name"], "Program": t(s["track"]),
            "Ready /100": total(s), "Admissions": t(s["admission"]),
            "Departure": t("passed") if s["final"] and departure_requirements else t("waiting"),
            "Evidence": "✓" if s["verified"] else "—",
        })
    st.subheader(t("overview"))
    a, b, c = st.columns(3)
    a.metric("Students", len(students))
    b.metric(t("short"), sum(s["track"] == "short" for s in students.values()))
    c.metric(t("long"), sum(s["track"] == "long" for s in students.values()))
    st.dataframe(rows, hide_index=True, use_container_width=True)
    st.divider()
    st.subheader(t("detail"))
    sid = st.selectbox(t("student"), list(students.keys()),
                       format_func=lambda s: f"{s} · {students[s]['name']}", key="admin_selected")
    student = students[sid]
    metric_row(student)
    states(student)
    with st.form(f"assess_{sid}"):
        c1, c2 = st.columns(2)
        with c1:
            st.number_input(t("basic_edit"), min_value=0, max_value=40, step=10,
                            value=student["basic"], key=f"base_admin_{sid}", disabled=True)
            speech = st.slider(t("speaking_edit"), min_value=0, max_value=40,
                               value=student["speaking"], step=1, key=f"speech_{sid}")
            st.number_input(t("school_edit"), min_value=0, max_value=20, step=10,
                            value=student["school"], key=f"school_admin_{sid}", disabled=True)
        with c2:
            verified = st.checkbox(t("proof_verify"), value=student["verified"],
                                   disabled=not bool(student["evidence"]), key=f"verify_{sid}")
            admissions = st.selectbox(t("decision"), ["pending", "approved", "rejected"],
                                      index=["pending", "approved", "rejected"].index(student["admission"]),
                                      format_func=t, key=f"admit_{sid}")
            note = st.text_area(t("memo"), value=student["note"], key=f"note_{sid}")
        save = st.form_submit_button(t("save"), type="primary", use_container_width=True)
    if save:
        student["speaking"] = speech
        student["verified"] = bool(verified) if student["evidence"] else False
        student["admission"] = admissions
        student["note"] = note[:1000]
        mark_updated(student)
        if not flags(student)[1]:
            student["final"] = False
        st.rerun()

    st.caption(t("time") + ": " + student["updated"])
    st.info(t("threshold_warning"))
    if flags(student)[1]:
        if not student["final"]:
            if st.button(t("finalize"), type="primary"):
                student["final"] = True
                mark_updated(student)
                st.rerun()
        else:
            if st.button(t("undo")):
                student["final"] = False
                mark_updated(student)
                st.rerun()
    else:
        st.caption(t("not_confirmed"))

    with st.expander(t("criteria")):
        track = st.radio(t("track"), ["short", "long"], horizontal=True,
                         format_func=t, key="criteria_track")
        crit = st.session_state.criteria[track]
        with st.form(f"criteria_{track}"):
            admit_total = st.number_input(t("admit_target"), 0, 100, value=crit["admission"])
            admit_speak = st.number_input(t("speaking_target") + " (" + t("admission") + ")", 0, 40,
                                          value=crit["admission_speak"])
            depart_total = st.number_input(t("depart_target"), 0, 100, value=crit["departure"])
            depart_speak = st.number_input(t("speaking_target") + " (" + t("departure") + ")", 0, 40,
                                           value=crit["departure_speak"])
            change = st.form_submit_button(t("save"))
        if change:
            crit.update({"admission": admit_total, "admission_speak": admit_speak,
                         "departure": depart_total, "departure_speak": depart_speak})
            for s in students.values():
                if not flags(s)[1]:
                    s["final"] = False
            st.rerun()
    if st.button(t("reset")):
        st.session_state.students = seed_students()
        st.session_state.criteria = seed_criteria()
        st.session_state.attempts = []
        st.rerun()


init_state()
with st.sidebar:
    st.markdown("### YNGW Japan Ready Passport")
    lang_names = {"日本語": "ja", "English": "en", "ภาษาไทย": "th"}
    choice = st.selectbox("Language / 言語 / ภาษา", list(lang_names),
                          index=list(lang_names.values()).index(st.session_state.lang))
    st.session_state.lang = lang_names[choice]
    st.caption("N5 · Mobile-first · Prototype")

st.markdown(
    '<div class="hero"><small>YANAGAWA · JAPAN READY PASSPORT</small>'
    f'<h1>{escape(t("intro"))}</h1><p>{escape(t("subtitle"))}</p></div>',
    unsafe_allow_html=True,
)
st.warning(t("demo"), icon="🧪")
page = st.radio(t("view"), ["learner", "admin"], format_func=t,
                horizontal=True, label_visibility="collapsed")
if page == "learner":
    learner_view()
else:
    admin_view()

st.divider()
st.caption("YNGW Japan Ready Passport · Independent demo, not official JLPT certification")
