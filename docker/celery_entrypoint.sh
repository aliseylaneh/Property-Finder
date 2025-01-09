#!/bin/sh
echo "--> Starting celery process"
celery -A config worker -l info
