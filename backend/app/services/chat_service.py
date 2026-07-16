import json
import logging
import os
import re
from dataclasses import dataclass
from datetime import date, timedelta
from typing import Literal

from openai import (
    APIConnectionError,
    APIStatusError,
    APITimeoutError,
    OpenAI,
)
from sqlalchemy import or_
from sqlalchemy.orm import Session

from .. import models


logger = logging.getLogger(__name__)


Category = Literal[
    "tourist",
    "shopping",
    "festival",
    "mixed",
]


ALLOWED_MODEL = "gpt-5-mini"

DEFAULT_RESULT_LIMIT = 4
MAX_RESULT_LIMIT = 5


SEOUL_DISTRICTS = [
    "종로구",
    "중구",
    "용산구",
    "성동구",
    "광진구",
    "동대문구",
    "중랑구",
    "성북구",
    "강북구",
    "도봉구",
    "노원구",
    "은평구",
    "서대문구",
    "마포구",
    "양천구",
    "강서구",
    "구로구",
    "금천구",
    "영등포구",
    "동작구",
    "관악구",
    "서초구",
    "강남구",
    "송파구",
    "강동구",
]


CATEGORY_KEYWORDS = {
    "tourist": (
        "관광지",
        "관광 명소",
        "명소",
        "랜드마크",
        "볼거리",
    ),
    "shopping": (
        "쇼핑",
        "쇼핑몰",
        "시장",
        "백화점",
        "상점",
        "기념품",
    ),
    "festival": (
        "축제",
        "행사",
        "페스티벌",
        "이벤트",
    ),
}


MIXED_KEYWORDS = {
    "가볼만한 곳",
    "가볼 만한 곳",
    "데이트",
    "놀거리",
    "갈만한 곳",
    "갈 만한 곳",
    "주말 추천",
    "여행 추천",
}


STOPWORDS = {
    "서울",
    "서울시",
    "근처",
    "주변",
    "에서",
    "으로",
    "에게",
    "있는",
    "추천",
    "추천해줘",
    "추천해주세요",
    "알려줘",
    "알려주세요",
    "보여줘",
    "찾아줘",
    "검색해줘",
    "위치",
    "어디",
    "관련",
    "정보",
    "관광",
    "관광지",
    "명소",
    "쇼핑",
    "쇼핑몰",
    "시장",
    "축제",
    "행사",
    "페스티벌",
    "오늘",
    "내일",
    "이번",
    "이번주",
    "이번주말",
    "이번달",
    "주말",
    "이번 주",
    "이번 주말",
    "이번 달",
    "현재",
    "진행",
    "진행중",
    "열리는",
    "갈만한",
    "가볼만한",
    "곳",
}


class ChatConfigurationError(RuntimeError):
    """API 키, 모델명 등 챗봇 설정 오류."""


class ChatExternalAPIError(RuntimeError):
    """외부 AI API 호출 오류."""


@dataclass
class SearchPlan:
    intent: Category
    district: str | None
    keywords: list[str]
    start_date: date | None
    end_date: date | None


def get_openai_client() -> OpenAI:
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise ChatConfigurationError(
            "OPENAI_API_KEY가 설정되지 않았습니다."
        )

    return OpenAI(
        api_key=api_key,
        timeout=10000.0,
        max_retries=1,
    )


def get_model_name() -> str:
    configured_model = os.getenv(
        "OPENAI_MODEL",
        ALLOWED_MODEL,
    ).strip()

    if configured_model != ALLOWED_MODEL:
        raise ChatConfigurationError(
            "LocalHub 챗봇은 gpt-5-mini 모델만 사용할 수 있습니다."
        )

    return ALLOWED_MODEL


def get_result_limit() -> int:
    raw_value = os.getenv(
        "CHAT_RESULT_LIMIT",
        str(DEFAULT_RESULT_LIMIT),
    )

    try:
        limit = int(raw_value)
    except ValueError:
        limit = DEFAULT_RESULT_LIMIT

    return max(
        1,
        min(limit, MAX_RESULT_LIMIT),
    )


