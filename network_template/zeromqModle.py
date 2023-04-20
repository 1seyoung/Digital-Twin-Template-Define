from pyevsim.behavior_model_executor import BehaviorModelExecutor
import zmq

class ZeroMQTemplate(BehaviorModelExecutor):
    def __init__(self, inst_t, dest_t, mname, ename, **kwargs):
        super().__init__(inst_t, dest_t, mname, ename)
        self.init_state("wait")
        self.insert_state("wait", Infinite)
        self.insert_state("send", 1)
        self.insert_input_port("in")
        self.insert_output_port("out")

        # ZeroMQ 소켓 생성
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PUB)
        self.socket.bind(f"tcp://*:5555")

    def ext_trans(self, port, msg):
        if port == "in":
            self._cur_state = "send"

    def output(self):
        if self._cur_state == "send":
            self.socket.send_json({
                "data": "Hello from ZeroMQ template!"
            })

    def int_trans(self):
        if self._cur_state == "send":
            self._cur_state = "wait"
