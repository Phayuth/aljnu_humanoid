from pymodbus.client import ModbusSerialClient
import yaml
import time


class LiftDriver:

    def __init__(self):
        self.p = self.load_parameters()

        self.client = ModbusSerialClient(
            port="/dev/ttyUSB0",
            baudrate=self.p["BAUD_RATE"],
            parity=self.p["PARITY"],
            stopbits=self.p["STOP_BITS"],
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

    def read(self, address, count=1):
        result = self.client.read_holding_registers(
            address=address,
            count=count,
            device_id=self.p["SLAVE_ADDRESS"],
        )
        if not result.isError():
            return result.registers
        else:
            print(f"Error reading address {address}")
            return None

    def write(self, address, value):
        return self.client.write_register(
            address=address,
            value=value,
            device_id=self.p["SLAVE_ADDRESS"],
        )

    def control_to_position(self, position):
        # command desired
        self.write(self.p["COMMAND_M1_POSITION_REGISTER"], position)

        # trigger action
        self.write(
            self.p["TRIGGER_REGISTER"], self.p["TRIGGER_DATA_M1_POSITION_CONTROL"]
        )

    def jog_up(self):
        self.write(
            self.p["TRIGGER_REGISTER"], self.p["TRIGGER_DATA_M1_EXTENDS_JOG"]
        )

    def jog_down(self):
        self.write(
            self.p["TRIGGER_REGISTER"], self.p["TRIGGER_DATA_M1_RETRACTS_JOG"]
        )

    def stop(self):
        self.write(self.p["TRIGGER_REGISTER"], self.p["TRIGGER_DATA_M1M2_STOP"])

    def control_full_extend(self):
        self.write(
            self.p["TRIGGER_REGISTER"],
            self.p["TRIGGER_DATA_M1M2_EXTENDS_UPPER_LIMIT"],
        )

    def control_full_retract(self):
        self.write(
            self.p["TRIGGER_REGISTER"],
            self.p["TRIGGER_DATA_M1M2_RETRACTS_LOWER_LIMIT"],
        )

    def get_position(self):
        value = self.read(self.p["M1_POSITION"], count=1)
        print(f"Current Position: {value}")
        return value

    def get_actuator_commands(self):
        cmddata = {
            "M1_CURRENT_LIMIT_EXTEND": None,
            "M1_CURRENT_LIMIT_RETRACT": None,
            "M1_PWM_EXTEND": None,
            "M1_PWM_RETRACT": None,
            "M1_STROKE_LIMIT": None,
            "M1_VIRTUAL_UPPER_LIMIT": None,
            "M1_VIRTUAL_LOWER_LIMIT": None,
            "M1_SOFTSTART_EXTEND": None,
            "M1_SOFTSTART_RETRACT": None,
            "M1_SOFTSTOP_EXTEND": None,
            "M1_SOFTSTOP_RETRACT": None,
            "M1_DEACCEL_UPPERSTROKE_LIMIT": None,
            "M1_DEACCEL_LOWERSTROKE_LIMIT": None,
            "TERMINATION_RESISTOR": None,
        }
        for key in cmddata.keys():
            value = self.read(self.p[key], count=1)
            cmddata[key] = value
            print(f"{key}: {value}")

        return cmddata

    def get_actuator_status(self):
        stsdata = {
            "MEASURED_INPUT_VOLTAGE": None,
            "M1_MEASURED_CURRENT": None,
            "M1_POSITION": None,
            "M1_STATUS": None,
            "MEASURED_TEMPERATURE_DRIVER": None,
        }
        stsbitdata = [
            "MOVING_IN_EXTEND_DIRECTION",
            "MOVING_IN_RETRACT_DIRECTION",
            "STOP_AT_UPPER_LIMIT",
            "STOP_AT_LOWER_LIMIT",
            "OVER_TEMPERATURE",
            "OVER_VOLTAGE",
            "UNDER_VOLTAGE",
            "RESERVED",
            "OVER_CURRENT",
            "STALL",
            "RESERVED_0",
            "RESERVED_1",
            "RESERVED_2",
            "RESERVED_3",
            "RESERVED_4",
            "RESERVED_5",
        ]

        for key in stsdata.keys():
            value = self.read(self.p[key], count=1)
            stsdata[key] = value
            print(f"{key}: {value}")

        binvalue = format(stsdata["M1_STATUS"][0], "016b")
        for i, bit in enumerate(reversed(binvalue)):
            print(f"{stsbitdata[i]}: {bit}")

        return stsdata, stsbitdata

    def get_service_data(self):
        srvdata = {
            "M1_TOTAL_EXTEND_COUNT": None,
            "M1_TOTAL_RETRACT_COUNT": None,
            "M1_TOTAL_TIME_ONLINE": None,
            "DRIVER_HIHEST_TEMPERATURE": None,
            "DRIVER_LOWEST_TEMPERATURE": None,
            "DRIVER_TOTAL_OVER_TEMPERATURE_PROTECTIONS_COUNT": None,
            "DRIVER_TOTAL_OVER_VOLTAGE_PROTECTIONS_COUNT": None,
            "DRIVER_TOTAL_UNDER_VOLTAGE_PROTECTIONS_COUNT": None,
            "M1_TOTAL_OVER_CURRENT_PROTECTIONS_EXTEND_COUNT": None,
            "M1_TOTAL_OVER_CURRENT_PROTECTIONS_RETRACT_COUNT": None,
            "M1_TOTAL_EXTEND_STALLS_COUNT": None,
            "M1_TOTAL_RETRACT_STALLS_COUNT": None,
            "M1_TOTAL_EXTEND_RETRACT_DISTANCE": None,
            "M1_TOTAL_LOW_TEMPERATURE_OPERATIONS_COUNT": None,
        }

        for key in srvdata.keys():
            value = self.read(self.p[key][0], count=self.p[key][1])
            srvdata[key] = value
            print(f"{key}: {value}")
        return srvdata


if __name__ == "__main__":
    lift = LiftDriver()
    lift.connect()

    lift.get_position()

    # must call stop before issuing new commands
    lift.stop()

    # lift.jog_up()
    # lift.jog_down()
    # time.sleep(10)
    # lift.stop()
    # lift.control_to_position(75)
    # lift.control_full_extend()
    # lift.control_full_retract()
    # lift.get_actuator_commands()
    # lift.get_actuator_status()
    # lift.get_service_data()

    lift.disconnect()
