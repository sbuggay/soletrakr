#!/bin/bash

createuser -P --createdb soletrakr_admin
createdb -T template_postgis soletrakr_db
