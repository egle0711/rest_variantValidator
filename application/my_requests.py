import requests

class MyRequests:

    def __init__(self):
        self.base_url = None
        self.url = None

    # method that makes the call to the API using the get method
    def request_data(self):
        return requests.get(self.url)

    # method that assembles the url to request data from the hello endpoint
    def hello(self):
        self.url = f"{self.base_url}hello"
        return self.request_data()

    # method that assembles the url to request data from the name endpoint
    def get_name(self, name):
        self.url = f"{self.base_url}name/{name}"
        return self.request_data()

if __name__ == "__main__":
    mrq = MyRequests()
    
    # Set the base url
    mrq.base_url = "http://127.0.0.1:5000/"
    
    # request the data from hello endpoint
    response_hello = mrq.hello()
    print(response_hello.status_code)
    print(response_hello.headers)
    print(response_hello.text)
    
    # request the data from name endpoint
    name = "Egle"
    response_name = mrq.get_name(name)
    print(response_name.status_code)
    print(response_name.headers)
    print(response_name.text)
