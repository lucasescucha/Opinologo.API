from database import engine
from models import Selector, Base

def initializeDb(session):
    Base.metadata.create_all(bind=engine)

    if len(session.query(Selector).all()) == 0:
        session.add(Selector(url='www.pagina12.com.ar/.*',
            selector='div.article-main-content.article-text'))

    session.commit()