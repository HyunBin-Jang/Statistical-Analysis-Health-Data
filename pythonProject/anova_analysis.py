import pandas as pd
import statsmodels.api as sm
from statsmodels.formula.api import ols


def classify_region_type(region_name):
    region_name = str(region_name)  # float → str 변환
    if region_name.endswith("구"):
        return "구"
    elif region_name.endswith("군"):
        return "군"
    elif region_name.endswith("특별시"):
        return "특별시"
    elif region_name.endswith("광역시"):
        return "광역시"
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

# 결측 제거
df = df.dropna(subset=["depression_rate","obesity_rate", "region_type"])

# 2. 시/군/구 분류 추가
df["region_type"] = df["sgg_nm"].apply(classify_region_type)

# 3. 비만율, 우울감경험률 숫자화
df["obesity_rate"] = pd.to_numeric(df["obesity_rate"], errors="coerce")
df["depression_rate"] = pd.to_numeric(df["depression_rate"], errors="coerce")


# ANOVA 모델 설정 및 적합
model1 = ols('obesity_rate ~ C(region_type)', data=df).fit()
anova_table1 = sm.stats.anova_lm(model1, typ=2)

model2 = ols('depression_rate ~ C(region_type)', data=df).fit()
anova_table2 = sm.stats.anova_lm(model2, typ=2)

print("✅ ANOVA 결과:")
print(anova_table1)
print()
print(anova_table2)
