import sqlite3


def check_quantity_in_shipping(invoice_number, product_number):
    ship_conn = sqlite3.connect("../db/shipping_lists.db")
    ship_cursor = ship_conn.cursor()
    ship_query = (
        "SELECT quantity FROM products WHERE invoice_number = "
        + str(invoice_number)
        + " AND product_number = "
        + str(product_number)
    )
    # print(ship_query)
    ship_cursor.execute(ship_query)
    result = ship_cursor.fetchone()
    # print(result)
    ship_conn.commit
    ship_conn.close()
    if result is None:
        return "None"
    return result[0]


# print(check_quantity_in_shipping(25121, 271674))

inv_conn = sqlite3.connect("../db/invoices.db")
inv_cursor = inv_conn.cursor()
inv_data = inv_cursor.execute("SELECT * FROM invoices ORDER BY invoice_number")
inv_output = inv_cursor.fetchall()

for inv_row in inv_output:
    inv_number = inv_row[0]
    # print(inv_number)
    statement = "SELECT * FROM products WHERE invoice_number = " + inv_number
    # print("---------------------------------")
    # print(statement)
    inv_cursor.execute(statement)
    output = inv_cursor.fetchall()
    for prod_row in output:
        prod_number = prod_row[1]
        inv_quantity = prod_row[3]
        # print(
        #    f"Invoice: {inv_number}, Product: {prod_number}, Invoice Quantity: {inv_quantity}"
        # )
        ship_quantity = check_quantity_in_shipping(inv_number, prod_number)
        if ship_quantity != "None":
            if ship_quantity != inv_quantity:
                print(
                    f"Invoice: {inv_number}, Product Number: {prod_number}, Invoice Quantity: {inv_quantity}, Delivered: {check_quantity_in_shipping(inv_number, prod_number)}."
                )


inv_conn.close()
