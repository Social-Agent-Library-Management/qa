# Library Management System UI Kit

Interactive hi-fi prototype for the **도서 관리 시스템** admin interface.

## Screens

| Screen ID       | Korean Label     | Description                                      |
|-----------------|------------------|--------------------------------------------------|
| login           | 로그인           | Login form with ID/PW inputs                     |
| dashboard       | 대시보드         | 4 stat cards + loan table + overdue panel        |
| book-register   | 도서 등록        | Form + book list table                           |
| copy-register   | 소장본 등록      | 관리번호 form + inventory table + 분실/폐기 상태 변경 |
| loan-register   | 대출 등록        | Form + active loans table                        |
| return          | 반납 처리        | Search + return-action table with live updates   |
| loan-history    | 대출 내역 조회   | Multi-condition filtered history table           |
| overdue         | 연체 목록        | Derived overdue list, 경과일 내림차순 정렬        |

## Usage

Open `index.html` directly. Login with any credentials (prototype accepts all input). The current screen is persisted in `localStorage` so refreshing keeps your place.

## Dependencies

Loads from the design system bundle at `../../_ds_bundle.js`:
- `Button`, `Badge`, `Input`, `Card` (core)
- `StatCard`, `DdayCard` (display)
- `DataTable` (data)
- `Sidebar` (navigation)

## Notes

- All data is mock/sample — no backend connection
- Form submissions show a success toast; no actual data mutation
- Return processing screen has live state (click "반납 처리" to mark items returned)
- Loan history screen has functional search + status filter
- Notification settings screen has functional toggles and threshold selector
