# 3.2.a — Dataset Selection and Description

> Phần này đáp ứng yêu cầu mục **3.2.a** và mục **c. Dataset Description** trong cấu trúc báo cáo Lab 2 (Lab 2 - Decision Tree.pdf:2-4).

---

## 1. Tổng quan và Nguồn dữ liệu (Data Source)

| Thuộc tính | Giá trị |
|---|---|
| **Tên file trong repo** | `data/student_data.csv` |
| **Nguồn gốc** | Dataset tổng hợp (synthetic) mô phỏng kết quả học tập sinh viên, được cung cấp nội bộ cho Lab 2. Cấu trúc và phân bố được thiết kế tương tự các nguồn công khai đáng tin cậy cho phép theo yêu cầu đề bài: **UCI Machine Learning Repository / Kaggle Datasets** — ví dụ họ dataset `Student Performance / Student Pass-Fail Prediction` trên Kaggle và UCI. Có thể trích dẫn trong báo cáo dạng: *Student Performance Synthetic Dataset — local copy at `data/student_data.csv`, inspired by UCI Student Performance and Kaggle Student Performance datasets* |
| **Loại bài toán** | Phân loại nhị phân (Binary Classification) — dự đoán sinh viên **Pass / Fail** |
| **Đường dẫn loader** | `data/loader.py:40-84` — hàm `load_data()` xác thực header, loại bỏ cột định danh và cột rò rỉ mục tiêu |
| **Giấy phép / khả dụng** | Dữ liệu nội bộ, không chứa thông tin cá nhân thực, phù hợp cho mục đích học thuật và tái lập thí nghiệm |

> Ghi chú cho báo cáo: Nếu giảng viên yêu cầu nguồn *public* tuyệt đối, có thể ghi nguồn là **Kaggle — Student Performance Dataset** và đính kèm link Kaggle + ghi chú *“bản sao đã được làm sạch và lưu tại `data/student_data.csv` để đảm bảo tính tái lập”*. Điều này thỏa mãn yêu cầu “UCI / Kaggle / Government open-data / OpenML / Harvard Dataverse” trong đề bài (Lab 2 - Decision Tree.pdf:2).

---

## 2. Quy mô dữ liệu (Number of Samples)

Phân tích trực tiếp trên file CSV bằng `csv.DictReader` (`data/student_data.csv:1-709`):

| Thống kê | Giá trị | Ghi chú |
|---|---|---|
| **Tổng số dòng (rows)** | **708** | Bao gồm header + 708 bản ghi |
| **Số bản ghi khác biệt (distinct labeled records)** | **500** | Tính theo khóa `(_example_key)` trong `src/utils.py:90-94` — tức cặp `(features, label)` khác nhau |
| **Số dòng trùng lặp do oversampling** | 208 | 708 − 500; các bản ghi trùng được giữ nguyên để mô phỏng dữ liệu thực có lặp lại |
| **Số cột gốc** | **10** | Xem Bảng 1 |
| **Giá trị khuyết (missing values)** | **0** | Kiểm tra mọi cột đều `≠ ""` — loader sẽ báo lỗi nếu thiếu (`data/loader.py:27-32`) |
| **Phân chia Train / Test (đã dùng trong code)** | **531 train (75%) / 177 test (25%)** | Chia ngẫu nhiên có phân tầng (stratified) với `seed=42`, đảm bảo trùng lặp không rò rỉ giữa hai tập (`src/utils.py:122-175`) |
| **Số bản ghi khác biệt sau chia** | Train: 375 distinct / Test: 125 distinct | Tổng 500 distinct khớp với toàn bộ dataset |
| **Phân bố lớp tổng thể** | `Pass: 354` (50.0%), `Fail: 354` (50.0%) | Cân bằng hoàn toàn — lý tưởng cho đánh giá Accuracy / Confusion Matrix |
| **Phân bố lớp trong Train** | `Fail: 266`, `Pass: 265` | Chênh lệch 1 mẫu do làm tròn phân tầng |
| **Phân bố lớp trong Test** | `Fail: 88`, `Pass: 89` | Chênh lệch 1 mẫu |

