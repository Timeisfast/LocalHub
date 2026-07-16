from sqlalchemy import inspect

from app.database import engine


TABLE_NAME = "festival_items"

NEW_COLUMNS = {
    "start_date": "TEXT",
    "end_date": "TEXT",
    "description": "TEXT",
}


def alter_festival_table() -> None:
    print(f"연결된 데이터베이스: {engine.url}")

    inspector = inspect(engine)

    # 테이블 존재 여부 확인
    table_names = inspector.get_table_names()

    if TABLE_NAME not in table_names:
        raise RuntimeError(
            f"'{TABLE_NAME}' 테이블이 존재하지 않습니다. "
            f"현재 테이블 목록: {table_names}"
        )

    # 기존 컬럼 이름 조회
    existing_columns = {
        column["name"]
        for column in inspector.get_columns(TABLE_NAME)
    }

    print(f"기존 컬럼: {sorted(existing_columns)}")

    # begin(): 성공하면 commit, 실패하면 rollback
    with engine.begin() as conn:
        for column_name, column_type in NEW_COLUMNS.items():
            if column_name in existing_columns:
                print(f"건너뜀: {column_name} 컬럼이 이미 존재합니다.")
                continue

            sql = (
                f'ALTER TABLE "{TABLE_NAME}" '
                f'ADD COLUMN "{column_name}" {column_type}'
            )

            conn.exec_driver_sql(sql)
            print(f"추가 완료: {column_name} {column_type}")

    print("festival_items 테이블 수정이 완료되었습니다.")


if __name__ == "__main__":
    alter_festival_table()