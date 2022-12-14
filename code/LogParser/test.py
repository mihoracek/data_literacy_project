from candb import CanDB

# Load json file used to interpret the bytes in the log
db = CanDB(["/home/cyxeh/data_literacy/data_literacy_project/code/LogParser/D1.json"])

with open("/home/cyxeh/data_literacy/data_literacy_project/data/2022_06_13_16_12.asc", "r") as source:
    for i in range(4):
        source.readline()   # skip header
    
    for line in source:
        line = line.strip().split()
        try:    # Stopping condition. Last line isnt "" but a bunch of NUL symbols from C (\x00)
            timestamp, canbus, msg_id, txrx, frame_type, data_length = line[:6]
        except ValueError:
            break
        data = [int(b) for b in line[6:]]

        # Wanted to try the match case construct, this is a new feature in python 3.10
        match int(msg_id):
            case 0x131: # EKF_QUAT
                print("0x131")
            case 0x132: # EKF_EULER
                print("0x132")
            case 0x133: # EKF_ORIENT_ACC
                print("0x133")
            case 0x173: # GPS1_COURSE
                parsed = db.parseData(int(msg_id), bytearray(data), float(timestamp)).as_namedtuple()                
                course = parsed[0]
                course_acc = parsed[1]
                print(f"{course.name} is {course.value}, {course_acc.name} is {course_acc.value}")
            case 0x179: # GPS1_HDT
                print("0x179")
            case 0x183: # GPS2_COURSE
                print("0x183")
            case 0x189: # GPS2_HDT
                print("0x189")
            case _:     # Something else
                pass
