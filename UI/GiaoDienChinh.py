import tkinter as tk
from tkinter import ttk
import pyodbc 
import numpy as np
import pickle
import joblib
import pandas as pd
from tensorflow.keras.models import load_model
import tensorflow as tf

class ConnectDB:
    def __init__(self):
        server = 'LAPTOP-BGGEL34O'
        database = 'StrokePrediction'
        username = 'sa'
        password = '123456'
        global conn_str
        conn_str = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'

    def lay_TTBenhNhan(self):
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        sql = 'select * from BenhNhan'
        cursor.execute(sql)
        return cursor
    def lay_TTBenhAn(self, sdt):
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        sql = f'select gioitinh, tuoi, tanghuyetap, benhtim, kethon, loaicongviec,noio,glucosetrungbinh, bmi, hutthuoc,chuandoan,nhanxet from HoSoBenhAn where sdt = {sdt}'
        cursor.execute(sql)
        return cursor
    def LuuBenhAn(self, sdt, data):
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        for row in data:
            gioitinh, tuoi, tanghuyetap, benhtim, kethon, loaicongviec, noio, glucosetrungbinh, bmi, hutthuoc, chuandoan, nhanxet = row
            sdt = sdt 
            query = f"INSERT INTO HoSoBenhAn (gioitinh, tuoi, tanghuyetap, benhtim, kethon, loaicongviec, noio, glucosetrungbinh, bmi, hutthuoc, chuandoan, nhanxet, sdt) VALUES ({gioitinh}, {tuoi}, {tanghuyetap}, {benhtim}, {kethon}, {loaicongviec}, {noio}, {glucosetrungbinh}, {bmi}, {hutthuoc}, {chuandoan}, {nhanxet}, '{sdt}')"
            conn.execute(query)
        conn.commit()
        conn.close()

    def TaoBenhNhan(self, sdt, ten):
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        sql = f"INSERT INTO BenhNhan (sdt, hoten) VALUES (?,?)"
        # Thực thi câu lệnh SQL với các tham số
        cursor.execute(sql,(sdt,ten))
        # Lưu thay đổi vào cơ sở dữ liệu
        conn.commit()
        conn.close()


