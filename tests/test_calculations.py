import os
import shutil
import tempfile
import unittest
import pandas as pd

# Import the calculation functions being tested
from app.calculations import (
    calculate_total_requirements,
    calculate_completed_requirements,
    calculate_open_risk_count,
)


class TestCalculations(unittest.TestCase):
    """
    Unit tests for calculation functions used in the dashboard.
    These tests validate correctness, edge case handling, and robustness
    against inconsistent or messy CSV data.
    """

    def setUp(self):
        """
        Create a temporary working directory for each test.
        This prevents tests from modifying real project data.
        """
        self.test_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()

        # Switch to temporary directory
        os.chdir(self.test_dir)

        # Create expected data folder structure
        os.makedirs("data", exist_ok=True)

    def tearDown(self):
        """
        Restore original working directory and remove temp files after each test.
        """
        os.chdir(self.original_cwd)
        shutil.rmtree(self.test_dir)

    def test_calculate_total_requirements_returns_zero_when_file_missing(self):
        """
        Verify function returns 0 when requirements.csv does not exist.
        """
        self.assertEqual(calculate_total_requirements(), 0)

    def test_calculate_total_requirements_counts_unique_ids(self):
        """
        Verify that duplicate requirement IDs are only counted once.
        """
        requirements = pd.DataFrame([
            {"requirement_id": "1", "requirement_type": "Functional", "description": "Login page", "status": "Completed", "priority": "High"},
            {"requirement_id": "2", "requirement_type": "Functional", "description": "Dashboard", "status": "In Progress", "priority": "Medium"},
            {"requirement_id": "2", "requirement_type": "Functional", "description": "Duplicate", "status": "In Progress", "priority": "Medium"},
        ])
        requirements.to_csv("data/requirements.csv", index=False)

        self.assertEqual(calculate_total_requirements(), 2)

    def test_calculate_completed_requirements_returns_zero_when_file_missing(self):
        """
        Verify function returns 0 when requirements.csv is missing.
        """
        self.assertEqual(calculate_completed_requirements(), 0)

    def test_calculate_completed_requirements_counts_completed(self):
        """
        Verify that only requirements with status 'completed' are counted.
        """
        requirements = pd.DataFrame([
            {"requirement_id": "1", "requirement_type": "Functional", "description": "Login", "status": "Completed", "priority": "High"},
            {"requirement_id": "2", "requirement_type": "Functional", "description": "Dashboard", "status": "completed", "priority": "Medium"},
            {"requirement_id": "3", "requirement_type": "Non-Functional", "description": "Performance", "status": " In Progress ", "priority": "Low"},
        ])
        requirements.to_csv("data/requirements.csv", index=False)

        self.assertEqual(calculate_completed_requirements(), 2)

    def test_calculate_open_risk_count_returns_zero_when_file_missing(self):
        """
        Verify function returns 0 when risks.csv does not exist.
        """
        self.assertEqual(calculate_open_risk_count(), 0)

    def test_calculate_open_risk_count_counts_open_risks(self):
        """
        Verify that only risks marked as 'open' are counted.
        """
        risks = pd.DataFrame([
            {"id": 1, "project_id": 1, "risk_name": "Schedule delay", "risk_priority": "High", "risk_status": "Open"},
            {"id": 2, "project_id": 1, "risk_name": "Scope creep", "risk_priority": "Medium", "risk_status": " open "},
            {"id": 3, "project_id": 1, "risk_name": "Testing issues", "risk_priority": "Low", "risk_status": "Closed"},
        ])
        risks.to_csv("data/risks.csv", index=False)

        self.assertEqual(calculate_open_risk_count(), 2)

    def test_calculate_open_risk_count_returns_zero_when_column_missing(self):
        """
        Verify function returns 0 when required column 'risk_status' is missing.
        """
        risks = pd.DataFrame([
            {"id": 1, "project_id": 1, "risk_name": "Schedule delay", "risk_priority": "High"}
        ])
        risks.to_csv("data/risks.csv", index=False)

        self.assertEqual(calculate_open_risk_count(), 0)

    def test_calculate_completed_requirements_handles_messy_status_values(self):
        """
        Verify normalization handles spaces and capitalization for 'completed'.
        """
        requirements = pd.DataFrame([
            {"requirement_id": "1", "requirement_type": "Functional", "description": "Login", "status": " COMPLETED ", "priority": "High"},
            {"requirement_id": "2", "requirement_type": "Functional", "description": "Dashboard", "status": "completed", "priority": "Medium"},
            {"requirement_id": "3", "requirement_type": "Non-Functional", "description": "Performance", "status": "Completed ", "priority": "Low"},
            {"requirement_id": "4", "requirement_type": "Functional", "description": "Reports", "status": " in progress ", "priority": "Medium"},
        ])
        requirements.to_csv("data/requirements.csv", index=False)

        self.assertEqual(calculate_completed_requirements(), 3)

    def test_calculate_total_requirements_handles_duplicate_ids_and_spaces(self):
        """
        Verify trimming spaces and handling duplicate IDs correctly.
        """
        requirements = pd.DataFrame([
            {"requirement_id": " 1 ", "requirement_type": "Functional", "description": "Login", "status": "Completed", "priority": "High"},
            {"requirement_id": "1", "requirement_type": "Functional", "description": "Duplicate", "status": "Completed", "priority": "High"},
            {"requirement_id": " 2", "requirement_type": "Functional", "description": "Dashboard", "status": "In Progress", "priority": "Medium"},
            {"requirement_id": "2 ", "requirement_type": "Functional", "description": "Duplicate", "status": "In Progress", "priority": "Medium"},
            {"requirement_id": "3", "requirement_type": "Non-Functional", "description": "Performance", "status": "Not Started", "priority": "Low"},
        ])
        requirements.to_csv("data/requirements.csv", index=False)

        self.assertEqual(calculate_total_requirements(), 3)

    def test_calculate_open_risk_count_handles_messy_status_values(self):
        """
        Verify normalization of risk status handles spaces and capitalization.
        """
        risks = pd.DataFrame([
            {"id": 1, "project_id": 1, "risk_name": "Schedule delay", "risk_priority": "High", "risk_status": " OPEN "},
            {"id": 2, "project_id": 1, "risk_name": "Scope creep", "risk_priority": "Medium", "risk_status": "open"},
            {"id": 3, "project_id": 1, "risk_name": "Testing delay", "risk_priority": "Low", "risk_status": "Open "},
            {"id": 4, "project_id": 1, "risk_name": "Resource issue", "risk_priority": "High", "risk_status": " closed "},
        ])
        risks.to_csv("data/risks.csv", index=False)

        self.assertEqual(calculate_open_risk_count(), 3)

    def test_calculate_open_risk_count_handles_mixed_realistic_dataset(self):
        """
        Verify correct counting in a realistic dataset with mixed statuses.
        """
        risks = pd.DataFrame([
            {"id": 1, "project_id": 1, "risk_name": "Schedule delay", "risk_priority": "High", "risk_status": "Open"},
            {"id": 2, "project_id": 1, "risk_name": "Scope creep", "risk_priority": "Medium", "risk_status": " OPEN "},
            {"id": 3, "project_id": 1, "risk_name": "Team availability", "risk_priority": "High", "risk_status": "closed"},
            {"id": 4, "project_id": 1, "risk_name": "Integration issue", "risk_priority": "Low", "risk_status": "In Progress"},
            {"id": 5, "project_id": 1, "risk_name": "Documentation gap", "risk_priority": "Low", "risk_status": " open "},
        ])
        risks.to_csv("data/risks.csv", index=False)

        self.assertEqual(calculate_open_risk_count(), 3)


if __name__ == "__main__":
    unittest.main()