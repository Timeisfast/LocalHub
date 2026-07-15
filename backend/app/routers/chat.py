import logging
from typing import Literal

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from ..database import get_db
from ..services.chat_service import (
    ChatConfigurationError,
    ChatExternalAPIError,
    process_chat,
)


logger = logging.getLogger(__name__)


router = APIRouter(
    prefix="/api",
    tags=["chat"],
)


class ChatRequest(BaseModel):
    """챗봇 요청 데이터."""

    message: str = Field(
        min_length=1,
        max_length=500,
        description="사용자의 서울 지역 정보 질문",
        examples=[
            "강남구 관광지 추천해줘",
            "종로구 쇼핑 장소 알려줘",
            "이번 주말 서울 축제 알려줘",
        ],
    )


class ChatItem(BaseModel):
    """챗봇이 추천하는 장소 또는 축제 정보."""

    id: int

    category: Literal[
        "tourist",
        "shopping",
        "festival",
    ]

    title: str

    address: str | None = None
    phone: str | None = None
    image_url: str | None = None

    mapx: float | None = None
    mapy: float | None = None

    # 축제 데이터에서만 사용
    start_date: str | None = None
    end_date: str | None = None
    description: str | None = None


class ChatResponse(BaseModel):
    """챗봇 최종 응답 데이터."""

    answer: str

    # tourist, shopping, festival, mixed
    intent: str

    district: str | None = None

    items: list[ChatItem] = Field(
        default_factory=list
    )

    # OpenAI 답변이 사용됐는지 여부
    used_ai: bool


@router.post(
    "/chat",
    response_model=ChatResponse,
    summary="LocalHub 장소 추천 챗봇",
    description=(
        "관광지, 쇼핑 장소, 축제 데이터를 기반으로 "
        "서울 지역 정보를 추천합니다."
    ),
)
def chat_endpoint(
    request: ChatRequest,
    db: Session = Depends(get_db),
):
    try:
        # process_chat()이 ChatResponse와 동일한 구조의
        # dict를 반환하므로 그대로 반환한다.
        return process_chat(
            user_message=request.message,
            db=db,
        )

    except ChatConfigurationError as error:
        # API 키 누락, 허용되지 않은 모델 등 설정 문제
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(error),
        ) from error

    except ChatExternalAPIError as error:
        # OpenAI 연결 실패, 시간 초과 등 외부 API 문제
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=str(error),
        ) from error

    except Exception as error:
        # 예상하지 못한 오류는 서버 터미널에 상세 기록
        logger.exception(
            "챗봇 처리 중 예상하지 못한 오류가 발생했습니다."
        )

        # 클라이언트에는 내부 코드나 DB 정보 노출 금지
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="챗봇 처리 중 서버 오류가 발생했습니다.",
        ) from error