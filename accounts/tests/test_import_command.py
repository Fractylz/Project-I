import os
import tempfile
import pandas as pd
from io import StringIO
from django.test import TestCase
from django.core.management import call_command
from django.conf import settings
from accounts import CustomUser, StudentProfile, SupervisorProfile

class ImportUsersCommandTest(TestCase):
    def setUp(self):
        # Create a temporary directory that will be deleted after the test
        self.temp_dir = tempfile.TemporaryDirectory()
        
        # Flag that we're in a test environment
        settings.TESTING = True
        
    def tearDown(self):
        # Clean up the temporary directory
        self.temp_dir.cleanup()
        
        # Reset the testing flag
        settings.TESTING = False
    
    def create_test_excel(self, data):
        """Helper method to create a test Excel file"""
        # Create a pandas DataFrame
        df = pd.DataFrame(data)
        
        # Create a temporary file path
        file_path = os.path.join(self.temp_dir.name, 'test_import.xlsx')
        
        # Write to Excel
        df.to_excel(file_path, index=False)
        
        return file_path
    
    def test_basic_import(self):
        """Test that the command imports users correctly"""
        # Create test data
        test_data = [
            {
                'username': 'test_user1',
                'email': 'test1@example.com',
                'first_name': 'Test',
                'last_name': 'User1',
                'role': 'student',
                'phone': '123-456-7890',
                'student_id': 'STU001'
            },
            {
                'username': 'test_user2',
                'email': 'test2@example.com',
                'first_name': 'Test',
                'last_name': 'User2',
                'role': 'supervisor',
                'phone': '987-654-3210',
                'campus': 'Test Campus'
            }
        ]
        
        # Create the test file
        excel_path = self.create_test_excel(test_data)
        
        # Count existing users before import
        initial_user_count = CustomUser.objects.count()
        initial_student_count = StudentProfile.objects.count()
        initial_supervisor_count = SupervisorProfile.objects.count()
        
        # Capture output
        out = StringIO()
        
        # Call the management command
        call_command('import_users', excel_path, stdout=out)
        
        # Check that the output contains success messages
        output = out.getvalue()
        self.assertIn('Import Summary', output)
        self.assertIn('Users created/updated: 2', output)
        self.assertIn('Student profiles created: 1', output)
        self.assertIn('Supervisor profiles created: 1', output)
        
        # Check that users were created
        self.assertEqual(CustomUser.objects.count(), initial_user_count + 2)
        self.assertEqual(StudentProfile.objects.count(), initial_student_count + 1)
        self.assertEqual(SupervisorProfile.objects.count(), initial_supervisor_count + 1)
        
        # Check user details
        user1 = CustomUser.objects.get(username='test_user1')
        self.assertEqual(user1.email, 'test1@example.com')
        self.assertEqual(user1.role, 'student')
        
        user2 = CustomUser.objects.get(username='test_user2')
        self.assertEqual(user2.email, 'test2@example.com')
        self.assertEqual(user2.role, 'supervisor')
        
        # Check profile details
        student_profile = StudentProfile.objects.get(user=user1)
        self.assertEqual(student_profile.student_id, 'STU001')
        self.assertEqual(student_profile.phone, '123-456-7890')
        
        supervisor_profile = SupervisorProfile.objects.get(user=user2)
        self.assertEqual(supervisor_profile.campus, 'Test Campus')
        self.assertEqual(supervisor_profile.phone, '987-654-3210')
    
    def test_dry_run(self):
        """Test that dry run doesn't create users"""
        # Create test data
        test_data = [
            {
                'username': 'dry_run_user',
                'email': 'dryrun@example.com',
                'role': 'student',
                'student_id': 'DRY001'
            }
        ]
        
        # Create the test file
        excel_path = self.create_test_excel(test_data)
        
        # Count existing users before import
        initial_user_count = CustomUser.objects.count()
        
        # Call the management command with dry-run flag
        call_command('import_users', excel_path, dry_run=True)
        
        # Check that no users were created
        self.assertEqual(CustomUser.objects.count(), initial_user_count)
        self.assertFalse(CustomUser.objects.filter(username='dry_run_user').exists())
    
    def test_invalid_data(self):
        """Test handling of invalid data"""
        # Create test data with invalid role
        test_data = [
            {
                'username': 'invalid_role_user',
                'email': 'invalid@example.com',
                'role': 'invalid_role',  # Invalid role
                'student_id': 'INV001'
            }
        ]
        
        # Create the test file
        excel_path = self.create_test_excel(test_data)
        
        # Capture output
        out = StringIO()
        
        # Call the management command
        call_command('import_users', excel_path, stdout=out)
        
        # Check that the warning is in the output
        output = out.getvalue()
        self.assertIn("Invalid role 'invalid_role'", output)
        
        # Check that user was created with default role
        user = CustomUser.objects.get(username='invalid_role_user')
        self.assertEqual(user.role, 'student')