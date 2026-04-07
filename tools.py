from langchain_core.tools import tool
#
# MOCK DATA - Dữ liệu giả lập hệ thống du lịch
#
#
#Lưu ý: Giá cả có logic (VD: cuối tuần đắt hơn, hạng cao hơn đắt hơn)
#Sinh viên cần đọc hiểu data để debug test cases.
#
FLIGHTS_DB = {
    ("Hà Nội", "Đà Nẵng"): [
        {"airline": "Vietnam Airlines", "departure": "06:00", "arrival": "07:20", "price": 1_450_000, "class": "economy"},
        {"airline": "Vietnam Airlines", "departure": "14:00", "arrival": "15:20", "price": 2_800_000, "class": "business"},
        {"airline": "VietJet Air", "departure": "08:30", "arrival": "09:50", "price": 890_000, "class": "economy"},
        {"airline": "Bamboo Airways", "departure": "11:00", "arrival": "12:20", "price": 1_200_000, "class": "economy"},
    ],
    ("Hà Nội", "Phú Quốc"): [
        {"airline": "Vietnam Airlines", "departure": "07:00", "arrival": "09:15", "price": 2_100_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "10:00", "arrival": "12:15", "price": 1_350_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "16:00", "arrival": "18:15", "price": 1_100_000, "class": "economy"},
    ],
    ("Hà Nội", "Hồ Chí Minh"): [
        {"airline": "Vietnam Airlines", "departure": "06:00", "arrival": "08:10", "price": 1_600_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "07:30", "arrival": "09:40", "price": 950_000, "class": "economy"},
        {"airline": "Bamboo Airways", "departure": "12:00", "arrival": "14:10", "price": 1_300_000, "class": "economy"},
        {"airline": "Vietnam Airlines", "departure": "18:00", "arrival": "20:10", "price": 3_200_000, "class": "business"},
    ],
    ("Hồ Chí Minh", "Đà Nẵng"): [
        {"airline": "Vietnam Airlines", "departure": "09:00", "arrival": "10:20", "price": 1_300_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "13:00", "arrival": "14:20", "price": 780_000, "class": "economy"},
    ],
    ("Hồ Chí Minh", "Phú Quốc"): [
        {"airline": "Vietnam Airlines", "departure": "08:00", "arrival": "09:00", "price": 1_100_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "15:00", "arrival": "16:00", "price": 650_000, "class": "economy"},
    ],
}

HOTELS_DB = {
    "Đà Nẵng": [
        {"name": "Mường Thanh Luxury", "stars": 5, "price_per_night": 1_800_000, "area": "Mỹ Khê", "rating": 4.5},
        {"name": "Sala Danang Beach", "stars": 4, "price_per_night": 1_200_000, "area": "Mỹ Khê", "rating": 4.3},
        {"name": "Fivitel Danang", "stars": 3, "price_per_night": 650_000, "area": "Sơn Trà", "rating": 4.1},
        {"name": "Memory Hostel", "stars": 2, "price_per_night": 250_000, "area": "Hải Châu", "rating": 4.6},
        {"name": "Christina's Homestay", "stars": 2, "price_per_night": 350_000, "area": "An Thượng", "rating": 4.7},
    ],
    "Phú Quốc": [
        {"name": "Vinpearl Resort", "stars": 5, "price_per_night": 3_500_000, "area": "Bãi Dài", "rating": 4.4},
        {"name": "Sol by Meliá", "stars": 4, "price_per_night": 1_500_000, "area": "Bãi Trường", "rating": 4.2},
        {"name": "Lahana Resort", "stars": 3, "price_per_night": 800_000, "area": "Dương Đông", "rating": 4.0},
        {"name": "9Station Hostel", "stars": 2, "price_per_night": 200_000, "area": "Dương Đông", "rating": 4.5},
    ],
    "Hồ Chí Minh": [
        {"name": "Rex Hotel", "stars": 5, "price_per_night": 2_800_000, "area": "Quận 1", "rating": 4.3},
        {"name": "Liberty Central", "stars": 4, "price_per_night": 1_400_000, "area": "Quận 1", "rating": 4.1},
        {"name": "Cochin Zen Hotel", "stars": 3, "price_per_night": 550_000, "area": "Quận 3", "rating": 4.4},
        {"name": "The Common Room", "stars": 2, "price_per_night": 180_000, "area": "Quận 1", "rating": 4.6},
    ],
}