class GiaoDien:
    def __init__(self):
        self.root = tk.Tk()
        # Thông tin bệnh nhân
        self.frame_ThongTinBN = tk.Frame(self.root, highlightbackground='black',highlightthickness=2)
        self.lb_1 = tk.Label(self.frame_ThongTinBN,text='Danh sách bệnh nhân').grid(row=0,column=0)
        self.tb_ThongTinBN = ttk.Treeview(self.frame_ThongTinBN, columns=('SDT','HoTen'))
        self.tb_ThongTinBN.column('SDT',width=100)
        self.tb_ThongTinBN.column('HoTen',width=130)
        self.tb_ThongTinBN.column('#0',width=0)
        self.tb_ThongTinBN.heading('#0',text='')
        
        self.tb_ThongTinBN.heading('SDT',text='SDT')
        self.tb_ThongTinBN.heading('HoTen',text='HoTen')
        cn = ConnectDB()
        data = cn.lay_TTBenhNhan()
        for row in data:
            values = [value.strip("'") if isinstance(value, str) else value for value in row]
            self.tb_ThongTinBN.insert("", "end", values=values)
        self.tb_ThongTinBN.grid(row=1, column=0)
        self.frame_ThongTinBN.grid(row=0,column=0, padx=10, pady=10)
        self.tb_ThongTinBN.bind("<<TreeviewSelect>>", lambda event: self.displaySelectedItem())
        # hồ sơ bệnh án
        self.frame_HosoBA = tk.Frame(self.root, highlightbackground='black',highlightthickness=2,width=100, height=100)
        self.lb_hsba = tk.Label(self.frame_HosoBA,text='Ho so benh an').grid(row=0,column=0)
        self.tb_HoSoBA = ttk.Treeview(self.frame_HosoBA, columns=('gioitinh','tuoi','tanghuyetap','benhtim','kethon','loaicongviec','noio','glucosetrungbinh','bmi','hutthuoc','chuandoan','nhanxet'))
        # Thiết lập độ rộng cho từng cột
        self.tb_HoSoBA.column('gioitinh', width=100)
        self.tb_HoSoBA.column('tuoi', width=50)
        self.tb_HoSoBA.column('tanghuyetap', width=100)
        self.tb_HoSoBA.column('benhtim', width=100)
        self.tb_HoSoBA.column('kethon', width=80)
        self.tb_HoSoBA.column('loaicongviec', width=100)
        self.tb_HoSoBA.column('noio', width=100)
        self.tb_HoSoBA.column('glucosetrungbinh', width=100)
        self.tb_HoSoBA.column('bmi', width=80)
        self.tb_HoSoBA.column('hutthuoc', width=80)
        self.tb_HoSoBA.column('chuandoan', width=100)
        self.tb_HoSoBA.column('nhanxet', width=100)

        # Bỏ cột ID
        self.tb_HoSoBA.column('#0', width=0)
        self.tb_HoSoBA.heading('#0', text='')

        # Hiển thị các cột
        self.tb_HoSoBA.heading('gioitinh', text='Giới tính')
        self.tb_HoSoBA.heading('tuoi', text='Tuổi')
        self.tb_HoSoBA.heading('tanghuyetap', text='Tăng huyết áp')
        self.tb_HoSoBA.heading('benhtim', text='Bệnh tim')
        self.tb_HoSoBA.heading('kethon', text='Kết hôn')
        self.tb_HoSoBA.heading('loaicongviec', text='Loại công việc')
        self.tb_HoSoBA.heading('noio', text='Nơi ở')
        self.tb_HoSoBA.heading('glucosetrungbinh', text='Glucose trung bình')
        self.tb_HoSoBA.heading('bmi', text='BMI')
        self.tb_HoSoBA.heading('hutthuoc', text='Hút thuốc')
        self.tb_HoSoBA.heading('chuandoan', text='Chuẩn đoán')
        self.tb_HoSoBA.heading('nhanxet', text='Nhận xét')
        self.tb_HoSoBA.grid(row=1,column=0)
        self.frame_HosoBA.grid(row=0, column=1,padx= 10, pady=10)
        
        # frame thong tin benh nhan
        self.frame_NhapTTBenhNhan = tk.Frame(self.root,highlightbackground='black',highlightthickness=2)
        self.lbNhapTTBN = tk.Label(self.frame_NhapTTBenhNhan,text='Nhập thông tin bênh nhân').grid(row=0,column=0)
        self.lb_NhapSDT = tk.Label(self.frame_NhapTTBenhNhan,text='Nhập số điện thoại').grid(row=1,column=0)
        self.SDT = tk.StringVar()
        self.txt_SDT = tk.Entry(self.frame_NhapTTBenhNhan,textvariable=self.SDT)
        self.txt_SDT.grid(row=1,column=1)
        self.lbNhapTen = tk.Label(self.frame_NhapTTBenhNhan,text='Nhập họ tên').grid(row=2,column=0)
        self.HoTen = tk.StringVar()
        self.txt_HoTen = tk.Entry(self.frame_NhapTTBenhNhan,textvariable=self.HoTen)
        self.txt_HoTen.grid(row=2,column=1)
        self.btn_Moi = tk.Button(self.frame_NhapTTBenhNhan,text='Mới',command=self.Moi)
        self.btn_Moi.grid(row=3,column=0)
        self.btn_ThemBN = tk.Button(self.frame_NhapTTBenhNhan,text='Bệnh nhân mới',command=self.TaoBN)
        self.btn_ThemBN.grid(row=3, column=1)
        self.frame_NhapTTBenhNhan.grid(row=1,column=0, padx=10,pady=10)
        # frame ho so benh an
        self.frame_NhapHSBA = tk.Frame(self.root,highlightbackground='black',highlightthickness=2)
        self.lb_NhapTTBenh = tk.Label(self.frame_NhapHSBA,text='Nhập thông tin bệnh').grid(row=0,column=0)
        
        self.lb_NhapTuoi = tk.Label(self.frame_NhapHSBA,text='Nhập tuổi').grid(row=1,column=0, ipady=8,ipadx=8)
        self.Tuoi = tk.IntVar()
        self.txt_Tuoi = tk.Entry(self.frame_NhapHSBA,textvariable=self.Tuoi).grid(row=1,column=1)
        
        self.lb_ChonGT = tk.Label(self.frame_NhapHSBA,text='Chọn giới tính').grid(row=1, column=2,ipady=8,ipadx=8)
        self.GioiTinh = tk.IntVar()
        self.rdo_GTNam = tk.Radiobutton(self.frame_NhapHSBA,text='Nam',variable=self.GioiTinh,value=1).grid(row=1,column=3)
        self.rdo_GTNu = tk.Radiobutton(self.frame_NhapHSBA,text='Nữ',variable=self.GioiTinh,value=0).grid(row=1,column=4)
        self.rdo_GTKhac = tk.Radiobutton(self.frame_NhapHSBA,text='Khác',variable=self.GioiTinh,value=2).grid(row=1,column=5) 
        
        self.lb_TangHuyetAp = tk.Label(self.frame_NhapHSBA,text='Tăng huyết áp').grid(row=1,column=6, ipady=8,ipadx=8)
        self.TangHuyetAp = tk.IntVar()
        self.rdo_CoTangHA = tk.Radiobutton(self.frame_NhapHSBA,text='Có',variable=self.TangHuyetAp,value=1).grid(row=1,column=7)
        self.rdo_KhongTangHA = tk.Radiobutton(self.frame_NhapHSBA,text='Không',variable=self.TangHuyetAp,value=0).grid(row=1, column=8)
        
        self.lb_BenhTim = tk.Label(self.frame_NhapHSBA,text='Bệnh tim').grid(row=2,column=0, ipady=8,ipadx=8)
        self.BenhTim = tk.IntVar()
        self.rdo_CoBenhTim = tk.Radiobutton(self.frame_NhapHSBA,text='Có',variable=self.BenhTim,value=1).grid(row=2,column=1)
        self.rdo_KhongBenhTim = tk.Radiobutton(self.frame_NhapHSBA,text='Không',variable=self.BenhTim,value=0).grid(row=2, column=2)
        
        self.lb_KetHon = tk.Label(self.frame_NhapHSBA,text='Kết hôn').grid(row=2,column=3, ipady=8,ipadx=8)
        self.KetHon = tk.IntVar()
        self.rdo_DaKetHon = tk.Radiobutton(self.frame_NhapHSBA,text='Đã',variable=self.KetHon,value=1).grid(row=2,column=4)
        self.rdo_ChuaKetHon = tk.Radiobutton(self.frame_NhapHSBA,text='Chưa',variable=self.KetHon,value=0).grid(row=2, column=5)
        
        self.lb_LoaiCV = tk.Label(self.frame_NhapHSBA,text='Loại công việc').grid(row=3,column=0, ipady=8,ipadx=8)
        self.LoaiCV = tk.IntVar()
        self.rdo_HocSinh = tk.Radiobutton(self.frame_NhapHSBA,text='Học sinh',variable=self.LoaiCV,value=4).grid(row=3,column=1)
        self.rdo_NhaNuoc = tk.Radiobutton(self.frame_NhapHSBA,text='Nhà nước',variable=self.LoaiCV,value=0).grid(row=3, column=2)
        self.rdo_KhongLam = tk.Radiobutton(self.frame_NhapHSBA,text='Không làm việc',variable=self.LoaiCV,value=1).grid(row=3,column=3)
        self.rdo_RiengTu = tk.Radiobutton(self.frame_NhapHSBA,text='Riêng tư',variable=self.LoaiCV,value=2).grid(row=3, column=4)
        self.rdo_LamChu = tk.Radiobutton(self.frame_NhapHSBA,text='Làm chủ',variable=self.LoaiCV,value=3).grid(row=3, column=5)
        
        self.lb_NoiO = tk.Label(self.frame_NhapHSBA,text='Nơi ở').grid(row=4,column=0, ipady=8,ipadx=8)
        self.NoiO = tk.IntVar()
        self.rdo_ThanhPho = tk.Radiobutton(self.frame_NhapHSBA,text='Thành phố',variable=self.NoiO,value=1).grid(row=4,column=1)
        self.rdo_NongThon = tk.Radiobutton(self.frame_NhapHSBA,text='Nông thôn',variable=self.NoiO,value=0).grid(row=4, column=2)
        
        self.lb_NhapLuongDuong = tk.Label(self.frame_NhapHSBA,text='Nhập lượng đường trong máu').grid(row=5,column=0, ipady=8,ipadx=8)
        self.LuongDuong = tk.DoubleVar()
        self.txt_LuongDuong = tk.Entry(self.frame_NhapHSBA,textvariable=self.LuongDuong).grid(row=5,column=1)
        
        self.lb_NhapBMI = tk.Label(self.frame_NhapHSBA,text='Nhập chỉ số khối cơ thể').grid(row=6,column=0, ipady=8,ipadx=8)
        self.BMI = tk.DoubleVar()
        self.txt_BMI = tk.Entry(self.frame_NhapHSBA,textvariable=self.BMI).grid(row=6,column=1)
        
        self.lb_HutThuoc = tk.Label(self.frame_NhapHSBA,text='Hút thuốc').grid(row=7,column=0, ipady=8,ipadx=8)
        self.HutThuoc = tk.IntVar()
        self.rdo_KhongBiet = tk.Radiobutton(self.frame_NhapHSBA,text='Không biết',variable=self.HutThuoc,value=0).grid(row=7,column=1)
        self.rdo_HutNhieu = tk.Radiobutton(self.frame_NhapHSBA,text='Hút nhiều',variable=self.HutThuoc,value=1).grid(row=7, column=2)
        self.rdo_CoHut = tk.Radiobutton(self.frame_NhapHSBA,text='Có hút',variable=self.HutThuoc,value=2).grid(row=7,column=3)
        self.rdo_KhongHut = tk.Radiobutton(self.frame_NhapHSBA,text='Không hút',variable=self.HutThuoc,value=3).grid(row=7, column=4)

        self.lb_DuDoan = tk.Label(self.frame_NhapHSBA,text='Dự đoán bệnh').grid(row=8,column=0, ipady=8,ipadx=8)
        self.DuDoan = tk.IntVar()
        self.rdo_CoBenh = tk.Radiobutton(self.frame_NhapHSBA,text='Có bệnh',variable=self.DuDoan,value=1)
        self.rdo_CoBenh.grid(row=8,column=1)
        self.rdo_KhongBenh = tk.Radiobutton(self.frame_NhapHSBA,text='Không bệnh',variable=self.DuDoan,value=0)
        self.rdo_KhongBenh.grid(row=8, column=2)
        self.lb_KetQuaDuDoan = tk.Label(self.frame_NhapHSBA,text='Chờ kết quả').grid(row=8,column=3)
        
        self.lb_NhanXet = tk.Label(self.frame_NhapHSBA,text='Nhận xét').grid(row=9,column=0, ipady=8,ipadx=8)
        self.NhanXet = tk.IntVar()
        self.rdo_DongY = tk.Radiobutton(self.frame_NhapHSBA,text='Đồng ý',variable=self.NhanXet,value=1).grid(row=9,column=1)
        self.rdo_KhongDY = tk.Radiobutton(self.frame_NhapHSBA,text='Không đồng ý',variable=self.NhanXet,value=0).grid(row=9, column=2)
        
        self.btn_DuDoanRDF = tk.Button(self.frame_NhapHSBA,text='Dự đoán RDF',command=self.DuDoanBenhRDF)
        self.btn_DuDoanRDF.grid(row=10,column=0,padx=10,pady=10)
        self.btn_DuDoanSVM = tk. Button(self.frame_NhapHSBA,text='Dụ đoán SVM',command=self.DuDoanSVM)
        self.btn_DuDoanSVM.grid(row=10,column=2)
        self.btn_DuDoanCNN = tk. Button(self.frame_NhapHSBA,text='Dụ đoán CNN',command=self.DuDoanCNN)
        self.btn_DuDoanCNN.grid(row=10,column=3)
        self.btn_LuuBenhAn = tk.Button(self.frame_NhapHSBA,text='Lưu bệnh án',command=self.LuuBenhAn)
        self.btn_LuuBenhAn.grid(row=10,column=1,padx=10,pady=10)
        self.frame_NhapHSBA.grid(row=1, column=1,padx=10,pady=10)
        self.root.mainloop()

    def displaySelectedItem(self):
        selected_item = self.tb_ThongTinBN.selection()
        item_values = self.tb_ThongTinBN.item(selected_item, "values")
        self.txt_SDT.delete(0,'end')
        self.txt_HoTen.delete(0,'end')
        self.txt_SDT.insert(0,item_values[0])
        self.txt_HoTen.insert(0,item_values[1])
        print(item_values[0])
        cn = ConnectDB()
        data = cn.lay_TTBenhAn(item_values[0])
        if self.tb_HoSoBA.get_children():
            # Xóa các hàng trong cây
            self.tb_HoSoBA.delete(*self.tb_HoSoBA.get_children())
        for row in data:
            values = [value.strip("'") if isinstance(value, str) else value for value in row]
            self.tb_HoSoBA.insert("", "end", values=values)
    def DuDoanBenhRDF(self):
        data= [[self.Tuoi.get(),
                self.GioiTinh.get(),
                self.TangHuyetAp.get(),
                self.BenhTim.get(),
                self.KetHon.get(),
                self.LoaiCV.get(),
                self.NoiO.get(),
                self.LuongDuong.get(),
                self.BMI.get(),
                self.HutThuoc.get()]]
        print(data)
        input_df = pd.DataFrame(data=data)

        model = joblib.load('StrokePrediction/Model/random_forest.pkl')
        dudoan = model.predict(input_df)
        confidence = model.predict_proba(input_df)
        print(dudoan)
        # In độ tự tin của các lớp
        for class_index, class_confidence in enumerate(confidence):
            print(f"Lớp {class_index}: {class_confidence}")
        if dudoan[0] == 1:
            self.rdo_CoBenh.select()
            self.lb_KetQuaDuDoan = tk.Label(self.frame_HosoBA,text='Có Bệnh').grid(row=8,column=3)
            print('Có bệnh')
        else:
            self.rdo_KhongBenh.select()
            self.lb_KetQuaDuDoan = tk.Label(self.frame_HosoBA,text='Không Bệnh').grid(row=8,column=3)
            print('Không bệnh')
    def LuuBenhAn(self):
        selected_item = self.tb_ThongTinBN.selection()
        item_values = self.tb_ThongTinBN.item(selected_item, "values")
        data= [[self.Tuoi.get(),
                self.GioiTinh.get(),
                self.TangHuyetAp.get(),
                self.BenhTim.get(),
                self.KetHon.get(),
                self.LoaiCV.get(),
                self.NoiO.get(),
                self.LuongDuong.get(),
                self.BMI.get(),
                self.HutThuoc.get(),
                self.DuDoan.get(),
                self.NhanXet.get()]]
        cn = ConnectDB()
        cn.LuuBenhAn(item_values[0],data)
        data_tb = cn.lay_TTBenhAn(item_values[0])
        if self.tb_HoSoBA.get_children():
            # Xóa các hàng trong cây
            self.tb_HoSoBA.delete(*self.tb_HoSoBA.get_children())
        for row in data_tb:
            values = [value.strip("'") if isinstance(value, str) else value for value in row]
            self.tb_HoSoBA.insert("", "end", values=values)
    def Moi(self):
        self.txt_SDT.delete(0,'end')
        self.txt_HoTen.delete(0,'end')
    def TaoBN(self):
        cn = ConnectDB()
        cn.TaoBenhNhan(self.SDT.get(),self.HoTen.get())
        cn1 = ConnectDB()
        data = cn1.lay_TTBenhNhan()
        if self.tb_ThongTinBN.get_children():
            # Xóa các hàng trong cây
            self.tb_ThongTinBN.delete(*self.tb_ThongTinBN.get_children())
        for row in data:
            values = [value.strip("'") if isinstance(value, str) else value for value in row]
            self.tb_ThongTinBN.insert("", "end", values=values)

    def DuDoanSVM(self):
        data= [[self.Tuoi.get(),
                self.GioiTinh.get(),
                self.TangHuyetAp.get(),
                self.BenhTim.get(),
                self.KetHon.get(),
                self.LoaiCV.get(),
                self.NoiO.get(),
                self.LuongDuong.get(),
                self.BMI.get(),
                self.HutThuoc.get()]]
        print(data)
        input_df = pd.DataFrame(data=data)

        model = joblib.load('Model\svm_model_1.pkl')
        dudoan = model.predict(input_df)

        print(dudoan)
        if dudoan[0] == 1:
            self.rdo_CoBenh.select()
            self.lb_KetQuaDuDoan = tk.Label(self.frame_HosoBA,text='Có Bệnh').grid(row=8,column=3)
            print('Có bệnh')
        else:
            self.rdo_KhongBenh.select()
            self.lb_KetQuaDuDoan = tk.Label(self.frame_HosoBA,text='Không Bệnh').grid(row=8,column=3)
            print('Không bệnh')

    def DuDoanCNN(self):
        data= [[self.Tuoi.get(),
                self.GioiTinh.get(),
                self.TangHuyetAp.get(),
                self.BenhTim.get(),
                self.KetHon.get(),
                self.LoaiCV.get(),
                self.NoiO.get(),
                self.LuongDuong.get(),
                self.BMI.get(),
                self.HutThuoc.get()]]
        print(data)
        model = load_model('StrokePrediction\Model\cnn.h5')
        X_tensor = tf.convert_to_tensor(data, dtype=tf.float32)
        prediction = model.predict(X_tensor)
        if prediction[0] > 0.2:
            self.rdo_CoBenh.select()
            self.lb_KetQuaDuDoan = tk.Label(self.frame_HosoBA,text='Có Bệnh').grid(row=8,column=3)
            print('Có bệnh')
        else:
            self.rdo_KhongBenh.select()
            self.lb_KetQuaDuDoan = tk.Label(self.frame_HosoBA,text='Không Bệnh').grid(row=8,column=3)
            print('Không bệnh')
GiaoDien()