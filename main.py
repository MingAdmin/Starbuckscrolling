import datetime
import requests

# 프로그램 시작 화면 디자인
print('──────────────────────────────────────────────────────────────')
print('★★★★★★★★STARBUCKS 매장조회 프로그램★★★★★★★★')
print('──────────────────────────────────────────────────────────────')

while True:
    # 스타벅스 시/도 정보 조회
    targetSite1 = 'https://www.starbucks.co.kr/store/getSidoList.do'
    request = requests.post(targetSite1)
    sido_list = request.json()

    # 사용자로부터 시/도 선택
    print('00 : 전체')
    for sido in sido_list['list']:
        print(sido['sido_cd'] + ' : ' + sido['sido_nm'])

    sido_cd = input('시/도 코드를 입력해주세요 : ')

    if sido_cd == '00':
        sido_cd = ''
        gugun_cd = ''
    else:
        # 스타벅스 구/군 정보 조회
        targetSite2 = 'https://www.starbucks.co.kr/store/getGugunList.do'
        request = requests.post(targetSite2, data={'sido_cd': sido_cd})
        gugun_list = request.json()

        # 사용자로부터 구/군 선택
        gugunList = {}
        print('00 : 전체')
        for gugun in gugun_list['list']:
            gugunList[gugun['gugun_cd']] = gugun['gugun_nm']
            if gugun['gugun_nm'] is not None:
                print(gugun['gugun_cd'] + ' : ' + gugun['gugun_nm'])

        gugun_cd = input('구/군을 입력해주세요 : ')

    if gugun_cd == '00':
        gugun_cd = ''

    # 스타벅스 매장 정보 조회
    targetSite3 = 'https://www.starbucks.co.kr/store/getStore.do?r=006KL3QESV'
    request = requests.post(targetSite3, data={
        'p_sido_cd': sido_cd,
        'p_gugun_cd': gugun_cd,
        'ins_lat': '',
        'ins_lng': '',
        'in_biz_cd': '',
        'iend': 3000,
        'set_date': ''
    })

    store_list = request.json()

    # 현재 날짜 및 시간 기록
    dt_datetime = datetime.datetime.now()
    fformat = "%Y%m%d%H%M%S"
    str_today = datetime.datetime.strftime(dt_datetime, fformat)

    # 결과를 텍스트 파일로 저장
    f = open('starbucks_' + str_today + '.txt', 'w')

    count = 0
    f.write('순번' + '\t' + '지점명' + '\t' + '도로명주소' + '\t' + '위도/경도' + '\n')
    for store in store_list['list']:
        count += 1
        f.write('{0:4d} {1} {2} ({3}, {4})'.format(count, '\t' + store['s_name'] + '\t',
                                                   store['doro_address'] + '\t', store['lat'], store['lot']) + '\n')

    f.close()

    # 조회 결과 출력 및 사용자 상호작용
    print('\n 조회 및 텍스트파일 생성이 완료되었습니다. \n ')
    requ = int(input('>>> 프로그램 종료 : 1, 계속 : 2 입력해 주세요 : '))

    # 에러 처리: 유효한 선택지가 아닌 경우 반복
    while requ != 1 and requ != 2:
        print('유효한 입력이 아닙니다. 1 또는 2를 입력해주세요.')
        requ = int(input('>>> 프로그램 종료 : 1, 계속 : 2 입력해 주세요 : '))

    if requ == 2:
        continue
    else:
        break


