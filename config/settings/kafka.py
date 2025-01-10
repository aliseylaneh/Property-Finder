from config.env_conf.env import env

KAFKA_BOOTSTRAP_SERVERS = [f'{env('KAFKA_HOST')}:{env('KAFKA_PORT')}']
KAFKA_CONSUMER_GROUP = env('KAFKA_CONSUMER_GROUP')
KAFKA_TOPIC_PREFIX = env('KAFKA_TOPIC_PREFIX')