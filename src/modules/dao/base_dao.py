from sqlalchemy.orm import declarative_base


class BaseDao(declarative_base()):
    __abstract__ = True

