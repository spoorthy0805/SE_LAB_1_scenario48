
"""Library catalog management module."""

import ast
import hashlib
import operator
import secrets

catalog = {
    "B01": {"title": "Clean Code", "copies": 3},
    "B02": {"title": "The Pragmatic Programmer", "copies": 1},
    "B03": {"title": "Design Patterns", "copies": 2},
}


def issue_book(book_id, patron, active_issues=None):
    """Issue an available book to a patron."""
    if active_issues is None:
        active_issues = []

    if book_id not in catalog or catalog[book_id]["copies"] <= 0:
        return False

    catalog[book_id]["copies"] -= 1
    active_issues.append(f"Issued book {book_id} to patron {patron}")
    return True


def return_book(book_id):
    """Return a book to the catalog."""
    if book_id not in catalog:
        return False

    catalog[book_id]["copies"] += 1
    return True


def check_availability(book_id):
    """Check whether a book has available copies."""
    if book_id not in catalog:
        return False

    return catalog[book_id]["copies"] > 0


def calculate_fine(days_overdue, calc_expr):
    """Calculate a fine using a restricted arithmetic expression."""
    operations = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
    }

    def evaluate(node):
        """Evaluate supported arithmetic expression nodes."""
        if isinstance(node, ast.Expression):
            result = evaluate(node.body)
        elif isinstance(node, ast.Constant) and type(node.value) in (int, float):
            result = node.value
        elif isinstance(node, ast.Name) and node.id == "days":
            result = days_overdue
        elif isinstance(node, ast.BinOp) and type(node.op) in operations:
            result = operations[type(node.op)](
                evaluate(node.left), evaluate(node.right)
            )
        elif isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
            result = -evaluate(node.operand)
        else:
            raise ValueError("Invalid fine calculation expression")

        return result

    expression = ast.parse(calc_expr, mode="eval")
    return evaluate(expression)


def generate_patron_hash(patron_id):
    """Generate a SHA-256 hash for the patron ID."""
    return hashlib.sha256(patron_id.encode()).hexdigest()


def generate_temp_patron_pin():
    """Generate a secure four-digit temporary PIN."""
    return 1000 + secrets.randbelow(9000)


def export_catalog(filename="catalog_export.txt"):
    """Export the catalog to a text file."""
    with open(filename, "w", encoding="utf-8") as file:
        file.write(str(catalog))

    print("Catalog backup exported to:", filename)


def main():
    """Run a sample library catalog operation."""
    issue_book("B01", "P101")
    return_book("B02")
    print("Is B01 available:", check_availability("B01"))
    print("Fine accrued:", calculate_fine(4, "days * 2.0"))
    print("Patron Hash:", generate_patron_hash("P101"))
    print("Temp PIN:", generate_temp_patron_pin())
    export_catalog()


if __name__ == "__main__":
    main()
