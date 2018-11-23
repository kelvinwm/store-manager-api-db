import datetime
import psycopg2
from flask import make_response, jsonify, request
from flask_restful import reqparse
from app.api.v2.utils import Validate
from db_init import connection
from app.api.v2.models.users_model import login_required


class SalesModel:
    """Categories functions"""

    def __init__(self):
        self.conn = connection()
        self.cur = self.conn.cursor()
        self.now = datetime.datetime.now()

    @login_required
    def get_all_sales(self, current_user, token):
        """get all products"""
        validate = Validate(current_user['role'], " view all sales")
        rows = validate.validate_get_sales(current_user)
        sales = []
        try:
            if not rows:
                return make_response(jsonify({
                    "message": "Nothing has been stored yet"
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
                "message": "Error retrieving sales"
            }))

    @login_required
    def add_sale(self, current_user, token):
        """add a product"""
        data = request.get_json()
        pars = reqparse.RequestParser()
        pars.add_argument("products", required=True, help="products key/value invalid entry", location=['json'])
        data2 = pars.parse_args()
        validate = Validate(current_user['role'], "no message")
        products = data["products"]
        if not products:
            return {"Alert": "Add products"}
        if validate.validate_sale(products) != "ok":
            return validate.validate_sale(products)
        global price, product_id, quantity, total_price
        total_cost = 0
        sold_list = []
        try:
            for product in products:
                query = "SELECT * FROM products WHERE product_name ='{0}'".format(product["product_name"])
                self.cur.execute(query)
                rows = self.cur.fetchall()
                for row in rows:
                    product_id = row[0]
                    quantity = int(row[3])
                    price = int(row[4])

                new_quantity = quantity - int(product["quantity"])
                sql = """ UPDATE products SET quantity=%s WHERE id = %s"""
                self.cur.execute(sql, (new_quantity, product_id))
                self.conn.commit()

                total_price = price * int(product["quantity"])
                insert_query = """INSERT INTO sales (username,product_id,quantity, price, date_created) VALUES (
                    %s,%s,%s,%s,%s)"""
                self.cur.execute(insert_query,
                                 (current_user['username'], product_id, product["quantity"], total_price, self.now))
                self.conn.commit()
                sold_list.append(str(quantity) + " " + product["product_name"] + " at " + str(price) + " = " +
                                 str(total_price))
                total_cost += total_price
            return make_response(jsonify({
                "message": "Sales created successfully",
                "Remaining": new_quantity,
                "Total cost": str(total_cost)
            }), 201)
        except (Exception, psycopg2.DatabaseError) as error:
            return make_response(jsonify({
                "message": "error"
            }))

    @login_required
    def get_one_sale(self, sale_id, current_user, token):
        """get one product"""
        validate = Validate(current_user['role'], " view sales")
        if validate.admin_checker() != "true":
            return validate.admin_checker()
        sale = []
        try:
            query = "SELECT * FROM sales WHERE id ='{0}'".format(sale_id)
            self.cur.execute(query)
            rows = self.cur.fetchall()
            if not rows:
                return make_response(jsonify({
                    "message": "Item does not exist"
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
                "message": "error getting the sale"
            }))

    @login_required
    def update_sale(self, sale_id, current_user, token):
        """modify products"""
        global quantity, price
        validate = Validate(current_user['role'], " update sales")
        if validate.admin_checker() != "true":
            return validate.admin_checker()
        data = request.get_json()
        try:
            sql = """ UPDATE sales SET quantity=%s, price=%s WHERE id = %s"""
            query = "SELECT * FROM sales WHERE id ='{0}'".format(sale_id)
            self.cur.execute(query)
            rows = self.cur.fetchall()
            if not rows:
                return make_response(jsonify({
                    "message": "Product not found"
                }), 200)
            for row in rows:
                quantity = int(row[3])
                price = int(row[4])
            if "quantity" in data:
                if validate.validate_updates("quantity", data) != "done":
                    return validate.validate_updates("quantity", data)
                quantity = data["quantity"]
            if "price" in data:
                if validate.validate_updates("price", data) != "done":
                    return validate.validate_updates("price", data)
                price = data["price"]
            if "" in data:
                return {"Enter key/value data format"}
            self.cur.execute(sql, (quantity, price, sale_id))
            self.conn.commit()
            return make_response(jsonify({
                "status": str(price),
                "message": "Updated successfully"
            }), 200)
        except (Exception, psycopg2.DatabaseError) as error:
            return {"Error": "Unable to  sale try again!"}

    @login_required
    def delete_sale(self, sale_id, current_user, token):
        """delete a product"""
        validate = Validate(current_user['role'], " delete a sale record")
        if validate.admin_checker() != "true":
            return validate.admin_checker()
        try:
            self.cur.execute("SELECT * FROM sales WHERE id= '{0}'".format(sale_id))
            if not self.cur.fetchone():
                return jsonify({"message": "Item does not exist"})
            query = "DELETE FROM sales WHERE id= '{0}'".format(sale_id)
            self.cur.execute(query)
            self.conn.commit()
            return make_response(jsonify({
                "message": "Sales deleted successfully"
            }), 200)
        except (Exception, psycopg2.DatabaseError) as error:
            return make_response(jsonify({
                "status": "OK",
                "message": error
            }))
