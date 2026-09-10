from client import DPDKRingBuffer

def main():
    print("=== Testing DPDK Zero-Copy Packet Ring Buffer ===")
    ring = DPDKRingBuffer(capacity=8)
    pkts = [{"id": i, "size": 64 + i*16} for i in range(5)]
    enq = ring.enqueue_burst(pkts)
    print(f"Enqueued {enq} packets into DPDK ring.")
    assert enq == 5

    deq = ring.dequeue_burst(10)
    print(f"Dequeued {len(deq)} packets: {deq}")
    assert len(deq) == 5
    print("=== All tests passed successfully! ===")

if __name__ == "__main__":
    main()
