set -o errexit

# Install dependencies (optional if using render.yaml build command)
# pip install -r requirements.txt

# Convert static asset files
python manage.py collectstatic --no-input

# Apply any outstanding database migrations
python manage.py migrate