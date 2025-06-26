from server.app import app
from server.config import db
from server.models import Volunteer,Project, Donation, User
from datetime import datetime
from faker import Faker
import random

fake = Faker()

donation_types = ["Money", "Clothes", "Food", "Other"]
projects_data = [
  {
    "project_type": "Health",
    "image": "https://images.unsplash.com/photo-1588776814546-ec7d7f3dbdd5?auto=format&fit=crop&w=1170&q=80"
  },
  {
    "project_type": "Education",
    "image": "https://images.unsplash.com/photo-1588072432836-e10032774350?auto=format&fit=crop&w=1170&q=80"
  },
  {
    "project_type": "Environment",
    "image": "https://images.unsplash.com/photo-1501004318641-b39e6451bec6?auto=format&fit=crop&w=1170&q=80"
  },
  {
    "project_type": "Community",
    "image": "https://images.unsplash.com/photo-1581578016310-4fce7f2b1d44?auto=format&fit=crop&w=1170&q=80"
  },
  {
    "project_type": "Emergency",
    "image": "https://images.unsplash.com/photo-1605733160314-4ce5f1c56d8b?auto=format&fit=crop&w=1170&q=80"
  }
]

with app.app_context():
    print("Seeding database...")

    db.drop_all()
    db.create_all()

    # Create Users
    print("Creating Users...")

    users = []
    for _ in range(9):
        user = User(
            email=fake.unique.email(),
            first_name=fake.first_name(),
            last_name=fake.last_name()
        )
        user.password_hash = "password123"
        users.append(user)

    # Add admin user
    admin_user = User(
        email=fake.unique.email(),
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        role="admin"
    )
    admin_user.password_hash = "adminpass"
    users.append(admin_user)

    db.session.add_all(users)
    db.session.commit()

    # Create Donations - At least one per user, total 15, 5 non-money
    print("Creating Donations...")
    
    donations = []

    non_money_count = 0
    for user in users[:10]:  # Only regular users
        dtype = random.choice(donation_types)
        if dtype != "money":
            non_money_count += 1

        donation = Donation(
            type=dtype,
            group=fake.word().capitalize() + " Group",
            details=fake.sentence() if dtype != "money" else None,
            phone_number=fake.msisdn()[:10],
            amount=random.randint(100, 5000) if dtype == "money" else None,
            user_id=user.id,
            date=datetime.now()
        )
        donations.append(donation)

    while len(donations) < 15:
        dtype = random.choice(donation_types)
        
        # Ensure exactly 5 non-money donations
        if dtype != "money" and non_money_count >= 5:
            dtype = "money"

        if dtype != "money":
            non_money_count += 1

        donation = Donation(
            type=dtype,
            group=fake.word().capitalize() + " Group",
            details=fake.sentence() if dtype != "money" else None,
            phone_number=fake.msisdn()[:10],
            amount=random.randint(100, 5000) if dtype == "money" else None,
            user_id=random.choice(users[:10]).id,
            date=datetime.now()
        )
        donations.append(donation)

    db.session.add_all(donations)
    db.session.commit()

    # Create Projects
    print("Creating Projects...")
    project_images = []
    projects = []
    for item in projects_data:
        project = Project(
            type=item["project_type"],
            image_url=item["image"],
            description=fake.text(max_nb_chars=150),
            date=fake.date_between(start_date="today", end_date="+1y")

        )
        projects.append(project)

    db.session.add_all(projects)
    db.session.commit()
    # Create Volunteers (Separate from Users)
    print("Creating Volunteers...")
    volunteers = []
    for _ in range(10):
        volunteer = Volunteer(
            name=fake.name(),
            email=fake.unique.email(),
            phone_number=fake.msisdn()[:10],
            age=random.randint(18, 60),
            city=fake.city()
        )
        volunteers.append(volunteer)

    db.session.add_all(volunteers)
    db.session.commit()

    print("Seeding complete!")