def normalize_message(message: str) -> str:
    return " ".join(message.strip().split())


def extract_intent(message: str) -> Category:
    detected_categories: list[Category] = []

    for category, keywords in CATEGORY_KEYWORDS.items():
        if any(keyword in message for keyword in keywords):
            detected_categories.append(category)

    # 관광지와 쇼핑 등 여러 유형이 동시에 등장
    if len(detected_categories) >= 2:
        return "mixed"

    if len(detected_categories) == 1:
        return detected_categories[0]

    # "강남구 데이트 장소 추천"처럼
    # 특정 유형 없이 전체 추천을 요청
    if any(keyword in message for keyword in MIXED_KEYWORDS):
        return "mixed"

    # 유형을 명시하지 않은 질문도 세 테이블에서 통합 검색
    return "mixed"


def extract_district(message: str) -> str | None:
    # 강남구, 종로구처럼 전체 이름 우선 확인
    for district in SEOUL_DISTRICTS:
        if district in message:
            return district

    # 강남, 종로처럼 '구' 생략 처리
    for district in SEOUL_DISTRICTS:
        short_name = district.removesuffix("구")

        # 중구 → 중과 같은 한 글자 별칭은 오인식 위험이 큼
        if len(short_name) < 2:
            continue

        if short_name in message:
            return district

    return None


def get_week_range(today: date) -> tuple[date, date]:
    monday = today - timedelta(days=today.weekday())
    sunday = monday + timedelta(days=6)

    return monday, sunday


def get_weekend_range(today: date) -> tuple[date, date]:
    # 토요일
    if today.weekday() == 5:
        return today, today + timedelta(days=1)

    # 일요일
    if today.weekday() == 6:
        return today, today

    saturday = today + timedelta(
        days=5 - today.weekday()
    )
    sunday = saturday + timedelta(days=1)

    return saturday, sunday


def extract_date_range(
    message: str,
) -> tuple[date | None, date | None]:
    today = date.today()

    if "오늘" in message:
        return today, today

    if "내일" in message:
        tomorrow = today + timedelta(days=1)
        return tomorrow, tomorrow

    if "이번 주말" in message or "이번주말" in message:
        return get_weekend_range(today)

    if "이번 주" in message or "이번주" in message:
        return get_week_range(today)

    if "이번 달" in message or "이번달" in message:
        first_day = today.replace(day=1)

        if today.month == 12:
            next_month = date(
                today.year + 1,
                1,
                1,
            )
        else:
            next_month = date(
                today.year,
                today.month + 1,
                1,
            )

        last_day = next_month - timedelta(days=1)

        return first_day, last_day

    # 2026-07-20, 2026.07.20, 2026/07/20
    date_match = re.search(
        r"(20\d{2})[-./](\d{1,2})[-./](\d{1,2})",
        message,
    )

    if date_match:
        try:
            selected_date = date(
                int(date_match.group(1)),
                int(date_match.group(2)),
                int(date_match.group(3)),
            )

            return selected_date, selected_date
        except ValueError:
            pass

    # 7월 20일 또는 2026년 7월 20일
    korean_date_match = re.search(
        r"(?:(20\d{2})년\s*)?"
        r"(\d{1,2})월\s*(\d{1,2})일",
        message,
    )

    if korean_date_match:
        year = (
            int(korean_date_match.group(1))
            if korean_date_match.group(1)
            else today.year
        )

        try:
            selected_date = date(
                year,
                int(korean_date_match.group(2)),
                int(korean_date_match.group(3)),
            )

            return selected_date, selected_date
        except ValueError:
            pass

    return None, None


