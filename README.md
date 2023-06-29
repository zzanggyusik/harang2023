

## 하랑2023 프로젝트 개발을 위한 README.MD

### 본 레포지토리는 하랑2023 덕명마을 방범대에서 진행되는 프로젝트 개발을 위해 제작됨

### 프로젝트 참여자는 해당 내용을 숙지하여 프로젝트를 진행하도록 한다(주의사항 숙지 필수).

### 프로젝트 개발환경을 위한 사전 설정

- VScode 설치
- Github 아이디 필요
- Sublinemerge 설치(위치 확인 및 오류 해결을 위함) // oh-my-zsh (terminal) 사용 또한 

# Github
- 깃허브 사용 목적 :
  1. 코드 분할 개발 후 통합 과정에서 빈번한 오류 발생
     이를 해결 하기 위해 통합 환경을 구축 후 개발 진행
  2. 또한 깃허브는 이번 버전또한 저장하고 있어 오류 발생 및 데이터가 삭제되었을시 빠른 복구가 가능
- 기본 용어 정리 :
  - 레포지토리 : 저장장소(repo)
  - origin : 원격
  - git init : 초기화
  - git clone : GitHub에 있는 저장소의 주소를 입력하여 로컬로 복제
  - branch : 자신만의 버전
  - commit : 코드를 변경한 후 스냅샷을 찍음. -m 을 이용하여 메세지를 남김
  - git commit -m "{message}" : 커밋 명령어
  - git checkout {원하는 브랜치} : 원하는 브랜치로 이동
  - git push : 작업하는 로컬환경(본인 컴퓨터)에서 깃허브 프로젝트 레포지리에 올릴때 사용
  - git pull : 레포지토리에 있는 최신 버전을 받아올때 사용
  - git merge {합칠 브랜치} -m "{message}" : 현재 브랜치에서 다른 브랜치를 합칠때 사용
