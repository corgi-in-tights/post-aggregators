from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


def create_tables(engine, *args):  # noqa: ARG001
    Base.metadata.create_all(bind=engine)
