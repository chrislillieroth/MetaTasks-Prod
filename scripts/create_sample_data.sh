#!/bin/bash
# Create sample data for development

set -e

echo "Creating sample data..."

python manage.py shell <<EOF
from apps.accounts.models import User

# Create superuser if doesn't exist
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='admin123'
    )
    print("Created superuser: admin / admin123")

EOF

echo "✓ Sample data created"
