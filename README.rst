Middlebury Directory
====================

.. image:: https://travis-ci.org/coursereviews/directory.svg?branch=master
    :target: https://travis-ci.org/coursereviews/directory

A Python API for the Middlebury directory.

Usage
-----

.. code-block:: python

    from directory.search import Search

    query = Search(email="dsilver@middlebury.edu")
    people = query.results()

    dana = people[0]
    
