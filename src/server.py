import time
from pystack.pystack import PyStack
from pystack.layers.tcp_application import TCPApplication


def server(interface, port):
    server_stack = PyStack(interface)  # Create a stack
    print '1'

    server_app = TCPApplication()  # Create a TCPApplication

    server_stack.register_tcp_application(server_app)
    server_stack.run(doreactor = False)  # Run the stack to start listening using a thread to make it non-blocking

    server_app.bind(port,server_app,False)

    print '2'
    server_app.listen(3) # the maximum tcp clients to establish connections
    print '3'
    flow_one = server_app.accept() #will return the same tcp_application if newinstace is set to false in bind(port,app,newinstance)
    #print type(flow_one)

    print 'accept client request'

    while True:
        time.sleep(1)
        #flow_one.send_packet('ok')
        data = flow_one.fetch_data()
        if data != None:
            print data


if __name__ == '__main__':

    interface = 'ens38'
    port = 6688

    server(interface, port)