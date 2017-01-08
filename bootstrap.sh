echo "================================================"
echo "START PROVISIONING WITH BOOTSTRAP SHELL SCRIPT"
echo "================================================"
PROJECT_NAME=gamemart
APP_DB_USER=gamemartdbadmin
APP_DB_PASS=snowisdeliciouswithsyrup
APP_DB_NAME=gamemart
PG_VERSION=9.3

echo "------------------------------------------------"
echo "upgrading ubuntu box"
echo "------------------------------------------------"
sudo apt-get update
sudo apt-get -y upgrade

echo "------------------------------------------------"
echo "install python3-pip, apache2 and mod_wsgi"
echo "------------------------------------------------"
sudo apt-get install -y python3-pip apache2 libapache2-mod-wsgi-py3

echo "------------------------------------------------"
echo "install virtualenv"
echo "------------------------------------------------"
sudo pip3 install virtualenv

echo "------------------------------------------------"
echo "set web root to /vagrant directory instead of the default /var/www"
echo "------------------------------------------------"
if ! [ -L /var/www ]; then
  rm -rf /var/www
  ln -fs /vagrant /var/www
fi

echo "------------------------------------------------"
echo "install and setting up PostgreSQL"
echo "------------------------------------------------"
###########################################################
# Changes below this line are probably not necessary
###########################################################
print_db_usage () {
  echo "Your PostgreSQL database has been setup and can be accessed on your local machine on the forwarded port (default: 15432)"
  echo "  Host: localhost"
  echo "  Port: 15432"
  echo "  Database: $APP_DB_NAME"
  echo "  Username: $APP_DB_USER"
  echo "  Password: $APP_DB_PASS"
  echo ""
  echo "Admin access to postgres user via VM:"
  echo "  vagrant ssh"
  echo "  sudo su - postgres"
  echo ""
  echo "psql access to app database user via VM:"
  echo "  vagrant ssh"
  echo "  sudo su - postgres"
  echo "  PGUSER=$APP_DB_USER PGPASSWORD=$APP_DB_PASS psql -h localhost $APP_DB_NAME"
  echo ""
  echo "Env variable for application development:"
  echo "  DATABASE_URL=postgresql://$APP_DB_USER:$APP_DB_PASS@localhost:15432/$APP_DB_NAME"
  echo ""
  echo "Local command to access the database via psql:"
  echo "  PGUSER=$APP_DB_USER PGPASSWORD=$APP_DB_PASS psql -h localhost -p 15432 $APP_DB_NAME"
}

export DEBIAN_FRONTEND=noninteractive

PROVISIONED_ON=/etc/vm_provision_on_timestamp
if [ -f "$PROVISIONED_ON" ]
then
  echo "VM was already provisioned at: $(cat $PROVISIONED_ON)"
  echo "To run system updates manually login via 'vagrant ssh' and run 'apt-get update && apt-get upgrade'"
  echo ""
  print_db_usage
  exit
fi

PG_REPO_APT_SOURCE=/etc/apt/sources.list.d/pgdg.list
if [ ! -f "$PG_REPO_APT_SOURCE" ]
then
  # Add PG apt repo:
  echo "deb http://apt.postgresql.org/pub/repos/apt/ trusty-pgdg main" > "$PG_REPO_APT_SOURCE"

  # Add PGDG repo key:
  wget --quiet -O - https://apt.postgresql.org/pub/repos/apt/ACCC4CF8.asc | apt-key add -
fi

#apt-get install -y postgresql postgresql-contrib
apt-get -y install "postgresql-$PG_VERSION" "postgresql-contrib-$PG_VERSION"

PG_CONF="/etc/postgresql/$PG_VERSION/main/postgresql.conf"
PG_HBA="/etc/postgresql/$PG_VERSION/main/pg_hba.conf"
PG_DIR="/var/lib/postgresql/$PG_VERSION/main"

# Edit postgresql.conf to change listen address to '*':
sed -i "s/#listen_addresses = 'localhost'/listen_addresses = '*'/" "$PG_CONF"

# Append to pg_hba.conf to add password auth:
echo "host    all             all             all                     md5" >> "$PG_HBA"

# Explicitly set default client_encoding
echo "client_encoding = utf8" >> "$PG_CONF"

# Restart so that all new config is loaded:
service postgresql restart

cat << EOF | su - postgres -c psql
-- Create the database user:
CREATE USER $APP_DB_USER WITH PASSWORD '$APP_DB_PASS';

-- Create the database:
CREATE DATABASE $APP_DB_NAME WITH OWNER=$APP_DB_USER
                                  LC_COLLATE='en_US.utf8'
                                  LC_CTYPE='en_US.utf8'
                                  ENCODING='UTF8'
                                  TEMPLATE=template0;
EOF

# Tag the provision time:
date > "$PROVISIONED_ON"

echo "Successfully created PostgreSQL dev virtual machine."
echo ""
print_db_usage



echo "------------------------------------------------"
echo "activate virtualenv"
echo "------------------------------------------------"
#mkdir /vagrant/$PROJECT_NAME
virtualenv /vagrant/$PROJECT_NAME/$PROJECT_NAME"env"
source /vagrant/$PROJECT_NAME/$PROJECT_NAME"env/bin/activate"

echo "------------------------------------------------"
echo "install python-psycopg2 to connect python with postgresql within the virtualenv"
echo "------------------------------------------------"
sudo apt-get install -y python-psycopg2
sudo apt-get install -y libpq-dev
pip install psycopg2

echo "------------------------------------------------"
echo "install django"
echo "------------------------------------------------"
pip install django
#django-admin.py startproject $PROJECT_NAME /vagrant/$PROJECT_NAME

echo "------------------------------------------------"
echo "test django with python web server"
echo "------------------------------------------------"
sudo ufw allow 8000
timeout 10s /vagrant/$PROJECT_NAME/manage.py runserver 0.0.0.0:8000
deactivate

echo "------------------------------------------------"
echo "set apache config to work with django "
echo "------------------------------------------------"
#mkdir /vagrant/$PROJECT_NAME/static
#sudo cp /vagrant/settings/django.py /vagrant/$PROJECT_NAME/$PROJECT_NAME/settings.py
sudo cp /vagrant/settings/apache.conf /etc/apache2/sites-available/000-default.conf
sudo apache2ctl restart

echo "================================================"
echo "ALL DONE!"
echo "================================================"
#source /vagrant/gamemart/gamemartenv/bin/activate
#/vagrant/gamemart/manage.py runserver 0.0.0.0:8000
