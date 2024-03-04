# 패키지 불러오기
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from urllib.request import urlretrieve
from datetime import datetime
import pandas as pd
import requests
import random
import time
import os
import re


def meta_crawling(search : str, job_folder_path : str, time_sleep : int = 10) :
    """
    Input
        1) search (str) :
            크롤링 할 검색어
        
        2) job_folder_path (str) :
            텍스트 크롤링 결과물이 저장될 경로, 해당 경로에 이미지와 영상이 저장될 검색어 명으로 된 폴더를 추가로 생성
            
        3) time_sleep (int) :
            웹 브라우저 창이 열리기 까지의 대기시간
    Output
        1) CSV :
            svae_folder_path에 텍스트결과 라이브러리 ID, 제목, 내용 컬럼으로 저장
        
        2) jpg & mp4 :
            svae_folder_path에 검색어 명의 폴더에 저장
    """
    # 최소 및 최대 대기 시간 설정 (예: 'min_wait초 에서 'max_wait'초 사이의 랜덤 대기)
    min_wait = 1 # 최소 대기 시간 (초)
    max_wait = 5 # 최대 대기 시간 (초)

    # 랜덤 대기 시간 생성
    random_wait = random.uniform(min_wait, max_wait)

    ind = 1
    no = 2
    ye = 4
    con = 0
    list_1 = [] # 결과물이 저장되는 리스트
    today = datetime.today().date()

    driver = webdriver.Chrome()
    driver.get(f"https://www.facebook.com/ads/library/?active_status=all&ad_type=all&country=KR&q={search}&search_type=keyword_unordered&media_type=all&content_languages[0]=ko")
    
    # 작업날짜 폴더 생성
    date_folder_path = os.path.join(job_folder_path, f"{today}")
    
    # 이미지 저장할 폴더 생성
    svae_folder_path = os.path.join(date_folder_path, f"{search}")
    
    # 디렉토리를 만듭니다.
    try :
        os.makedirs(date_folder_path)
        print(f"'{date_folder_path}' 디렉토리를 생성합니다.")
        
    except FileExistsError :
        print(f"'{date_folder_path}' 디렉토리는 이미 존재합니다.")
        pass
    
    try :
        os.makedirs(svae_folder_path)
        print(f"'{svae_folder_path}' 디렉토리를 생성합니다.")
    
    except FileExistsError :
        print(f"'{svae_folder_path}' 디렉토리는 이미 존재합니다.")
        pass
    
    time.sleep(time_sleep) # 브라우저가 열릴떄 까지 대기
    
    # 검색 자료 개수 파악
    try :
        number = driver.find_element(by='xpath', \
                    value = f'//*[@id="content"]/div/div[1]/div/div[5]/div[1]/div/div/div/div/div/div[1]/div').text

        result = re.search(r'~(\d+)개', number)
        number_s = int(result.group(1))
        
    except :
        time.sleep(10) # 브라우저가 열릴떄 까지 대기

        number = driver.find_element(by='xpath', \
                    value = f'//*[@id="content"]/div/div[1]/div/div[5]/div[1]/div/div/div/div/div/div[1]/div').text

        result = re.search(r'~(\d+)개', number)
        number_s = int(result.group(1))
    
    # 데이터 찾기
    while True :
        try :
            # 라이브러리 ID
            id_raw = driver.find_element(by='xpath', \
                value = f'//*[@id="content"]/div/div[1]/div/div[5]/div[2]/div[{no}]/div[{ye}]/div[1]/div[{ind}]/div/div[1]/div/div[1]/div[1]/div').text
            
            # 게재 날짜
            date_raw = driver.find_element(by='xpath', \
                value = f'//*[@id="content"]/div/div[1]/div/div[5]/div[2]/div[{no}]/div[{ye}]/div[1]/div[{ind}]/div/div[1]/div/div[1]/div[3]/span').text
            
            # 이름
            name_raw = driver.find_element(by='xpath', \
                value = f'//*[@id="content"]/div/div[1]/div/div[5]/div[2]/div[{no}]/div[{ye}]/div[1]/div[{ind}]/div/div[3]/div/div/div[1]/div').text
            
            name = str(name_raw.split('\n광고')[0]) # 원하는 문자 추출
            
            # 내용
            contents = driver.find_element(by='xpath', \
                value = f'//*[@id="content"]/div/div[1]/div/div[5]/div[2]/div[{no}]/div[{ye}]/div[1]/div[{ind}]/div/div[3]/div/div/div[2]/div/span/div/div/div').text
            
            # 원하는 문자 추출
            id = str(id_raw.split(': ')[1])
            pattern = r"(\d{4})\. (\d{1,2})\. (\d{1,2})\."
            match = re.search(pattern, date_raw)
            year, month, day = int(match.group(1)), int(match.group(2)), int(match.group(3))
            date = datetime(year, month, day).date()
            name = str(name_raw.split('\n광고')[0])
            
            try :
                # 이미지
                img_element = driver.find_element(by = 'xpath', \
                    value = f'//*[@id="content"]/div/div[1]/div/div[5]/div[2]/div[{no}]/div[{ye}]/div[1]/div[{ind}]/div/div[3]/div/div/div[2]/a/div[1]/img')
                
                img_src = img_element.get_attribute("src")
                
                # 이미지 저장
                file_name = f"{id}.jpg"
                file_path = os.path.join(svae_folder_path, file_name)
                urlretrieve(img_src, file_path)
            
            except :
                try :
                    # 동영상
                    video_element = driver.find_element(by = 'xpath', \
                        value = f'//*[@id="content"]/div/div[1]/div/div[5]/div[2]/div[{no}]/div[{ye}]/div[1]/div[{ind}]/div/div[3]/div/div/div[2]/div[2]/div/div/div/div/div/div/video')
                
                    video_src = video_element.get_attribute("src")
                    
                    # 동영상 파일 저장
                    video = requests.get(video_src)
                    file_name = f"{id}.mp4"
                    file_path = os.path.join(svae_folder_path, file_name)
                    with open(file_path, "wb") as f :
                        f.write(video.content)
                
                except :
                    try :
                        for no_ in range(1, 21):
                            # 이미지
                            img_element_1 = driver.find_element(by = 'xpath', \
                                value = f'//*[@id="content"]/div/div[1]/div/div[5]/div[2]/div[{no}]/div[{ye}]/div[1]/div[{ind}]/div/div[3]/div/div/div[3]/div/div/div/div[{no_}]/div/div/a/div[1]/img')
                            
                            img_src_1 = img_element_1.get_attribute("src")
                            
                            # 이미지 저장
                            file_name = f"{id}_{no_}.jpg"
                            file_path = os.path.join(svae_folder_path, file_name)
                            urlretrieve(img_src_1, file_path)
                            
                    except :
                        pass
            
            # 리스트에 추가
            if [today, search, id, date, name, contents] not in list_1 :
                list_1.append([today, search, id, date, name, contents])
                
                # 텍스트 저장
                df = pd.DataFrame(list_1)
                df = df.rename(columns = {0 : "c_date", 1 : "keyword", 2 : "ID", 3 : "p_date", 4 : "user", 5 : "contents"})
                file_name = f"{search}.csv"
                file_path = os.path.join(date_folder_path, file_name)
                df.to_csv(file_path, index = False)
                
                print(f"1번 : {no}-{ye}-{ind} 까지 저장을 완료 하였습니다.")
                
                time.sleep(random_wait) # 랜덤 타임 대기
                
                ind += 1
                
            else :
                ind += 1
            
        except :
            ind += 1
            
            if ind >= number_s :
                print("ind 초기화 및 페이지 다운")
                # 스크롤 내리기 (페이지 다운 키를 사용)
                driver.find_element(by = By.TAG_NAME, value = "body").send_keys(Keys.PAGE_DOWN)
                
                ind = 1
                no += 1
            
            if no >= 15 :
                print("year -1 :", ye - 1)
                print("no 초기화 및 페이지 다운")
                # 스크롤 내리기 (페이지 다운 키를 사용)
                driver.find_element(by = By.TAG_NAME, value = "body").send_keys(Keys.PAGE_DOWN)
                
                time.sleep(random_wait) # 랜덤 타임 대기
                
                ye -= 1
                ind = 1
                no = 2
            
            if ye <= 2 :
                ye = 4
                con += 1
                print(con)
            
            if number_s <= 50 :
                if con >= 2 :
                    print(f"{search}, {len(list_1)}개 작업 완료")
                    break
            
            if number_s <= 100 :
                if con >= 3 :
                    print(f"{search}, {len(list_1)}개 작업 완료")
                    break
            
            if number_s <= 150 :
                if con >= 4 :
                    print(f"{search}, {len(list_1)}개 작업 완료")
                    break
            
            if con >= 5 :
                print(f"{search}, {len(list_1)}개 작업 완료")
                break
    
    # 브라우저 창 닫기
    driver.quit()


