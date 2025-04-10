import pandas as pd
import json

#
# # 1. 인구 데이터 불러오기 (엑셀)
# df_pop = pd.read_excel("resource/인구정태.xlsx")
#
# # 필요한 컬럼만 추출 (예: '시군구명', '인구수')
# df_pop = df_pop[["시군구", "인구수"]]
# df_pop.columns = ["sgg_nm", "population"]  # 병합을 위해 이름 통일
#
# # 인구수를 int 형으로 변환 (쉼표 제거 등 포함)
# df_pop["population"] = (
#     df_pop["population"]
#     .astype(str)
#     .str.replace(",", "", regex=False)
#     .str.strip()
#     .astype(int)
# )
#
# # 2. 패스트푸드점 JSON 불러오기
# with open("fastfood_summary.json", encoding="utf-8") as f:
#     fastfood_data = json.load(f)
#
# df_fast = pd.DataFrame(fastfood_data)  # JSON → DataFrame
#
# # 패스트푸드 수 int로 보장
# df_fast["fastfood_count"] = pd.to_numeric(df_fast["corp_cnt"], errors="coerce").fillna(0).astype(int)
#
#
# # 3. 두 데이터 병합 (sggn_nm 기준)
# df_merged = pd.merge(df_fast, df_pop, on="sgg_nm", how="inner")
#
# # 4. 인구 1,000명당 패스트푸드점 수 계산
# df_merged["패스트푸드점_1000명당"] = (df_merged["corp_cnt"] / df_merged["population"]) * 1000
#
# # 5. 결과 확인
# print(df_merged[["sgg_nm", "fastfood_count", "population", "패스트푸드점_1000명당"]])
#
# # 6. 저장 (선택)
# df_merged.to_csv("패스트푸드_인구1000명당_지표.csv", index=False, encoding="utf-8-sig")
#



# 1. 비만율 데이터 불러오기
df_obesity = pd.read_excel("resource/비만율.xlsx")
print(df_obesity.columns)
df_obesity = df_obesity[["시군구", "비만율"]]
df_obesity.columns = ["sgg_nm", "obesity_rate"]

# 2. 인구정태 데이터 불러오기
df_population = pd.read_excel("resource/인구정태.xlsx")
df_population = df_population[["시군구", "인구수"]]
df_population.columns = ["sgg_nm", "population"]

# 3. 문자열 정리 (공백, 개행 제거 등)
df_obesity["sgg_nm"] = df_obesity["sgg_nm"].astype(str).str.strip()
df_population["sgg_nm"] = df_population["sgg_nm"].astype(str).str.strip()

# 4. 인구수 → int 형 변환
df_population["population"] = (
    df_population["population"]
    .astype(str)
    .str.replace(",", "", regex=False)
    .str.strip()
    .astype(int)
)

# 5. 병합 (region 기준)
df_merged = pd.merge(df_obesity, df_population, on="sgg_nm", how="inner")

# 6. 결과 확인
print(df_merged.head())

# 7. 저장 (선택)
df_merged.to_excel("비만율_인구_병합결과.xlsx", index=False)

