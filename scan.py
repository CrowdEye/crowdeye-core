def get_cams():
    all_cams = []
    print("-", end="", flush=True)
    x = requests.get(AI_CORE_IP + "/" + "get_cameras")
    data = x.json()
    # print(data)

    for node_id in data:
        x = requests.get(AI_CORE_IP + "/" + "camera" + "/" + node_id)
        DATA[node_id] = x.json()
