import requests
from config import MainServerConfig

def send_numpy_data_to_main_server(data):
    # numpy 배열을 리스트로 변환
    data_list = data.tolist()

    # 메인 서버의 주소 
    main_server = MainServerConfig()

    # 데이터를 JSON 형태로 변환하여 전송
    response = requests.post(main_server, json={"data": data_list})

    if response.status_code == 200:
        print("Data sent successfully!")
    else:
        print("Failed to send data:", response.text)
