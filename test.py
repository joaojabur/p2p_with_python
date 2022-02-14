import base64

data: str = "Hello world!"

encoded = base64.b64encode(data.encode('utf-8'))
print(encoded)

decoded = base64.b64decode(encoded)
print(decoded.decode('utf-8'))