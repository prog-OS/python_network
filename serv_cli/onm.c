TBMM_VASP 검색
sprintf(query, "INSERT INTO TBMM_VASP(code, value) VALUES (%d, '%s')", stVasp.count, VASID);
stVasp.count 값이 어떻게 설정 되는지 등등
--------------------------------------------------------------------------------------------
OMP (Operation Maintenance Processor) : MP와 연동하여 실제 운영관리 기능을 제공하는 운영 및 보전 프로세서 (통계 관리 서버)

FIMD (Fault Information Management Daemon) : OMP 상태 장애관리 프로세스
--------------------------------------------------------------------------------------------
OMP - src - PSAD - FIN_PRC - proc_db.cc / init.c

typedef struct {
	int  code;
	char value[20];	// (주의) table에 맞춘것이며, minfo의 originator와 동일하지 않음
	//char description[40];	// (주석) table에는 있지만 의미 없으므로 제거함
}_ST_VASP_ID_BODY;

typedef struct {
	int count;
	_ST_VASP_ID_BODY body[MAX_VASP];
}_ST_VASP_ID;

_ST_VASP_ID			*vasp_id, stVasp;

===============================================================================================
OMP/src/PSAD/FIN_PRC/init.c
init_shm_statistic() : 통계용 공유 메모리 로드 및 생성
	conflib_getNthTokenInFileSection (
		const char *fname,		/* configuration file name */
		const char *section,	/* section name */
		const char *keyword,	/* keyword -> 찾고자 하는 라인에 있는 첫번째 token name ("=" 앞에 있는 token) */
		int  n,					/* 몇번째 token을 찾을것인지 지정 ("=" 뒤에 있는 n번째 token) */
		char *string)			/* 찾은 token이 저장된 string */
	/*------------------------------------------------------------------------------
	 * file을 열어 지정된 section내에서 keyword에 해당하는 라인을 찾아,
	 *	"=" 뒤쪽에서 n번째 token를 string에 복사한다.
	 * - conf 파일에는 "keyword = aaa bbb ccc ..." 의 형식으로 구성되어 있어야 한다.
	 * - conf 파일 한줄에 keyword = 를 제외하고 최대 16개까지 token를 기록할 수 있다.
	 * - 예를들어, "xxxx = aaa bbb ccc" 에서 bbb를 찾고 싶은 경우,
	 *	keyword=xxxx, n=2를 지정해야 한다.
	------------------------------------------------------------------------------*/

		- section의 시작위치로 이동
		conflib_seekSection()

		- section내에서 keyword에 해당하는 line을 찾아 "=" 뒤쪽 내용을 buff에 복사
		conflib_getStringInSection()
		/*------------------------------------------------------------------------------
		 * fopen으로 열려있는 파일에서 현재 fp위치에서부터 현재 section내에서 지정된 keyword에
		 *	해당하는 line을 찾아, "=" 뒤쪽 내용을 string에 복사한다.
		 * - 검색한 line_number를 return한다.
		------------------------------------------------------------------------------*/

		- n번째 token을 string에 복사
		- 찾은 token을 user영역에 복사





===============================================================================================
OMP/src/PSAD/FIN_PRC/main.c

main()
	getenv() : 환경 변수 리스트 검색
	gstrtail() : 문자열(main)을 구분자(delimiter)로 나눠진 마지막 문자열을 리턴함
	구분자가 없으면, main의 포인터를 넘김
		gstrgstr() : 문자열(main)의 마지막에서 부터 일치하는 문자열(find)의 포인터를 넘김

	init_sys() : mid_prc init 함수들 호출
		commlib_setupSignals(NULL)
		init_log()
		init_common() : 필요한 환경 변수들 정보 가져오기
			conflib_getStringInFileSectionToInt()
			/*------------------------------------------------------------------------------
			 * file을 열어 지정된 section내에서 keyword에 해당하는 라인을 찾아,
			 *   "=" 뒤에 있는 내용을 string에 모두 복사한다.
			 * string 의 내용을 int 형으로 변환하여 리턴한다.
			------------------------------------------------------------------------------*/
				- section의 시작위치로 이동
				conflib_seekSection()

				- section내에서 keyword에 해당하는 line을 찾아 "=" 뒤쪽 내용을 buff에 복사
				conflib_getStringInSection()
				/*------------------------------------------------------------------------------
				 * fopen으로 열려있는 파일에서 현재 fp위치에서부터 현재 section내에서 지정된 keyword에
				 *	해당하는 line을 찾아, "=" 뒤쪽 내용을 string에 복사한다.
				 * - 검색한 line_number를 return한다.
				------------------------------------------------------------------------------*/

		keepalivelib_init()
			conflib_getNthTokenInFileSection()

		init_shm() : 공유메모리 연동
			conflib_getNthTokenInFileSection()


		init_msgQ() : message Queue 연동
			conflib_getNthTokenInFileSection()



	thread 함수
	t_alive() : Process Alive state Check thread
		keepalivelib_increase()
		commlib_milliSleepEx()

	thread 함수
	t_change_flag() : 각 공유메모리의 flag 값을 일정 시간에 변경
		//------------------------------------------------------------------------------
		//  PSAD_RUN_ON 이면 PSAD 프로세스들이 일을 시작한다. (최대처리시간 1분)
		//  PSAD 에서 공유메모리의 통계를 가져간다음에는 바로 PSAD_RUN_OFF 로 변경시켜준다.
		//------------------------------------------------------------------------------

		//------------------------------------------------------------------------------
		//  모든 flag가 PSAD_RUN_OFF 면 MIDDLE_PRC/FIN_PRC 가 일을 시작한다.
		//  (1분이상 지연될 경우 강제로 초기화해 줌)
		//------------------------------------------------------------------------------

		//------------------------------------------------------------------------------
		//  flag off 는 psad 각 프로세스에서 memset시 자동 OFF 된다
		//------------------------------------------------------------------------------

	thread 함수
	observe_thread() : thread 들의 상태 체크하는 감시 쓰레드
		thread_recreate() :
			//  기존 thread 가 맺고있던 socket close
			//  해당 thread 취소 요청
			//  새로운 thread 생성 전  각 필드 초기화
			//  thread 의 socket connect
			connect_psad() : PSAD_INFO 와 연결
				socket()
				fcntl() : 비봉쇄
				signal(SIGPIPE, SIG_IGN)
				connect()



