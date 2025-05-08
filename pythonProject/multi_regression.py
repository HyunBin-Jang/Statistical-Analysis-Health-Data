import pandas as pd
import statsmodels.api as sm

# 1. 데이터 불러오기
df = pd.read_excel("resource/최종병합데이터.xlsx")
df.columns = df.columns.str.strip()

# 2. 필요한 컬럼만 선택 + 결측값 제거
df = df[["비만율표준화율", "지역사회 대중교통 만족도_표준화율", "인구천명당 공원수", "인구천명당담배소매업소 수"]].dropna()
df.columns = ["obesity_rate", "pub_transport", "numOfParks", "retail_tobacco"]

# 3. 독립변수, 종속변수 정의
X = df[["pub_transport", "numOfParks", "retail_tobacco"]]
y = df["obesity_rate"]

# 4. 상수항 추가
X = sm.add_constant(X)

# 5. OLS 회귀모형 적합
model = sm.OLS(y, X).fit()

# 6. 결과 출력
print(model.summary())
