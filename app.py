import streamlit as st
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

load_dotenv()

# -----------------------------
# 専門家定義（A/B）
# -----------------------------
EXPERTS = {
    "A": {
        "label": "A：キャリアコーチ",
        "desc": "転職・学習計画・不安の整理が得意。状況整理→優先順位→次の一歩を提案します。",
        "system": (
            "あなたは経験豊富なキャリアコーチです。"
            "相談者の状況を丁寧に整理し、安心感のある言葉で、"
            "具体的な行動プラン（今日できる一歩）を提案してください。"
            "必要に応じて質問も1〜3個だけ返してください。"
        ),
    },
    "B": {
        "label": "B：AIエンジニア",
        "desc": "生成AI/LLM開発が得意。実装手順・落とし穴・デバッグの観点で回答します。",
        "system": (
            "あなたはシニアAIエンジニアです。"
            "回答は技術的に正確に、手順を箇条書きで示し、"
            "注意点（よくあるミス）と確認コマンド例も添えてください。"
            "不確かな場合は推測せず、前提条件を確認してください。"
        ),
    },
}


# -----------------------------
# LLM呼び出し関数（提出要件）
# -----------------------------
def ask_llm(user_text: str, expert_type: str) -> str:
    expert = EXPERTS.get(expert_type, EXPERTS["A"])

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.7,
    )

    messages = [
        SystemMessage(content=expert["system"]),
        HumanMessage(content=user_text),
    ]

    result = llm.invoke(messages)
    return result.content


# -----------------------------
# UI
# -----------------------------
st.set_page_config(page_title="Expert Switch LLM App", page_icon="🤖", layout="centered")

st.title("🤖 Expert Switch LLM App")
st.caption("専門家タイプを切り替えて、同じ質問でも観点の違う回答を得られるStreamlitアプリです。")

with st.expander("このアプリについて / 使い方", expanded=True):
    st.markdown(
        """
**できること**
- 入力した質問をLLMに渡し、回答を表示します。
- 「専門家タイプ」を切り替えることで、回答の視点・口調・出力形式が変わります。

**使い方**
1. 専門家タイプ（A/B）を選ぶ  
2. 入力欄に質問を入力する  
3. 「送信」を押す  
"""
    )

st.subheader("専門家タイプを選んでね")
expert_type = st.radio(
    label="",
    options=["A", "B"],
    format_func=lambda x: EXPERTS[x]["label"],
    horizontal=True,
)

st.info(f"**{EXPERTS[expert_type]['label']}**：{EXPERTS[expert_type]['desc']}")

user_text = st.text_area("入力テキスト", placeholder="例：Streamlit CloudでSecretsはどこに設定する？", height=100)
send = st.button("送信")

if send:
    if not user_text.strip():
        st.warning("入力テキストを入れてね。")
    else:
        with st.spinner("考え中..."):
            try:
                answer = ask_llm(user_text, expert_type)
                st.subheader("LLMの回答")
                st.write(answer)
            except Exception as e:
                st.error("LLM呼び出しでエラーが出たよ。APIキーやパッケージを確認してね。")
                st.exception(e)

st.divider()
st.caption("※ APIキーはGitHubに含めず、ローカルは .env / デプロイ先は Secrets で設定します。")