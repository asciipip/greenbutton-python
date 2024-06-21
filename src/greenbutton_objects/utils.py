#!/usr/bin/python

ns = {'atom': 'http://www.w3.org/2005/Atom',
      'espi': 'http://naesb.org/espi'}

def getEntity(source, target, accessor=None, multiple=False):
    """Extracts the named entity from the source XML tree.  `accessor` is a
    function of one argyment; if provided and the target entity is found, the
    target will be passed into `accessor` and its result will be returned.  If
    `multiple` is true, the result will be all entities that match (i.e. the
    function will use `finall` instead of `find`)."""
    if multiple:
        es = source.findall(target, ns)
        if accessor:
            return [ accessor(e) for e in es ]
        else:
            return es
    else:
        e = source.find(target, ns)
        if e is not None and accessor is not None:
            return accessor(e)
        else:
            return e

def getLink(source, relation, multiple=False):
    """Shorthand for pulling a link with the given "rel" attribute from the source."""
    return getEntity(source, './atom:link[@rel="%s"]' % relation, lambda e: e.attrib['href'], multiple)

