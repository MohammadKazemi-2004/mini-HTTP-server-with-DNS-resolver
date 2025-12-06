'''
from dnslib import DNSRecord, RR, QTYPE, A
import socketserver

DNS_table = {
    'nwtest1.local' : '192.168.1.50'
}

class DNS_handler(socketserver.BaseRequestHandler):
    def handle(self):
        print('start')
        data, sock = self.request[0], self.request[1] # data = header + question + answer
        # print(f'data = {data}')
        request = DNSRecord.parse(data)
        print(request)
        qname = str(request.q.qname)
        
        if qname in DNS_table:
            reply = request.reply()
            
            reply.add_answer(
                RR(
                    rname=qname,
                    rtype=QTYPE.A,
                    rclass=1,
                    rdata=A(DNS_table[qname]),
                    ttl=2
                    
                )
            )
        sock.sendto(reply.pack(), self.client_address)
        
        
if __name__ == '__main__':
    server = socketserver.UDPServer(('127.0.0.1',53),DNS_handler)
    print("UDP server is running on port 53 of '127.0.0.1' ...")
    server.serve_forever()



'''
from dnslib import DNSRecord, RR, QTYPE, A
import socketserver

DNS_table = {
    'nwtest.ir': '127.0.0.1',
}

class DNS_handler(socketserver.BaseRequestHandler):
    def handle(self):
        try:
            data, sock = self.request
            request = DNSRecord.parse(data)
            qname = str(request.q.qname).rstrip('.')  # Remove trailing dot
            
            print(f"DNS query for: {qname}")
            
            if qname in DNS_table:
                reply = request.reply()
                reply.add_answer(
                    RR(
                        rname=qname,
                        rtype=QTYPE.A,
                        rclass=1,
                        rdata=A(DNS_table[qname]),
                        ttl=300
                    )
                )
                print(f"Responding with: {DNS_table[qname]}")
            else:
                # Send NXDOMAIN response for unknown domains
                reply = request.reply()
                reply.header.rcode = 3  # NXDOMAIN
                # print(f"Domain not found: {qname}")
            
            sock.sendto(reply.pack(), self.client_address)
            
        except Exception as e:
            print(f"Error handling request: {e}")

if __name__ == '__main__':
    try:
        # Use port 53 (requires admin/root privileges)
        server = socketserver.UDPServer(('127.0.0.1', 53), DNS_handler)
        print("UDP server is running on port 53 of '127.0.0.1' ...")
        server.serve_forever()
    except PermissionError:
        print("Error: Need administrator/root privileges to bind to port 53")
        print("Alternatively, you can:")
        print("1. Run with sudo (Linux/Mac) or as Administrator (Windows)")
        print("2. Or change to a higher port number and configure DNS manually")