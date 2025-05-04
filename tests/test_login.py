import unittest
from database.crud import login_permission, create_new_user
from database.connection import Session
from database.models import User, Admin
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class TestLogin(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Create a test database in memory
        cls.engine = create_engine('sqlite:///:memory:')
        cls.TestSession = sessionmaker(bind=cls.engine)
        cls.session = cls.TestSession()
        
        # Create all tables in the test database
        from database.models import Base
        Base.metadata.create_all(cls.engine)
        
        # Create a test admin user
        create_new_user(
            cls.session, 
            'test_admin', 
            'test_lastname',
            '1234567890',
            '9876543210',
            'admin',
            'testadmin',
            'testpass123'
        )

    def test_successful_login(self):
        """Test login with correct credentials"""
        result = login_permission(self.session, 'testadmin', 'testpass123')
        self.assertTrue(result, "Login should succeed with correct credentials")

    def test_wrong_password(self):
        """Test login with incorrect password"""
        result = login_permission(self.session, 'testadmin', 'wrongpassword')
        self.assertFalse(result, "Login should fail with incorrect password")


    @classmethod
    def tearDownClass(cls):
        # Clean up the test database
        cls.session.close()
        from database.models import Base
        Base.metadata.drop_all(cls.engine)

if __name__ == '__main__':
    unittest.main()