-- ���������������ϵͳ
create database IMS
go

use IMS
go

-- �����û���
CREATE TABLE Users 
(
    UserID nvarchar(10) PRIMARY KEY,
    UName nvarchar(100) NOT NULL,
    Passwords nvarchar(100) NOT NULL,
    Permission nvarchar(1) NOT NULL,
    Remarks nvarchar(500)
);

-- ������Ʒ��
CREATE TABLE Goods 
(
    GID nvarchar(10) PRIMARY KEY,
    GName nvarchar(50) NOT NULL,
    IQuantity int NOT NULL,
    IMin int NOT NULL,
    IMax int NOT NULL,
    Remarks nvarchar(500)
);

-- ���������̱�
CREATE TABLE Supplier 
(
    SupplierID nvarchar(10) PRIMARY KEY,
    SName nvarchar(100) NOT NULL,
    Contacts nvarchar(50) NOT NULL,
    Phone nvarchar(50) NOT NULL,
    Addresses nvarchar(200) NOT NULL,
    Remarks nvarchar(500)
);

-- �����ͻ���
CREATE TABLE Customer 
(
    CID nvarchar(10) PRIMARY KEY,
    CName nvarchar(100) NOT NULL,
    Contacts nvarchar(50) NOT NULL,
    Phone nvarchar(50) NOT NULL,
    Addresses nvarchar(200) NOT NULL,
    Remarks nvarchar(500)
);

-- ������������
CREATE TABLE Purchase_list 
(
    PID nvarchar(10) PRIMARY KEY,
    SupplierID nvarchar(10) FOREIGN KEY REFERENCES Supplier(SupplierID),
    Amount_paid float NOT NULL,
    PDate date NOT NULL,
    Remarks nvarchar(500)
);

-- �������������¿���
CREATE TABLE Purchase_updates_inventory 
(
    PID nvarchar(10),
    GID nvarchar(10),
    GNum int NOT NULL,
    Price float NOT NULL,
    Remarks nvarchar(500),
    PRIMARY KEY (PID, GID),
    FOREIGN KEY (PID) REFERENCES Purchase_list(PID),
    FOREIGN KEY (GID) REFERENCES Goods(GID)
);

-- �����˻�����
CREATE TABLE Return_list 
(
    RID nvarchar(10) PRIMARY KEY,
    SupplierID nvarchar(10) FOREIGN KEY REFERENCES Supplier(SupplierID),
    Amount_paid float NOT NULL,
    RDate date NOT NULL,
    Remarks nvarchar(500)
);

-- �����˻������¿���
CREATE TABLE Return_updates_inventory 
(
    RID nvarchar(10),
    GID nvarchar(10),
    GNum int NOT NULL,
    Price float NOT NULL,
    Remarks nvarchar(500),
    PRIMARY KEY (RID, GID),
    FOREIGN KEY (RID) REFERENCES Return_list(RID),
    FOREIGN KEY (GID) REFERENCES Goods(GID)
);

-- �������۵���
CREATE TABLE Sale_list 
(
    SLID nvarchar(10) PRIMARY KEY,
    CID nvarchar(10) FOREIGN KEY REFERENCES Customer(CID),
    Amount_paid float NOT NULL,
    SLDate date NOT NULL,
    Remarks nvarchar(500)
);

-- �������۵����¿���
CREATE TABLE Sale_updates_inventory 
(
    SLID nvarchar(10),
    GID nvarchar(10),
    GNum int NOT NULL,
    Price float NOT NULL,
    Remarks nvarchar(500),
    PRIMARY KEY (SLID, GID),
    FOREIGN KEY (SLID) REFERENCES Sale_list(SLID),
    FOREIGN KEY (GID) REFERENCES Goods(GID)
);

-- �����ͻ��˻�����
CREATE TABLE Customer_return_list 
(
    CRID nvarchar(10) PRIMARY KEY,
    CID nvarchar(10) FOREIGN KEY REFERENCES Customer(CID),
    Amount_paid float NOT NULL,
    CRDate date NOT NULL,
    Remarks nvarchar(500)
);

-- �����ͻ��˻������¿���
CREATE TABLE Customer_return_updates_inventory 
(
    CRID nvarchar(10),
    GID nvarchar(10),
    GNum int NOT NULL,
    Price float NOT NULL,
    Remarks nvarchar(500),
    PRIMARY KEY (CRID, GID),
    FOREIGN KEY (CRID) REFERENCES Customer_return_list(CRID),
    FOREIGN KEY (GID) REFERENCES Goods(GID)
);

-- ��ʼ���û�������
INSERT INTO Users (UserID, UName, Passwords, Permission, Remarks) VALUES
('U001', 'admin', 'admin123', 'A', 'ϵͳ����Ա'),
('U002', 'user1', 'user123', 'U', '��ͨ�û�'),
('U003', 'user2', 'user456', 'U', '��ͨ�û�');

-- ��ʼ����Ʒ������
INSERT INTO Goods (GID, GName, IQuantity, IMin, IMax, Remarks) VALUES
('G001', '��ƷA', 100, 10, 200, ''),
('G002', '��ƷB', 50, 5, 100, ''),
('G003', '��ƷC', 75, 8, 150, ''),
('G004', '��ƷD', 120, 15, 250, ''),
('G005', '��ƷE', 90, 10, 180, '');

