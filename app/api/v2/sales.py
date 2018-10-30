import datetime
import psycopg2
from flask import make_response, jsonify, request

from app.api.v2.utils import Validate
from db_init import connection

from app.api.v2.models import login_required, Products

now = datetime.datetime.now()
conn = connection()
cur = conn.cursor()


class SalesModel:
    """Categories functions"""

    @login_required
    def get_all_sales(self, current_user, token):
        """get all products"""
        sales = []
        try:
            cur.execute("SELECT id, username, product_id, quantity, price, date_created from sales")
            rows = cur.fetchall()
            if not rows:
                return make_response(jsonify({
                    "Message": "Nothing has been stored yet"
                }), 200)
            for row in rows:
                item = {
                    "Id": row[0],
                    "username": row[1],
                    "product_id": row[2],
                    "quantity": int(row[3]),
                    "price": int(row[4]),
                    "date": row[5]
                }
                sales.append(item)
            return make_response(jsonify({
                "All sales": sales
            }), 200)
        except (Exception, psycopg2.DatabaseError) as error:
            return make_response(jsonify({
                "Message": "Error retrieving sales"
            }))

    @login_required
    def add_sale(self, current_user, token):
        """add a product"""
        if Validate().validate_sale() != "true":
            return Validate().validate_sale()
        global price, product_id, quantity, product_name
        data = request.get_json()
        try:
            query = "SELECT * FROM products WHERE product_name ='{0}'".format(data["product_name"])
            cur.execute(query)
            rows = cur.fetchall()
            if not rows:
                return "product does not exist"
            for row in rows:
                product_id = row[0]
                product_name = row[1]
                quantity = int(row[3])
                price = int(row[4])
            if int(data["quantity"]) > quantity:
                return {"Message": "Product out of stock", "Remaining " + product_name: quantity}

            new_quantity = quantity - int(data["quantity"])
            sql = """ UPDATE products SET quantity=%s WHERE id = %s"""
            cur.execute(sql, (new_quantity, product_id))
            conn.commit()

            total_price = price * int(data["quantity"])
            insert_query = """INSERT INTO sales (username,product_id,quantity, price, date_created) VALUES (
                %s,%s,%s,%s,%s)"""
            cur.execute(insert_query, (current_user['username'], product_id, data["quantity"], total_price, now))
            conn.commit()
            return make_response(jsonify({
                "Message": "Sale created successfully",
                product_name + " remaining": new_quantity
            }), 201)
        except (Exception, psycopg2.DatabaseError) as error:
            return make_response(jsonify({
                "status": "OK",
                "Message": error
            }))

    @login_required
    def get_one_sale(self, sale_id, current_user, token):
        """get one product"""
        sale = []
        try:
            query = "SELECT * FROM sales WHERE id ='{0}'".format(sale_id)
            cur.execute(query)
            rows = cur.fetchall()
            if not rows:
                return make_response(jsonify({
                    "Message": "Item does not exist"
                }), 200)
            for row in rows:
                item = {
                    "Id": row[0],
                    "username": row[1],
                    "product_id": row[2],
                    "quantity": int(row[3]),
                    "price": int(row[4]),
                    "date": row[5]
                }
                sale.append(item)
            return make_response(jsonify({
                "sale": sale
            }), 200)
        except (Exception, psycopg2.DatabaseError) as error:
            return make_response(jsonify({
                "Message": "error getting the sale"
            }))

    @login_required
    def update_sale(self, sale_id, current_user, token):
        """modify products"""
        data = request.get_json()
        try:
            sql = """ UPDATE sales SET product_id = %s, quantity=%s, price=%s WHERE id = %s"""
            query = "SELECT * FROM sales WHERE id ='{0}'".format(sale_id)
            cur.execute(query)
            rows = cur.fetchall()
            if not rows:
                return make_response(jsonify({
                    "Message": "Product not found"
                }), 200)
            cur.execute(sql, (data["product_name"], data["quantity"], data["price"], sale_id))
            conn.commit()
            return make_response(jsonify({
                "status": "OK",
                "Message": "Updated successfully"
            }), 200)
        except (Exception, psycopg2.DatabaseError) as error:
            return {"Error": "Unable to update product try again!"}

    @login_required
    def delete_sale(self, sale_id, current_user, token):
        """delete a product"""
        try:
            cur.execute("SELECT * FROM sales WHERE id= '{0}'".format(sale_id))
            if not cur.fetchone():
                return jsonify({"Message": "Item does not exist"})
            query = "DELETE FROM sales WHERE id= '{0}'".format(sale_id)
            cur.execute(query)
            conn.commit()
            return make_response(jsonify({
                "Message": "Sales deleted successfully"
            }), 200)
        except (Exception, psycopg2.DatabaseError) as error:
            return make_response(jsonify({
                "status": "OK",
                "Message": error
            }))
