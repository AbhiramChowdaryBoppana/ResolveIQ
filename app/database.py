import sqlite3
from pathlib import Path
from datetime import datetime


BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "resolveiq.db"


DEMO_CUSTOMERS = [
    ("Arjun Kumar", "arjun@example.com", "+91 9000000001"),
    ("Rahul Reddy", "rahul@example.com", "+91 9000000002"),
    ("Venkatesh", "venkatesh@example.com", "+91 9000000003"),
    ("Karunya", "karunya@example.com", "+91 9000000004"),
    ("Priya Sharma", "priya@example.com", "+91 9000000005"),
    ("Karthik Rao", "karthik@example.com", "+91 9000000006"),
    ("Sneha Reddy", "sneha@example.com", "+91 9000000007"),
    ("Aditya Verma", "aditya@example.com", "+91 9000000008"),
    ("Nikhil Kumar", "nikhil@example.com", "+91 9000000009"),
    ("Ananya Rao", "ananya@example.com", "+91 9000000010"),
]


# ============================================================
# DATABASE CONNECTION
# ============================================================

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


# ============================================================
# DATABASE INITIALIZATION
# ============================================================

def init_database():

    conn = get_connection()
    cur = conn.cursor()

    # --------------------------------------------------------
    # CUSTOMERS
    # --------------------------------------------------------

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS customers (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            phone TEXT,
            created_at TEXT NOT NULL
        )
        """
    )

    # --------------------------------------------------------
    # TICKETS
    # --------------------------------------------------------

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticket_code TEXT NOT NULL UNIQUE,
            customer_id TEXT NOT NULL,
            issue TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Open',
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            FOREIGN KEY(customer_id)
                REFERENCES customers(id)
        )
        """
    )

    # --------------------------------------------------------
    # TICKET EVENTS
    #
    # New schema contains event_type.
    # --------------------------------------------------------

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS ticket_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticket_id INTEGER NOT NULL,
            event_type TEXT NOT NULL DEFAULT 'note',
            message TEXT NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY(ticket_id)
                REFERENCES tickets(id)
        )
        """
    )

    # --------------------------------------------------------
    # DATABASE MIGRATION
    #
    # Your existing database was created by an older version.
    # If event_type is missing, add it safely.
    # --------------------------------------------------------

    cur.execute(
        "PRAGMA table_info(ticket_events)"
    )

    columns = [
        row["name"]
        for row in cur.fetchall()
    ]

    if "event_type" not in columns:

        cur.execute(
            """
            ALTER TABLE ticket_events
            ADD COLUMN event_type TEXT
            NOT NULL DEFAULT 'note'
            """
        )

    conn.commit()

    # --------------------------------------------------------
    # DEMO CUSTOMERS
    # --------------------------------------------------------

    cur.execute(
        "SELECT COUNT(*) AS count FROM customers"
    )

    customer_count = cur.fetchone()["count"]

    if customer_count == 0:

        for index, customer in enumerate(
            DEMO_CUSTOMERS,
            start=1,
        ):

            customer_id = f"CUST-{index:03d}"

            cur.execute(
                """
                INSERT INTO customers
                (
                    id,
                    name,
                    email,
                    phone,
                    created_at
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    customer_id,
                    customer[0],
                    customer[1],
                    customer[2],
                    datetime.now().isoformat(),
                ),
            )

    conn.commit()
    conn.close()


# ============================================================
# HELPERS
# ============================================================

def _row_to_dict(row):

    if row is None:
        return None

    return dict(row)


# ============================================================
# CUSTOMERS
# ============================================================

def get_all_customers():

    conn = get_connection()

    rows = conn.execute(
        """
        SELECT *
        FROM customers
        ORDER BY name COLLATE NOCASE
        """
    ).fetchall()

    conn.close()

    return [
        _row_to_dict(row)
        for row in rows
    ]


def get_customer(customer_id):

    conn = get_connection()

    row = conn.execute(
        """
        SELECT *
        FROM customers
        WHERE id = ?
        """,
        (customer_id,),
    ).fetchone()

    conn.close()

    return _row_to_dict(row)


