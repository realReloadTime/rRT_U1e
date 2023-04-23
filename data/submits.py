import sqlalchemy as sa
from data.db_session import SqlAlchemyBase
from sqlalchemy.orm import relationship

Base = SqlAlchemyBase


class Services(SqlAlchemyBase):
    __tablename__ = 'services'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True, unique=True, nullable=False)
    title = sa.Column(nullable=False)
    description = sa.Column()
    cost = sa.Column()

    submit = relationship("Submit", back_populates='sub_ser')


class Statuses(SqlAlchemyBase):
    __tablename__ = 'statuses'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True, unique=True, nullable=False)
    title = sa.Column()

    submit = relationship("Submit", back_populates='sub_sta')


class Submit(Base):
    __tablename__ = 'submits'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True, unique=True, nullable=False)
    name = sa.Column()
    text = sa.Column()
    type = sa.Column(sa.ForeignKey('services.id'))
    time = sa.Column()
    email = sa.Column()
    phone = sa.Column()
    status = sa.Column(sa.ForeignKey('statuses.id'))

    sub_ser = relationship('Services')
    sub_sta = relationship('Statuses')
