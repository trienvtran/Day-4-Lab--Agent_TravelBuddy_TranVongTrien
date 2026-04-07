
# TravelBuddy AI Agent - Lab 4 (LangGraph)
## 📌 Giới thiệu
Dự án xây dựng Trợ lý Du lịch Thông minh cho startup TravelBuddy. Agent có khả năng tự động lập kế hoạch chuyến đi hoàn chỉnh bằng cách kết hợp nhiều nguồn dữ liệu (Chuyến bay, Khách sạn, Ngân sách) trong một cuộc hội thoại duy nhất.

Model: gemma-4-31b-it (Google AI Studio).

Framework: LangGraph

## 🚀 Tính năng chính
Suy luận đa bước (Multi-step Reasoning): Tự động phân tích yêu cầu từ người dùng (điểm đến, ngân sách, thời gian).
- **search_flights(origin, destination)**  
  Tìm kiếm chuyến bay giữa hai thành phố, trả về hãng bay, giờ khởi hành và giá vé.  
  Tự động xử lý cả chiều đi và chiều ngược lại nếu cần.

- **search_hotels(location, max_budget_per_night)**  
  Tìm khách sạn theo thành phố và ngân sách mỗi đêm.  
  Kết quả được lọc theo giá và sắp xếp theo rating cao nhất.

- **calculate_budget(total_budget, expenses)**  
  Tính toán ngân sách còn lại dựa trên các khoản chi.  
  Trả về bảng chi tiết chi phí và cảnh báo nếu vượt ngân sách.

## 🛠 Cấu trúc thư mục
lab4_agent/

├── tools.py              # Định nghĩa các Tools (Mock DB)

├── agent.py              # Xây dựng đồ thị (Graph) và Logic Agent

├── test_result.md        # Kết quả 5 test case

├── test_api.py           # Chạy thử api

└── system prompt.txt     # System Instruction 
