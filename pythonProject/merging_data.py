import pandas as pd

# 1. 두 엑셀 파일 불러오기
df1 = pd.read_excel("resource/병합된_데이터2.xlsx")  # 예: 비만율 데이터
df2 = pd.read_excel("resource/보건의료시설.xlsx")  # 예: 주점업 수 데이터

# 2. 병합 기준 열 앞뒤 공백 제거 (필요 시)
df1["시도"] = df1["시도"].str.strip()
df1["시군구"] = df1["시군구"].str.strip()
df2["시도"] = df2["시도"].str.strip()
df2["시군구"] = df2["시군구"].str.strip()

# 3. "시도", "시군구" 기준으로 병합
merged_df = pd.merge(df1, df2, on=["시도", "시군구"], how="outer")
# "inner" → 공통된 것만, "outer" → 전체 다 포함 (누락도 포함)

# 4. 결과 저장 (선택)
merged_df.to_excel("resource/병합된_데이터3.xlsx", index=False)

# 5. 확인
print(merged_df.head())
