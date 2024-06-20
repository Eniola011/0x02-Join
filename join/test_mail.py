import requests

def send_simple_message():
    return requests.post(
        "https://api.mailgun.net/v3/sandboxc91f0dc44721473f99911c9a2ae3f8de.mailgun.org/messages",
        auth=("api", "488491dcaced3fe9954f8a4a714e68de-6fafb9bf-9fe95044"),
        data={
            "from": "Excited User <mailgun@sandboxc91f0dc44721473f99911c9a2ae3f8de.mailgun.org>",
            "to": ["eniolaagbalu@gmail.com", "YOU@sandboxc91f0dc44721473f99911c9a2ae3f8de.mailgun.org"],
            "subject": "Hello",
            "text": "Testing some Mailgun awesomeness!"
        })

response = send_simple_message()
print(response.status_code)
print(response.json())
