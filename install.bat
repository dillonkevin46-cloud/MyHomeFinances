@echo off
echo Setting up FamilyFinance...

echo Installing dependencies...
pip install -r requirements.txt

echo Creating database migrations...
python manage.py makemigrations finance
python manage.py makemigrations

echo Applying database migrations...
python manage.py migrate

echo Populating initial data...
python populate_data.py

echo Setup complete! You can now run 'run.bat' to start the server.
pause
