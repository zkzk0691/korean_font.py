
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib as mpl
import os
import platform # 운영체제 정보를 가져오기 위함

def set_korean_font(font_name='AppleGothic', force_rebuild=False):
    """
    Matplotlib에서 한글 폰트를 설정하고 마이너스 부호 깨짐을 방지합니다.
    macOS에서는 기본적으로 'AppleGothic'을 사용하며, 다른 폰트도 지정 가능합니다.
    Windows에서는 'Malgun Gothic'을 기본으로 시도합니다.
    
    Args:
        font_name (str): 설정하려는 폰트의 이름. 기본값은 'AppleGothic' (macOS) 또는 'Malgun Gothic' (Windows).
        force_rebuild (bool): True로 설정하면 Matplotlib 폰트 캐시를 강제로 재구축합니다.
                               폰트가 제대로 적용되지 않을 때 시도해볼 수 있습니다.
    """

    # 폰트 캐시 재구축 (필요한 경우에만 수행하도록 옵션 추가)
    if force_rebuild:
        print("Matplotlib 폰트 캐시를 재구축 중입니다. 잠시 기다려 주세요...")
        fm.fontManager.rebuild()
        print("폰트 캐시 재구축 완료.")

    # 운영체제별 기본 폰트 설정
    if platform.system() == 'Darwin': # macOS
        default_font = 'AppleGothic'
        # macOS 폰트 디렉토리
        font_dirs = [
            "/System/Library/Fonts",
            "/System/Library/Fonts/Supplemental",
            "/Library/Fonts",
            os.path.expanduser("~/Library/Fonts")
        ]
    elif platform.system() == 'Windows': # Windows
        default_font = 'Malgun Gothic'
        # Windows 폰트 디렉토리 (일반적으로 이 경로에 한글 폰트가 있습니다)
        font_dirs = [
            os.environ.get("WINDIR") + "\Fonts" if os.environ.get("WINDIR") else "C:\Windows\Fonts"
        ]
    else: # Linux 등 기타 OS (나눔고딕을 많이 사용하므로 예시 추가)
        default_font = 'NanumGothic' # 리눅스는 보통 기본 한글 폰트가 없으므로 직접 설치 필요
        font_dirs = [
            "/usr/share/fonts",
            "/usr/local/share/fonts",
            os.path.expanduser("~/.local/share/fonts")
        ]
    
    # 사용자가 font_name을 지정하지 않았다면 운영체제 기본 폰트 사용
    if font_name == 'AppleGothic' and platform.system() != 'Darwin': # macOS가 아니면 기본값 변경
        font_name = default_font
    elif font_name == 'Malgun Gothic' and platform.system() != 'Windows': # Windows가 아니면 기본값 변경
        font_name = default_font
    # 그 외의 경우 (사용자가 특정 폰트를 지정했거나, 기본값이 다른 OS용이 아닐 경우) font_name 그대로 사용

    # 폰트 파일 탐색 및 설정
    font_found = False
    # findSystemFonts는 인자로 fontpaths를 받음 (2.x 버전에서는 font_dirs 인자명으로 사용)
    # 현재 matplotlib 버전은 fm.findSystemFonts(fontpaths=font_dirs) 사용
    for font_path in fm.findSystemFonts(fontpaths=font_dirs, fontext='ttf'):
        try:
            # 폰트의 실제 이름 가져오기
            font_prop = fm.FontProperties(fname=font_path)
            # 대소문자 구분 없이 비교
            if font_name.lower() in font_prop.get_name().lower():
                mpl.rcParams['font.family'] = font_prop.get_name()
                font_found = True
                print(f"'{mpl.rcParams['font.family']}' 폰트가 성공적으로 설정되었습니다.")
                break # 폰트를 찾았으면 반복 중단
        except Exception:
            # 유효하지 않은 폰트 파일은 건너뜀
            continue

    if not font_found:
        print(f"경고: '{font_name}' 폰트를 시스템에서 찾을 수 없습니다.")
        print("설정 가능한 폰트 목록:")
        # 모든 사용 가능한 폰트 이름 출력
        for fprop in fm.fontManager.ttflist:
            print(fprop.name)
        print("위 목록에서 다른 폰트 이름을 시도해보세요. (예: 'NanumGothic', 'Malgun Gothic' 등)")
        print("또는 해당 폰트가 시스템에 설치되어 있는지 확인해주세요.")
        # 대체 폰트 설정 (기본 sans-serif 계열)
        mpl.rcParams['font.family'] = 'sans-serif'


    # 마이너스 부호 깨짐 방지
    mpl.rcParams['axes.unicode_minus'] = False
    print("Matplotlib 마이너스 부호 깨짐 방지가 설정되었습니다.")


# 이 부분이 모듈로 임포트될 때는 실행되지 않고, 직접 스크립트 실행할 때만 실행되도록 보호
if __name__ == "__main__":
    print("이 스크립트를 직접 실행했습니다. 한글 폰트 설정을 시도합니다.")
    # 사용 예시 (macOS 기본 폰트)
    set_korean_font('AppleGothic') 
    
    # 만약 폰트가 적용되지 않는다면 아래처럼 강제로 캐시 재구축 시도
    # set_korean_font('AppleGothic', force_rebuild=True)

    # 폰트가 제대로 설정되었는지 확인하는 간단한 그래프
    plt.figure(figsize=(6, 4))
    plt.plot([1, 2, 3], [10, 20, 15])
    plt.title('한글 제목 테스트')
    plt.xlabel('엑스축')
    plt.ylabel('와이축')
    plt.text(1.5, 12, '텍스트 표시', fontsize=12) # 텍스트도 한글 확인
    plt.show()


#아래 두 줄을 입력하여 실행합니다.
#import jupyter_fonts
#jupyter_fonts.set_korean_font('AppleGothic') # 또는 원하는 폰트 이름
