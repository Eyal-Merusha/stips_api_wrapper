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

    
    def _make_get_request(self, params: dict) -> dict:
        """
        Makes a get request to Stips with the input parameters and returns a parsed json response
            
            Parameters:
                params: The parameters of the request
            
            Returns:
                The response of the server
        """
        response = self.session.get(URL, params=params)

        return json.loads(response.text)
    

    def _make_post_request(self, params: dict) -> dict:
        """
        Makes a post request to Stips with the input parameters and returns a parsed json response
            
            Parameters:
                params: The parameters of the request
            
            Returns:
                The response of the server
        """
        response = self.session.post(URL, params=params)

        return json.loads(response.text)


    def send_private_message(self, user_id : int, message : str) -> dict:
        """
        Sends a message to a user

            Parameters:
                user_id: The id of the user
                message: The message to send

            Returns:
                The servers response as a dict
        """
        params = {
            "name": "messages.send",
            "api_params": json.dumps({"touserid": user_id, "msg": message})}
        
        res = self._make_get_request(params)

        return res


    def login(self, email : str, password : str) -> dict:
        """
        Logs in to a user

            Parameters:
                email: The email of the user
                password: The password of the user

            Returns:
                The servers response as a dict
        """
        params = {
            "name": "user.login",
            "api_params": json.dumps({"email": email, "password": password, "auth_token": ""})}
        
        res = self._make_get_request(params)
        
        return res


    def logout(self) -> dict:
        """
        Logs out

            Returns:
                The servers response as a dict
        """
        params = {
            "name": "user.logout",
            "api_params": json.dumps({})}
        
        res = self._make_get_request(params)

        return res
    
    
    def username_to_id(self, username: str) -> int:
        """
        Finds id of a user

            Parameters:
                username: The username of the user

            Returns:
                The id of the user
        """
        params = {
            "name": "smartdata.get",
            "api_params": json.dumps({"namespace":"users","unit":"Search","q":username})}
        
        res = self._make_get_request(params)

        profiles = res["data"]["results"]["profiles"]

        if profiles:
            for profile in profiles:
                if profile["nickname"].lower() == username.lower():
                    return profiles[0]["userid"]
        return -1
        

    def post_message(self, message: str) -> dict:
        """
        Posts a message in pen friends

            Parameters:
                message: The message to post

            Returns:
                The servers response as a dict
        """
        params = {
            "name": "omniobj",
            "rest_action": "PUT",
            "omniobj": json.dumps({"data":{"msg": message},"objType":"penfriendsitem"})}
        
        res = self._make_post_request(params)

        return res
