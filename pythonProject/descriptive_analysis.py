import pandas as pd
import seaborn as sns
import platform
import matplotlib.pyplot as plt

def classify_region_type(region_name):
    region_name = str(region_name)  # float → str 변환
    if region_name.endswith("구"):
        return "구"
    elif region_name.endswith("군"):
        return "군"
    elif region_name.endswith("광역시"):
        return "기타"
    elif region_name.endswith("시"):
        return "시"
    else:
        return "기타"

# 1. 비만율 데이터 불러오기
df = pd.read_excel("resource/비만_우울감.xlsx")
df = df[["시군구", "비만율", "우울감경험률"]]
df.columns = ["sgg_nm", "obesity_rate", "depression_rate"]

# 2. 시/군/구 분류 추가
df["region_type"] = df["sgg_nm"].apply(classify_region_type)

# 3. 비만율, 우울감경험률 숫자화
df["obesity_rate"] = pd.to_numeric(df["obesity_rate"], errors="coerce")
df["depression_rate"] = pd.to_numeric(df["depression_rate"], errors="coerce")

# 4. 그룹별 기술통계 요약 - 비만율
grouped_stats1 = df.groupby("region_type")["obesity_rate"].agg(["count", "mean", "std", "min", "max"])
grouped_stats1["CV"] = grouped_stats1["std"] / grouped_stats1["mean"] * 100  # 변이계수(%)

# 5. 그룹별 기술통계 요약 - 우울감경험률
grouped_stats2 = df.groupby("region_type")["depression_rate"].agg(["count", "mean", "std", "min", "max"])
grouped_stats2["CV"] = grouped_stats2["std"] / grouped_stats2["mean"] * 100

# 5. 결과 출력
print(grouped_stats1.round(2))
print()
print(grouped_stats2.round(2))


# 그룹별 평균 계산
grouped = df.groupby("region_type")[["obesity_rate", "depression_rate"]].mean().round(2)

# 시각화 준비
labels = grouped.index
obesity = grouped["obesity_rate"]
depression = grouped["depression_rate"]
x = range(len(labels))

# OS별 기본 한글 폰트 설정
if platform.system() == 'Windows':
    plt.rcParams['font.family'] = 'Malgun Gothic'  # 맑은 고딕
elif platform.system() == 'Darwin':  # Mac
    plt.rcParams['font.family'] = 'AppleGothic'
else:  # Linux (구글 코랩 등)
    plt.rcParams['font.family'] = 'NanumGothic'

# 마이너스 기호 깨짐 방지
plt.rcParams['axes.unicode_minus'] = False
# 시각화
plt.figure(figsize=(10, 6))
bar_width = 0.35

plt.bar(x, obesity, width=bar_width, label="비만율", alpha=0.7)
plt.bar([i + bar_width for i in x], depression, width=bar_width, label="우울감경험률", alpha=0.7)

plt.xlabel("지역 유형")
plt.ylabel("비율 (%)")
plt.title("시/군/구 유형별 비만율 vs 우울감경험률 (평균)")
plt.xticks([i + bar_width / 2 for i in x], labels)
plt.legend()
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()