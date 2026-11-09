import sys
from datetime import datetime
from pathlib import Path

# 사용법:
#   uv run python 03-python-apps/rename_files.py 폴더 [이름머리]          미리보기만
#   uv run python 03-python-apps/rename_files.py 폴더 [이름머리] --apply  실제로 바꾸기


def plan(folder, prefix):
    """바꿀 이름 목록을 만든다: 이름머리_수정날짜_순번.확장자"""
    files = sorted(p for p in folder.iterdir() if p.is_file())
    result = []
    for number, path in enumerate(files, start=1):
        day = datetime.fromtimestamp(path.stat().st_mtime).strftime("%Y%m%d")
        new_name = f"{prefix}_{day}_{number:03d}{path.suffix.lower()}"
        result.append((path, path.with_name(new_name)))
    return result


def main():
    args = [a for a in sys.argv[1:] if a != "--apply"]
    apply = "--apply" in sys.argv
    if not args:
        print("폴더를 알려 주세요. 예: uv run python 03-python-apps/rename_files.py 03-python-apps/rename_test 여행")
        return
    folder = Path(args[0])
    prefix = args[1] if len(args) > 1 else "photo"

    changes = plan(folder, prefix)
    targets = [new for _, new in changes]
    if len(set(targets)) != len(targets) or any(new.exists() and new != old for old, new in changes):
        print("바꿀 이름이 이미 있는 파일과 겹칩니다. 이름머리를 바꿔 주세요.")
        return

    for old, new in changes:
        print(f"  {old.name}  ->  {new.name}")
    if not apply:
        print(f"미리보기입니다. {len(changes)}개 파일 이름이 위처럼 바뀝니다. 바꾸려면 끝에 --apply를 붙여 다시 실행하세요.")
        return
    for old, new in changes:
        old.rename(new)
    print(f"{len(changes)}개 파일 이름을 바꿨습니다.")


main()
