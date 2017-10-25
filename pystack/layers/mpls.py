from scapy.contrib.mpls import MPLS

from pystack.layers.layer import Layer


class MPLSProtocol(Layer):

    name = "MPLS"

    def __init__(self, interface=None):
        Layer.__init__(self)

    def packet_received(self, packet, **kwargs):
        name = packet.payload.name
        target = self.upperLayers.get(name, self.upperLayers["default"])
        kwargs["MPLS"] = packet.fields
        target.packet_received(packet.payload,**kwargs)

    def send_packet(self, packet, **kwargs):
        if not kwargs.has_key("MPLS"):
            kwargs["MPLS"] = {}
        if not kwargs["MPLS"].has_key("ttl"):
            kwargs["MPLS"]["ttl"] = 64
        if not kwargs["MPLS"].has_key("s"):
            kwargs["MPLS"]["s"] = 1
        if not kwargs["MPLS"].has_key("label"):
            kwargs["MPLS"]["label"] = 0

        self.transfer_packet(self.forge_packet(packet,**kwargs["MPLS"]),**kwargs)

    def forge_packet(self, packet, **kwargs):
        return MPLS(**kwargs) / packet