@tool
def search_flights(origin: str, destination: str) -> str:
    """
    Tìm kiếm các chuyến bay giữa hai thành phố.
    Tham số:
    - origin: thành phố khởi hành (VD: 'Hà Nội', 'Hồ Chí Minh')
    - destination: thành phố đến (VD: 'Đà Nẵng', 'Phú Quốc')
    Trả về danh sách chuyến bay với hãng, giờ bay, giá vé.
    Nếu không tìm thấy tuyến bay, trả về thông báo không có chuyến.
    """
    
    # 1. Chuẩn hóa đầu vào (xóa khoảng trắng thừa)
    ori = origin.strip()
    dest = destination.strip()
    
    # 2. Tra cứu xuôi: (origin, destination)
    flights = FLIGHTS_DB.get((ori, dest))
    
    # 3. Nếu không thấy, thử tra ngược: (destination, origin)
    if not flights:
        flights = FLIGHTS_DB.get((dest, ori))
        # Nếu tra ngược thấy, cập nhật lại thông tin hiển thị để user không nhầm lẫn
        if flights:
            current_route = f"{dest} -> {ori}"
        else:
            return f"Xin lỗi, hiện tại không tìm thấy chuyến bay nào giữa {ori} và {dest}."
    else:
        current_route = f"{ori} -> {dest}"

    # 4. Định dạng danh sách chuyến bay thành chuỗi dễ đọc
    response = f"Danh sách chuyến bay chặng {current_route}:\n"
    for f in flights:
        # Định dạng giá tiền có dấu chấm phân cách (VD: 1.450.000)
        formatted_price = "{:,}".format(f['price']).replace(',', '.')
        
        response += (
            f"- {f['airline']} | Khởi hành: {f['departure']} | "
            f"Hạng: {f['class'].capitalize()} | Giá: {formatted_price} VNĐ\n"
        )
    
    return response

@tool
def search_hotels(location: str, max_budget_per_night: int = 99999999) -> str:
    """
    Tìm kiếm khách sạn tại một thành phố, có thể lọc theo giá tối đa mỗi đêm
    Tham số:
    city: tên thành phố (VD: 'Đà Nẵng', 'Phú Quốc', 'Hồ Chí Minh')
    - max_price per_night: giá tối đa mỗi đêm (VNĐ), mặc định không giới
    Trả về danh sách khách sạn phù hợp với tên, số sao, giá, khu vực,
    rating.
    """
    loc = location.strip()
    hotels = HOTELS_DB.get(loc)
    
    if not hotels:
        return f"Không tìm thấy khách sạn tại {loc}."

    # 1. Lọc theo ngân sách tối đa mỗi đêm
    filtered = [h for h in hotels if h['price_per_night'] <= max_budget_per_night]
    
    if not filtered:
        return f"Không có khách sạn nào tại {loc} dưới {max_budget_per_night:,}₫/đêm."

    # 2. Sắp xếp theo Rating (ưu tiên chất lượng)
    sorted_hotels = sorted(filtered, key=lambda x: x['rating'], reverse=True)

    # 3. Định dạng kết quả
    res = [f"Khách sạn tốt nhất tại {loc} (phù hợp ngân sách):"]
    for h in sorted_hotels:
        p_fmt = "{:,}₫".format(h['price_per_night']).replace(",", ".")
        res.append(f"- {h['name']} ({h['stars']}⭐) - Giá: {p_fmt} | Khu vực: {h['area']} | Rating: {h['rating']}")
    
    return "\n".join(res)

@tool
def calculate_budget(total_budget: int, expenses: str) -> str:
    """
    Tính toán ngân sách còn lại sau khi trừ các khoản chi phí.
    Tham số:
    - total_budget: tổng ngân sách ban đầu (VNĐ)
    - expenses: chuỗi mô tả các khoản chi, định dạng 'tên_khoản:số_tiền', cách nhau bởi dấu phẩy.
    """
    try:
        # 1. Parse chuỗi expenses thành list các tuple (tên, số tiền)
        # Sử dụng list để giữ thứ tự nhập vào thay vì dict
        expense_items = []
        parts = [p.strip() for p in expenses.split(",")]
        
        for part in parts:
            if ":" not in part:
                return f"Lỗi định dạng: '{part}' thiếu dấu hai chấm (:). Định dạng đúng là 'tên:số_tiền'."
            
            name, amount_str = part.split(":", 1)
            try:
                amount = int(amount_str.strip())
                expense_items.append((name.strip().capitalize(), amount))
            except ValueError:
                return f"Lỗi: Số tiền cho '{name}' không hợp lệ (phải là số nguyên)."

        # 2. Tính tổng chi phí
        total_spent = sum(item[1] for item in expense_items)
        remaining = total_budget - total_spent

        # Hàm bổ trợ định dạng tiền tệ Việt Nam
        def fmt(n):
            return "{:,}₫".format(n).replace(",", ".")

        # 3. Format bảng chi tiết
        lines = ["**Bảng chi phí chi tiết:**"]
        for name, amount in expense_items:
            lines.append(f"- {name}: {fmt(amount)}")
        
        lines.append("") # Dòng trống phân cách
        lines.append(f"**Tổng chi:** {fmt(total_spent)}")
        lines.append(f"**Ngân sách:** {fmt(total_budget)}")
        
        # 4. Kiểm tra ngân sách và đưa ra kết luận
        if remaining >= 0:
            lines.append(f"**Còn lại:** {fmt(remaining)}")
            lines.append(" Kế hoạch này nằm trong ngân sách cho phép.")
        else:
            deficit = abs(remaining)
            lines.append(f" **Vượt ngân sách:** {fmt(deficit)}")
            lines.append(f" Cảnh báo: Bạn đang thiếu {fmt(deficit)}. Cần điều chỉnh lại lựa chọn!")

        return "\n".join(lines)

    except Exception as e:
        return f"Đã xảy ra lỗi không xác định khi tính toán ngân sách: {str(e)}"
