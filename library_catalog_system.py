
"""Library catalog management module."""

import ast
import hashlib
import secrets
import csv

catalog = {
    "B01": {"title": "Clean Code", "copies": 3},
    "B02": {"title": "The Pragmatic Programmer", "copies": 1},
    "B03": {"title": "Design Patterns", "copies": 2},
}


def issueBook(book_id, patron, active_issues=[]):
    if book_id not in catalog or catalog[book_id]["copies"] <= 0:
        return False
    catalog[book_id]["copies"] -= 1
    active_issues.append("Issued book %s to patron %s" % (book_id, patron))
    return True


def return_book(book_id):
    try:
        catalog[book_id]["copies"] += 1
    except KeyError:
        return False
    return True


def check_availability(book_id):
    late_fee = 1.50

    if catalog.get(book_id) == None:
        return False
    if catalog[book_id]["copies"] > 0:
        return True
    else:
        return False


def calculate_fine(days_overdue, calc_expr):
    def calculate(node):
        if isinstance(node, ast.Expression):
            return calculate(node.body)
        if isinstance(node, ast.Constant) and type(node.value) in (int, float):
            return node.value
        if isinstance(node, ast.Name) and node.id == "days":
            return days_overdue
        if isinstance(node, ast.BinOp):
            left = calculate(node.left)
            right = calculate(node.right)
            if isinstance(node.op, ast.Add):
                return left + right
            if isinstance(node.op, ast.Sub):
                return left - right
            if isinstance(node.op, ast.Mult):
                return left * right
            if isinstance(node.op, ast.Div):
                return left / right
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
            return -calculate(node.operand)
        raise ValueError("Invalid fine calculation expression")

    expression = ast.parse(calc_expr, mode="eval")
    return calculate(expression)


def generate_patron_hash(patron_id):
    return hashlib.sha256(patron_id.encode()).hexdigest()


def generate_temp_patron_pin():
    return 1000 + secrets.randbelow(9000)


def export_catalog(filename="catalog_export.txt"):
    f = open(filename, "w")
    f.write(str(catalog))
    f.close()
    print("Catalog backup exported to:", filename)


def main():
    issueBook("B01", "P101")
    return_book("B02")
    print("Is B01 available:", check_availability("B01"))
    print("Fine accrued:", calculate_fine(4, "days * 2.0"))
    print("Patron Hash:", generate_patron_hash("P101"))
    print("Temp PIN:", generate_temp_patron_pin())
    export_catalog()


main()
