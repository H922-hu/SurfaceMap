import socket
s = socket.socket()
s.settimeout(2)
result = s.connect_ex(('112.203.250.208', 21))
print('Open Target' if result == 0 else 'Closed')
s.close()
