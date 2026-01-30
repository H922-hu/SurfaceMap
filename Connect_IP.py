import socket, sys, ftplib
with open('alive_ips.txt') as f:
    for line in f:
        try:
            ip, port = line.strip().split(':')
            s = socket.socket()
            s.settimeout(2)
            if s.connect_ex((ip, int(port))) == 0:
                try:
                    ftp = ftplib.FTP()
                    ftp.connect(ip, int(port), timeout=3)
                    ftp.login('anonymous', '')
                    print(f'✓ {ip}:{port} - Anonymous OK')
                    ftp.quit()
                except:
                    print(f'✗ {ip}:{port} - No anonymous access')
            s.close()
        except:
            pass