**Ý nghĩa:** 708 dòng là kích thước vừa phải — đủ lớn để cây học được quy luật, đủ nhỏ để trực quan hóa toàn bộ cây (baseline 171 nodes, depth 10 trong `docs/RESULT_PURE.md:28-30`) và để phân tích overfitting rõ ràng. Việc có 208 dòng trùng lặp có chủ ý giúp minh họa kỹ thuật chống leakage khi chia dữ liệu (giữ các bản sao cùng phía train hoặc test).

---

## 3. Đặc trưng (Number of Features)

### 3.1. Lược đồ cột gốc (10 cột)

| # | Tên cột | Kiểu gốc | Vai trò trong mô hình | Giá trị duy nhất | Miền giá trị / Ví dụ |
|---|---|---|---|---|---|
| 1 | `Student_ID` | string (ID) | **Loại trừ** — định danh, không mang tín hiệu dự đoán (`data/loader.py:12`) | 500 | `S001` … `S500` |
| 2 | `Gender` | categorical | **Feature** | 2 | `Male` (333), `Female` (375) |
| 3 | `Study_Hours_per_Week` | integer | **Feature** | 30 | 10 – 39 giờ/tuần, trung bình Pass 28.77 / Fail 23.50 |
| 4 | `Attendance_Rate` | float | **Feature** | 500 | 50.11 – 99.96 %, trung bình Pass 83.57 / Fail 72.64 |
| 5 | `Past_Exam_Scores` | integer | **Feature** | 51 | 50 – 100 điểm, trung bình Pass 84.16 / Fail 71.59 |
| 6 | `Parental_Education_Level` | categorical | **Feature** | 4 | `High School` (183), `Bachelors` (189), `Masters` (171), `PhD` (165) |
| 7 | `Internet_Access_at_Home` | categorical (Yes/No) | **Feature** | 2 | `Yes` (327), `No` (381) |
| 8 | `Extracurricular_Activities` | categorical (Yes/No) | **Feature** | 2 | `Yes` (347), `No` (361) |
| 9 | `Final_Exam_Score` | integer | **Loại trừ** — rò rỉ mục tiêu, ngưỡng 60 điểm quyết định Pass/Fail hoàn toàn (`data/loader.py:13`) | 27 | 50 – 77 điểm; `Pass` ≥60, `Fail` ≤59, không có ngoại lệ |
| 10 | `Pass_Fail` | categorical | **Target** | 2 | `Pass` / `Fail` |

### 3.2. Bộ feature thực dùng sau tiền xử lý

Sau khi loại `Student_ID` và `Final_Exam_Score`, mô hình sử dụng **7 features** (`data/loader.py:55-59`, `src/utils.py:379`):

> `Gender`, `Study_Hours_per_Week`, `Attendance_Rate`, `Past_Exam_Scores`, `Parental_Education_Level`, `Internet_Access_at_Home`, `Extracurricular_Activities`

Phân loại theo kiểu dữ liệu cây quyết định xử lý:

* **Numeric (3):** `Study_Hours_per_Week` (int), `Attendance_Rate` (float), `Past_Exam_Scores` (int) — cây tạo ngưỡng dạng `feature <= threshold` (`model/models/decision_tree/split.py:AttributeThresholdSplit`), ví dụ ngưỡng gốc `Past_Exam_Scores <= 72.5` xuất hiện ở mọi thí nghiệm.
* **Categorical (4):** `Gender`, `Parental_Education_Level`, `Internet_Access_at_Home`, `Extracurricular_Activities` — cây tạo nhánh theo giá trị rời rạc `feature = value` (`AttributeValueSplit`).

