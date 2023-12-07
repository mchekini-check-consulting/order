import os

from flask import Flask, request, make_response, jsonify
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from sqlalchemy import Column, String, Integer, TIMESTAMP

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SQLALCHEMY_DATABASE_URI")
db = SQLAlchemy(app)
migrate = Migrate(app, db)
ma = Marshmallow(app)


class Order(db.Model):
    __tablename__ = 'orders'
    id = Column(String, primary_key=True, index=True)
    created_on = Column(TIMESTAMP, default=db.func.current_timestamp())
    updated_on = Column(TIMESTAMP, onupdate=db.func.current_timestamp())
    user_id = Column(String, nullable=False)
    product_id = Column(String, nullable=False)
    amount = Column(Integer, nullable=False)
    address = Column(String, nullable=False)

    def __init__(self, id, user_id, product_id, amount, address):
        self.id = id
        self.user_id = user_id
        self.product_id = product_id
        self.amount = amount
        self.address = address


class OrderSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Order


FLASK_RUN_PORT = os.getenv('FLASK_RUN_PORT', '8080')


@app.route('/')
def hello_world():
    return 'Hello World from Order!'


@app.route("/orders", methods=['GET'])
def get_orders():
    orders = Order.query.all()
    return OrderSchema().dump(orders, many=True)


@app.route("/orders/user/<user_id>", methods=['GET'])
def get_orders_for_user(user_id):
    orders = db.session.query(Order).filter(Order.user_id == user_id)
    return OrderSchema().dump(orders, many=True)


@app.route("/orders", methods=['POST'])
def create_order():
    data = request.json
    order = Order(
        id=data["id"],
        user_id=data["user_id"],
        product_id=data["product_id"],
        amount=data["amount"],
        address=data["address"]
    )
    db.session.add(order)
    db.session.commit()
    return make_response(jsonify(OrderSchema().dump(order)), 201)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=FLASK_RUN_PORT, debug=True)
