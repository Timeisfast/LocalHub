import json
from pathlib import Path

from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models_event import FestivalItem


# update_festival.py와 같은 폴더에 있는 JSON 파일
JSON_PATH = Path(__file__).resolve().parent / "seoul_festival_plus.json"

# 이번에 업데이트할 컬럼만 명시
UPDATE_FIELDS = (
    "start_date",
    "end_date",
    "description",
)


def clean_value(value):
    """
    문자열 앞뒤 공백을 제거한다.
    빈 문자열은 DB에 빈 문자열 대신 None(NULL)으로 저장한다.
    """
    if isinstance(value, str):
        value = value.strip()

        if value == "":
            return None

    return value


def load_festival_items() -> list[dict]:
    """
    JSON 파일을 읽어 축제 목록을 반환한다.

    다음 두 구조를 모두 지원한다.

    1. {"items": [...]}
    2. [...]
    """
    if not JSON_PATH.exists():
        raise FileNotFoundError(
            f"JSON 파일을 찾을 수 없습니다: {JSON_PATH}"
        )

    with JSON_PATH.open("r", encoding="utf-8") as file:
        data = json.load(file)

    if isinstance(data, dict):
        items = data.get("items")

    elif isinstance(data, list):
        items = data

    else:
        raise ValueError(
            "JSON의 최상위 구조는 객체 또는 배열이어야 합니다."
        )

    if not isinstance(items, list):
        raise ValueError(
            "JSON에서 축제 목록을 찾지 못했습니다. "
            "'items' 배열이 있는지 확인하세요."
        )

    return items


def update_festivals() -> None:
    items = load_festival_items()

    print(f"JSON 경로: {JSON_PATH}")
    print(f"JSON 축제 개수: {len(items)}개")

    updated_count = 0
    not_found_count = 0
    skipped_count = 0

    not_found_contentids = []

    db: Session = SessionLocal()

    try:
        for index, item in enumerate(items, start=1):
            contentid = item.get("contentid")

            # contentid가 없으면 어떤 DB 행인지 찾을 수 없음
            if contentid is None or str(contentid).strip() == "":
                skipped_count += 1
                print(
                    f"[{index}] 건너뜀: contentid가 없습니다."
                )
                continue

            # DB의 contentid 타입이 문자열이라면 아래 변환이 적절함
            lookup_contentid = str(contentid).strip()

            festival = (
                db.query(FestivalItem)
                .filter(
                    FestivalItem.contentid == lookup_contentid
                )
                .first()
            )

            if festival is None:
                not_found_count += 1
                not_found_contentids.append(lookup_contentid)

                print(
                    f"[{index}] DB에서 찾지 못함: "
                    f"contentid={lookup_contentid}"
                )
                continue

            has_update_field = False

            # 기존 title, address 등의 컬럼은 건드리지 않고
            # 새로 추가한 세 컬럼만 업데이트
            for field_name in UPDATE_FIELDS:
                if field_name in item:
                    value = clean_value(item[field_name])

                    setattr(
                        festival,
                        field_name,
                        value,
                    )

                    has_update_field = True

            if not has_update_field:
                skipped_count += 1

                print(
                    f"[{index}] 건너뜀: "
                    f"추가 컬럼 데이터가 없습니다. "
                    f"contentid={lookup_contentid}"
                )
                continue

            updated_count += 1

        # 모든 축제 업데이트가 정상 처리된 뒤 한 번만 반영
        db.commit()

    except Exception:
        # 중간에 오류가 발생하면 이번 실행에서 변경한 내용을 취소
        db.rollback()
        raise

    finally:
        db.close()

    print()
    print("========== 업데이트 결과 ==========")
    print(f"업데이트 완료: {updated_count}개")
    print(f"DB에서 찾지 못함: {not_found_count}개")
    print(f"데이터 부족으로 건너뜀: {skipped_count}개")

    if not_found_contentids:
        print()
        print("DB에서 찾지 못한 contentid:")
        print(not_found_contentids)


if __name__ == "__main__":
    update_festivals()