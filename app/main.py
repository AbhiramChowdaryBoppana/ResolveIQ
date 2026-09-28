import streamlit as st

from database import (
    init_database,
    get_all_customers,
    get_customer,
    search_customers,
    create_customer,
    create_ticket,
    get_all_tickets,
    get_customer_tickets,
    update_ticket_status,
    get_ticket_events,
    get_dashboard_stats,
)

from agent import (
    resolve_customer_issue,
    record_customer_outcome,
    remember_escalation,
    recall_customer_history,
    list_memories,
)


# ============================================================
# PAGE
# ============================================================

st.set_page_config(
    page_title="ResolveIQ",
    page_icon="R",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# PREMIUM CSS
# ============================================================

st.markdown(
    """
<style>

@import url(
'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap'
);

html,
body,
[class*="css"] {
    font-family: "Inter", sans-serif;
}

.stApp {
    background: #090a0d;
    color: #f2f3f5;
}

.block-container {
    max-width: 1380px;
    padding-top: 2.5rem;
    padding-bottom: 4rem;
}

header[data-testid="stHeader"] {
    background: transparent;
}

#MainMenu,
footer {
    visibility: hidden;
}


/* SIDEBAR */

section[data-testid="stSidebar"] {
    background: #0d0f13;
    border-right: 1px solid #20232a;
}

section[data-testid="stSidebar"] button {
    background: transparent;
    border: 1px solid #24272e;
    border-radius: 8px;
    color: #b4b7be;
    min-height: 39px;
    font-size: 12px;
}

section[data-testid="stSidebar"] button:hover {
    background: #181a20;
    border-color: #42464f;
    color: white;
}


/* HEADINGS */

h1 {
    font-weight: 700 !important;
    letter-spacing: -0.045em !important;
}

h2,
h3 {
    font-weight: 600 !important;
    letter-spacing: -0.025em !important;
}


/* BUTTONS */

.stButton > button {
    background: #14161b;
    border: 1px solid #2b2e35;
    border-radius: 8px;
    color: #d8dae0;
    min-height: 40px;
    font-weight: 500;
}

.stButton > button:hover {
    background: #1b1e24;
    border-color: #4a4e57;
    color: white;
}

.stButton > button[kind="primary"] {
    background: #f1f2f4;
    color: #090a0d;
    border-color: #f1f2f4;
}


/* INPUTS */

.stTextInput input,
.stTextArea textarea,
.stSelectbox div[data-baseweb="select"] > div {
    background: #14161b !important;
    border: 1px solid #292c33 !important;
    color: #eeeeef !important;
    border-radius: 8px !important;
}

.stTextInput input:focus,
.stTextArea textarea:focus {
    border-color: #555a64 !important;
    box-shadow: none !important;
}


/* CONTAINERS */

div[data-testid="stVerticalBlockBorderWrapper"] {
    background: #101216;
    border: 1px solid #252830;
    border-radius: 10px;
}


/* METRICS */

[data-testid="stMetric"] {
    background: #101216;
    border: 1px solid #252830;
    border-radius: 10px;
    padding: 17px;
}

[data-testid="stMetricLabel"] {
    color: #70747d !important;
}

[data-testid="stMetricValue"] {
    color: #f1f2f4 !important;
}


/* CAPTION */

.stCaption {
    color: #70747d !important;
}


/* ALERTS */

div[data-testid="stAlert"] {
    border-radius: 8px;
}


/* DIVIDER */

hr {
    border-color: #24272e !important;
}

</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# DATABASE
# ============================================================

init_database()


# ============================================================
# SESSION STATE
# ============================================================

defaults = {
    "page": "Dashboard",
    "selected_customer_id": None,
    "selected_ticket_id": None,
    "last_resolution": None,
    "last_ticket_id": None,
    "last_customer_id": None,
    "outcome_recorded": False,
    "show_add_customer": False,
}

for key, value in defaults.items():

    if key not in st.session_state:
        st.session_state[key] = value


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        "### ResolveIQ"
    )

    st.caption(
        "Customer support with memory."
    )

    st.success(
        "● Hindsight connected"
    )

    st.caption(
        "MEMORY BANK"
    )

    st.code(
        "resolveiq-v2",
        language=None,
    )

    st.divider()

    st.caption(
        "WORKSPACE"
    )

    navigation = [
        ("Dashboard", "Overview"),
        ("Customers", "Customers"),
        ("Tickets", "Tickets"),
        ("Support Desk", "Support Desk"),
        ("Memory Explorer", "Memory"),
        ("Escalations", "Escalations"),
    ]

    for page, label in navigation:

        if st.button(
            label,
            key=f"nav_{page}",
            use_container_width=True,
            type=(
                "primary"
                if st.session_state.page == page
                else "secondary"
            ),
        ):

            st.session_state.page = page
            st.rerun()


# ============================================================
# DASHBOARD
# ============================================================

if st.session_state.page == "Dashboard":

    st.caption(
        "WORKSPACE OVERVIEW"
    )

    st.title(
        "Dashboard"
    )

    st.caption(
        "Customer activity, support workload, and memory."
    )

    stats = get_dashboard_stats()

    cols = st.columns(5)

    metrics = [
        ("Customers", stats["customers"]),
        ("Tickets", stats["tickets"]),
        ("Open", stats["open_tickets"]),
        ("Escalated", stats["escalated"]),
        ("Resolved", stats["resolved"]),
    ]

    for col, (label, value) in zip(
        cols,
        metrics,
    ):

        with col:

            st.metric(
                label,
                value,
            )

    st.markdown(
        "<br>",
        unsafe_allow_html=True,
    )

    left, right = st.columns(
        [1.4, 1]
    )

    with left:

        st.caption(
            "RECENT ACTIVITY"
        )

        tickets = get_all_tickets()

        if not tickets:

            st.info(
                "No ticket activity yet."
            )

        else:

            for ticket in tickets[:6]:

                with st.container(
                    border=True
                ):

                    c1, c2, c3 = st.columns(
                        [1.1, 4.5, 1.4]
                    )

                    with c1:

                        st.markdown(
                            f"**{ticket['ticket_code']}**"
                        )

                    with c2:

                        st.write(
                            f"{ticket['customer_name']} · "
                            f"{ticket['issue']}"
                        )

                    with c3:

                        if ticket["status"] == "Escalated":

                            st.error(
                                "ESCALATED"
                            )

                        elif ticket["status"] == "Resolved":

                            st.success(
                                "RESOLVED"
                            )

                        elif ticket["status"] == "In Progress":

                            st.warning(
                                "IN PROGRESS"
                            )

                        else:

                            st.info(
                                "OPEN"
                            )

    with right:

        st.caption(
            "HOW MEMORY WORKS"
        )

        with st.container(
            border=True
        ):

            st.markdown(
                "**01  Recall**"
            )

            st.caption(
                "Relevant customer history is retrieved before responding."
            )

            st.divider()

            st.markdown(
                "**02  Respond**"
            )

            st.caption(
                "Previous outcomes influence the next support action."
            )

            st.divider()

            st.markdown(
                "**03  Learn**"
            )

            st.caption(
                "Confirmed worked or failed outcomes become long-term memory."
            )


# ============================================================
# CUSTOMERS
# ============================================================

elif st.session_state.page == "Customers":

    c1, c2 = st.columns(
        [5, 1]
    )

    with c1:

        st.caption(
            "CUSTOMER DIRECTORY"
        )

        st.title(
            "Customers"
        )

        st.caption(
            "Manage customer profiles and support history."
        )

    with c2:

        st.write("")

        if st.button(
            "+ Add customer",
            type="primary",
            use_container_width=True,
        ):

            st.session_state.show_add_customer = True

    if st.session_state.show_add_customer:

        with st.container(
            border=True
        ):

            st.subheader(
                "New customer"
            )

            with st.form(
                "new_customer_form"
            ):

                a, b = st.columns(2)

                with a:

                    name = st.text_input(
                        "Full name *",
                        placeholder="Vishal Reddy",
                    )

                with b:

                    email = st.text_input(
                        "Email *",
                        placeholder="vishal@example.com",
                    )

                phone = st.text_input(
                    "Phone",
                    placeholder="+91 9876543210",
                )

                x, y = st.columns(2)

                with x:

                    create = st.form_submit_button(
                        "Create customer",
                        type="primary",
                        use_container_width=True,
                    )

                with y:

                    cancel = st.form_submit_button(
                        "Cancel",
                        use_container_width=True,
                    )

                if cancel:

                    st.session_state.show_add_customer = False
                    st.rerun()

                if create:

                    try:

                        customer = create_customer(
                            name,
                            email,
                            phone,
                        )

                        st.session_state.show_add_customer = False

                        st.success(
                            f"Customer {customer['id']} created successfully."
                        )

                        st.rerun()

                    except Exception as exc:

                        st.error(
                            str(exc)
                        )

    search = st.text_input(
        "Search customers",
        placeholder="Search name, email, phone, or customer ID",
    )

    if search.strip():

        customers = search_customers(
            search
        )

    else:

        customers = get_all_customers()

    st.caption(
        f"{len(customers)} customer(s)"
    )

    for customer in customers:

        with st.container(
            border=True
        ):

            a, b, c, d = st.columns(
                [1.2, 2.3, 3.5, 1]
            )

            with a:

                st.markdown(
                    f"**{customer['id']}**"
                )

            with b:

                st.write(
                    customer["name"]
                )

            with c:

                st.caption(
                    customer["email"]
                )

            with d:

                if st.button(
                    "Open",
                    key=f"open_customer_{customer['id']}",
                    use_container_width=True,
                ):

                    st.session_state.selected_customer_id = customer["id"]
                    st.session_state.page = "Customer Profile"
                    st.rerun()


# ============================================================
# CUSTOMER PROFILE
# ============================================================

elif st.session_state.page == "Customer Profile":

    customer = get_customer(
        st.session_state.selected_customer_id
    )

    if not customer:

        st.error(
            "Customer not found."
        )

    else:

        st.caption(
            "CUSTOMER PROFILE"
        )

        st.title(
            customer["name"]
        )

        if st.button(
            "← Back to customers"
        ):

            st.session_state.page = "Customers"
            st.rerun()

        a, b, c = st.columns(3)

        with a:

            st.metric(
                "Customer ID",
                customer["id"],
            )

        with b:

            st.metric(
                "Email",
                customer["email"],
            )

        with c:

            st.metric(
                "Phone",
                customer["phone"] or "Not provided",
            )

        st.divider()

        left, right = st.columns(
            [1.3, 1]
        )

        with left:

            st.caption(
                "TICKET HISTORY"
            )

            tickets = get_customer_tickets(
                customer["id"]
            )

            if not tickets:

                st.info(
                    "No tickets yet."
                )

            else:

                for ticket in tickets:

                    with st.container(
                        border=True
                    ):

                        st.markdown(
                            f"**{ticket['ticket_code']}**"
                        )

                        st.write(
                            ticket["issue"]
                        )

                        if ticket["status"] == "Escalated":

                            st.error(
                                "Escalated"
                            )

                        elif ticket["status"] == "Resolved":

                            st.success(
                                "Resolved"
                            )

                        else:

                            st.warning(
                                ticket["status"]
                            )

        with right:

            st.caption(
                "CUSTOMER MEMORY"
            )

            try:

                memories = recall_customer_history(
                    customer["name"],
                    "previous customer support history",
                )

                if not memories:

                    st.info(
                        "No relevant Hindsight memories found."
                    )

                else:

                    for memory in memories:

                        if isinstance(
                            memory,
                            dict,
                        ):

                            text = (
                                memory.get("text")
                                or memory.get("content")
                                or memory.get("memory")
                                or ""
                            )

                        else:

                            text = str(memory)

                        if text:

                            with st.container(
                                border=True
                            ):

                                st.write(
                                    text
                                )

            except Exception as exc:

                st.warning(
                    f"Could not load customer memory: {exc}"
                )


# ============================================================
# TICKETS
# ============================================================

elif st.session_state.page == "Tickets":

    st.caption(
        "SUPPORT OPERATIONS"
    )

    st.title(
        "Tickets"
    )

    st.caption(
        "Track active, resolved, and escalated support cases."
    )

    tickets = get_all_tickets()

    if not tickets:

        st.info(
            "No tickets yet."
        )

    else:

        for ticket in tickets:

            with st.container(
                border=True
            ):

                a, b, c = st.columns(
                    [1.2, 4.4, 1.5]
                )

                with a:

                    st.markdown(
                        f"**{ticket['ticket_code']}**"
                    )

                with b:

                    st.markdown(
                        f"**{ticket['customer_name']}**"
                    )

                    st.caption(
                        ticket["issue"]
                    )

                with c:

                    if ticket["status"] == "Escalated":

                        st.error(
                            "ESCALATED"
                        )

                    elif ticket["status"] == "Resolved":

                        st.success(
                            "RESOLVED"
                        )

                    elif ticket["status"] == "In Progress":

                        st.warning(
                            "IN PROGRESS"
                        )

                    else:

                        st.info(
                            "OPEN"
                        )

                selected = (
                    st.session_state.selected_ticket_id
                    == ticket["id"]
                )

                if selected:

                    st.divider()

                    st.caption(
                        "TICKET ACTIVITY"
                    )

                    events = get_ticket_events(
                        ticket["id"]
                    )

                    for event in events:

                        with st.container(
                            border=True
                        ):

                            st.markdown(
                                f"**{event['message']}**"
                            )

                            st.caption(
                                event["created_at"]
                            )

                if st.button(
                    "Hide details"
                    if selected
                    else "View details",
                    key=f"ticket_{ticket['id']}",
                ):

                    if selected:

                        st.session_state.selected_ticket_id = None

                    else:

                        st.session_state.selected_ticket_id = ticket["id"]

                    st.rerun()


# ============================================================
# SUPPORT DESK
# ============================================================

elif st.session_state.page == "Support Desk":

    st.caption(
        "CUSTOMER SUPPORT"
    )

    st.title(
        "Support Desk"
    )

    st.caption(
        "Resolve the current issue using customer-specific Hindsight memory."
    )

    customers = get_all_customers()

    customer_map = {
        f"{customer['name']} · {customer['email']} · {customer['id']}":
        customer
        for customer in customers
    }

    selected_customer = st.selectbox(
        "Customer",
        list(customer_map.keys()),
    )

    customer = customer_map[
        selected_customer
    ]

    with st.container(
        border=True
    ):

        st.markdown(
            f"**{customer['name']}**"
        )

        st.caption(
            f"{customer['email']} · {customer['id']}"
        )

    issue = st.text_area(
        "Customer issue",
        placeholder=(
            "Example: My Wi-Fi keeps disconnecting every 10 minutes."
        ),
        height=130,
    )

    if st.button(
        "Resolve with Hindsight",
        type="primary",
        use_container_width=True,
    ):

        if not issue.strip():

            st.error(
                "Please enter the customer's issue."
            )

        else:

            with st.spinner(
                "Recalling customer history..."
            ):

                try:

                    result = resolve_customer_issue(
                        customer["name"],
                        issue,
                    )

                    ticket = create_ticket(
                        customer["id"],
                        issue,
                        "In Progress",
                    )

                    st.session_state.last_resolution = result
                    st.session_state.last_ticket_id = ticket["id"]
                    st.session_state.last_customer_id = customer["id"]
                    st.session_state.outcome_recorded = False

                    st.rerun()

                except Exception as exc:

                    st.error(
                        f"Could not resolve issue: {exc}"
                    )

    result = st.session_state.last_resolution

    if result:

        st.divider()

        st.caption(
            "WHAT RESOLVEIQ REMEMBERED"
        )

        memory = result.get(
            "memory",
            "",
        )

        if memory:

            with st.container(
                border=True
            ):

                st.write(
                    memory
                )

        else:

            st.info(
                "No previous relevant memory was found."
            )

        st.caption(
            "AI SUPPORT RESPONSE"
        )

        with st.container(
            border=True
        ):

            st.write(
                result.get(
                    "message",
                    "",
                )
            )

        action = result.get(
            "recommended_action",
            "",
        )

        reason = result.get(
            "reason",
            "",
        )

        if action:

            st.caption(
                "RECOMMENDED ACTION"
            )

            with st.container(
                border=True
            ):

                st.markdown(
                    f"**{action}**"
                )

                if reason:

                    st.caption(
                        f"Why: {reason}"
                    )

        st.divider()

        st.caption(
            "WHAT HAPPENED AFTER THE RECOMMENDATION?"
        )

        a, b, c = st.columns(3)

        ticket_id = st.session_state.last_ticket_id

        with a:

            if st.button(
                "✕ Action failed",
                use_container_width=True,
                disabled=st.session_state.outcome_recorded,
            ):

                try:

                    record_customer_outcome(
                        customer["name"],
                        issue,
                        action or "No action",
                        "failed",
                    )

                    update_ticket_status(
                        ticket_id,
                        "In Progress",
                        f"Recommended action failed: {action}",
                    )

                    st.session_state.outcome_recorded = True

                    st.success(
                        "Failure saved to Hindsight."
                    )

                    st.rerun()

                except Exception as exc:

                    st.error(
                        str(exc)
                    )

        with b:

            if st.button(
                "✓ Action worked",
                use_container_width=True,
                disabled=st.session_state.outcome_recorded,
            ):

                try:

                    record_customer_outcome(
                        customer["name"],
                        issue,
                        action or "No action",
                        "worked",
                    )

                    update_ticket_status(
                        ticket_id,
                        "Resolved",
                        f"Recommended action worked: {action}",
                    )

                    st.session_state.outcome_recorded = True

                    st.success(
                        "Successful outcome saved to Hindsight."
                    )

                    st.rerun()

                except Exception as exc:

                    st.error(
                        str(exc)
                    )

        with c:

            if st.button(
                "Not tried yet",
                use_container_width=True,
                disabled=st.session_state.outcome_recorded,
            ):

                update_ticket_status(
                    ticket_id,
                    "In Progress",
                    "Customer has not tried the recommended action yet.",
                )

                st.session_state.outcome_recorded = True

                st.rerun()

        st.divider()

        if st.button(
            "Escalate to human support",
            use_container_width=True,
        ):

            try:

                remember_escalation(
                    customer["name"],
                    issue,
                    result.get(
                        "message",
                        "",
                    ),
                )

                update_ticket_status(
                    ticket_id,
                    "Escalated",
                    "Ticket escalated to human support.",
                )

                st.session_state.page = "Escalations"

                st.rerun()

            except Exception as exc:

                st.error(
                    f"Could not escalate ticket: {exc}"
                )


# ============================================================
# MEMORY
# ============================================================

elif st.session_state.page == "Memory Explorer":

    st.caption(
        "HINDSIGHT"
    )

    st.title(
        "Memory"
    )

    st.caption(
        "Long-term support knowledge stored by ResolveIQ."
    )

    query = st.text_input(
        "Search memory",
        placeholder="Wi-Fi, failed, worked, customer name...",
    )

    try:

        memories = list_memories(
            query
        )

        st.caption(
            f"{len(memories)} memory item(s)"
        )

        if not memories:

            st.info(
                "No memories found."
            )

        else:

            for index, memory in enumerate(
                memories,
                start=1,
            ):

                with st.container(
                    border=True
                ):

                    st.caption(
                        f"MEMORY {index}"
                    )

                    if isinstance(
                        memory,
                        dict,
                    ):

                        text = (
                            memory.get("text")
                            or memory.get("content")
                            or memory.get("memory")
                            or ""
                        )

                        st.write(
                            text
                        )

                        if memory.get("fact_type"):

                            st.caption(
                                f"Type: {memory['fact_type']}"
                            )

                        if memory.get("date"):

                            st.caption(
                                f"Date: {memory['date']}"
                            )

                    else:

                        st.write(
                            str(memory)
                        )

    except Exception as exc:

        st.error(
            f"Could not load Hindsight memories: {exc}"
        )


# ============================================================
# ESCALATIONS
# ============================================================

elif st.session_state.page == "Escalations":

    tickets = get_all_tickets()

    escalated = [
        ticket
        for ticket in tickets
        if ticket["status"] == "Escalated"
    ]

    a, b = st.columns(
        [5, 1]
    )

    with a:

        st.caption(
            "HUMAN SUPPORT QUEUE"
        )

        st.title(
            "Escalations"
        )

        st.caption(
            "Cases that require human intervention."
        )

    with b:

        st.metric(
            "Active",
            len(escalated),
        )

    st.divider()

    if not escalated:

        st.success(
            "No active escalations."
        )

    else:

        for ticket in escalated:

            with st.container(
                border=True
            ):

                st.markdown(
                    f"## {ticket['ticket_code']}"
                )

                st.markdown(
                    f"**{ticket['customer_name']}**"
                )

                st.caption(
                    ticket["customer_email"]
                )

                st.error(
                    "ESCALATED · HUMAN REVIEW REQUIRED"
                )

                st.divider()

                left, right = st.columns(
                    [1.6, 1]
                )

                with left:

                    st.caption(
                        "ISSUE"
                    )

                    st.markdown(
                        f"### {ticket['issue']}"
                    )

                    st.caption(
                        "ESCALATION REASON"
                    )

                    st.info(
                        "ResolveIQ could not confidently resolve "
                        "the issue using the available support history. "
                        "Human review is required."
                    )

                    st.caption(
                        "RECOMMENDED NEXT STEP"
                    )

                    with st.container(
                        border=True
                    ):

                        st.write(
                            "Review the customer's previous "
                            "troubleshooting attempts before "
                            "suggesting another solution."
                        )

                with right:

                    st.caption(
                        "CASE DETAILS"
                    )

                    st.markdown(
                        f"**Ticket**  \n"
                        f"{ticket['ticket_code']}"
                    )

                    st.markdown(
                        f"**Customer**  \n"
                        f"{ticket['customer_name']}"
                    )

                    st.markdown(
                        "**Status**  \n"
                        "Waiting for human review"
                    )

                    st.markdown(
                        f"**Opened**  \n"
                        f"{ticket['created_at']}"
                    )

                    st.markdown(
                        f"**Updated**  \n"
                        f"{ticket['updated_at']}"
                    )

                st.divider()

                st.caption(
                    "ACTIVITY"
                )

                events = get_ticket_events(
                    ticket["id"]
                )

                if events:

                    for event in events[-5:]:

                        with st.container(
                            border=True
                        ):

                            st.markdown(
                                f"**{event['message']}**"
                            )

                            st.caption(
                                event["created_at"]
                            )

                else:

                    st.caption(
                        "No activity recorded."
                    )

                a, b, c = st.columns(
                    [1.3, 1.3, 3]
                )

                with a:

                    if st.button(
                        "Open ticket",
                        key=f"open_escalation_{ticket['id']}",
                        use_container_width=True,
                    ):

                        st.session_state.selected_ticket_id = ticket["id"]
                        st.session_state.page = "Tickets"
                        st.rerun()

                with b:

                    if st.button(
                        "Resolve",
                        key=f"resolve_escalation_{ticket['id']}",
                        use_container_width=True,
                    ):

                        update_ticket_status(
                            ticket["id"],
                            "Resolved",
                            "Escalation resolved by human support.",
                        )

                        st.rerun()