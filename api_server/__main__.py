import argparse

if __name__ == "__main__":
    # 파서 생성
    parser = argparse.ArgumentParser(description='인자를 받는 스크립트입니다.')

    # 인자 추가
    # parser.add_argument('', type=str, help='입력 파일명')

    # 인자 파싱
    args = parser.parse_args()