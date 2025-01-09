#!/bin/sh
echo "--> Starting beats process"
celery -A config beat --scheduler django_celery_beat.schedulers:DatabaseScheduler