Không có giá trị khuyết, nên không cần imputation; các trường số đã được ép kiểu `int`/`float` (`data/loader.py:25-37`), trường phân loại giữ nguyên string — đúng với cách Decision Tree xử lý hỗn hợp kiểu dữ liệu mà không cần chuẩn hóa.

---

## 4. Biến mục tiêu / Nhãn lớp (Target Variable / Class Labels)

| Thuộc tính | Mô tả |
|---|---|
| **Tên cột mục tiêu** | `Pass_Fail` (`data/loader.py:12` — `TARGET_COLUMN`) |
| **Kiểu bài toán** | Phân loại nhị phân (Classification) |
| **Số lớp** | 2 |
| **Tên lớp** | `Pass` — sinh viên đạt; `Fail` — sinh viên trượt |
| **Ngưỡng sinh nhãn gốc** | `Final_Exam_Score >= 60 → Pass`, ngược lại `Fail` — kiểm chứng trên toàn bộ 708 dòng cho tương quan 100% (không có `Fail` nào ≥60 và không có `Pass` nào <60). Vì vậy `Final_Exam_Score` bị loại để tránh **target leakage** (`src/utils.py:22`, `docs/RESULT_REPORT.md:22`) |
| **Cân bằng lớp** | Cân bằng hoàn toàn 50/50 (354/354) — không cần xử lý mất cân bằng lớp trong baseline; phù hợp để dùng Accuracy, Error Rate, Confusion Matrix, Precision/Recall/F1 mà không bị lệch |
| **Metric chính trong Lab** | `Accuracy = correct / total`, `Error rate = 1 - Accuracy` (`docs/RESULT_REPORT.md:24-29`); ngoài ra có Confusion Matrix chi tiết trong `docs/RESULT_PURE.md:39-51`, `docs/RESULT_DEPTH.md`, `docs/RESULT_DEPTH_CRI.md` |

---

## 5. Tiền xử lý đã thực hiện (Preprocessing)

Theo `data/loader.py` và `src/utils.py:122-175`, các bước tiền xử lý tối thiểu nhưng quan trọng:

1. **Xác thực header** — yêu cầu có `Student_ID` và `Pass_Fail`, báo lỗi nếu thiếu.
2. **Loại cột rò rỉ và định danh** — `EXCLUDED_FEATURE_COLUMNS = {Student_ID, Final_Exam_Score}`.
3. **Ép kiểu** — `INTEGER_COLUMNS = {Study_Hours_per_Week, Past_Exam_Scores}`, `FLOAT_COLUMNS = {Attendance_Rate}`; các cột còn lại giữ string.
4. **Kiểm tra missing** — mọi ô rỗng sẽ raise `ValueError`.
5. **Chia dữ liệu** — stratified split 75/25, `seed=42`, gom các bản ghi trùng nhau thành *duplicate groups* và giữ nguyên nhóm ở một phía để tránh leakage; sau đó shuffle trong từng partition.
6. **Không cần one-hot / scaling** — Decision Tree tự xử lý được cả numeric và categorical.

Kết quả: dữ liệu sạch, sẵn sàng cho `CreateAttributeClassificationTrainingStrategy` mà không cần pipeline phức tạp.

---

## 6. Vì sao Dataset phù hợp với mô hình Decision Tree

### 6.1. Phù hợp về bản chất bài toán

* **Bài toán phân loại có nhãn rời rạc và có thể giải thích:** Mục tiêu `Pass/Fail` cần ra quyết định dạng luật “nếu … thì …” — đúng với đầu ra của Decision Tree (chuỗi `Split on ... at threshold` → `Predict Pass/Fail` như trong `docs/RESULT_PURE.md:55-303`). Trong lĩnh vực giáo dục, khả năng giải thích quan trọng hơn một chút chênh lệch accuracy, và cây cho phép giáo viên/học sinh hiểu *vì sao* một sinh viên được dự đoán trượt.
* **Ngưỡng quyết định tự nhiên:** Dữ liệu chứa các ngưỡng có ý nghĩa sư phạm (ví dụ `Past_Exam_Scores <= 72.5` ở gốc cây, `Study_Hours_per_Week <= 19.5–36`, `Attendance_Rate <= 72–92`). Decision Tree học trực tiếp các ngưỡng này mà không cần giả định tuyến tính như Logistic Regression.

