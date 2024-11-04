


# from xarm.wrapper import XArmAPI
# import time
# arm = XArmAPI('192.168.1.167')
# arm.connect('connect!')
# tcp_speed = 100
# tcp_acc = 2000
# angle_speed = 10
# angle_acc = 500
# print('start motion...')


from xarm.wrapper import XArmAPI
import time


# 로봇 초기화 함수
def initialize_arm(ip_address='192.168.1.167'):
    arm = XArmAPI(ip_address)
    arm.connect('connect!')
    arm.motion_enable(True)
    arm.set_mode(0)
    arm.set_state(0)
    return arm

# 초기 위치 설정
def set_initial_position(arm, angle_speed=10, angle_acc=500):
    print("Moving to initial position...")
    arm.set_servo_angle(angle=[180.0, 0.0, 6.0, 180.0, 90.0, 180.0, 0.0], speed=angle_speed, mvacc=angle_acc, wait=False, radius=0.0)

# 그리퍼 열기
def open_grippers(arm):
    print("Opening gripper...")
    arm.open_lite6_gripper()

# 그리퍼 닫기
def close_grippers(arm):
    print("Closing gripper...")
    arm.close_lite6_gripper()

# 지정된 위치로 이동하는 함수
def move_to_positions(arm, angle_speed=10, angle_acc=500):
    positions = [
        [180.271831, 0.120436, 10.520193, 136.153565, 75.540188, 183.65847, 0.0],
    ]

    for i, position in enumerate(positions):
        print(f"Moving to position {i + 1}...")
        arm.set_servo_angle(angle=position, speed=angle_speed, mvacc=angle_acc, wait=False, radius=0.0)
        if i == 2:  # 그리퍼 닫기 전에 잠시 대기
            time.sleep(3)
            close_grippers(arm)
            time.sleep(1)

# 전체 동작 수행
def perform_robot_motion1():
    print("Start Motion1.")
    arm = initialize_arm()
    # set_initial_position(arm)
    open_grippers(arm)
    close_grippers(arm)
    print("Motion1 complete.")

def perform_robot_motion2():
    arm = initialize_arm()
    # set_initial_position(arm)
    # move_to_positions(arm)
    open_grippers(arm)
    close_grippers(arm)
    open_grippers(arm)
    close_grippers(arm)
    print("Motion2 complete.")

def perform_robot_motion3():
    arm = initialize_arm()
    # set_initial_position(arm)
    
    close_grippers(arm)
    open_grippers(arm)
    close_grippers(arm)
    open_grippers(arm)
    
    print("Motion3 complete.")
    
    
# 주문 응답을 처리하고 로봇 동작을 수행하는 함수
def process_order_response(response_text):
    print(response_text)
    # 응답 문자열에서 각 항목을 줄바꿈 기준으로 분리
    lines = response_text.strip().split("\n")
    print(lines)
    
    # 각 제품별 로봇 동작 호출
    for line in lines:
        # '-'으로 시작하는 경우 제품 이름을 가져옴
        if line.startswith("-"):
            product_name = line[1:].strip()
            print('product_name')
            print(product_name)
            
            # 제품명에 따라 각 함수 호출
            if product_name == "코코볼":
                perform_robot_motion1()
            elif product_name == "시리얼":
                perform_robot_motion2()
            elif product_name == "아몬드":
                perform_robot_motion3()
            else:
                print(f"알 수 없는 제품: {product_name}")
