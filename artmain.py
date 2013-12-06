#!/usr/local/bin/python2.7

import cherrypy

class Root(object):

    from index import index as index
    index.exposed = True

    from artmash import artmash
    artmash.exposed = True

    from artmash_score import artmash_score
    artmash_score.exposed = True

# To be implemented at a later date:

##    from artmash_rank import artmash_rank
##    artmash_rank.exposed = True

##    from learn_more import learn_more as learn_more
##    learn_more.exposed = True
##
##    # This is most likely unique to the Luce Center API
##    from luce_zoom import luce_zoom
##    luce_zoom.exposed = True
##
##    from luce_zoom_score import luce_zoom_score
##    luce_zoom_score.exposed = True
    
if __name__ == '__main__':

    import os.path
    current_dir = os.path.dirname(os.path.abspath(__file__))

    cherrypy.config.update({'server.socket_port': 8080,
                            'server.socket_host': '127.0.0.1',
                            'log.screen': True,
                            'log.error_file': 'site.log'
                            })

    conf = {'/static': {'tools.staticdir.on': True,
                      'tools.staticdir.dir': os.path.join(current_dir, 'static'),
                        }
            }
    
    cherrypy.quickstart(Root(), '/', config=conf)
