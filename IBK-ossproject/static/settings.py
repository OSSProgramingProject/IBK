import os

# 프로젝트의 루트 디렉터리 경로를 BASE_DIR에 할당
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 정적 파일 URL 경로
STATIC_URL = '/static/'  # 정적 파일의 기본 URL 경로

# 정적 파일을 모으는 디렉터리 (collectstatic 명령어로 파일이 모임)
STATIC_ROOT = BASE_DIR / 'staticfiles'

# 추가적인 정적 파일 디렉터리 (개발 중에 사용하는 디렉터리 경로)
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]
