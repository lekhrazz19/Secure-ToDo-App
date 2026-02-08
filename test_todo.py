import unittest
from app import app, db, User, Todo

class TestTodo(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['WTF_CSRF_ENABLED'] = False
        self.app = app.test_client()
        with app.app_context():
            db.create_all()
            
            # Create two users
            u1 = User(username='user1')
            u1.set_password('pass')
            u2 = User(username='user2')
            u2.set_password('pass')
            db.session.add_all([u1, u2])
            db.session.commit()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def login(self, username, password):
        return self.app.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def test_add_todo(self):
        self.login('user1', 'pass')
        response = self.app.post('/todos', data=dict(
            title='Buy Milk',
            description='2 liters'
        ), follow_redirects=True)
        self.assertIn(b'Todo added successfully', response.data)
        self.assertIn(b'Buy Milk', response.data)

    def test_access_control(self):
        # User 1 adds a todo
        self.login('user1', 'pass')
        self.app.post('/todos', data=dict(title='User1 Secret', description='shhh'), follow_redirects=True)
        
        with app.app_context():
            todo = Todo.query.first()
            todo_id = todo.id
            
        # User 2 tries to delete User 1's todo
        self.login('user2', 'pass')
        response = self.app.get(f'/delete/{todo_id}', follow_redirects=True)
        
        self.assertIn(b'You do not have permission', response.data)
        
        # Verify it wasn't deleted
        with app.app_context():
            self.assertIsNotNone(db.session.get(Todo, todo_id))

if __name__ == '__main__':
    unittest.main()
