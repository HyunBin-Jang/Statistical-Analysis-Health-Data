import platform
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt

# 1. 엑셀 파일 불러오기
df = pd.read_excel("resource/비만_우울감.xlsx")
df.columns = df.columns.str.strip()  # 공백 제거

# 2. 필요한 컬럼만 선택
df = df[["비만율", "인구천명당주점업 수"]].dropna()
df.columns = ["obesity_rate", "bar_per_1000"]


# 3. 변수 정리
X = df["bar_per_1000"]     # 독립변수
y = df["obesity_rate"]          # 종속변수

# 4. 상수항 추가 (절편 포함 회귀분석)
X = sm.add_constant(X)

# 5. OLS 회귀모형 적합
model = sm.OLS(y, X).fit()

# 6. 결과 요약 출력
print(model.summary())


# OS별 기본 한글 폰트 설정
if platform.system() == 'Windows':
    plt.rcParams['font.family'] = 'Malgun Gothic'  # 맑은 고딕
elif platform.system() == 'Darwin':  # Mac
    plt.rcParams['font.family'] = 'AppleGothic'
else:  # Linux (구글 코랩 등)
    plt.rcParams['font.family'] = 'NanumGothic'
# 마이너스 기호 깨짐 방지
plt.rcParams['axes.unicode_minus'] = False

# 7. 산점도 + 회귀선 시각화
plt.figure(figsize=(8, 6))
plt.scatter(df["bar_per_1000"], df["obesity_rate"], alpha=0.7, label="Data")
plt.plot(df["bar_per_1000"], model.predict(X), color="red", label="Regression Line")
plt.xlabel("1000명당 주점업 수")
plt.ylabel("비만율 (%)")
plt.title("주점업 수 vs 비만율 (선형회귀)")
plt.legend()
plt.grid(True, linestyle="--", alpha=0.5)
plt.tight_layout()
plt.show()
