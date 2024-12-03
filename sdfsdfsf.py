import requests
from collections import defaultdict
import matplotlib.pyplot as plt

# Codeforces API URL
url = "https://codeforces.com/api/problemset.problems"
response = requests.get(url)

# JSON 응답 데이터를 파싱
data = response.json()

# 문제들 데이터 추출
problems = data.get("result", {}).get("problems", [])

# rating 통계 수집
rating_count = defaultdict(int)

for problem in problems:
    rating = problem.get("rating")
    if rating is not None:
        rating_count[rating] += 1

# rating 통계 출력
print("Rating 통계:")
for rating, count in sorted(rating_count.items()):
    print(f"Rating {rating}: {count} 문제")

# 그래프로 rating 통계 시각화
plt.figure(figsize=(10, 6))
plt.bar(rating_count.keys(), rating_count.values())
plt.xlabel('Rating')
plt.ylabel('Number of Problems')
plt.title('Codeforces Problems by Rating')
plt.xticks(rotation=45)
plt.show()
