class Arm_Device(object):
    def __init__(self):
        self.addr = 0x15
        self.hpattern = ['┌', '─', '┐', '│']
        self.lpattern = ['─', '┘', '└', '┴']

    def print_i2c_block_data(self, address, register, data, inc_scl=True, inc_sda=True, inc_bits=True,
                             inc_add_data=True):
        i2c_bits_msg = f"s {address:08b} w a {register:08b} a {data[0]:08b} a {data[1]:08b} a {data[2]:08b} a {data[3]:08b} a p"
        i2c_adr_data_msg = f"s 0x{address:02x} w a 0x{register:02x} a 0x{data[0]:02x} a 0x{data[1]:02x} a 0x{data[2]:02x} a 0x{data[3]:02x} a p"

        print(i2c_bits_msg.replace(' ', '') + "\n")

        if inc_scl:
            offset_l1 = " " * 5
            offset_h1 = " " * 2
            len_signal = len(i2c_bits_msg.replace(' ', '')) - 2
            scl_h = f"{self.hpattern[1] * 5}{self.hpattern[2]}{offset_h1}" + f"{self.hpattern[0]}{self.hpattern[1]}{self.hpattern[2]} " * len_signal + \
                    f"{self.hpattern[0]}{self.hpattern[1] * 3}"
            scl_l = f"{offset_l1}{self.lpattern[2]}{self.lpattern[0] * 2}" + f"{self.lpattern[1]} {self.lpattern[2]}{self.lpattern[0]}" * len_signal + \
                    self.lpattern[1]
            print(f"scl: {scl_h}\n     {scl_l}")

        if inc_sda:
            scl_l = ''
            scl_h = ''
            old_cr = ''
            to_up = False
            to_down = False
            for cr in i2c_bits_msg.replace(' ', ''):
                if old_cr == '':
                    old_cr = cr
                if cr == 'w':
                    cr = '0'
                elif cr == 'r':
                    cr = '1'
                if old_cr != cr:
                    if old_cr == '1':
                        to_down = True
                    elif old_cr == '0':
                        to_up = True
                    old_cr = cr
                if cr == 's':
                    scl_h += f"{self.hpattern[1] * 3}{self.hpattern[2]} "
                    scl_l += f"   {self.lpattern[2]}{self.lpattern[0]}"
                if cr == 'p':
                    pass
                if cr == '0':
                    scl_l += self.lpattern[2] if to_down else self.lpattern[0]
                    scl_l += self.lpattern[0]
                    scl_l += self.lpattern[1] if to_up else self.lpattern[0]
                    scl_h += self.hpattern[2] if to_down else ' '
                    scl_h += ' ' * 2
                    if to_up:
                        to_up = False
                    if to_down:
                        to_down = False
                if cr == '1':
                    scl_l += self.lpattern[1] if to_up else ' '
                    scl_l += ' ' * 2
                    scl_h += self.hpattern[0] if to_up else self.hpattern[1]
                    scl_h += self.hpattern[1]
                    scl_h += self.hpattern[2] if to_down else self.hpattern[1]
                    if to_up:
                        to_up = False
                    if to_down:
                        to_down = False
                if cr == 'a':
                    scl_l += self.lpattern[3]
                    scl_h += self.hpattern[3]
                    to_up = to_down = False

            print(f"sda: {scl_h}\n     {scl_l}")

        if inc_bits:
            print(f"\ni2c bits: {i2c_bits_msg}")

        if inc_add_data:
            print(f"\ni2c address: {i2c_adr_data_msg}\n       data")

    # Set the bus servo angle interface: id: 1-6 (0 means sending 6 servos) angle: 0-180 Set the angle to which the servo will move.
    def Arm_serial_servo_write(self, id, angle, time):
        print(f"[GOAL]: {id}(0x{id:02x}) angle: {angle}(0x{angle:02x}) time: {time} (0x{time:02x})")
        if id == 0:  # This is all servo controls
            # self.Arm_serial_servo_write6(angle, angle, angle, angle, angle, angle, time)
            pass
        elif id == 2 or id == 3 or id == 4:  # Opposite angle to reality
            print(f"id[{id}] -> Opposite angle to reality")
            angle = 180 - angle
            pos = int((3100 - 900) * (angle - 0) / (180 - 0) + 900)
            print(f"New angle: {angle}, servo position: {pos}")
            # pos = ((pos << 8) & 0xff00) | ((pos >> 8) & 0xff)
            value_H = (pos >> 8) & 0xFF
            value_L = pos & 0xFF
            time_H = (time >> 8) & 0xFF
            time_L = time & 0xFF
            # print output
            # self.bus.write_i2c_block_data(self.addr, 0x10 + id, [value_H, value_L, time_H, time_L])
            print(
                f"[TO_SEND] -> address: {self.addr}, id: {(0x10 + id)}, data[{value_H}, {value_L}, {time_H}, {time_L}]")
            self.print_i2c_block_data(self.addr, 0x10 + id, [value_H, value_L, time_H, time_L])
        elif id == 5:
            print(f"id[{id}]")
            pos = int((3700 - 380) * (angle - 0) / (270 - 0) + 380)
            # pos = ((pos << 8) & 0xff00) | ((pos >> 8) & 0xff)
            print(f"servo position: {pos}")
            value_H = (pos >> 8) & 0xFF
            value_L = pos & 0xFF
            time_H = (time >> 8) & 0xFF
            time_L = time & 0xFF
            # print output
            # self.bus.write_i2c_block_data(self.addr, 0x10 + id, [value_H, value_L, time_H, time_L])
            print(
                f"[TO_SEND] -> address: {self.addr}, id: {(0x10 + id)}, data[{value_H}, {value_L}, {time_H}, {time_L}]")
            self.print_i2c_block_data(self.addr, 0x10 + id, [value_H, value_L, time_H, time_L])
        else:
            print(f"id[{id}]")
            pos = int((3100 - 900) * (angle - 0) / (180 - 0) + 900)
            print(f"servo position: {pos}")
            # pos = ((pos << 8) & 0xff00) | ((pos >> 8) & 0xff)
            value_H = (pos >> 8) & 0xFF
            value_L = pos & 0xFF
            time_H = (time >> 8) & 0xFF
            time_L = time & 0xFF
            # print output
            # self.bus.write_i2c_block_data(self.addr, 0x10 + id, [value_H, value_L, time_H, time_L])
            print(
                f"[TO_SEND] -> address: {self.addr}, id: {(0x10 + id)}, data[{value_H}, {value_L}, {time_H}, {time_L}]")
            self.print_i2c_block_data(self.addr, 0x10 + id, [value_H, value_L, time_H, time_L])


def main():
    arm = Arm_Device()
    # arm.print_i2c_block_data(0x15, 0x11, [120, 0, 45, 45])
    print("\n----------\nid: 3, angle:45: time: 500\n----------")
    arm.Arm_serial_servo_write(3, 45, 500)
    print("\n----------\nid: 1, angle:60: time: 250\n----------")
    arm.Arm_serial_servo_write(1, 60, 250)


if __name__ == '__main__':
    main()
