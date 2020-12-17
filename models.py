from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class History(db.Model):
    __tablename__ = "History"
    id = db.Column(db.Integer, primary_key=True)
    #username = db.Column(db.String(25),nullable=False)
    message = db.Column(db.String(10000),nullable=False)
    time_stamp = db.Column(db.String(20),nullable=False)
    room = db.Column(db.String(20),nullable=False)
    #enc_key = db.Column(db.String(100),nullable=False)

