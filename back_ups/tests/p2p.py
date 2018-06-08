from uuid import uuid4
generate_nodeid = str(uuid4())

print(generate_nodeid)

from twisted.internet.endpoints import TCP4ServerEndpoint
from twisted.internet.protocol import Protocol, Factory
from twisted.internet import reactor

class MyProtocol(Protocol):
    def __init__(self, factory):
        self.factory = factory
        self.nodeid = self.factory.nodeid

class MyFactory(Factory):
    def startFactory(self):
        self.peers = {}
        self.nodeid = generate_nodeid()

    def buildProtocol(self, addr):
        return NCProtocol(self)
        
endpoint = TCP4ServerEndpoint(reactor, 5999)
endpoint.listen(MyFactory())