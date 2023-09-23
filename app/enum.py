from enum import StrEnum


class ContactCategoryEnum(StrEnum):
    WORK = "직장"
    CLIENT = "거래처"
    CUSTOMER = "고객"
    ETC = "기타"


class ContactRepeatIntervalEnum(StrEnum):
    ONE = "1"
    THREE = "3"
    SIX = "6"
    TWELVE = "12"


class CalendarRecurringFrequencyEnum(StrEnum):
    DAY = "일"
    WEEK = "주"
    MONTH = "월"
    YEAR = "년"
