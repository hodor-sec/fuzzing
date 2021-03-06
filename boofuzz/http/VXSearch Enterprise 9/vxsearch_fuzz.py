#!/usr/bin/env python
# Designed for use with boofuzz v0.0.9
from boofuzz import *
import sys, time

host = '192.168.252.10'
port = 80
program = 'vxsrchs.exe'

def banner(sock):
    sock.recv(1024)

def main():
    start_cmd = ['C:\\Program Files (x86)\\VX Search Enterprise\\bin\\' + program]
    session = Session(
    	target = Target(
	    connection = SocketConnection(host, port, proto='tcp'),
            procmon = pedrpc.Client(host, 26002),
            procmon_options = {
                "proc_name" : program,
                "stop_commands" : ['wmic process where (name="' + program + '") delete'],
                "start_commands" : [start_cmd],
            },
	),
        session_filename = "vxsearch.session",
    )

    s_initialize(name="Request")
    with s_block("Request-Line"):
        s_static("POST /login HTTP/1.1\r\n")
        s_static('Host: ' + host + ":" + str(port) + "\r\n")
        s_static("User-Agent: hodorweb\r\n")
        s_static("Connection: close\r\n")
        s_static("Content-Length: 10000\r\n\r\n")
        s_static("username=")
        s_string("admin", name='username')
        s_static("&password=")
        s_string("1234", name='password')
        s_static("\r\n")
        s_static("\r\n", "Request-CRLF")
    session.connect(s_get("Request"))
    session.fuzz()


if __name__ == "__main__":
    main()

