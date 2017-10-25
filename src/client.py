import time
from pystack.pystack import PyStack
from pystack.layers.tcp_application import TCPApplication
import threading


def client(interface, server_ip, server_port,**kwargs):
    full_stack = PyStack(interface) #Create a stack

    client_app = TCPApplication() #Create a TCPApplication

    full_stack.register_tcp_application(client_app) #Register the application to the stack which will manage to create the TCPSession etc.
    full_stack.run(doreactor = False) #Run the stack to start listening using a thread to make it non-blocking

    if client_app.connect(server_ip, server_port): #Connect to the given server
        print 'connect to server'
        i = 0;
        while True:
            print 'send packet'
            i += 1

            mpls_info = {}
            mpls_info["cos"] = 0L
            mpls_info["ttl"] = 64
            mpls_info["s"] = 1L
            mpls_info["label"] = 1L
            kwargs["MPLS"] =  mpls_info

            client_app.send_packet("{0}:changjiang!".format(i),**kwargs) #Send the request to the server

            time.sleep(1)

        client_app.close()

    print 'can not connect to server'
    full_stack.stop() #Stop the stack

if __name__ == '__main__':

    interface = 'ens38'
    address = '192.168.2.184'
    port = 6688

    client(interface, address, port)