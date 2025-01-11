#!/bin/sh
echo "--> Starting beats process"
celery -A src.property_finder.tasks beat --scheduler django_celery_beat.schedulers:DatabaseScheduler

