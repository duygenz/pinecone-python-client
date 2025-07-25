import os
import random
from pinecone import Pinecone

# --- BƯỚC 1: KẾT NỐI TỚI PINECONE ---
# Lấy API key và Host từ biến môi trường của Render.
# Để chạy thử trên máy, bạn có thể thay thế giá trị mặc định.
api_key = os.environ.get('PINECONE_API_KEY', 'pcsk_2G3La4_CUZkWDHF5y9wCYpWMJXkThvZcAnQQkHou6gMBpC2YwYu5Ab5JuXcVSHpMKMhAsn')
host = os.environ.get('PINECONE_HOST', 'https://duygenz1-jxzv2b2.svc.aped-4627-b74a.pinecone.io')

# Khởi tạo Pinecone client
pc = Pinecone(api_key=api_key)

# [span_0](start_span)Kết nối trực tiếp đến index của bạn bằng host[span_0](end_span)
idx = pc.Index(host=host)

print("--- Kết nối thành công đến Index ---")
print(idx.describe_index_stats())


# --- BƯỚC 2: THÊM DỮ LIỆU (UPSERT) ---
# Dữ liệu mẫu với vector 768 chiều.
# BẠN PHẢI THAY THẾ CÁC VECTOR NÀY BẰNG DỮ LIỆU CỦA BẠN.
print("\n--- Đang thêm hoặc cập nhật dữ liệu (Upsert) ---")
idx.upsert(
    vectors=[
        {"id": "vec1", "values": [0.1] * 768, "metadata": {"genre": "history"}},
        {"id": "vec2", "values": [0.2] * 768, "metadata": {"genre": "fiction"}},
        {"id": "vec3", "values": [0.3] * 768, "metadata": {"genre": "history"}},
        {"id": "vec4", "values": [0.4] * 768, "metadata": {"genre": "biography"}},
    ],
    namespace="example-namespace"
[span_1](start_span)) #[span_1](end_span)
print("Upsert hoàn tất!")
print(idx.describe_index_stats())


# --- BƯỚC 3: TRUY VẤN (QUERY) ---
# Tạo một vector truy vấn mẫu 768 chiều.
# BẠN PHẢI THAY THẾ VECTOR NÀY BẰNG VECTOR TRUY VẤN THỰC TẾ.
query_vector = [0.15] * 768

print("\n--- Đang truy vấn dữ liệu ---")
results = idx.query(
    namespace="example-namespace",
    vector=query_vector,
    top_k=3, # Lấy 3 kết quả gần nhất
    include_metadata=True
[span_2](start_span)) #[span_2](end_span)

print("\n--- Kết quả truy vấn ---")
for match in results['matches']:
    print(f"ID: {match['id']}, Score: {match['score']:.4f}, Metadata: {match['metadata']}")

# Ví dụ truy vấn với bộ lọc (filter)
print("\n--- Đang truy vấn với bộ lọc (genre: 'history') ---")
filter_results = idx.query(
    namespace="example-namespace",
    vector=query_vector,
    top_k=3,
    include_metadata=True,
    filter={"genre": {"$eq": "history"}}
[span_3](start_span)) #[span_3](end_span)

print("\n--- Kết quả truy vấn với bộ lọc ---")
for match in filter_results['matches']:
    print(f"ID: {match['id']}, Score: {match['score']:.4f}, Metadata: {match['metadata']}")

