# MYSQL details
#MYSQL_HOST = '127.0.0.1'
#On AWS cloud
MYSQL_HOST = '<YOUR_DATABASE_NAME_ON_RDS>.ap-southeast-1.rds.amazonaws.com'
#working in local internal
#MYSQL_HOST = 'host.docker.internal'
MYSQL_USER = 'root'
MYSQL_PASSWORD = '<YOUR_MYSQL_PASSWORD'
MYSQL_DB = 'wiki'

# Following DB commands should not be part of request body
FORBIDDEN_DB_COMMANDS = ['delete', 'create', 'update', 'alter', 'drop', 'alter', 'insert', 'grant', 'revoke',
                         'commit', 'truncate', 'rename', 'comment']
