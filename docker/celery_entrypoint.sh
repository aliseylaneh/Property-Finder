#!/bin/sh
echo "--> Starting celery process"
celery -A src.property_finder.tasks worker -l info