-- ��ʼ����Ӧ�̱�����
INSERT INTO Supplier (SupplierID, SName, Contacts, Phone, Addresses, Remarks) VALUES
('S001', '������A', '��ϵ��A', '123456789', '��ַA', ''),
('S002', '������B', '��ϵ��B', '987654321', '��ַB', ''),
('S003', '������C', '��ϵ��C', '456123789', '��ַC', ''),
('S004', '������D', '��ϵ��D', '789456123', '��ַD', ''),
('S005', '������E', '��ϵ��E', '321654987', '��ַE', '');

-- ��ʼ���ͻ�������
INSERT INTO Customer (CID, CName, Contacts, Phone, Addresses, Remarks) VALUES
('C001', '�ͻ�A', '��ϵ��A', '123123123', '��ַA', ''),
('C002', '�ͻ�B', '��ϵ��B', '321321321', '��ַB', ''),
('C003', '�ͻ�C', '��ϵ��C', '456456456', '��ַC', ''),
('C004', '�ͻ�D', '��ϵ��D', '654654654', '��ַD', ''),
('C005', '�ͻ�E', '��ϵ��E', '789789789', '��ַE', '');

-- ��ʼ��������������
INSERT INTO Purchase_list (PID, SupplierID, Amount_paid, PDate, Remarks) VALUES
('P001', 'S001', 1500.00, '2024-06-25', ''),
('P002', 'S002', 800.00, '2024-06-26', ''),
('P003', 'S003', 950.00, '2024-06-27', ''),
('P004', 'S004', 1650.00, '2024-06-28', ''),
('P005', 'S005', 1100.00, '2024-06-29', '');

-- ��ʼ�����������¿�������
INSERT INTO Purchase_updates_inventory (PID, GID, GNum, Price, Remarks) VALUES
('P001', 'G001', 50, 15.00, ''),
('P001', 'G002', 50, 15.00, ''),
('P002', 'G001', 20, 20.00, ''),
('P002', 'G003', 25, 16.00, ''),
('P003', 'G002', 30, 10.00, ''),
('P003', 'G004', 65, 10.00, ''),
('P004', 'G001', 40, 30.00, ''),
('P004', 'G003', 30, 15.00, ''),
('P005', 'G002', 20, 15.00, ''),
('P005', 'G005', 40, 20.00, '');

-- ��ʼ���˻���������
INSERT INTO Return_list (RID, SupplierID, Amount_paid, RDate, Remarks) VALUES
('R001', 'S001', 300.00, '2024-06-27', ''),
('R002', 'S002', 200.00, '2024-06-28', ''),
('R003', 'S003', 400.00, '2024-06-29', ''),
('R004', 'S004', 250.00, '2024-06-30', ''),
('R005', 'S005', 350.00, '2024-07-01', '');

-- ��ʼ���˻������¿�������
INSERT INTO Return_updates_inventory (RID, GID, GNum, Price, Remarks) VALUES
('R001', 'G001', 10, 15.00, ''),
('R001', 'G002', 10, 15.00, ''),
('R002', 'G001', 5, 20.00, ''),
('R002', 'G003', 5, 20.00, ''),
('R003', 'G002', 20, 10.00, ''),
('R003', 'G004', 20, 10.00, ''),
('R004', 'G001', 5, 30.00, ''),
('R004', 'G003', 5, 20.00, ''),
('R005', 'G002', 10, 15.00, ''),
('R005', 'G005', 10, 20.00, '');

-- ��ʼ�����۵�������
INSERT INTO Sale_list (SLID, CID, Amount_paid, SLDate, Remarks) VALUES
('S001', 'C001', 2000.00, '2024-06-28', ''),
('S002', 'C002', 1800.00, '2024-06-29', ''),
('S003', 'C003', 2600.00, '2024-06-30', ''),
('S004', 'C004', 2100.00, '2024-07-01', ''),
('S005', 'C005', 1150.00, '2024-07-02', '');

-- ��ʼ�����۵����¿�������
INSERT INTO Sale_updates_inventory (SLID, GID, GNum, Price, Remarks) VALUES
('S001', 'G001', 40, 25.00, ''),
('S001', 'G002', 40, 25.00, ''),
('S002', 'G003', 45, 20.00, ''),
('S002', 'G004', 45, 20.00, ''),
('S003', 'G001', 40, 20.00, ''),
('S003', 'G002', 45, 20.00, ''),
('S003', 'G003', 45, 20.00, ''),
('S004', 'G004', 42, 25.00, ''),
('S004', 'G005', 42, 25.00, ''),
('S005', 'G001', 46, 25.00, '');

-- ��ʼ���ͻ��˻���������
INSERT INTO Customer_return_list (CRID, CID, Amount_paid, CRDate, Remarks) VALUES
('CR001', 'C001', 500.00, '2024-06-29', ''),
('CR002', 'C002', 400.00, '2024-06-30', ''),
('CR003', 'C003', 900.00, '2024-07-01', ''),
('CR004', 'C004', 450.00, '2024-07-02', ''),
('CR005', 'C005', 350.00, '2024-07-03', '');

-- ��ʼ���ͻ��˻������¿�������
INSERT INTO Customer_return_updates_inventory (CRID, GID, GNum, Price, Remarks) VALUES
('CR001', 'G001', 10, 25.00, ''),
('CR001', 'G002', 10, 25.00, ''),
('CR002', 'G003', 10, 20.00, ''),
('CR002', 'G004', 10, 20.00, ''),
('CR003', 'G001', 15, 20.00, ''),
('CR003', 'G002', 15, 20.00, ''),
('CR003', 'G003', 15, 20.00, ''),
('CR004', 'G004', 9, 25.00, ''),
('CR004', 'G005', 9, 25.00, ''),
('CR005', 'G001', 14, 25.00, '');