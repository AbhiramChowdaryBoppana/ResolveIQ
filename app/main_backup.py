import streamlit as st
import requests
from pathlib import Path
from dotenv import dotenv_values

from agent import (
    BANK_ID,
    resolve_customer_issue,
    record_customer_outcome,
    remember_escalation
)


# ============================================================
# CONFIGURATION
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent
ENV_FILE = PROJECT_ROOT / ".env"

config = dotenv_values(str(ENV_FILE))

HINDSIGHT_API_KEY = config["HINDSIGHT_API_KEY"]

HINDSIGHT_BASE_URL = config.get(
    "HINDSIGHT_BASE_URL",
    "https://api.hindsight.vectorize.io"
)


# ============================================================
# PAGE
# ============================================================

st.set_page_config(
    page_title="ResolveIQ",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# SESSION STATE
# ============================================================

if "result" not in st.session_state:
    st.session_state.result = None

if "customer_name" not in st.session_state:
    st.session_state.customer_name = ""

if "customer_message" not in st.session_state:
    st.session_state.customer_message = ""

if "history" not in st.session_state:
    st.session_state.history = []

if "outcome_recorded" not in st.session_state:
    st.session_state.outcome_recorded = False


# ============================================================
# CSS
# ============================================================

st.markdown(
    """
    <style>

    /* Main background */
    .stApp {
        background: #0b0f14;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: #111720;
        border-right: 1px solid #202936;
    }

    /* Main title */
    .hero-title {
        font-size: 46px;
        font-weight: 800;
        letter-spacing: -1.5px;
        margin-bottom: 0px;
    }

    .hero-subtitle {
        color: #9ca8b8;
        font-size: 17px;
        margin-top: -5px;
        margin-bottom: 25px;
    }

    /* Status cards */
    .stat-card {
        background: #111720;
        border: 1px solid #202936;
        border-radius: 14px;
        padding: 18px;
        min-height: 105px;
    }

    .stat-label {
        color: #8995a5;
        font-size: 13px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .stat-value {
        font-size: 24px;
        font-weight: 700;
        margin-top: 6px;
    }

    /* Memory */
    .memory-card {
        background: #111720;
        border: 1px solid #293342;
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 12px;
    }

    .memory-label {
        font-size: 12px;
        color: #8995a5;
        text-transform: uppercase;
        letter-spacing: 0.8px;
    }

    /* Response */
    .response-card {
        background: #111720;
        border: 1px solid #293342;
        border-radius: 14px;
        padding: 22px;
    }

    /* Small text */
    .muted {
        color: #8995a5;
    }

    /* Hide default decoration */
    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        """
        <div style="
            font-size:28px;
            font-weight:800;
            margin-bottom:5px;
        ">
            🧠 ResolveIQ
        </div>

        <div style="
            color:#8995a5;
            margin-bottom:25px;
        ">
            Memory-powered support
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("### 👤 Customer")

    customer_name = st.text_input(
        "Customer name",
        value=st.session_state.customer_name
        or "Arjun Kumar"
    )

    st.session_state.customer_name = customer_name

    st.divider()

    st.markdown("### 🧠 Memory System")

    st.success("Hindsight Connected")

    st.caption(
        f"Bank: `{BANK_ID}`"
    )

    st.divider()

    st.markdown("### How it works")

    st.caption(
        """
        1. Recall previous history
        2. Understand the current issue
        3. Generate a response
        4. Confirm the outcome
        5. Store the experience
        6. Improve the next interaction
        """
    )


# ============================================================
# HEADER
# ============================================================

st.markdown(
    """
    <div class="hero-title">
        🧠 ResolveIQ
    </div>

    <div class="hero-subtitle">
        Support that remembers what already happened.
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# TABS
# ============================================================

support_tab, history_tab, memory_tab = st.tabs(
    [
        "💬 Support Desk",
        "📚 Customer History",
        "🔎 Memory Explorer"
    ]
)


# ============================================================
# SUPPORT DESK
# ============================================================

with support_tab:

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown(
            """
            <div class="stat-card">
                <div class="stat-label">Memory</div>
                <div class="stat-value">🧠 Active</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:

        st.markdown(
            """
            <div class="stat-card">
                <div class="stat-label">Reasoning</div>
                <div class="stat-value">⚡ Groq</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:

        st.markdown(
            """
            <div class="stat-card">
                <div class="stat-label">Mode</div>
                <div class="stat-value">Support</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("")

    st.subheader("Customer issue")

    customer_message = st.text_area(
        "What did the customer say?",
        value="",
        placeholder=(
            "Example: My Wi-Fi keeps disconnecting "
            "every 10 minutes."
        ),
        height=130
    )

    st.session_state.customer_message = customer_message

    resolve = st.button(
        "🚀 Resolve with Memory",
        type="primary",
        use_container_width=True
    )

    if resolve:

        if not customer_name.strip():

            st.error("Enter a customer name.")

            st.stop()

        if not customer_message.strip():

            st.error("Enter the customer's issue.")

            st.stop()

        with st.spinner(
            "🧠 Recalling customer history and reasoning..."
        ):

            try:

                result = resolve_customer_issue(
                    customer_name.strip(),
                    customer_message.strip()
                )

                st.session_state.result = result
                st.session_state.history = result["memories"]
                st.session_state.outcome_recorded = False

            except Exception as e:

                st.error(
                    f"ResolveIQ error: {e}"
                )

                st.stop()


    # ========================================================
    # RESULT
    # ========================================================

    if st.session_state.result:

        result = st.session_state.result

        memories = result["memories"]
        response = result["response"]


        # ----------------------------------------------------
        # MEMORY
        # ----------------------------------------------------

        st.markdown("---")

        st.subheader(
            "🧠 What ResolveIQ remembered"
        )

        if not memories:

            st.info(
                "No previous history found. "
                "This looks like a new customer issue."
            )

        else:

            for index, memory in enumerate(
                memories,
                start=1
            ):

                st.markdown(
                    f"""
                    <div class="memory-card">
                        <div class="memory-label">
                            MEMORY {index}
                        </div>
                        <br>
                        {memory}
                    </div>
                    """,
                    unsafe_allow_html=True
                )


        # ----------------------------------------------------
        # AI RESPONSE
        # ----------------------------------------------------

        st.subheader(
            "🤖 ResolveIQ response"
        )

        st.markdown(
            f"""
            <div class="response-card">
            """,
            unsafe_allow_html=True
        )

        st.markdown(response)

        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )


        # ----------------------------------------------------
        # OUTCOME
        # ----------------------------------------------------

        st.markdown("---")

        st.subheader(
            "📌 What happened after the recommendation?"
        )

        st.caption(
            "Only confirmed outcomes become long-term customer memory."
        )

        outcome_col1, outcome_col2, outcome_col3 = st.columns(3)

        with outcome_col1:

            if st.button(
                "❌ It failed",
                use_container_width=True
            ):

                record_customer_outcome(
                    customer_name,
                    customer_message,
                    response,
                    "The customer tried the recommended troubleshooting and it FAILED."
                )

                st.session_state.outcome_recorded = True

                st.error(
                    "Failure recorded in Hindsight."
                )

        with outcome_col2:

            if st.button(
                "✅ It worked",
                use_container_width=True
            ):

                record_customer_outcome(
                    customer_name,
                    customer_message,
                    response,
                    "The customer tried the recommended troubleshooting and it WORKED."
                )

                st.session_state.outcome_recorded = True

                st.success(
                    "Successful outcome recorded in Hindsight."
                )

        with outcome_col3:

            if st.button(
                "⏳ Not tried yet",
                use_container_width=True
            ):

                record_customer_outcome(
                    customer_name,
                    customer_message,
                    response,
                    "The customer has NOT tried the recommendation yet."
                )

                st.session_state.outcome_recorded = True

                st.info(
                    "Pending outcome recorded."
                )


        # ----------------------------------------------------
        # ESCALATION
        # ----------------------------------------------------

        st.markdown("")

        if st.button(
            "🚨 Escalate to Human Support",
            use_container_width=True
        ):

            remember_escalation(
                customer_name,
                customer_message,
                "Customer issue requires human investigation."
            )

            st.warning(
                "Escalation recorded. "
                "A human support specialist should follow up."
            )


# ============================================================
# CUSTOMER HISTORY
# ============================================================

with history_tab:

    st.subheader(
        f"📚 History for {customer_name}"
    )

    history_query = st.text_input(
        "Search this customer's memory",
        value=(
            f"What happened previously with "
            f"{customer_name}?"
        )
    )

    search_history = st.button(
        "🔎 Search History",
        use_container_width=True
    )

    if search_history:

        with st.spinner(
            "Searching Hindsight..."
        ):

            try:

                from agent import recall_customer_history

                memories = recall_customer_history(
                    customer_name,
                    history_query
                )

                if not memories:

                    st.info(
                        "No history found."
                    )

                else:

                    for i, memory in enumerate(
                        memories,
                        start=1
                    ):

                        with st.container(
                            border=True
                        ):

                            st.caption(
                                f"Memory {i}"
                            )

                            st.write(memory)

            except Exception as e:

                st.error(
                    f"History search failed: {e}"
                )


# ============================================================
# MEMORY EXPLORER
# ============================================================

with memory_tab:

    st.subheader(
        "🔎 Hindsight Memory Explorer"
    )

    st.caption(
        "View recently stored memory units in the ResolveIQ bank."
    )

    load_memories = st.button(
        "🔄 Load Memories",
        use_container_width=True
    )

    if load_memories:

        try:

            url = (
                f"{HINDSIGHT_BASE_URL}"
                f"/v1/default/banks/{BANK_ID}/memories/list"
            )

            headers = {
                "Authorization":
                    f"Bearer {HINDSIGHT_API_KEY}"
            }

            response = requests.get(
                url,
                headers=headers,
                timeout=30
            )

            response.raise_for_status()

            data = response.json()

            items = data.get(
                "items",
                data.get("memories", [])
            )

            if not items:

                st.info(
                    "No memory units found yet."
                )

            else:

                st.success(
                    f"{len(items)} memory units returned."
                )

                for item in items:

                    memory_text = item.get(
                        "text",
                        item.get(
                            "content",
                            "No text available"
                        )
                    )

                    memory_type = item.get(
                        "type",
                        "memory"
                    )

                    with st.container(
                        border=True
                    ):

                        st.caption(
                            f"TYPE: {memory_type}"
                        )

                        st.write(
                            memory_text
                        )

        except Exception as e:

            st.error(
                f"Could not load Hindsight memories: {e}"
            )