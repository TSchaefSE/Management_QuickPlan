import os
import csv
import shutil
import tempfile
import unittest

from app import services


class TestUserServices(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.test_users_file = os.path.join(self.test_dir, "users.csv")

        services.DATA_FOLDER = self.test_dir
        services.USERS_FILE = self.test_users_file

        with open(self.test_users_file, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([
                "user_id",
                "first_name",
                "last_name",
                "email",
                "phone_number",
                "job_title",
                "department",
                "bio",
                "profile_picture"
            ])
            writer.writerow([
                "1",
                "John",
                "Smith",
                "john.smith@company.com",
                "15551234567",
                "Product Owner",
                "Product Management",
                "Experienced product owner.",
                "images/John_Smith_Profile_Picture.png"
            ])
            writer.writerow([
                "2",
                "Suzanne",
                "Que",
                "que@company.com",
                "15559876541",
                "Developer",
                "Quality Assurance",
                "Experienced developer.",
                "images/Suzanne_Que_Profile_Picture.png"
            ])

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_load_users_returns_all_users(self):
        users = services.load_users()

        self.assertEqual(2, len(users))
        self.assertEqual("John", users[0]["first_name"])
        self.assertEqual("Suzanne", users[1]["first_name"])

    def test_get_user_by_id_returns_correct_user(self):
        user = services.get_user_by_id("2")

        self.assertIsNotNone(user)
        self.assertEqual("Suzanne", user["first_name"])
        self.assertEqual("Que", user["last_name"])

    def test_get_user_by_id_returns_none_for_missing_user(self):
        user = services.get_user_by_id("999")

        self.assertIsNone(user)

    def test_update_user_updates_existing_row(self):
        updated_user = {
            "user_id": "1",
            "first_name": "Johnny",
            "last_name": "Smith",
            "email": "johnny.smith@company.com",
            "phone_number": "19998887777",
            "job_title": "Senior Product Owner",
            "department": "Product Strategy",
            "bio": "Updated bio.",
            "profile_picture": "images/John_Smith_Profile_Picture.png"
        }

        services.update_user(updated_user)
        user = services.get_user_by_id("1")

        self.assertEqual("Johnny", user["first_name"])
        self.assertEqual("johnny.smith@company.com", user["email"])
        self.assertEqual("Senior Product Owner", user["job_title"])
        self.assertEqual("Updated bio.", user["bio"])

    def test_ensure_users_csv_exists_creates_file_with_header(self):
        os.remove(self.test_users_file)

        services.ensure_users_csv_exists()

        self.assertTrue(os.path.exists(self.test_users_file))

        with open(self.test_users_file, newline="", encoding="utf-8") as file:
            reader = csv.reader(file)
            header = next(reader)

        self.assertEqual([
            "user_id",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "job_title",
            "department",
            "bio",
            "profile_picture"
        ], header)


if __name__ == "__main__":
    unittest.main()