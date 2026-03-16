from src import create_app
from flask import Flask
from src.models import db

app = Flask(__name__)

# connect MySQL database
app.config['SQLALCHEMY_DATABASE_URI'] = (
    'mysql+pymysql://root:nongminhhai123@localhost:3306/quan_ly_giang_vien'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'bi_mat'

# Khởi tạo SQLAlchemy
db.init_app(app)

# routes
import src.admin
import src.auth_user
import src.user

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)