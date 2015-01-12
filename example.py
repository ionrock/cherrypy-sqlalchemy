import os

import cherrypy

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column
from sqlalchemy.types import String, Integer

from cp_sqlalchemy import SQLAlchemyTool, SQLAlchemyPlugin

Base = declarative_base()
HERE = os.path.dirname(os.path.abspath(__file__))


class LogMessage(Base):

    __tablename__ = 'logs'

    id = Column(Integer, primary_key=True)
    value = Column(String)


class Root(object):

    @property
    def db(self):
        return cherrypy.request.db

    def page(self):
        return '''
        <html>
          <head><title>CherryPy-SQLAlchemy Example</title></head>
          <body>
            <form action='/' method='post'>
              <input type='text' name='message' /><input type='submit' value='add' />
            </form>
            %s
          </body>
        <html>
        '''

    @cherrypy.expose
    def index(self, message=None, submit=None):
        if message:
            self.db.add(LogMessage(value=message))
            self.db.commit()
            raise cherrypy.HTTPRedirect('/')

        page = self.page()

        ol = ['<ol>']
        for msg in self.db.query(LogMessage).all():
            ol.append('<li>%s</li>' % msg.value)
        ol.append('</ol>')

        return page % ('\n'.join(ol))


def run():
    cherrypy.tools.db = SQLAlchemyTool()

    app_config = {
        '/': {
            'tools.db.on': True,
        }
    }
    cherrypy.tree.mount(Root(), '/', config=app_config)
    dbfile = os.path.join(HERE, 'log.db')

    if not os.path.exists(dbfile):
        open(dbfile, 'w+').close()

    sqlalchemy_plugin = SQLAlchemyPlugin(
        cherrypy.engine, Base, 'sqlite:///%s' % (dbfile),
        echo=True
    )
    sqlalchemy_plugin.subscribe()
    sqlalchemy_plugin.create()
    cherrypy.engine.start()
    cherrypy.engine.block()


if __name__ == '__main__':
    run()
