from locust import HttpUser, task


class Tests(HttpUser):

    @task
    def is_prime_test(self):
        self.client.get(url='prime/147')

    @task(1)
    def invert_picture_test(self):
        in_file = open('lena.png', 'rb')
        data = in_file.read()
        self.client.post(url='picture/invert', files={'img': data})

    @task(2)
    def user_test(self):
        self.client.get(url='user/time', headers={"username": "test", "password": "test"})

