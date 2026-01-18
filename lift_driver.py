from pymodbus.client import ModbusSerialClient
import yaml


class LiftDriver:

    def __init__(self):
        self.param = self.load_parameters()

        self.client = ModbusSerialClient(
            port="/dev/ttyUSB0",
            baudrate=self.param["BAUD_RATE"],
            parity=self.param["PARITY"],
            stopbits=self.param["STOP_BITS"],
            bytesize=8,
            timeout=1,
        )

    def load_parameters(self):
        param = "./lift_param.yaml"
        with open(param, "r") as file:
            param = yaml.safe_load(file)
        return param

    def connect(self):
        self.client.connect()

    def disconnect(self):
        self.client.close()

    def read(self, address, count=1, slave=1):
        return self.client.read_holding_registers(address, count, slave=slave)

    def write(self, address, value, slave=1):
        return self.client.write_register(address, value, slave=slave)

    def control_to_position(self, position):
        # command desired
        self.write(self.param["COMMAND_M1_POSITION_REGISTER"], position)

        # trigger action
        self.write(self.param["TRIGGER_M1_POSITION_COMMAND_REGISTER"], 1)

    def jog_up(self):
        pass

    def jog_down(self):
        pass

    def stop(self):
        pass

    def control_full_extend(self):
        pass

    def control_full_retract(self):
        pass

    def get_position(self):
        pass

    def get_status(self):
        pass


if __name__ == "__main__":
    lift = LiftDriver()
    lift.connect()
    lift.disconnect()
