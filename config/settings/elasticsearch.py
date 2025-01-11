from config.env_conf.env import env

ELASTICSEARCH_DSL = {
    'default': {
        'hosts': f'http://{env('ELASTICSEARCH_HOST')}:{env('ELASTICSEARCH_PORT')}',
    }
}
ELASTICSEARCH_DSL_AUTOSYNC = False  # Turned off this feature because we want to insert and sync manually
