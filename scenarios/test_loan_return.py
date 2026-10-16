"""대출·반납 핵심 흐름.

시드: 문학-0001(데미안, 대출 가능) · 문학-0002(어린 왕자, 대출 중) · IT-0001(클린 코드, 20일 전 대출 → 연체)
"""

from datetime import date

from playwright.sync_api import Page, expect


def _fill_loan_form(page: Page, management_number: str) -> None:
    page.get_by_label("관리번호").fill(management_number)
    page.get_by_label("대출자 이름").fill("홍길동")
    page.get_by_label("부서명").fill("교육지원팀")
    page.get_by_label("대여일").fill(date.today().isoformat())
    page.get_by_role("button", name="대출 등록").click()


def test_search_shows_copy_status(page: Page):
    """도서 검색: 도서명을 검색하면 첫 결과가 자동 선택되고 소장본과 대출 상태가 보인다."""
    page.goto("/books/search")
    page.get_by_label("도서명, 저자 검색").fill("데미안")

    copies = page.get_by_role("table", name="데미안 소장본 목록")
    expect(copies.get_by_role("row").filter(has_text="문학-0001")).to_contain_text("대출가능")


def test_loan_then_return(page: Page):
    """대출 → 반납: 대출 등록 후 반납 처리하면 대출 내역에 반납완료로 남고 대출자 정보는 파기된다."""
    page.goto("/loans/new")
    _fill_loan_form(page, "문학-0001")
    expect(page.get_by_role("status").filter(has_text="대출이 등록되었습니다")).to_be_visible()
    current = page.get_by_role("table", name="현재 대출 중인 소장본 목록")
    expect(current.get_by_role("row").filter(has_text="문학-0001")).to_be_visible()

    page.goto("/returns")
    targets = page.get_by_role("table", name="반납 처리 대상 목록")
    targets.get_by_role("row").filter(has_text="문학-0001").get_by_role("button", name="반납 처리").click()
    expect(page.get_by_role("status").filter(has_text='"데미안" 반납 처리되었습니다.')).to_be_visible()
    expect(targets.get_by_role("row").filter(has_text="문학-0001")).to_have_count(0)

    page.goto("/admin/loans/history")
    page.get_by_role("combobox", name="상태").select_option(label="반납완료")
    history = page.get_by_role("table", name="대출 내역 목록")
    returned = history.get_by_role("row").filter(has_text="문학-0001")
    expect(returned).to_contain_text("반납완료")
    expect(returned).to_contain_text("대출자 정보 파기됨")
    expect(returned).not_to_contain_text("홍길동")


def test_duplicate_loan_rejected(page: Page):
    """중복 대출 차단: 이미 대출 중인 소장본을 대출하면 관리번호 칸에 오류가 표시되고 등록되지 않는다."""
    page.goto("/loans/new")
    _fill_loan_form(page, "문학-0002")

    expect(page.get_by_label("관리번호")).to_have_attribute("aria-invalid", "true")
    current = page.get_by_role("table", name="현재 대출 중인 소장본 목록")
    expect(current.get_by_role("row").filter(has_text="문학-0002")).to_have_count(1)


def test_overdue_filter(page: Page):
    """연체 조회: 대출 내역에서 상태를 연체로 거르면 반납 예정일이 지난 대출만 연체로 표시된다."""
    page.goto("/admin/loans/history")
    page.get_by_role("combobox", name="상태").select_option(label="연체")

    history = page.get_by_role("table", name="대출 내역 목록")
    expect(history.get_by_role("row").filter(has_text="IT-0001")).to_contain_text("연체")
    expect(history.get_by_role("row").filter(has_text="문학-0002")).to_have_count(0)