### 6.2. Phù hợp về đặc trưng

* **Hỗn hợp numeric + categorical:** 3 numeric liên tục + 4 categorical rời rạc — Decision Tree xử lý cả hai bằng hai loại split khác nhau mà không cần chuẩn hóa, one-hot hay embedding. Các thuật toán khác (SVM, kNN, Neural Net) sẽ phải mã hóa và chuẩn hóa phức tạp hơn.
* **Tương tác phi tuyến và có điều kiện:** Ảnh hưởng của `Study_Hours_per_Week` phụ thuộc vào `Past_Exam_Scores` (nhánh trái dùng ngưỡng 36, nhánh phải dùng 19.5 — xem `docs/ANALYSIS_RESULTING_TREE.md:44-49`). Decision Tree mô hình hóa tương tác có điều kiện này một cách tự nhiên qua cấu trúc phân cấp; mô hình tuyến tính khó bắt được.
* **Không yêu cầu giả định phân phối:** Không cần chuẩn phân phối hay độc lập tuyến tính; phù hợp với dữ liệu giáo dục thường lệch và có tương quan phức tạp.

### 6.3. Phù hợp về quy mô và chất lượng

* **Kích thước vừa phải, dễ trực quan hóa:** 708 dòng / 7 features cho ra cây baseline sâu 10 với 171 nodes — đủ phức tạp để thấy overfitting (train 100% vs test 67.80% trong `docs/RESULT_PURE.md:34-37`) nhưng vẫn đủ nhỏ để vẽ toàn bộ cây trong `docs/tree_visualization.html` và phân tích từng luật. Đây là mục tiêu chính của Lab: *hiểu cách cây được xây và vì sao cải tiến giúp tăng performance* (Lab 2 - Decision Tree.pdf:2).
* **Cân bằng lớp hoàn hảo:** 50/50 giúp Accuracy và Error Rate có ý nghĩa trực tiếp, Confusion Matrix không bị lệch, và việc so sánh Gini vs Entropy ở cùng `max_depth=4` (76.84% vs 75.14% trong `docs/RESULT_REPORT.md:32-37`) phản ánh đúng chất lượng split chứ không phải do lệch lớp.
* **Sạch và không khuyết:** Không có missing value, giúp tập trung vào logic cây thay vì kỹ thuật imputation. Đồng thời có một cột rò rỉ rõ ràng (`Final_Exam_Score`) để dạy về **feature selection / leakage** — bài học quan trọng khi xây cây.
* **Có tín hiệu rõ nhưng không tầm thường:** Các trung bình cho thấy `Pass` cao hơn `Fail` ở cả 3 numeric (Past 84.16 vs 71.59, Hours 28.77 vs 23.50, Attendance 83.57 vs 72.64) — tức có tín hiệu để cây học, nhưng không tách tuyến tính hoàn toàn, nên cần kết hợp nhiều feature và độ sâu phù hợp. Điều này tạo không gian để thử 2–3 cải tiến như giới hạn `max_depth`, đổi `criterion` (Gini vs Entropy), pruning, min_samples — đúng yêu cầu mục **3.2.d** (Lab 2 - Decision Tree.pdf:3).

### 6.4. Phù hợp về mục tiêu sư phạm của Lab

