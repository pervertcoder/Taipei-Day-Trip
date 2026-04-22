# 台北一日遊 - 旅遊電商網站

- Webdite: [https://practice.nodynote.com/](https://practice.nodynote.com/)

- API Docs: [https://practice.nodynote.com/docs](https://practice.nodynote.com/docs)

本專案為一個旅遊電商網站，提供景點查詢、行程規劃與線上預訂功能，並整合第三方金流 API，實作完整的訂單與付款流程。

## 使用DEMO

測試帳號1

帳號：test1@test.com

密碼：123

測試帳號2

帳號：test2@test.com

密碼：456

信用卡測試卡號：4242 4242 4242 4242

日期：任意未來的日期

驗證碼：123

![homepage demo](Taipei_Day_Trip_DEMO_images/homepage_desktop.png)

![homepage demo mobile](Taipei_Day_Trip_DEMO_images/homepage_mobile.png)

![attractions demo](Taipei_Day_Trip_DEMO_images/attraction_info_desktop.png)

![attractions demo mobile](Taipei_Day_Trip_DEMO_images/attraction_info_mobile.png)

![booking demo](Taipei_Day_Trip_DEMO_images/booking_one_desktop.png)

![booking demo mobile](Taipei_Day_Trip_DEMO_images/booking_two_mobile.png)

![payment demo](Taipei_Day_Trip_DEMO_images/payment_complete.png)

![payment demo mobile](Taipei_Day_Trip_DEMO_images/payment_complete_mobile.png)

## 專案說明

### 此專案為一個旅遊電商網站，提供：

- 使用者註冊 / 登入（JWT 驗證）
- 景點查詢與瀏覽
- 行程規劃功能
- 建立訂單流程
- 串接第三方金流 API 進行付款
- 訂單狀態管理（建立 / 付款 / 更新）

### 後端設計重點

- 設計完整訂單流程（建立訂單 → 發起付款 → 更新訂單狀態），確保流程清晰且可追蹤

- 串接第三方金流 API，處理付款結果回傳並同步更新訂單狀態

- 系統採簡化交易模型，單筆訂單完成付款後即清除資料，以確保流程驗證與穩定性

## 後端設計核心

- 以簡化訂單流程為設計出發點，初期採用單一訂單模型，專注於完成從建立到付款的核心流程

- 在訂單完成付款後清除資料，確保流程單一且易於驗證金流整合邏輯

- 系統設計以流程正確性為優先，後續可擴展為多訂單與歷史紀錄管理機制

## 技術使用

- 使用 FastAPI 建立 RESTful API，處理使用者、景點與訂單相關請求，實現前後端分離架構

- 使用 MySQL 設計資料庫結構，儲存使用者、行程與訂單資料，並支援基本查詢與關聯資料處理

- 使用 JWT 實作使用者身份驗證機制，確保 API 存取安全性

- 串接第三方金流 API（TayPay），處理付款流程並接收付款結果回傳

- 部署至 AWS，提供線上服務環境

## 系統功能

### 使用者系統

- 使用者註冊與登入（JWT 身分驗證）
- 會員狀態驗證與權限控管

### 景點瀏覽

- 查詢景點資料並顯示詳細資訊
- 支援景點卡片瀏覽

### 行程與訂單

- 建立行程與預訂資料
- 建立訂單並進行付款流程
- 訂單狀態管理（建立 / 付款 / 更新）

### 金流整合

- 串接第三方金流 API 完成付款
- 接收付款結果並更新訂單狀態

## API 設計（部分）

### 使用者

- POST /api/user → 註冊
- PUT /api/user/auth → 登入

### 景點

- GET /api/attractions → 景點列表

### 訂單

- POST /api/booking → 建立預訂
- POST /api/orders → 建立付款
- GET /api/orders → 查詢訂單

---

## 專案亮點

- 設計完整電商流程（瀏覽 → 下單 → 付款），涵蓋核心交易邏輯
- 串接第三方金流 API，處理付款流程與訂單狀態同步
- 建立模組化 RESTful API 架構，提升系統可維護性
