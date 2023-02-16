# VulDock
## 🐋 VulDock: Vulnerability Scanning Tool for Docker Images🐋
![VulDock](./images/슬라이드1.PNG)
<b>VulDock</b> 은 `Vulnerability`와 `Docker`의 앞글자를 따서 만든 단어로, Vulnerability Scanning Tool for Docker Images 즉, `도커 이미지 취약점 탐지 툴`이다.
Vuldock은 <b>컨테이너를 실행하기 전에 사용된 이미지가 가지고 있을 수 있는 버전 등의 잠재적인 문제 검사</b>를 목표로 하며, python 기반의 리눅스 환경에서 실행되는 프로그램이다. 
<br><br>
또한, Vuldock은 여러 개의 컨테이너로부터 이루어진 서비스 구축을 위한 `docker-compose로 작성된 도커 이미지` 분석에 적합하며, 툴을 사용하기 위해서는 <b>해당 이미지가 실행할 로컬 환경에 다운로드</b> 되어 있어야한다.

서비스 개요는 다음과 같다.


#### ✅ 서비스 개요 
- 도커 이미지 분석시 docker-compose 파일을 이용해 서비스 목록을 확인 후, 서비스들의 `취약점과 최신 버전 여부` 등을 검사한다.
- 서비스 취약점 검사에는 `Searchsploit` 툴이 사용되었으며, 해당 툴을 이용하여 os 및 version에 해당되는 취약점을 검색한다.
- 또한 `웹 크롤링`을 이용하여 각 취약점에 해당하는 `CVE 번호`를 매핑해준다.
- 분석 대상 이미지 중 포함된 서비스가 리눅스 기반인데 공식 이미지가 아닐 경우, `주요정보통신기발시설_기술적_취약점 검사`문서 가이드에 따라 추가 취약점 검사를 진행한다.
- 취약점 검사 후 결과는 표로 정렬하여 터미널에 출력된다.     


<sub>자세한 툴 설명은 밑의 'VulDock 세부 설명' 참고 바랍니다.</sub>

<br>

## ▶ 프로젝트 기간  
  2021.07 - 2021.08
<br/><br/>    

## ▶ 프로젝트 소개
- 2021 Incognito에서 진행한 프로젝트로, 주제 선정부터 개발까지 팀별로 진행한 프로젝트이다. 
- 도커 이미지 취약점 탐지 툴인 'VulDock'을 `개발하게 된 배경`은 다음과 같다.
  - 2021년 기준, 컨테이너 이미지 보안 분석한 결과 51%의 이미지에 최소 1개 이상의 중대한 취약점이 포함되었고, 2020년 2사분기 동안 컨테이너 환경과 Docker 이미지 공급망을 겨냥한 대표적인 공격이 600% 증가하였다.
  - Docker 취약점을 이용하여 공격한 사례가 적지 않게 발생한 현실에 직시하여, docker 이미지를 컨테이너화하여 사용하기 전에 이미지를 통해 취약점 여부를 확인할 수 있는 툴 개발을 계획하게 되었다.
<br>

- 주제 선정 후, 자료 조사 과정을 거친 후 세운 `툴의 방향성`은 다음과 같다.
  - ✓ 컨테이너를 실행하기 전에 사용된 이미지가 가지고 있을 수 있는 버전 등의 잠재적인 문제 검사
  - ✓ 도커 이미지 분석 시 docker-compose 파일을 사용해 서비스 목록 확인
    - 취약점을 분석할 때 해당 애플리케이션이 어떤 서비스를 사용하는지 확인하기 위함
  - ✓ dagda와 같은 기존의 취약점 점검 툴에 우리만의 차별성 포함

<br>