def extract_keywords(
    message: str,
    district: str | None,
) -> list[str]:
    cleaned = message

    # 유형 표현 제거
    removable_phrases = [
        *MIXED_KEYWORDS,
        *[
            keyword
            for keywords in CATEGORY_KEYWORDS.values()
            for keyword in keywords
        ],
    ]

    for phrase in sorted(
        removable_phrases,
        key=len,
        reverse=True,
    ):
        cleaned = cleaned.replace(phrase, " ")

    # 지역 표현 제거
    if district:
        cleaned = cleaned.replace(district, " ")
        cleaned = cleaned.replace(
            district.removesuffix("구"),
            " ",
        )

    # 날짜 표현 제거
    cleaned = re.sub(
        r"20\d{2}[-./]\d{1,2}[-./]\d{1,2}",
        " ",
        cleaned,
    )

    cleaned = re.sub(
        r"(?:(?:20\d{2})년\s*)?"
        r"\d{1,2}월\s*\d{1,2}일",
        " ",
        cleaned,
    )

    tokens = re.findall(
        r"[가-힣A-Za-z0-9]+",
        cleaned,
    )

    keywords: list[str] = []

    for token in tokens:
        if token in STOPWORDS:
            continue

        if len(token) < 2:
            continue

        if token not in keywords:
            keywords.append(token)

    # 검색 조건이 너무 복잡해지지 않게 최대 2개
    return keywords[:2]


def create_search_plan(message: str) -> SearchPlan:
    normalized_message = normalize_message(message)

    intent = extract_intent(normalized_message)
    district = extract_district(normalized_message)
    start_date, end_date = extract_date_range(
        normalized_message
    )
    keywords = extract_keywords(
        normalized_message,
        district,
    )

    return SearchPlan(
        intent=intent,
        district=district,
        keywords=keywords,
        start_date=start_date,
        end_date=end_date,
    )


def make_address(item) -> str | None:
    address_parts = [
        value
        for value in [
            getattr(item, "addr1", None),
            getattr(item, "addr2", None),
        ]
        if value
    ]

    return " ".join(address_parts) or None


def make_keyword_condition(
    model,
    keywords: list[str],
    include_description: bool = False,
):
    conditions = []

    for keyword in keywords:
        conditions.extend(
            [
                model.title.contains(keyword),
                model.addr1.contains(keyword),
                model.addr2.contains(keyword),
            ]
        )

        if include_description:
            conditions.append(
                model.description.contains(keyword)
            )

    if not conditions:
        return None

    return or_(*conditions)


def item_to_dict(
    item,
    category: str,
) -> dict:
    result = {
        "id": item.id,
        "category": category,
        "title": item.title,
        "address": make_address(item),
        "phone": getattr(item, "tel", None),
        "image_url": getattr(
            item,
            "firstimage",
            None,
        ),
        "mapx": getattr(item, "mapx", None),
        "mapy": getattr(item, "mapy", None),
    }

    if category == "festival":
        description = getattr(
            item,
            "description",
            None,
        )

        result.update(
            {
                "start_date": getattr(
                    item,
                    "start_date",
                    None,
                ),
                "end_date": getattr(
                    item,
                    "end_date",
                    None,
                ),
                # OpenAI 입력 토큰 절약
                "description": (
                    description[:120]
                    if description
                    else None
                ),
            }
        )

    return result


def calculate_score(
    item: dict,
    plan: SearchPlan,
) -> int:
    score = 0

    title = item.get("title") or ""
    address = item.get("address") or ""

    if plan.district and plan.district in address:
        score += 3

    for keyword in plan.keywords:
        if keyword in title:
            score += 5

        if keyword in address:
            score += 2

    # 정보가 충분한 장소를 약간 우선
    if item.get("image_url"):
        score += 1

    if item.get("address"):
        score += 1

    if item.get("phone"):
        score += 1

    if item["category"] == "festival":
        if item.get("start_date") and item.get("end_date"):
            score += 2

        if plan.start_date and plan.end_date:
            # SQL에서 기간 조건을 통과한 축제이므로 가산점
            score += 4

    return score


