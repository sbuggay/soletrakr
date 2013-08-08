#!/bin/bash

su - postgres -c 'createuser -P --createdb soletrakr_admin'
su - postgres -c 'createdb -T template_postgis soletrakr_db'