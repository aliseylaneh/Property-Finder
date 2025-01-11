from config.env_conf.env import env

ELASTICSEARCH_DSL = {
    'default': {
        'hosts': f'http://{env('ELASTICSEARCH_HOST')}:{env('ELASTICSEARCH_PORT')}',
    }
}