def dir_csv_excel(directory : str, index_col : int or str = None, encoding : str = None):
    """
    Input
        1) directory (str) :
            cvs, excel 파일들을 불러올 디렉토리 경로
        2) index_col (int | str) = None :
            인덱스로 사용할 열의 번호 또는 이름을 지정
        3) encoding (str) = None :
            파일의 인코딩을 지정
            한글 파일 에러 : 'cp949'
            아스키 코드 에러 : 'ISO-8859-1'
    Output
        1) dataset (dict) :
            directory_name (str) 내의 csv, excel 파일,
            변수 = dir_csv_excel('directory_name')['파일이름.확장자']로 사용
    """
    # 지정한 디렉토리 내의 파일과 하위 디렉토리 목록 -> 리스트로 반환
    data_list = os.listdir(directory)
    print(f"\n'{directory}' 내의 파일과 하위 디렉토리 목록 :\n", data_list)

    # csv 파일 대량 불러오기 -> dict 형태로 반환
    dataset = dict()
    
    try:
        for data in data_list:
            if data.lower().endswith('.csv') :
                print(data) # csv 파일들 출력
                dataset[data] = pd.read_csv(os.path.join(directory, data), index_col = index_col, encoding = encoding)
            
            elif data.lower().endswith('.xls') or data.lower().endswith('.xlsx') :
                print('/n', data) # excel 파일들 출력
                dataset[data] = pd.read_excel(os.path.join(directory, data), index_col = index_col)
    
    except Exception as e:
        print(e)
        
    return dataset