===============================================================================================
OMP/src/PSAD/FIN_PRC/updatelist.cc
main()
	utils_init_common()

	utils_init_shm_info()
		- MO CODE READ
		- VASP CODE READ
		- DOMAIN CODE READ
		- MVNE CODE READ
		- CONT_ERR_LIST CODE READ
		conflib_getNthTokenInFileSection()
		strtol()
		shmget()
		shmat()

	utils_init_shm_statistic()
		- MO 정보 리셋시 flag 확인을 위해 : MO통계에 쓰일 공유 메모리 키값을 얻어 온다
		- VASP 정보 리셋시 flag 확인을 위해 : W2P_MT통계에 쓰일 공유 메모리 키값을 얻어 온다
		- DOMAIN 정보 리셋시 flag 확인을 위해 : P2M통계에 쓰일 공유 메모리 키값을 얻어 온다
		conflib_getNthTokenInFileSection()
		strtol()
		shmget()
		shmat()

	utils_init_oracle() : ORACLE connect
		conflib_getNthTokenInFileSection() : 
		/*------------------------------------------------------------------------------
		 * file을 열어 지정된 section내에서 keyword에 해당하는 라인을 찾아,
		 *	"=" 뒤쪽에서 n번째 token를 string에 복사한다.
		 * - conf 파일에는 "keyword = aaa bbb ccc ..." 의 형식으로 구성되어 있어야 한다.
		 * - conf 파일 한줄에 keyword = 를 제외하고 최대 16개까지 token를 기록할 수 있다.
		 * - 예를들어, "xxxx = aaa bbb ccc" 에서 bbb를 찾고 싶은 경우,
		 *	keyword=xxxx, n=2를 지정해야 한다.
		------------------------------------------------------------------------------*/
			fopen()
			- section의 시작위치로 이동
			conflib_seekSection()
			- section내에서 keyword에 해당하는 line을 찾아 "=" 뒤쪽 내용을 buff에 복사
			conflib_getStringInSection()
			- n번째 token을 string에 복사
			sscanf()

			- 찾은 token을 user영역에 복사

		utils_connect_oracle()	

	update_code_mo() : MO(특번) LIST 획득 (soap.tab)
		- DB 연결 확인
		utils_check_connect_oracle()
		- fname = "/mmsnfs2/mms/conf/soap.tab"

		- 업데이트 조건 체크 시작
		fgets()
			- 문자 체크
			- Type
			- Number
			- AppID
			- SVName
			- VASID
			- 값 유효성 확인
			VASID 체크 ('$' 제외시킴 )
			MT 제외
			VASID로 NUMBER대체함
			- (중요) 대소문자 구분없이 검색하므로 모두 소문자화 함
			gstrtolower(Number);

			- mo_id 에서 찾기(정렬하지 않으므로 (부분일치로 검색되므로 bsearch를 사용하지 않음))

			- DB table 에 정보 INSERT/UPDATE
			- mo_id 에 정보 INSERT/UPDATE


	update_code_mvne() : MVNE LIST 획득

	update_list_cont_err() : CONTENTS ERROR LIST 획득

	update_code_vasp() : VASP LIST 획득
		- DB 연결 확인
		utils_check_connect_oracle()
		- fname = "/mmsnfs2/mms/conf/soap.tab"

		- 업데이트 조건 체크 시작
		fgets()
			- 문자 체크
			- Type
			- Number
			- AppID
			- SVName
			- VASID
			- 값 유효성 확인
			  MO 제외
			- (중요) 대소문자 구분없이 검색하므로 모두 소문자화 함
			gstrtolower(Number);

			- vasp_id 에서 찾기
			- 정의된 최대개수 체크
			- DB table 에 정보 INSERT
			sprintf(query, "INSERT INTO TBMM_VASP(code, value) VALUES (%d, '%s')", stVasp.count, VASID);
			- stVasp 에 정보 INSERT

	update_code_domain()

======================================================================================
OMP/src/PSAD/FIN_PRC/init.c
init_shm_info() : 기본 정보 데이타 용 공유메모리  로드 및 생성
	-  MO CODE 를 얻는다
	conflib_getNthTokenInFileSection()
	strtol()
	shmget()
	shmat()
	
	get_code_mo()
		/* DB 에 있는 특번 에 대한 정보를 공유메모리로 가져온다.
 *						주의) value로 오름차순 정렬되어야 binary search를 사용할 수 있음
 *						만약, 임의로 추가되는 정보가 있다면 다시 정렬해야함 */
	


	- VASP ID를 얻는다
	get_code_vasp()
		/* DB 에 있는 vasid 에 대한 정보를 공유메모리로 가져온다.
 *						주의) value로 오름차순 정렬되어야 binary search를 사용할 수 있음
 *						만약, 임의로 추가되는 정보가 있다면 다시 정렬해야함 */


~~~~~~~
	- DOMAIN CODE 를 얻는다
	get_code_domain()

	- MVNE ID CODE 를 얻는다
	get_code_mvne()

	- CONT_ERR_LIST ID CODE 를 얻는다
	get_code_cont_err()