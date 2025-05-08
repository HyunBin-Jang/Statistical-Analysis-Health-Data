import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
import seaborn as sns
import platform
from statsmodels.graphics.regressionplots import plot_partregress_grid

# 1. 데이터 불러오기
df = pd.read_excel("resource/최종병합데이터.xlsx")
df.columns = df.columns.str.strip()

# 2. 필요한 컬럼만 선택 + 결측값 제거
df = df[["우울감경험률", "지역사회 대중교통 만족도_표준화율", "인구천명당 공원수", "인구천명당담배소매업소 수", "인구천명당패스트푸드점 수", "인구천명당주점업 수"]].dropna()
df.columns = ["depressionExp_rate", "pub_transport", "numOfParks", "retail_tobacco", "bar", "fastfood"]

# 3. 독립변수, 종속변수 정의
X = df[["pub_transport", "numOfParks", "retail_tobacco", "bar", "fastfood"]]
y = df["depressionExp_rate"]

# 4. 상수항 추가
X = sm.add_constant(X)

# 5. OLS 회귀모형 적합
model = sm.OLS(y, X).fit()

# 6. 결과 출력
print(model.summary())

# 7. 예측값 저장
df["y_pred"] = model.predict(X)

# OS별 기본 한글 폰트 설정
if platform.system() == 'Windows':
    plt.rcParams['font.family'] = 'Malgun Gothic'  # 맑은 고딕
elif platform.system() == 'Darwin':  # Mac
    plt.rcParams['font.family'] = 'AppleGothic'
else:  # Linux (구글 코랩 등)
    plt.rcParams['font.family'] = 'NanumGothic'

# 마이너스 기호 깨짐 방지
plt.rcParams['axes.unicode_minus'] = False

# 8. 회귀계수 시각화
coefs = model.params.drop("const")
errors = model.bse.drop("const")

plt.figure(figsize=(8, 5))
coefs.plot(kind='bar', yerr=errors, capsize=4)
plt.axhline(0, color='gray', linestyle='--')
plt.title("회귀계수와 신뢰구간 (±1표준오차)")
plt.ylabel("계수 값")
plt.xticks(rotation=0)
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()

# 9. 실제값 vs 예측값 산점도
plt.figure(figsize=(7, 6))
sns.scatterplot(x='y_pred', y='depressionExp_rate', data=df)
plt.plot([df['y_pred'].min(), df['y_pred'].max()],
         [df['y_pred'].min(), df['y_pred'].max()],
         color='red', linestyle='--')
plt.xlabel("예측된 우울감경험률")
plt.ylabel("실제 우울감경험률")
plt.title("예측값 vs 실제값")
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()

# 10. 부분 회귀 플롯
fig = plt.figure(figsize=(12, 8))
plot_partregress_grid(model, fig=fig)
plt.tight_layout()
plt.show()
