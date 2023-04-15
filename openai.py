import requests

class ChatOpenaiAPIClient:
    def __init__(self, api_key=None, email=None, password=None):
        self.api_key = api_key
        self.session = requests.Session()
        if email and password:
            self.login(email, password)

    def login(self, email, password):
        url = "https://api.openai.com/v1/auth/login"
        data = {"email": email, "password": password}
        response = self.session.post(url, json=data)
        if response.status_code == 200:
            self.api_key = response.json().get("api_key")
            print("Login successful.")
        else:
            print("Login failed. Please check your credentials.")

    def get_response(self, prompt, model, max_tokens=16, temperature=0.5, n=1):
        url = "https://api.openai.com/v1/engines/{}/completions".format(model)
        headers = {"Authorization": "Bearer {}".format(self.api_key)}
        data = {
            "prompt": prompt,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "n": n
        }
        response = self.session.post(url, headers=headers, json=data)
        if response.status_code == 200:
            return response.json()
        else:
            print("Failed to generate response. Error code: ", response.status_code)
