# LINE Bot 與 Google Maps API 整合專案

## 專案簡介

這是一個基於 Python 的專案，旨在整合 LINE Bot 與 Google Maps API，透過 LINE 的 rich menu 和 flex message 功能，為用戶提供互動式的地圖服務。此專案適用於希望利用 LINE 平台與地圖服務來增強用戶互動體驗的開發者。

## 功能特色

- **LINE Flex Message 格式化**：支援生成多樣化的 Flex Message 來展示不同的資訊格式。
- **Google Maps API 整合**：提供與 Google Maps API 互動的功能，包括地理編碼、地點搜尋、路線規劃等。
- **LINE Bot 互動處理**：能夠處理用戶回傳訊息，以及處理使用者點擊 rich menu 與 flex message 事件。

## 檔案結構

- `flex_message_formmat.py`：此檔案包含用於生成 LINE Flex Message 的格式化函數。
- `googlemap_funhtion.py`：此檔案實現了與 Google Maps API 的互動功能。
- `line_flex.py`：此檔案主要處理與 LINE Flex Message 相關的功能。

## 使用方式

1. **安裝依賴套件**：首先，請確保已安裝所有必要的 Python 套件，可以使用以下指令進行安裝：

    
    pip install -r requirements.txt
    

2. **設置環境變數**：在專案的根目錄中，創建一個 `.env` 檔案，並設置以下變數：

    ```env
    LINE_CHANNEL_ACCESS_TOKEN=你的LINE_CHANNEL_ACCESS_TOKEN
    LINE_CHANNEL_SECRET=你的LINE_CHANNEL_SECRET
    GOOGLE_MAPS_API_KEY=你的GOOGLE_MAPS_API_KEY
    ```

3. **啟動專案**：在設定完成後，可以運行以下指令來啟動專案：

    使用ngrok作為伺服器端
    運行googlemap_funhtion.py
    

## 未來規劃

- 增強 Google Maps API 功能，支援更多的地圖操作。
- 增加更多的 Flex Message 模板，以滿足不同的應用場景。
- 優化使用者互動流程，使其更直觀。
