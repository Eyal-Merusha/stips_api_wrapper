import requests, json


URL = "https://stips.co.il/api"


class stips:
    def __init__(self):
        self.session = requests.Session()
    

    def __del__(self):
        if self.session:
            self.session.close()


    def __enter__(self):
        self.session = requests.Session()
        return self


    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            self.session.close()

    
    def _make_request(self, params: dict):
        response = self.session.get(URL, params=params)

        print(response.status_code)
        print(response.text)
    

    def send_message(self, user_id : int, message : str):
        params = {
            "name": "messages.send",
            "api_params": json.dumps({"touserid": user_id, "msg": message})}
        
        self._make_request(params)


    def login(self, email : str, password : str):
        params = {
            "name": "user.login",
            "api_params": json.dumps({"email": email, "password": password, "auth_token": ""})}
        
        self._make_request(params)


    def logout(self):
        params = {
            "name": "user.logout",
            "api_params": json.dumps({})}
        
        self._make_request(params)
