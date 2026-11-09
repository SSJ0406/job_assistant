"""Style CSS używane w interfejsie asystenta ofert pracy."""

# Wydzielenie CSS pozwala zmieniać wygląd bez ingerencji w przepływ rozmowy.

import streamlit as st


def apply_styles() -> None:
    """Dodaje dotychczasowe style aplikacji do bieżącej strony Streamlit."""
    # Streamlit potrzebuje allow_html, aby potraktować zawartość jako arkusz stylów.
    st.markdown(
        """
        <style>
        :root {
            color-scheme: light;
            --ink: #1d2540;
            --muted: #69738c;
            --accent: #a83e9b;
            --line: #ece7ef;
            --instagram-gradient: linear-gradient(
                110deg, #833ab4 0%, #c13584 38%, #e1306c 68%, #f77737 100%
            );
        }

        .stApp {
            color: var(--ink);
            background: #faf8fb;
        }

        [data-testid="stHeader"] {
            background: transparent;
        }

        .main .block-container {
            max-width: 900px;
            padding: 2.2rem 1.4rem 7rem;
        }

        .career-hero {
            position: relative;
            overflow: hidden;
            margin: 0 0 1.2rem;
            padding: 2rem 2.1rem 1.9rem;
            border: 1px solid rgba(98, 87, 217, 0.13);
            border-radius: 26px;
            background: #ffffff;
            box-shadow: 0 18px 48px rgba(67, 37, 70, 0.07);
        }

        .career-hero::before {
            position: absolute;
            top: 0;
            right: 0;
            left: 0;
            height: 5px;
            background: var(--instagram-gradient);
            content: "";
        }

        .career-eyebrow {
            display: flex;
            align-items: center;
            gap: 0.55rem;
            margin-bottom: 0.8rem;
            color: #9a3692;
            font-size: 0.72rem;
            font-weight: 750;
            letter-spacing: 0.13em;
            text-transform: uppercase;
        }

        .career-dot {
            width: 0.5rem;
            height: 0.5rem;
            border-radius: 50%;
            background: var(--instagram-gradient);
            box-shadow: 0 0 0 4px rgba(193, 53, 132, 0.12);
        }

        .career-title {
            max-width: 680px;
            margin: 0;
            color: var(--ink);
            font-size: clamp(2rem, 5vw, 3.15rem);
            font-weight: 750;
            letter-spacing: -0.045em;
            line-height: 1.06;
        }

        .career-copy {
            max-width: 620px;
            margin: 0.85rem 0 0;
            color: var(--muted);
            font-size: 1rem;
            line-height: 1.65;
        }

        .welcome-card {
            display: flex;
            align-items: flex-start;
            gap: 1rem;
            margin: 1.15rem 0 1.25rem;
            padding: 1.15rem 1.25rem;
            border: 1px solid var(--line);
            border-radius: 20px;
            background: rgba(255, 255, 255, 0.8);
            box-shadow: 0 10px 30px rgba(37, 43, 83, 0.045);
        }

        .welcome-icon {
            display: grid;
            flex: 0 0 2.5rem;
            width: 2.5rem;
            height: 2.5rem;
            place-items: center;
            border-radius: 13px;
            background: linear-gradient(145deg, #f9e9f2, #f1eafa);
            color: var(--accent);
            font-size: 1.2rem;
        }

        .welcome-title {
            margin: 0.05rem 0 0.25rem;
            color: var(--ink);
            font-size: 0.98rem;
            font-weight: 700;
        }

        .welcome-copy {
            margin: 0;
            color: var(--muted);
            font-size: 0.9rem;
            line-height: 1.55;
        }

        [data-testid="stAlert"] {
            border: 1px solid var(--line);
            border-radius: 16px;
            box-shadow: 0 7px 20px rgba(37, 43, 83, 0.035);
        }

        [data-testid="stChatMessage"] {
            margin-bottom: 0.8rem;
            padding: 0.8rem 1rem;
            border: 1px solid var(--line);
            border-radius: 19px;
            background: #ffffff;
            box-shadow: 0 8px 24px rgba(67, 37, 70, 0.045);
        }

        [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] p {
            line-height: 1.65;
        }

        [data-testid="stChatInput"] {
            border: 1px solid #dfe3ef;
            border-radius: 18px;
            background: #ffffff;
            box-shadow: 0 12px 32px rgba(37, 43, 83, 0.1);
        }

        [data-testid="stChatInput"] textarea {
            color: var(--ink);
            font-size: 0.98rem;
        }

        [data-testid="stChatInput"] button {
            border-radius: 12px;
            border: 0;
            background: var(--instagram-gradient);
        }

        @media (max-width: 640px) {
            .main .block-container {
                padding: 1.3rem 0.8rem 6.5rem;
            }

            .career-hero {
                padding: 1.5rem 1.25rem;
                border-radius: 21px;
            }

            .welcome-card {
                padding: 1rem;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
