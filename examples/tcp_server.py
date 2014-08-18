#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from enocean.consolelogger import init_logging
from enocean.communicators.tcpcommunicator import TCPCommunicator
from enocean.protocol.constants import PACKET, RORG
import sys
import traceback

try:
    import queue
except ImportError:
    import Queue as queue

init_logging()
tcp = TCPCommunicator()
tcp.start()
while tcp.is_alive():
    try:
        # Loop to empty the queue...
        p = tcp.receive.get(block=True, timeout=1)
        if p.type == PACKET.RADIO and p.rorg == RORG.BS4:
            for k in p.parse_eep(0x02, 0x05):
                print('%s: %s' % (k, p.parsed[k]))
        if p.type == PACKET.RADIO and p.rorg == RORG.BS1:
            for k in p.parse_eep(0x00, 0x01):
                print('%s: %s' % (k, p.parsed[k]))
        if p.type == PACKET.RADIO and p.rorg == RORG.RPS:
            for k in p.parse_eep(0x02, 0x04):
                print('%s: %s' % (k, p.parsed[k]))
    except queue.Empty:
        continue
    except KeyboardInterrupt:
        break
    except Exception:
        traceback.print_exc(file=sys.stdout)
        break

if tcp.is_alive():
    tcp.stop()
