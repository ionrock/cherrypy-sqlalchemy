from cherrypy.process import plugins

import cherrypy

from sqlalchemy import create_engine


class SQLAlchemyPlugin(plugins.SimplePlugin):
    def __init__(self, bus, orm_base, dburi, **kw):
        """
        The plugin is registered to the CherryPy engine and therefore
        is part of the bus (the engine *is* a bus) registery.

        We use this plugin to create the SA engine. At the same time,
        when the plugin starts we create the tables into the database
        using the mapped class of the global metadata.

        Finally we create a new 'bind' channel that the SA tool
        will use to map a session to the SA engine at request time.
        """
        plugins.SimplePlugin.__init__(self, bus)
        self.dburi = dburi
        self.orm_base = orm_base
        self.create_kwargs = kw

        self.bus.subscribe('db.bind', self.bind)
        self.bus.subscribe('db.create', self.create)

        self.sa_engine = None

    def start(self):
        self.sa_engine = create_engine(self.dburi, **self.create_kwargs)

    def create(self):
        if not self.sa_engine:
            self.start()
        cherrypy.log('Creating tables: %s' % self.sa_engine)
        self.orm_base.metadata.bind = self.sa_engine
        self.orm_base.metadata.create_all(self.sa_engine)

    def stop(self):
        if self.sa_engine:
            self.sa_engine.dispose()
            self.sa_engine = None

    def bind(self, session):
        session.configure(bind=self.sa_engine)
