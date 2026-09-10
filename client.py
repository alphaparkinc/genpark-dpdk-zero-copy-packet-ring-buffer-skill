class DPDKRingBuffer:
    """
    Lockless MPMC Ring Buffer inspired by DPDK rte_ring architecture
    for ultra-low latency packet burst pipelines.
    """
    def __init__(self, capacity=16):
        self.capacity = capacity
        self.ring = [None] * capacity
        self.prod_head = 0
        self.prod_tail = 0
        self.cons_head = 0
        self.cons_tail = 0

    def enqueue_burst(self, packets):
        free_entries = self.capacity - (self.prod_head - self.cons_tail)
        n = min(len(packets), free_entries)
        if n == 0:
            return 0
        for i in range(n):
            idx = (self.prod_head + i) % self.capacity
            self.ring[idx] = packets[i]
        self.prod_head += n
        self.prod_tail += n
        return n

    def dequeue_burst(self, max_pkts):
        avail = self.prod_tail - self.cons_head
        n = min(max_pkts, avail)
        if n == 0:
            return []
        res = []
        for i in range(n):
            idx = (self.cons_head + i) % self.capacity
            res.append(self.ring[idx])
            self.ring[idx] = None
        self.cons_head += n
        self.cons_tail += n
        return res