def search_customers(query):

    query = str(query).strip()

    if not query:
        return get_all_customers()

    pattern = f"%{query}%"

    conn = get_connection()

    rows = conn.execute(
        """
        SELECT *
        FROM customers
        WHERE
            name LIKE ?
            OR email LIKE ?
            OR phone LIKE ?
            OR id LIKE ?
        ORDER BY name COLLATE NOCASE
        """,
        (
            pattern,
            pattern,
            pattern,
            pattern,
        ),
    ).fetchall()

    conn.close()

    return [
        _row_to_dict(row)
        for row in rows
    ]


def create_customer(
    name,
    email,
    phone="",
):

    name = str(name).strip()
    email = str(email).strip().lower()
    phone = str(phone or "").strip()

    if not name:
        raise ValueError(
            "Customer name is required."
        )

    if not email:
        raise ValueError(
            "Customer email is required."
        )

    conn = get_connection()

    try:

        existing = conn.execute(
            """
            SELECT id
            FROM customers
            WHERE LOWER(email) = LOWER(?)
            """,
            (email,),
        ).fetchone()

        if existing:

            raise ValueError(
                f"A customer with email {email} already exists."
            )

        row = conn.execute(
            """
            SELECT id
            FROM customers
            ORDER BY
                CAST(
                    SUBSTR(id, 6)
                    AS INTEGER
                ) DESC
            LIMIT 1
            """
        ).fetchone()

        if row:

            try:
                last_number = int(
                    row["id"].split("-")[1]
                )
            except Exception:
                last_number = 0

        else:

            last_number = 0

        customer_id = (
            f"CUST-{last_number + 1:03d}"
        )

        created_at = datetime.now().isoformat()

        conn.execute(
            """
            INSERT INTO customers
            (
                id,
                name,
                email,
                phone,
                created_at
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                customer_id,
                name,
                email,
                phone,
                created_at,
            ),
        )

        conn.commit()

        return {
            "id": customer_id,
            "name": name,
            "email": email,
            "phone": phone,
            "created_at": created_at,
        }

    except sqlite3.IntegrityError as exc:

        conn.rollback()

        raise ValueError(
            f"Could not create customer: {exc}"
        )

    finally:

        conn.close()


# ============================================================
# TICKETS
# ============================================================

def create_ticket(
    customer_id,
    issue,
    status="Open",
):

    issue = str(issue).strip()

    if not issue:
        raise ValueError(
            "Issue is required."
        )

    conn = get_connection()

    try:

        # Find next safe ticket number.
        row = conn.execute(
            """
            SELECT
                MAX(
                    CAST(
                        SUBSTR(ticket_code, 5)
                        AS INTEGER
                    )
                ) AS max_number
            FROM tickets
            WHERE ticket_code LIKE 'RIQ-%'
            """
        ).fetchone()

        last_number = (
            row["max_number"]
            if row and row["max_number"]
            else 0
        )

        ticket_number = last_number + 1

        ticket_code = (
            f"RIQ-{ticket_number:04d}"
        )

        now = datetime.now().isoformat()

        cursor = conn.execute(
            """
            INSERT INTO tickets
            (
                ticket_code,
                customer_id,
                issue,
                status,
                created_at,
                updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                ticket_code,
                customer_id,
                issue,
                status,
                now,
                now,
            ),
        )

        ticket_id = cursor.lastrowid

        # IMPORTANT:
        # event_type is explicitly supplied.
        conn.execute(
            """
            INSERT INTO ticket_events
            (
                ticket_id,
                event_type,
                message,
                created_at
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                ticket_id,
                "created",
                f"Ticket created: {status}",
                now,
            ),
        )

        conn.commit()

        return {
            "id": ticket_id,
            "ticket_code": ticket_code,
            "customer_id": customer_id,
            "issue": issue,
            "status": status,
            "created_at": now,
            "updated_at": now,
        }

    except Exception:

        conn.rollback()
        raise

    finally:

        conn.close()


def get_all_tickets():

    conn = get_connection()

    rows = conn.execute(
        """
        SELECT
            t.*,
            c.name AS customer_name,
            c.email AS customer_email,
            c.phone AS customer_phone
        FROM tickets t
        JOIN customers c
            ON t.customer_id = c.id
        ORDER BY t.id DESC
        """
    ).fetchall()

    conn.close()

    return [
        _row_to_dict(row)
        for row in rows
    ]


def get_customer_tickets(
    customer_id,
):

    conn = get_connection()

    rows = conn.execute(
        """
        SELECT
            t.*,
            c.name AS customer_name,
            c.email AS customer_email
        FROM tickets t
        JOIN customers c
            ON t.customer_id = c.id
        WHERE t.customer_id = ?
        ORDER BY t.id DESC
        """,
        (customer_id,),
    ).fetchall()

    conn.close()

    return [
        _row_to_dict(row)
        for row in rows
    ]


def get_ticket(ticket_id):

    conn = get_connection()

    row = conn.execute(
        """
        SELECT
            t.*,
            c.name AS customer_name,
            c.email AS customer_email
        FROM tickets t
        JOIN customers c
            ON t.customer_id = c.id
        WHERE t.id = ?
        """,
        (ticket_id,),
    ).fetchone()

    conn.close()

    return _row_to_dict(row)


# ============================================================
# TICKET STATUS / EVENTS
# ============================================================

def update_ticket_status(
    ticket_id,
    status,
    event_message=None,
    event_type="status_change",
):

    conn = get_connection()

    try:

        now = datetime.now().isoformat()

        conn.execute(
            """
            UPDATE tickets
            SET
                status = ?,
                updated_at = ?
            WHERE id = ?
            """,
            (
                status,
                now,
                ticket_id,
            ),
        )

        if event_message:

            conn.execute(
                """
                INSERT INTO ticket_events
                (
                    ticket_id,
                    event_type,
                    message,
                    created_at
                )
                VALUES (?, ?, ?, ?)
                """,
                (
                    ticket_id,
                    event_type,
                    event_message,
                    now,
                ),
            )

        conn.commit()

    except Exception:

        conn.rollback()
        raise

    finally:

        conn.close()


def get_ticket_events(
    ticket_id,
):

    conn = get_connection()

    rows = conn.execute(
        """
        SELECT *
        FROM ticket_events
        WHERE ticket_id = ?
        ORDER BY id ASC
        """,
        (ticket_id,),
    ).fetchall()

    conn.close()

    return [
        _row_to_dict(row)
        for row in rows
    ]


# ============================================================
# DASHBOARD
# ============================================================

def get_dashboard_stats():

    conn = get_connection()

    customers = conn.execute(
        """
        SELECT COUNT(*) AS count
        FROM customers
        """
    ).fetchone()["count"]

    tickets = conn.execute(
        """
        SELECT COUNT(*) AS count
        FROM tickets
        """
    ).fetchone()["count"]

    open_tickets = conn.execute(
        """
        SELECT COUNT(*) AS count
        FROM tickets
        WHERE status IN (
            'Open',
            'In Progress'
        )
        """
    ).fetchone()["count"]

    escalated = conn.execute(
        """
        SELECT COUNT(*) AS count
        FROM tickets
        WHERE status = 'Escalated'
        """
    ).fetchone()["count"]

    resolved = conn.execute(
        """
        SELECT COUNT(*) AS count
        FROM tickets
        WHERE status = 'Resolved'
        """
    ).fetchone()["count"]

    conn.close()

    return {
        "customers": customers,
        "tickets": tickets,
        "open_tickets": open_tickets,
        "escalated": escalated,
        "resolved": resolved,
    }


# ============================================================
# DATABASE TEST
# ============================================================

if __name__ == "__main__":

    print(
        "Initializing ResolveIQ database..."
    )

    init_database()

    print()
    print(
        "ResolveIQ database ready."
    )

    print(
        f"Database: {DB_PATH}"
    )

    customers = get_all_customers()

    print(
        f"Customers: {len(customers)}"
    )

    print()

    for customer in customers:

        print(
            f"{customer['id']} - "
            f"{customer['name']} - "
            f"{customer['email']}"
        )

    print()

    # Show ticket_events schema
    conn = get_connection()

    columns = conn.execute(
        "PRAGMA table_info(ticket_events)"
    ).fetchall()

    conn.close()

    print(
        "ticket_events columns:"
    )

    for column in columns:

        print(
            f"  - {column['name']}"
        )