def search_category(
    category: Literal[
        "tourist",
        "shopping",
        "festival",
    ],
    plan: SearchPlan,
    db: Session,
    limit: int,
) -> list[dict]:
    model_map = {
        "tourist": models.TouristItem,
        "shopping": models.ShoppingItem,
        "festival": models.FestivalItem,
    }

    model = model_map[category]
    query = db.query(model)

    if plan.district:
        query = query.filter(
            model.addr1.contains(plan.district)
        )

    keyword_condition = make_keyword_condition(
        model=model,
        keywords=plan.keywords,
        include_description=category == "festival",
    )

    if keyword_condition is not None:
        query = query.filter(keyword_condition)

    # 사용자가 특정 날짜 범위를 요청한 경우에만
    # 축제 기간 조건을 적용
    if (
        category == "festival"
        and plan.start_date
        and plan.end_date
    ):
        requested_start = plan.start_date.isoformat()
        requested_end = plan.end_date.isoformat()

        query = query.filter(
            model.start_date.isnot(None),
            model.end_date.isnot(None),

            # 축제 기간과 조회 기간이 겹치는지 검사
            model.start_date <= requested_end,
            model.end_date >= requested_start,
        )

    # 점수 계산 전에 후보를 일정 수만 조회
    candidates = (
        query
        .order_by(model.title.asc())
        .limit(20)
        .all()
    )

    items = [
        item_to_dict(item, category)
        for item in candidates
    ]

    items.sort(
        key=lambda item: (
            calculate_score(item, plan),
            item.get("title") or "",
        ),
        reverse=True,
    )

    return items[:limit]


def search_mixed_items(
    plan: SearchPlan,
    db: Session,
    limit: int,
) -> list[dict]:
    # 각 유형에서 먼저 후보를 가져온다.
    buckets = {
        "tourist": search_category(
            "tourist",
            plan,
            db,
            limit=2,
        ),
        "festival": search_category(
            "festival",
            plan,
            db,
            limit=2,
        ),
        "shopping": search_category(
            "shopping",
            plan,
            db,
            limit=2,
        ),
    }

    # 한 카테고리에만 몰리지 않도록 번갈아 선택
    results: list[dict] = []

    category_order = [
        "tourist",
        "festival",
        "shopping",
    ]

    while len(results) < limit:
        added = False

        for category in category_order:
            if buckets[category]:
                results.append(
                    buckets[category].pop(0)
                )
                added = True

                if len(results) >= limit:
                    break

        if not added:
            break

    return results


def retrieve_items(
    plan: SearchPlan,
    db: Session,
    limit: int,
) -> list[dict]:
    if plan.intent == "mixed":
        return search_mixed_items(
            plan=plan,
            db=db,
            limit=limit,
        )

    return search_category(
        category=plan.intent,
        plan=plan,
        db=db,
        limit=limit,
    )


CATEGORY_LABELS = {
    "tourist": "관광지",
    "shopping": "쇼핑",
    "festival": "축제",
    "mixed": "지역 장소",
}


def create_fallback_answer(
    plan: SearchPlan,
    items: list[dict],
) -> str:
    if not items:
        conditions = []

        if plan.district:
            conditions.append(plan.district)

        if plan.keywords:
            conditions.append(
                ", ".join(plan.keywords)
            )

        condition_text = (
            " / ".join(conditions)
            if conditions
            else "입력한"
        )

        return (
            f"{condition_text} 조건에 맞는 장소를 "
            "현재 LocalHub 데이터에서 찾지 못했습니다. "
            "지역이나 장소명을 조금 넓혀 질문해 주세요."
        )

    header = (
        f"{plan.district or '서울'}에서 확인된 "
        f"{CATEGORY_LABELS[plan.intent]} 추천 후보입니다."
    )

    lines = [header]

    for index, item in enumerate(
        items,
        start=1,
    ):
        details = []

        if item.get("address"):
            details.append(item["address"])

        if item["category"] == "festival":
            start_date = item.get("start_date")
            end_date = item.get("end_date")

            if start_date or end_date:
                details.append(
                    f"{start_date or '미정'}"
                    f" ~ {end_date or '미정'}"
                )

        detail_text = (
            f" — {' / '.join(details)}"
            if details
            else ""
        )

        lines.append(
            f"{index}. {item['title']}{detail_text}"
        )

    return "\n".join(lines)


