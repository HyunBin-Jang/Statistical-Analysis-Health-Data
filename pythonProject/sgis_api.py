import requests
import pandas as pd
import json

# 본인의 SGIS 발급 키 입력
consumer_key = "3287556a9b144d8d9e9d"
consumer_secret = "5788915c975f45de96c8"

token_url = "https://sgisapi.kostat.go.kr/OpenAPI3/auth/authentication.json"
token_response = requests.get(f"{token_url}?consumer_key={consumer_key}&consumer_secret={consumer_secret}")
access_token = token_response.json()["result"]["accessToken"]
print("✅ Access Token 발급 완료")

# SGIS 시군구별 생활업종 사업체수 API
base_url = "https://sgisapi.kostat.go.kr/OpenAPI3/startupbiz/sggtobcorpcount.json"

# 업종 코드: 5612 (패스트푸드)
industry_code = "5007"

# API 호출
request_url = (
    f"{base_url}?accessToken={access_token}&theme_cd={industry_code}")

response = requests.get(request_url)
data = response.json()

# DataFrame 생성
df = pd.DataFrame(data)
filtered_data = [
    {
        "sgg_cd": item["sgg_cd"],
        "sgg_nm": item["sgg_nm"],
        "corp_cnt": int(item["corp_cnt"])  # 문자열이면 숫자로 변환
    }
    for item in data["result"]
]

# JSON 파일로 저장
with open("f    astfood_summary.json", "w", encoding="utf-8") as f:
    json.dump(filtered_data, f, ensure_ascii=False, indent=4)