- - -
## Git Flow 사용이유
- 레파지토리는 통합을 고려하여 관리해야 함.
- 관련 기능이 모여있는 폴더별로 관리하여 직관적으로 파악 가능해야 좋음. (동료 개발자 기준)
- 자기가 개발하고 있는 코드 내에 팀원이 개발한 코드를 복사, 붙여넣기하는 것이 아닌, 팀원의 코드 모듈을 호출해서 사용하는 방식을 사용해야 함. (주석을 잘 달아야 하는 이유 $\rightarrow$ 동료가 자신의 코드를 호출할 때 코드의 기능을 설명하기 위함)
  - 함수에 주석을 달면, 호출한 함수 위에 마우스커서를 갖다댈 시 함수에 대한 설명이 보임
  -  ![image](https://github.com/SYSAI-sojungdan/good-thing/assets/89232601/8ea45cf9-8414-453b-a10a-7555321b502b)

- 위 내용을 지키면서 여러명이 개발하기 어렵기 때문에, git flow 기능을 사용해서 개발물을 관리함
---
## branch 종류(당장 개발에 필요한 것만)
- branch는 지금까지 폴더명에 이니셜을 넣어서 구분하듯이, 개발물을 구분하기 위해 사용한다고 생각하면 됨
1. main : 가장 기본이 되는 branch. 동작에 지장이 없는(버그가 없는) 코드를 저장. $\rightarrow$ 개발 단계가 가장 뒤에 있어야 함.(동작이 되는 가장 옛날 코드)
2. develop : 현재 개발중인 단계의 코드 저장. 이 branch는 모든 개발자가 개발하는 기능이 통합되고, 이 branch에서 통합 테스트를 진행함. 테스트에 성공한 코드를 main에 옮기는 식. 이 프로젝트에서는 DiPMaS라는 큰 틀에 해당함.
3. feature : 특정 기능을 구현하는 branch. 시뮬레이션, pyzmq등의 소규모 단위의 기능을 개발할 때 쓰는 branch. feature/-- 등의 형식으로 사용되며(정확히는 develop/feature/--), feature/simul_model, feature/router_dealer 등 내가 어떤 기능을 구현하는지 적는 것이 일반적임. 이번 프로젝트에서도 이런 식으로 적어도 되지만, 기존에 관리하던 것처럼 feature/이름이니셜 등으로 사용해도 됨.

- origin이란
  - origin은 원격의 의미로, 명령어에 origin이 들어간다면 원격 저장소를 작업한다는 의미임
    - git pull main : 로컬(자기 컴퓨터)에 저장되어 있는 main branch의 작업물을 가져옴
    - git pull origin main : 원격(깃허브 클라우드)에 저장되어 있는 main branch의 작업물을 가져옴.
   - 깃허브는 참여중인 개발자가 모두 동일한 코드를 공유하기 위해 사용하므로, 최종적으로 origin(원격 저장소)를 잘 관리하는 것이 목표
- - -
## Git Flow 사용법
- 윈도우의 경우 git 설치 시 기본 설치, MAC은 brew를 사용해 따로 설치해야 함.
1. git 레파지토리를 clone한 디렉토리에서(.git이 있는), 터미널에 ```git init``` 명령어 입력
   1. ![image](https://github.com/SYSAI-sojungdan/good-thing/assets/89232601/e78c984c-7b8c-42d9-956f-d45a0af9a997)
2. 터미널에 ```git flow init``` 명령어 입력 후, 실행 내용이 나오면 엔터 연타(branch 이름 설정, 입력 없이 엔터 : Default 설정을 사용한다는 의미)
   1. ![image](https://github.com/SYSAI-sojungdan/good-thing/assets/89232601/167e3a5f-de62-4e08-bf2d-f2edaf0dd9a2)
3. 자동으로 branch가 develop으로 설정됨(VSCODE 기준 왼쪽 아래)
   1. ![image](https://github.com/SYSAI-sojungdan/good-thing/assets/89232601/3062f93f-843d-45ed-8d81-ce4587d44330)
   - 최초 git flow 설정 시 develop branch는 자신의 로컬 main폴더를 그대로 가져옴. 이미 팀원이 develop에서 작업을 하고있다면, ```git pull origin develop``` 명령어를 통해 작업물을 pull해야함.
4. develop branch에서 터미널에 ```git flow feature start "이름"```을 입력하여 feature branch 생성
   1. ![image](https://github.com/SYSAI-sojungdan/good-thing/assets/89232601/cd769453-2356-4a65-9cab-c73aaea5a787)
5. feature에서 자신이 맡은 부분을 개발(웬만하면 다른 팀원과 동일한 파일을 안 건드는 것이 좋음)
6. feature에서 개발하며 틈틈히 origin에 자신의 feature 업데이트
   1. ```git add .``` (.git파일이 있는 홈 디렉토리에서 해야 모든 변경사항이 반영됨)
   2. ```git commit -m "메세지"```
   3. ```git push origin feature/이름```
7. feature branch에서 특정 기능에 대한 개발 및 테스트가 완료되면, 해당 작업 내용을 develop으로 합쳐야 함
   1. ```git flow feature finish``` 명령어 입력
   2. develop branch와 비교하여 feature에서 변경된 사항만 develop과 병합되며, feature/이름 branch는 자동으로 삭제됨
   3. 되돌리기 힘들기 때문에 합치기 전에 체크 한번더!
8. develop에서 각자 개발한 기능의 통합이 잘 됐다면 해당 작업물을 main에 올림
   1. develop branch 업데이트
      1. ```git add .``` (.git파일이 있는 홈 디렉토리에서 해야 모든 변경사항이 반영됨)
      2. ```git commit -m "메세지"```
      3. ```git push origin develop```
   2. develop branch에서 ```git checkout main``` 명령어 입력.(main branch로 이동)
   3. ```git push origin main```명령어 입력. (로컬에 저장된 코드를 깃허브 클라우드 원격지로 옮김)

---
# 참고(깃허브 관리법)
### 프로젝트 개발

1. VSCode를 실행하고 GitHub repository를 clone 한다.
   ![스크린샷 2022-12-14 오후 8 02 53](https://user-images.githubusercontent.com/97441976/207578304-275e9d38-1b8f-4859-a15a-229c6b5e2b23.png)

2. 아래 그림과 같은 창에 레포지토리의 주소를 입력한다.
   <br>
   ![스크린샷 2022-12-14 오후 8 03 43](https://user-images.githubusercontent.com/97441976/207578636-c618f715-2db9-42d7-b2bd-2aa599c506d9.png)
   <br>
   (본 프로젝트의 경우 https://github.com/zzanggyusik/harang2023.git)

3. Sublinemerge를 이용하여 레포지토리 열기.

   - Local Repositories의 Open Repository
     폴더는 1, 2 번을 진행하며 clone으로 만들어진 폴더 선택

4. VSCode에서 터미널 실행 (!!아래 명령어는 각 오류가 없을시 다음단계 진행!!)
   <br>
   개발 브랜치까지 가는 방법 :

   - git pull

   - git checkout develop

   - git pull
   - git flow feature start {본인 이름 또는 팀}

   Sublimemerge를 이용하여 현재 위치 확인
   <br>![스크린샷 2022-12-14 오후 8 18 20](https://user-images.githubusercontent.com/97441976/207581727-c0fdfb88-aa26-4f14-99ed-986ccf608db1.png)
   <br>
   이처럼 feature/ 로 시작하는 곳에 불이 들어와있어야 함

5. 왼쪽 Explorer(종이 두장 이모티콘)를 이용하여 개발 진행

6. 개발 완료후

   - git add .

   - git commit -m "{message}"

   - git push
     <br>이떄 아래 그림
     <br>![스크린샷 2022-12-14 오후 8 22 39](https://user-images.githubusercontent.com/97441976/207582588-b1d701dc-798f-49ac-a9bd-2a481597d091.png)
     <br>과 같은 메세지가 뜨는데 중간의 git push --set 으로 시작하는 라인을 복사해서 다시 입력

7. 브랜치 통합
   예: 000님 기능 구현하신 브랜치 디벨롭에 올려주세요.

   - git checkout develop
   - git pull
   - git merge feature/{생성한 이름} -m "{message}"
   - git commit -m "{message}"
   - git push

### 주의 사항

1. 깃허브의 기본은 main으로 설정되어 있다. 따라서 개발을 진행할때 본인의 위치가 main이 아닌 개인 feature로 설정되어 있는지 반드시 확인해야 한다.
2. 깃허브의 메인은 되도록 건드리지 않는다.
   이는 개인 feature를 이용하여 개발을 진행하여 develop 브랜치를 이용하여 통합을 확인한다.
3. 본인 feature이외 다른 프로젝트 참여자의 feature는 되도록 건드리지 않는다.
4. 충돌 방지를 위해 다른 사람이 작성한 내용은 수정하지 않는다.
5. 깃허브 사용중 충돌 발생및 기타 오류 발생시 프로젝트 관리자(함규식, 김현기)에게 물어본다.

<br>

대표 작성자 : SysAI Lab 함규식
<br>
E-mail : gsham@edu.hanbat.ac.kr
<br>
Phone : 010-9946-9297
<br>
K-talk : zzanggyusik