class User:
    #
    # User Entity Class
    #
    # Endpoints
    # - Create User: Creates a new user
    # - View User: View details about an existing user
    # - Update User: Updates an existing user
    # - Delete User: Deletes an existing user
    #
    def __init__(self, username: str, first_name: str, last_name: str, table_number: int, user_id = int()):
        self.user_id = user_id
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.table_number = table_number
    def create_user(self):
        endpoint = "/api/v1/users"
        method = 'POST'
        body = {
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "table_number": self.table_number
        }