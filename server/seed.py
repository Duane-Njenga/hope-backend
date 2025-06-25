from server.app import app
from server.config import db
from server.models.user import User
from server.models.donation import Donation
from datetime import datetime
from faker import Faker

fake = Faker()

with app.app_context():
    print("Seeding database...")

    # Optional: Reset the tables completely
    db.drop_all()
    db.create_all()

    # Create Users
    user1 = User(
        email=fake.email(),
        first_name=fake.unique.first_name(),
        last_name=fake.last_name()
    )
    user1.password_hash = "password123"

    user2 = User(
        email=fake.email(),
        first_name=fake.unique.first_name(),
        last_name=fake.last_name()
    )
    user2.password_hash = "securepass"

    db.session.add_all([user1, user2])
    db.session.commit()

    # Create Donations
    donation1 = Donation(
        type="money",
        group="Community Fund",
        phone_number="0712345678",
        amount=1000,
        user_id=user1.id,
        date=datetime.now()
    )

    donation2 = Donation(
        type="clothes",
        group="Winter Drive",
        details="5 jackets and scarves",
        user_id=user2.id,
        date=datetime.now()
    )

    db.session.add_all([donation1, donation2])
    db.session.commit()

    print("Seeding complete!")
