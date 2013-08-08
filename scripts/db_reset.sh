#!/bin/bash

su - postgres -c 'dropdb soletrakr_db'
su - postgres -c 'createdb -T template_postgis soletrakr_db'