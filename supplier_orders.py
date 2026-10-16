
"""Manage supplier orders using an in-memory SQLite database."""

import sqlite3


def create_connection():
    """Create the database connection and orders table."""
    connection = sqlite3.connect(":memory:")
    connection.execute(
        "CREATE TABLE orders ("
        "id INTEGER PRIMARY KEY, supplier TEXT, item TEXT, "
        "quantity INTEGER, received INTEGER)"
    )
    return connection


def place_order(connection, supplier, item, quantity):
    """Place an order and return its quantity."""
    connection.execute(
        "INSERT INTO orders (supplier, item, quantity, received) "
        "VALUES (?, ?, ?, 0)",
        (supplier, item, quantity),
    )
    return quantity


def mark_received(connection, order_id):
    """Mark an order as received."""
    connection.execute(
        "UPDATE orders SET received = 1 WHERE id = ?",
        (order_id,),
    )


def notify_warehouse(supplier):
    """Print a warehouse notification."""
    print(f"notifying warehouse about {supplier}")


def cleanup(connection):
    """Delete received orders."""
    connection.execute("DELETE FROM orders WHERE received = 1")


def pending_count(connection):
    """Return the number of orders that are still pending."""
    return connection.execute(
        "SELECT COUNT(*) FROM orders WHERE received = 0"
    ).fetchone()[0]


def main():
    """Run the supplier-order example."""
    connection = create_connection()
    order_total = 0

    order_total += place_order(connection, "Acme Steel", "rods", 40)
    order_total += place_order(connection, "Bolt Co", "bolts", 500)

    mark_received(connection, 1)
    notify_warehouse("Acme")
    print(pending_count(connection), order_total)
    cleanup(connection)
    connection.close()


if __name__ == "__main__":
    main()