## 👨‍👨‍👦 404 Time 팀원 
| 이름 | Github |
| -- | -- |
| 김혜민 | [HyeM207](https://github.com/HyeM207)  |
| 임정수 | [JJ503](https://github.com/JJ503)  | 
| 정민희 | [jeongminhui99](https://github.com/jeongminhui99)  | 
| 황예원 | [wwyyww](https://github.com/wwyyww)  |

<br/><br/>  

# ▶ VulDock 세부 소개

## 📌 01. 사용 방법 
1. 해당 깃허브 레파지토리를, 분석할 도커 이미지가 있는 pc에 다운로드 혹은 git pull 한다. <Br>
  (단, pc는 리눅스 기반의 운영체제이어야 한다)
2. 터미널로 툴을 다운로드한 경로 이동하여, 사용자가 명령어로 옵션과 함께 이미지 이름을 파라미터로 입력 실행한다. <br>
   `VulDock (-옵션 1개 이상) 도커이미지명`  ex. `VulDock -sn test-image`
3. 명령어를 입력 후, 툴은 사용자가 입력한 이미지이름으로 도커이미지가 있는 경로를 찾아 터미널에 띄운다. <br>
  사용자는 터미널에 출력된 경로 중 <b>분석할 도커이미지가 있는 경로의 번호를 입력</b>한다.
4. 이후, 옵션에 따라 분석한 결과를 터미널로 보여준다.
  
#### 옵션
- `-h` : 서비스 사용 방법 출력
- `-s` : 서비스 이름과 버전 출력
- `-o` : 오피셜 이미지 검사
- `-n` : 총 취약점 개수
- `-t` : 취약점 이름만 출력
- `-c` : CVE만 출력
- `-l` : CVE 링크만 출력
- `-a` : 모든 옵션 적용
  
<details>
  <summary> ➡ 출력 예시(사진)</summary>
  
![VulDock](./images/슬라이드21.PNG) 
![VulDock](./images/슬라이드22.PNG)
![VulDock](./images/슬라이드23.PNG)
  
</details>

  
<br>
  
## 📌 02. 코드 구성 
VulDock은 총 3개의 파이썬 파일로 구성되며, 각 파일별 주요 기능은 다음과 같다.
  1. `main.py` <br>
    - 이미지 경로와 docker-compose 파일 경로 탐색 <br>
    - 사용 서비스의 이름과 버전 분석 <br>
    - 'Searchsploit' 툴과 웹 크롤링을 통한 CVE Mapping으로 취약점 검사 <br>
  2. `check_linux.py` <br>
    - '주요정보통신기반시설)기술적_취약점' 기반으로 작성한 취약점 검사 코드로 Linux 기반의 OS 서비스 취약점 검사
  3. `print_table.py` <br>
    - 분석 결과 화면 구성을 위해 표 생성 
  
  
<details>
  <summary>➡ 파일 별 세부 설명(사진)</summary>
   
![VulDock](./images/슬라이드12.PNG) 
![VulDock](./images/슬라이드13.PNG)
![VulDock](./images/슬라이드14.PNG)
![VulDock](./images/슬라이드15.PNG) 
![VulDock](./images/슬라이드16.PNG)
![VulDock](./images/슬라이드17.PNG)
![VulDock](./images/슬라이드18.PNG) 
![VulDock](./images/슬라이드19.PNG)
![VulDock](./images/슬라이드20.PNG)
![VulDock](./images/슬라이드21.PNG)
![VulDock](./images/슬라이드22.PNG)
![VulDock](./images/슬라이드23.PNG)
![VulDock](./images/슬라이드24.PNG)
![VulDock](./images/슬라이드25.PNG)
![VulDock](./images/슬라이드26.PNG)
![VulDock](./images/슬라이드27.PNG)
   
</details>
  
<br>
  
## 📌 03. VulDock 흐름도 
![VulDock](./images/슬라이드28.PNG)

<br>
  
## 📌 04. 툴 소개 ppt (슬라이드 전문) 
<details>
  <summary>➡ 전체 슬라이드 보기</summary>
  
![VulDock](./images/슬라이드1.PNG) 
![VulDock](./images/슬라이드2.PNG) 
![VulDock](./images/슬라이드3.PNG)
![VulDock](./images/슬라이드4.PNG)
![VulDock](./images/슬라이드5.PNG) 
![VulDock](./images/슬라이드6.PNG)
![VulDock](./images/슬라이드7.PNG)
![VulDock](./images/슬라이드8.PNG) 
![VulDock](./images/슬라이드9.PNG) 
![VulDock](./images/슬라이드10.PNG) 
![VulDock](./images/슬라이드11.PNG) 
![VulDock](./images/슬라이드12.PNG) 
![VulDock](./images/슬라이드13.PNG)
![VulDock](./images/슬라이드14.PNG)
![VulDock](./images/슬라이드15.PNG) 
![VulDock](./images/슬라이드16.PNG)
![VulDock](./images/슬라이드17.PNG)
![VulDock](./images/슬라이드18.PNG) 
![VulDock](./images/슬라이드19.PNG)
![VulDock](./images/슬라이드20.PNG)
![VulDock](./images/슬라이드21.PNG)
![VulDock](./images/슬라이드22.PNG)
![VulDock](./images/슬라이드23.PNG)
![VulDock](./images/슬라이드24.PNG)
![VulDock](./images/슬라이드25.PNG)
![VulDock](./images/슬라이드26.PNG)
![VulDock](./images/슬라이드27.PNG)
![VulDock](./images/슬라이드28.PNG)
![VulDock](./images/슬라이드29.PNG)
![VulDock](./images/슬라이드30.PNG)
![VulDock](./images/슬라이드31.PNG)
![VulDock](./images/슬라이드32.PNG)
![VulDock](./images/슬라이드33.PNG)
![VulDock](./images/슬라이드34.PNG)
![VulDock](./images/슬라이드35.PNG)
   
</details>
