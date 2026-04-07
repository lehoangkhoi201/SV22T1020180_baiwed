"""
Chat demo: xAI Grok + Google Gemini (OpenAI-compatible + Gemini SDK).
Run:  cd scripts/chat_gemini_groq
      pip install -r requirements.txt
      set XAI_API_KEY=...        (Grok — https://console.x.ai )
      set GEMINI_API_KEY=...     (Google AI Studio)
      streamlit run app.py
"""

from __future__ import annotations

import os
from pathlib import Path

import streamlit as st

_ENV_DIR = Path(__file__).resolve().parent
_ENV_FILE = _ENV_DIR / ".env"

try:
    from dotenv import load_dotenv

    # override=True: giá trị trong .env luôn thắng biến môi trường cũ (tránh key sai sau khi đổi .env).
    load_dotenv(_ENV_FILE, override=True)
except ImportError:
    pass

XAI_BASE = "https://api.x.ai/v1"


def _grok_models():
    """Chat / text — theo https://docs.x.ai/docs/models (Mar 2026). Không gồm imagine (ảnh/video)."""
    return [
        "grok-4-1-fast-non-reasoning",
        "grok-4-1-fast-reasoning",
        "grok-4.20-0309-non-reasoning",
        "grok-4.20-0309-reasoning",
        "grok-4.20-multi-agent-0309",
    ]


def _gemini_models():
    """Theo https://ai.google.dev/gemini-api/docs/models — 2.5 stable; 3.x preview (Mar 2026)."""
    return [
        "gemini-2.5-flash",
        "gemini-2.5-flash-lite",
        "gemini-2.5-pro",
        "gemini-3-flash-preview",
        "gemini-3.1-pro-preview",
        "gemini-3.1-flash-lite-preview",
    ]


def call_grok(api_key: str, model: str, messages: list[dict]) -> str:
    from openai import OpenAI

    client = OpenAI(api_key=api_key, base_url=XAI_BASE)
    completion = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.6,
        max_tokens=2048,
    )
    return completion.choices[0].message.content or ""


def call_gemini(api_key: str, model: str, messages: list[dict]) -> str:
    """messages: role in ('user', 'model') — model = phía Gemini."""
    import google.generativeai as genai

    genai.configure(api_key=api_key)
    gm = genai.GenerativeModel(model)
    if len(messages) == 1:
        r = gm.generate_content(messages[0]["content"])
        return (r.text or "").strip()

    history = []
    for m in messages[:-1]:
        role = m["role"]
        if role not in ("user", "model"):
            role = "model"
        history.append({"role": role, "parts": [m["content"]]})
    chat = gm.start_chat(history=history)
    r = chat.send_message(messages[-1]["content"])
    return (r.text or "").strip()


