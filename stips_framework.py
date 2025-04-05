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

    
    def _make_request(self, params: dict) -> dict:
        """
        Makes a request to Stips with the input parameters and returns a parsed json response
            
            Parameters:
                params: The parameters of the request
            
            Returns:
                The response of the server
        """
        response = self.session.get(URL, params=params)

        print(response.status_code)
        print(response.text)

        return json.loads(response.text)
    

    def send_message(self, user_id : int, message : str) -> int:
        """
        Sends a message to a user

            Parameters:
                user_id: The id of the user
                message: The message to send

            Returns:
                The id of the message which was sent (0 if failed)
        """
        params = {
            "name": "messages.send",
            "api_params": json.dumps({"touserid": user_id, "msg": message})}
        
        res = self._make_request(params)

        return res["data"]["newid"]


    def login(self, email : str, password : str) -> bool:
        """
        Logs in to a user

            Parameters:
                email: The email of the user
                password: The password of the user

            Returns:
                Whether or not it was successful
        """
        params = {
            "name": "user.login",
            "api_params": json.dumps({"email": email, "password": password, "auth_token": ""})}
        
        res = self._make_request(params)
        
        return res["data"]["logged"]


    def logout(self) -> bool:
        """
        Logs out

            Returns:
                Whether or not it was successful
        """
        params = {
            "name": "user.logout",
            "api_params": json.dumps({})}
        
        res = self._make_request(params)

        return res["data"]["success"]
