from pyevsim.behavior_model_executor import BehaviorModelExecutor
import zmq

class ZeroMQPubSub(BehaviorModelExecutor):
    def __init__(self, inst_t, dest_t, mname, ename, pub_addr, sub_addr, sub_filter=None):
        super().__init__(inst_t, dest_t, mname, ename)
        self.init_state("Wait")
        self.insert_state("Wait", Infinite)
        self.insert_state("Publish", 1)
        self.insert_input_port("data_in")
        self.insert_output_port("data_out")
        
        self.pub_addr = pub_addr
        self.sub_addr = sub_addr
        self.sub_filter = sub_filter
        
        # ZeroMQ 컨텍스트 생성
        self.context = zmq.Context()
        
        # Publisher 소켓 생성
        self.pub_socket = self.context.socket(zmq.PUB)
        self.pub_socket.bind(self.pub_addr)
        
        # Subscriber 소켓 생성
        self.sub_socket = self.context.socket(zmq.SUB)
        self.sub_socket.setsockopt(zmq.SUBSCRIBE, self.sub_filter or "")
        self.sub_socket.connect(self.sub_addr)

    def ext_trans(self, port, msg):
        if port == "data_in":
            self._cur_state = "Publish"
        
    def output(self):
        if self._cur_state == "Publish":
            self.pub_socket.send_json(msg)
        
    def int_trans(self):
        if self._cur_state == "Publish":
            self._cur_state = "Wait"
        else:
            self._cur_state = "Wait"
    
    def time_advance(self):
        return self.next_internal - self.time_advance()    
