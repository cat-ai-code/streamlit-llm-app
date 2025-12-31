import streamlit as st
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

load_dotenv()

def ask_llm(user_text: str, expert_type: str) -> str:
    # A/Bで専門家の振る舞いを変える（システムメッセージ）
    if expert_type == "A":
        system_prompt = "あなたはキャリアコーチです。状況整理→具体的な次の一歩を優しく提案してください。"
    else:
        system_prompt = "あなたはシニアAIエンジニアです。実装手順や注意点を具体例つきで簡潔に答えてください。"

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.7,
    )

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_text),
    ]

    result = llm.invoke(messages)
    return result.content

import streamlit as st

st.set_page_config(page_title="Streamlit LLM App", page_icon="🤖")

st.title("🤖 Streamlit LLM App")

# ① 概要・操作方法（課題条件）
st.write(
    """
### このアプリについて
入力したテキストを、選択した「専門家タイプ」に合わせてLLMに渡し、回答を表示します。

### 使い方
1. 専門家タイプ（A / B）を選ぶ  
2. 入力欄に質問を書く  
3. 「送信」を押す  
"""
)

# ② ラジオボタン（課題条件）
expert_type = st.radio(
    "専門家タイプを選んでね",
    options=["A", "B"],
    horizontal=True
)

# ③ 入力フォーム1つ（課題条件）
user_text = st.text_input("入力テキスト", value="")

# ④ 送信ボタンと表示枠（まだ仮）
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