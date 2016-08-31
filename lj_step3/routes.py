def includeme(config):
    ''' This function adds routes to Pyramid's Configurator '''
    config.add_static_view(name='static', path='learning_journal:static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('detail', '/detail/{id:\d+}')
    config.add_route('edit', '/edit/{id:\d+}')
    config.add_route('new', '/new')
