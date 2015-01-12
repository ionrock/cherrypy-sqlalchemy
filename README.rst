===================
CherryPy-SQLAlchemy
===================

.. image:: https://pypip.in/d/cp_sqlalchemy/badge.png
   :target: https://pypi.python.org/pypi/cp_sqlalchemy

..
   .. image:: https://badge.fury.io/py/cp_sqlalchemy.png
       :target: http://badge.fury.io/py/cp_sqlalchemy

   .. image:: https://travis-ci.org/ionrock/cp_sqlalchemy.png?branch=master
	   :target: https://travis-ci.org/ionrock/cp_sqlalchemy



CherryPy-SQLAlchemy makes it easy to use SQLAlchemy within CherryPy
apps.


Credits
=======

This package was primarily created from `Sylvain's SQLAlchemy
recipe
<http://www.defuze.org/archives/222-integrating-sqlalchemy-into-a-cherrypy-application.html>`_.


Basic Usage
===========

There are two elements of CherryPy-SQLAlchemy

 1. A CherryPy tool that will create a session for use with each
    request.
 2. A CherryPy plugin that can maintains information about the
    database and binds the session to the specific DB.

Here is an example connecting to a sqlite db: ::

  import cherrypy

  from app import Root
  from app.models import ORMBase
  from cp_sqlalchemy import SQLAlchemyTool, SQLAlchemyPlugin


  def run():
      cherrypy.tools.db = SQLAlchemyTool()
      cherrypy.tree.mount(Root(), '/', {
          '/': {
	      'tools.db.on': True
	  }
      })

      SQLAlchemyPlugin(
          cherrypy.engine, ORMBase, 'sqlite:////path/to/file.db'
      )

      cherrypy.engine.start()
      cherrypy.engine.block()


One thin to note is the ORMBase we imported is
`sqlalchemy.ext.declarative.declarative_base()` that was used when
creating models.

From there, each request will have access to `cherrypy.request.db`,
which is an instance of a SQLAlchemy session.

There is a more complete `example.py` in the source.


* Free software: BSD license
..
   * Documentation: https://cp_sqlalchemy.readthedocs.org.