def generate_ai_answer(
    user_message: str,
    plan: SearchPlan,
    items: list[dict],
) -> str | None:
    client = get_openai_client()
    model_name = get_model_name()

    # 들여쓰기를 제거해 입력 토큰 절약
    compact_context = json.dumps(
        items,
        ensure_ascii=False,
        separators=(",", ":"),
    )

    prompt = f"""
질문: {user_message}

분석 결과:
- 유형: {plan.intent}
- 지역: {plan.district}
- 검색어: {plan.keywords}
- 시작일: {plan.start_date}
- 종료일: {plan.end_date}

DB 검색 결과:
{compact_context}

요청:
DB 검색 결과에서 최대 {len(items)}개만 간단히 추천하세요.
장소명과 주소를 포함하고, 축제는 기간을 포함하세요.
각 항목은 한 문장 이내로 작성하세요.
"""

    try:
        response = client.responses.create(
            model=model_name,

            # 단순한 DB 결과 요약이므로
            # 추론 토큰을 최소화
            reasoning={
                "effort": "minimal",
            },

            instructions=(
                "당신은 LocalHub 서울 지역 안내 챗봇입니다. "
                "제공된 DB 결과만 사용하세요. "
                "데이터에 없는 사실은 만들지 마세요. "
                "'최고', '1위', '가장 인기 있는'처럼 "
                "근거 없는 순위를 표현하지 마세요. "
                "답변은 6문장 이내로 작성하세요."
            ),
            input=prompt,
            max_output_tokens=600,
        )

        if response.status == "incomplete":
            logger.warning(
                "OpenAI 응답 미완료: %s",
                response.incomplete_details,
            )
            return None

        if response.status == "failed":
            logger.warning(
                "OpenAI 응답 실패: %s",
                response.error,
            )
            return None

        answer = response.output_text.strip()

        return answer or None

    except APIConnectionError:
        logger.exception(
            "OpenAI API 연결 오류"
        )
        return None

    except APITimeoutError:
        logger.exception(
            "OpenAI API 시간 초과"
        )
        return None

    except APIStatusError as error:
        logger.exception(
            "OpenAI API 상태 오류: %s",
            error.status_code,
        )
        return None


def process_chat(
    user_message: str,
    db: Session,
) -> dict:
    message = normalize_message(user_message)

    if not message:
        return {
            "answer": "질문을 입력해 주세요.",
            "intent": "mixed",
            "district": None,
            "items": [],
            "used_ai": False,
        }

    plan = create_search_plan(message)
    limit = get_result_limit()

    items = retrieve_items(
        plan=plan,
        db=db,
        limit=limit,
    )

    fallback_answer = create_fallback_answer(
        plan=plan,
        items=items,
    )

    # DB 결과가 없으면 AI 호출을 하지 않아 토큰을 절약
    if not items:
        return {
            "answer": fallback_answer,
            "intent": plan.intent,
            "district": plan.district,
            "items": [],
            "used_ai": False,
        }

    ai_answer = generate_ai_answer(
        user_message=message,
        plan=plan,
        items=items,
    )

    return {
        "answer": ai_answer or fallback_answer,
        "intent": plan.intent,
        "district": plan.district,
        "items": items,
        "used_ai": ai_answer is not None,
    }
