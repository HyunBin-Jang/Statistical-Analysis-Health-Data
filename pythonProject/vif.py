import pandas as pd
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor

# 데이터 불러오기
df = pd.read_excel("resource/최종병합데이터.xlsx")
df.columns = df.columns.str.strip()

# 1. 독립변수들 선택
X = df[["지역사회 대중교통 만족도_표준화율", "인구천명당 공원수", "인구천명당담배소매업소 수", "인구천명당패스트푸드점 수", "인구천명당주점업 수"]].dropna()
X.columns = ["pub_transport", "numOfParks", "retail_tobacco", "bar", "fastfood"]
X = sm.add_constant(X)  # 상수항 추가

# 2. VIF 계산
vif_data = pd.DataFrame()
vif_data["변수명"] = X.columns
vif_data["VIF"] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]

# 3. 결과 출력
print(vif_data)
