import rbpodo as rb
import numpy as np


class ArmDriver:

    def __init__(self, ip):
        self.robot = rb.Cobot(ip)
        self.rc = rb.ResponseCollector()

    def connect(self):
        self.robot.set_operation_mode(self.rc, rb.OperationMode.Simulation)
        self.robot.set_speed_bar(self.rc, 0.5)
        self.robot.flush(self.rc)

    def move_joints(self, joint_deltas, speed=200, acceleration=400):
        self.robot.move_j(self.rc, np.array(joint_deltas), speed, acceleration)
        if (
            self.robot.wait_for_move_started(self.rc, 0.1).type()
            == rb.ReturnType.Success
        ):
            self.robot.wait_for_move_finished(self.rc)
        self.rc.error().throw_if_not_empty()

    def get_joints(self):
        [_, out] = self.robot.get_system_variable(
            self.rc, rb.SystemVariable.SD_J0_ANG
        )
        self.rc.error().throw_if_not_empty()
        return out


if __name__ == "__main__":
    LEFT_ROBOT_IP = "10.0.2.7"
    RIGHT_ROBOT_IP = "10.0.2.8"

    left_arm = ArmDriver(LEFT_ROBOT_IP)
    left_arm.connect()
    left_arm.move_joints([10, 0, 0, 0, 0, 0])

    right_arm = ArmDriver(RIGHT_ROBOT_IP)
    right_arm.connect()
    right_arm.move_joints([-10, 0, 0, 0, 0, 0])
