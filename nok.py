import requests

# 从这个网址的网页源码，试着获取m3u8地址 （但是无法播放，404或者403）
# http://nn.7x9d.cn/%E5%9C%B0%E6%96%B9%E5%8F%B08563/


def get_sub_key_from_channel_info(id, uin):
    url = f"https://1812501212048408.cn-hangzhou.fc.aliyuncs.com/2016-08-15/proxy/node-api.online/node-api/tv/channelInfo?id={id}&uin={uin}"
    headers = {
        "Referer": f"https://web.guangdianyun.tv/tv/?id={id}",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/117.0.0.0 Safari/537.36",
    }
    resp = requests.get(url, headers=headers)
    data = resp.json()
    if data.get("code") == 200 and data.get("errorCode") == 0:
        return data["data"]["sub_key"]
    else:
        print("❌ 获取 sub_key 失败:", data)
        return None

def get_m3u8_url(id, uin, client_id, client_ip=None):
    url = f"https://1812501212048408.cn-hangzhou.fc.aliyuncs.com/2016-08-15/proxy/node-api.online/node-api/tv/getPlayAddress?id={id}&uin={uin}&clientId={client_id}"
    headers = {
        "Referer": f"https://web.guangdianyun.tv",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/117.0.0.0 Safari/537.36",
    }
    # if client_ip:
    #     headers["X-Forwarded-For"] = client_ip
        # headers["CLIENT-IP"] = client_ip  # 视情况添加

    resp = requests.get(url, headers=headers)
    data = resp.json()
    if data.get("code") == 200 and data.get("errorCode") == 0 and data["data"].get("hlsUrl"):
        return data["data"]["hlsUrl"]
    else:
        print("❌ 获取 m3u8 地址失败:", data)
        return None


def get_current_ip():
    try:
        resp = requests.get("http://ip-api.com/json/?lang=zh-CN", timeout=5)
        data = resp.json()
        if data.get("query"):
            print(f"🌐 当前 IP 来源: {data.get('isp')} - {data.get('regionName')} {data.get('city')}")
            return data["query"]
        else:
            print("❌ IP 查询失败:", data)
            return None
    except Exception as e:
        print("❌ 获取当前 IP 失败:", e)
        return None
    

def gen_client_id():
    import uuid

    client_id = str(uuid.uuid4())
    # print("Generated clientId:", client_id)        
    return client_id

if __name__ == "__main__":
    # id = 391      # 巴中综合
    # uin = 1743
    id, uin = 175,1116
    print(f"📺 正在获取频道信息 id={id}, uin={uin} ...")
    current_ip = get_current_ip() # 伪装的客户端IP
    print("🌐 当前 IP:", current_ip)

    print("🔍 正在获取 sub_key ...")
    sub_key = get_sub_key_from_channel_info(id, uin)
    if sub_key:
        print("✅ 获取到 sub_key:", sub_key)

    
    if sub_key:
        sub_key = gen_client_id()
        print(f"🔑 生成 clientId: {sub_key}")
        print("📺 正在获取 m3u8 地址 ...")
        m3u8_url = get_m3u8_url(id, uin, sub_key, client_ip=None)
        if m3u8_url:
            print("✅ 播放地址:", m3u8_url)
        else:
            print("❌ 无法获取播放地址")
