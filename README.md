soletrakr_project
=================


How to get things working

1. install GIS dependencies then postgresql on Debian environment

        $ sudo apt-get install binutils libproj-dev gdal-bin
        $ sudo apt-get install postgresql-* postgresql-*-postgis postgresql-server-dev-*

2. run database setup script 

        $ sudo bash scripts/db_setup.sh

3. install virtualenv

        $ pip install virtualenv

4. run soletrakr virtual environment setup script

        $ bash scripts/virtualenv_setup.sh

5. activate the virtual environment

        $ source .ve/bin/activate
    
t