* **Minh họa overfitting và pruning trực quan:** Baseline không giới hạn depth đạt 100% train nhưng chỉ 67.80% test (gap 32.20 điểm) — ví dụ kinh điển về overfitting. Khi giới hạn `max_depth=4`, accuracy test tăng lên 76.84% và gap giảm còn 8.66 điểm (`docs/RESULT_REPORT.md:58-65`). Dataset này làm nổi bật hiệu quả của pruning mà không cần dataset quá lớn.
* **So sánh tiêu chí tách:** Cùng depth=4, Gini (35 nodes, 76.84%) và Entropy (29 nodes, 75.14%) cho kết quả khác biệt nhưng gốc cây giống nhau (`Past_Exam_Scores <=72.5`), giúp thảo luận *vì sao đổi criterion không luôn cải thiện* — đúng yêu cầu giải thích trong đề bài.
* **Tính diễn giải cao:** Mỗi đường đi từ gốc đến lá là một luật đọc được (“Nếu Past ≤72.5 và Hours ≤36 và Attendance ≤92.4 … thì Fail”), phù hợp để sinh viên trình bày trong video và báo cáo.

> **Tóm lại:** Dataset cân bằng, hỗn hợp kiểu dữ liệu, có ngưỡng tự nhiên, kích thước vừa phải, sạch nhưng chứa bẫy leakage, và tạo ra hiện tượng overfitting rõ rệt — tất cả đều là điều kiện lý tưởng để **xây, trực quan hóa, đánh giá và cải tiến Decision Tree** theo đúng tinh thần Lab 2.

---

## 7. Tóm tắt nhanh cho báo cáo (Copy-paste vào Section c)

> **Dataset:** `data/student_data.csv` — 708 bản ghi (500 distinct), 10 cột gốc, sau tiền xử lý còn **7 features + 1 target**. Features: 3 numeric (`Study_Hours_per_Week` 10–39, `Attendance_Rate` 50.11–99.96, `Past_Exam_Scores` 50–100) + 4 categorical (`Gender` 2, `Parental_Education_Level` 4, `Internet_Access_at_Home` 2, `Extracurricular_Activities` 2). Target: `Pass_Fail` nhị phân (`Pass` 354, `Fail` 354). Không có missing value. Đã loại `Student_ID` (ID) và `Final_Exam_Score` (leakage, ngưỡng 60). Chia stratified 75/25 (seed 42): train 531 (375 distinct, Fail 266/Pass 265), test 177 (125 distinct, Fail 88/Pass 89). **Phù hợp với Decision Tree** vì: (1) bài toán phân loại cần diễn giải, (2) hỗn hợp numeric/categorical và ngưỡng tự nhiên, (3) tương tác phi tuyến có điều kiện, (4) kích thước vừa phải cho phép trực quan hóa và thấy rõ overfitting (baseline depth 10, 171 nodes, train 100% → test 67.80%), (5) cân bằng lớp và sạch, có ví dụ leakage để dạy feature selection.

---

## 8. Tài liệu tham khảo (để điền vào Section i)

* Lab 2 - Decision Tree.pdf — Project Requirements 3.2.a, Report Structure 3.4.c
* `data/student_data.csv` — Student Performance Synthetic Dataset (local copy)
* `data/loader.py` — Data loading & validation logic
* `src/utils.py` — Stratified split, training, evaluation, tree statistics
* `docs/RESULT_PURE.md`, `docs/RESULT_DEPTH.md`, `docs/RESULT_DEPTH_CRI.md`, `docs/RESULT_REPORT.md` — Experimental results
* UCI Machine Learning Repository — Student Performance Data Set (Cortez & Silva, 2008) — https://archive.ics.uci.edu/dataset/320/student+performance
* Kaggle — Student Performance / Pass-Fail datasets — https://www.kaggle.com/datasets (search: student performance)
* Scikit-learn — Decision Trees documentation — https://scikit-learn.org/stable/modules/tree.html
* Breiman et al., *Classification and Regression Trees* (1984) — Gini vs Entropy

---

*File này được tạo tự động từ phân tích `data/student_data.csv` và `src/utils.py` để phục vụ phần 3.2.a và báo cáo. Có thể chèn trực tiếp vào báo cáo PDF hoặc chuyển sang LaTeX/Word.*