def main():
    st.set_page_config(page_title="Chat Grok + Gemini", layout="wide")
    st.title("Chat thử — Grok (xAI) & Gemini")

    xai_key = os.environ.get("XAI_API_KEY", "").strip()
    gemini_key = os.environ.get("GEMINI_API_KEY", "").strip()

    if not _ENV_FILE.is_file():
        st.error(
            "Chưa có file **`.env`** trong thư mục `scripts/chat_gemini_groq/`. "
            "App chỉ đọc **`.env`**, không đọc `.env.example`. "
            "Chạy: `Copy-Item .env.example .env` rồi mở `.env` và điền key."
        )

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Grok (xAI)")
        grok_model = st.selectbox("Model Grok", _grok_models(), key="grok_m")
        if not xai_key:
            st.warning("Thiếu `XAI_API_KEY` (trong `.env` hoặc biến môi trường hệ thống).")
    with col2:
        st.subheader("Gemini")
        gemini_model = st.selectbox("Model Gemini", _gemini_models(), key="gem_m")
        if not gemini_key:
            st.warning("Thiếu `GEMINI_API_KEY` (trong `.env` hoặc biến môi trường hệ thống).")

    # Một kênh + một chat_input — tránh xung đột khi đặt chat_input trong từng tab.
    channel = st.radio(
        "Kênh chat",
        ["Grok (xAI)", "Gemini"],
        horizontal=True,
        key="chat_channel",
    )

    if "msgs_grok" not in st.session_state:
        st.session_state.msgs_grok = []
    if "msgs_gem" not in st.session_state:
        st.session_state.msgs_gem = []
    if "err_grok" not in st.session_state:
        st.session_state.err_grok = ""
    if "err_gem" not in st.session_state:
        st.session_state.err_gem = ""

    st.markdown("##### Hội thoại")
    err_key = "err_grok" if channel == "Grok (xAI)" else "err_gem"
    chat_box = st.container(height=420, border=True)
    with chat_box:
        if channel == "Grok (xAI)":
            msgs = st.session_state.msgs_grok
            if not msgs:
                st.caption("Chưa có tin nhắn — gõ nội dung ở ô bên dưới và gửi.")
            for m in msgs:
                with st.chat_message(m["role"]):
                    st.markdown(m["content"])
        else:
            msgs = st.session_state.msgs_gem
            if not msgs:
                st.caption("Chưa có tin nhắn — gõ nội dung ở ô bên dưới và gửi.")
            for m in msgs:
                with st.chat_message(m["role"]):
                    st.markdown(m["content"])

    if err_key in st.session_state and st.session_state[err_key]:
        st.error(st.session_state[err_key])
        if st.button("Đóng thông báo lỗi", key=f"dismiss_{err_key}"):
            st.session_state[err_key] = ""
            st.rerun()

    prompt = st.chat_input(
        "Nhập tin nhắn…",
        key="chat_input_main",
    )

    if prompt:
        if channel == "Grok (xAI)":
            if not xai_key:
                st.session_state.err_grok = "Thiếu `XAI_API_KEY` trong `.env`."
                st.rerun()
            else:
                st.session_state.msgs_grok.append({"role": "user", "content": prompt})
                st.session_state.err_grok = ""
                try:
                    with st.spinner("Đang gọi Grok…"):
                        api_msgs = [
                            {"role": x["role"], "content": x["content"]}
                            for x in st.session_state.msgs_grok
                        ]
                        out = call_grok(xai_key, grok_model, api_msgs)
                    st.session_state.msgs_grok.append(
                        {"role": "assistant", "content": out}
                    )
                    st.rerun()
                except Exception as e:
                    st.session_state.msgs_grok.pop()
                    st.session_state.err_grok = f"Grok: {e}"
                    st.rerun()
        else:
            if not gemini_key:
                st.session_state.err_gem = "Thiếu `GEMINI_API_KEY` trong `.env`."
                st.rerun()
            else:
                st.session_state.msgs_gem.append({"role": "user", "content": prompt})
                st.session_state.err_gem = ""
                try:
                    with st.spinner("Đang gọi Gemini…"):
                        norm = []
                        for x in st.session_state.msgs_gem:
                            r = x["role"]
                            if r == "assistant":
                                r = "model"
                            norm.append({"role": r, "content": x["content"]})
                        out = call_gemini(gemini_key, gemini_model, norm)
                    st.session_state.msgs_gem.append(
                        {"role": "assistant", "content": out}
                    )
                    st.rerun()
                except Exception as e:
                    st.session_state.msgs_gem.pop()
                    st.session_state.err_gem = f"Gemini: {e}"
                    st.rerun()

    with st.sidebar:
        st.markdown("### Kiểm tra API")
        st.code(
            'curl -sS "' + XAI_BASE + '/models" \\\n'
            '  -H "Authorization: Bearer %XAI_API_KEY%"',
            language="bash",
        )
        st.code(
            'curl -sS "https://generativelanguage.googleapis.com/v1beta/models?key=%GEMINI_API_KEY%"',
            language="bash",
        )
        if st.button("Xóa lịch sử Grok"):
            st.session_state.msgs_grok = []
            st.session_state.err_grok = ""
            st.rerun()
        if st.button("Xóa lịch sử Gemini"):
            st.session_state.msgs_gem = []
            st.session_state.err_gem = ""
            st.rerun()


if __name__ == "__main__":
    main()
