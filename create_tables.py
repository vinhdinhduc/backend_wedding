#!/usr/bin/env python3
import pymysql

conn = pymysql.connect(host='localhost', user='root', database='tienmung_db')
cursor = conn.cursor()

# Drop existing tables if any
tables = ['lich_su_chinh_sua', 'lan_di_mung', 'trang_thai_mung_lai', 'lan_mung', 'su_kien', 'nguoi', 'loai_su_kien', 'ho_gia_dinh']
for table in tables:
    cursor.execute(f'DROP TABLE IF EXISTS {table}')

# Create tables
cursor.execute('''
CREATE TABLE ho_gia_dinh (
    id VARCHAR(36) PRIMARY KEY,
    email VARCHAR(200) UNIQUE NOT NULL,
    mat_khau_hash VARCHAR(255) NOT NULL,
    ngay_tao DATETIME DEFAULT CURRENT_TIMESTAMP,
    ngay_cap_nhat DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
''')

cursor.execute('''
CREATE TABLE loai_su_kien (
    id VARCHAR(36) PRIMARY KEY,
    ma VARCHAR(50) UNIQUE NOT NULL,
    ten_hien_thi VARCHAR(200) NOT NULL,
    thu_tu SMALLINT NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
''')

cursor.execute('''
CREATE TABLE nguoi (
    id VARCHAR(36) PRIMARY KEY,
    ho_gia_dinh_id VARCHAR(36) NOT NULL,
    ten_hien_thi VARCHAR(200) NOT NULL,
    ten_khong_dau VARCHAR(200) NOT NULL,
    ten_bi_danh VARCHAR(200),
    ghi_chu TEXT,
    ngay_tao DATETIME DEFAULT CURRENT_TIMESTAMP,
    ngay_cap_nhat DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (ho_gia_dinh_id) REFERENCES ho_gia_dinh(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
''')

cursor.execute('''
CREATE TABLE su_kien (
    id VARCHAR(36) PRIMARY KEY,
    ho_gia_dinh_id VARCHAR(36) NOT NULL,
    nguoi_id VARCHAR(36) NOT NULL,
    loai_su_kien_id VARCHAR(36) NOT NULL,
    ten_con_chau VARCHAR(200),
    ngay DATE,
    chi_co_nam BOOLEAN DEFAULT FALSE,
    nam SMALLINT,
    ghi_chu TEXT,
    ngay_tao DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (ho_gia_dinh_id) REFERENCES ho_gia_dinh(id),
    FOREIGN KEY (nguoi_id) REFERENCES nguoi(id),
    FOREIGN KEY (loai_su_kien_id) REFERENCES loai_su_kien(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
''')

cursor.execute('''
CREATE TABLE lan_mung (
    id VARCHAR(36) PRIMARY KEY,
    su_kien_id VARCHAR(36) NOT NULL,
    ho_gia_dinh_id VARCHAR(36) NOT NULL,
    nguoi_mung_id VARCHAR(36) NOT NULL,
    so_tien BIGINT,
    so_vang_chi DECIMAL(10, 2),
    so_bac_chi DECIMAL(10, 2),
    ghi_chu TEXT,
    ngay_tao DATETIME DEFAULT CURRENT_TIMESTAMP,
    ngay_cap_nhat DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (su_kien_id) REFERENCES su_kien(id),
    FOREIGN KEY (ho_gia_dinh_id) REFERENCES ho_gia_dinh(id),
    FOREIGN KEY (nguoi_mung_id) REFERENCES nguoi(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
''')

cursor.execute('''
CREATE TABLE trang_thai_mung_lai (
    id VARCHAR(36) PRIMARY KEY,
    lan_mung_id VARCHAR(36) UNIQUE NOT NULL,
    trang_thai VARCHAR(50) NOT NULL,
    ngay_mung_lai DATE,
    ghi_chu TEXT,
    ngay_cap_nhat DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (lan_mung_id) REFERENCES lan_mung(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
''')

cursor.execute('''
CREATE TABLE lan_di_mung (
    id VARCHAR(36) PRIMARY KEY,
    ho_gia_dinh_id VARCHAR(36) NOT NULL,
    nguoi_id VARCHAR(36) NOT NULL,
    loai_su_kien_id VARCHAR(36) NOT NULL,
    ten_con_chau VARCHAR(200),
    so_tien BIGINT,
    so_vang_chi DECIMAL(10, 2),
    so_bac_chi DECIMAL(10, 2),
    ngay_di DATE,
    chi_co_nam BOOLEAN DEFAULT FALSE,
    nam SMALLINT,
    trang_thai VARCHAR(50) DEFAULT 'CHUA_TRA',
    lan_mung_doi_chieu_id VARCHAR(36),
    chenh_lech_tien BIGINT,
    chenh_lech_vang DECIMAL(10, 2),
    chenh_lech_bac DECIMAL(10, 2),
    ngay_doi_chieu DATE,
    ghi_chu TEXT,
    ngay_tao DATETIME DEFAULT CURRENT_TIMESTAMP,
    ngay_cap_nhat DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (ho_gia_dinh_id) REFERENCES ho_gia_dinh(id),
    FOREIGN KEY (nguoi_id) REFERENCES nguoi(id),
    FOREIGN KEY (loai_su_kien_id) REFERENCES loai_su_kien(id),
    FOREIGN KEY (lan_mung_doi_chieu_id) REFERENCES lan_mung(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
''')

cursor.execute('''
CREATE TABLE lich_su_chinh_sua (
    id VARCHAR(36) PRIMARY KEY,
    bang VARCHAR(100) NOT NULL,
    ban_ghi_id VARCHAR(36) NOT NULL,
    truong VARCHAR(100) NOT NULL,
    gia_tri_cu TEXT,
    gia_tri_moi TEXT,
    ho_gia_dinh_id VARCHAR(36),
    thoi_diem DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (ho_gia_dinh_id) REFERENCES ho_gia_dinh(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
''')

print('✓ All tables created successfully!')
conn.commit()
conn.close()
