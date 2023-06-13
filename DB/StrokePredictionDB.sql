Create database StrokePrediction

use StrokePrediction

Create Table BenhNhan (
	sdt Char(10) Primary Key,
	hoten Nvarchar(50),

)

CREATE TABLE HoSoBenhAn (
    id int IDENTITY PRIMARY KEY,
    gioitinh INT,
    tuoi INT,
    tanghuyetap INT,
    benhtim INT,
    kethon INT,
    loaicongviec INT,
    noio INT,
    glucosetrungbinh FLOAT,
    bmi FLOAT,
    hutthuoc INT,
    chuandoan INT,
	nhanxet int,
	sdt CHAR(10),
    FOREIGN KEY (sdt) REFERENCES BenhNhan(sdt)
)