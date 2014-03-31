*Deployment Guide*

*Passwords and other things you wouldn't want to commit:*
1. Enter the Secret Key in settings.py
2. Enter the database credentials in settings.py (See Creating the database below)
3. Enter any API connection details in apps/mash/museum_apis/art_credentials.py

*Creating the database:*
4: If on a mac and you have not done so, you may need to start the postgres server: postgres -D /usr/local/var/postgres/
5. In the terminal: createdb art_games
6. In the terminal: psql -d art_games
7. At the psql prompt: create user art with password 'whatever_your_password_is';
8. At the psql prompt: grant all privileges on database art_games to art;
9. Exit the psql prompt with: \q

*Syncing the database:*
10. In the terminal: ./manage.py syncdb
11. Creating your superusers (be sure to write these down)
12. Add 'apps.mash' to the INSTALLED_APPS
13. In the terminal: ./manage.py schemamigration apps.mash --initial
14. In the terminal: ./manage.py migrate mash 
