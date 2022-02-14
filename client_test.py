from peer import Peer
from argparse import ArgumentParser

if __name__ == "__main__":
    parser = ArgumentParser(description="Program to test peers.")
    
    parser.add_argument("host", default="127.0.0.1", type=str, help="Ip address the peer runs at (default 127.0.0.1).")
    parser.add_argument("-p", metavar="PORT", type=int, help="Port the peer run at.")
    parser.add_argument("-pS", metavar="PORTSERVER", type=int, help="Port the server listens at.")

    args = parser.parse_args()
    peer = Peer(1, args.host, args.p, args.pS)