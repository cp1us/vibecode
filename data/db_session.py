# -*- coding: utf-8 -*-
import sqlalchemy.orm as orm
from flask_sqlalchemy import SQLAlchemy

__SqlAlchemyBase = orm.declarative_base()
__db = SQLAlchemy(model_class=__SqlAlchemyBase)


def db_init(app) -> SQLAlchemy:
    __db.init_app(app)

    with app.app_context():
        __db.create_all()

    return __db
