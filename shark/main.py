#!/usr/bin/env python3
from neo4j import GraphDatabase
import argparse, pyshark

class HelloWorldExample:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def add_link(self, src_mac, dst_mac,
            link_type=None, src_ip=None, dst_ip=None, src_ipv6=None, dst_ipv6=None):
        with self.driver.session() as session:
            greeting = session.write_transaction(self._add_link, src_mac, dst_mac,
                    link_type, src_ip, dst_ip, src_ipv6, dst_ipv6)
            # print(greeting)
    @staticmethod
    def _create_and_return_greeting(tx, message):
        result = tx.run("CREATE (a:Greeting) "
                        "SET a.message = $message "
                        "RETURN a.message + ', from node ' + id(a)", message=message)
    @staticmethod
    def _add_link(tx, src_mac, dst_mac, link_type=None,
            src_ip=None, dst_ip=None, src_ipv6=None, dst_ipv6=None):
        cypher = 'MERGE (src:Host {mac: $src_mac}) '
        if src_ip is not None or src_ipv6 is not None:
            if src_ip is not None:
                cypher += f"ON MATCH SET src.ip = '{src_ip}' "
            else:
                cypher += f"ON MATCH SET src.ipv6 = '{src_ipv6}' "
        cypher += 'MERGE (dst:Host {mac: $dst_mac}) '
        if dst_ip is not None or dst_ipv6 is not None:
            if dst_ip is not None:
                cypher += f"ON MATCH SET dst.ip = '{dst_ip}' "
            else:
                cypher += f"ON MATCH SET dst.ipv6 = '{dst_ipv6}' "
        cypher += "CREATE (src)-[:" + link_type + " { created_at: datetime({timezone: '+08:00'}) }]->(dst)"
        result = tx.run(cypher, src_mac=src_mac, dst_mac=dst_mac)
        # return result.single()[0]

def main(interface):
    capture = pyshark.LiveCapture(interface=interface)
    capture.set_debug()

    # neo4j
    greeter = HelloWorldExample("bolt://localhost:7687", "neo4j", "neo4jneo4j")
    def print_callback(pkt):
        print('Just arrived')
        src_mac = pkt.eth.src
        dst_mac = pkt.eth.dst
        link_type = 'unknown'
        src_ip = None
        dst_ip = None
        src_ipv6 = None
        dst_ipv6 = None
        # print((pkt.layers))
        # print('IPV6' in pkt)
        # if len(pkt.get_multiple_layers('ip')) > 0:
        if 'UDP' in pkt:
            link_type = 'udp'
        elif 'TCP' in pkt:
            link_type = 'tcp'
        else:
            link_type = pkt.layers[-1].layer_name
        if 'IP' in pkt:
            src_ip = pkt.ip.src
            dst_ip = pkt.ip.dst
        elif 'IPV6' in pkt:
            src_ipv6 = pkt.ipv6.src
            dst_ipv6 = pkt.ipv6.dst
        print(f'{src_mac} -> {dst_mac}')
        greeter.add_link(src_mac, dst_mac, link_type, src_ip, dst_ip, src_ipv6, dst_ipv6)
        # greeter.print_greeting("hello, world")
    # run forever
    try:
        capture.apply_on_packets(print_callback)
    except KeyboardInterrupt:
        print()
        greeter.close()
        print('Exit')

if __name__ == '__main__':
    pser = argparse.ArgumentParser()
    pser.add_argument('-i', '--interface', required=True, help='network interface name')
    args = pser.parse_args()
    main(args.i)
