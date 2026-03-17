from . import db
from datetime import datetime, timezone
import unicodedata, re
from werkzeug.security import generate_password_hash, check_password_hash
# auto slugify từ tên
def slugify(text: str) -> str:
    text = unicodedata.normalize('NFD', text)
    text = ''.join(c for c in text if unicodedata.category(c) != 'Mn')
    text = text.lower().strip()
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    text = re.sub(r'[\s]+', '-', text)
    return text
class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    user_name = db.Column(db.String(128), nullable = False)
    create_at = db.Column(db.DateTime(timezone=True), default = lambda: datetime.now(timezone.utc))

#1. Tổ chức
class ToChuc(db.Model):
    __tablename__ = 'TO_CHUC'
    id_to_chuc = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ten_to_chuc = db.Column(db.String(255), nullable=False)
    loai_to_chuc = db.Column(db.String(100))
    dia_chi = db.Column(db.Text)
    quoc_gia = db.Column(db.String(100), default='Việt Nam')
    website = db.Column(db.String(255))

    don_vis = db.relationship('DonVi', backref='to_chuc', lazy=True)
    qua_trinh_dao_tao = db.relationship('QuaTrinhDaoTao', backref='to_chuc', lazy=True)
    qua_trinh_cong_tac = db.relationship('QuaTrinhCongTac', backref='to_chuc', lazy=True)

    def to_dict(self):
        return {
            'id_to_chuc': self.id_to_chuc,
            'ten_to_chuc': self.ten_to_chuc,
            'loai_to_chuc': self.loai_to_chuc,
            'dia_chi': self.dia_chi,
            'quoc_gia': self.quoc_gia,
            'website': self.website,
        } 
#2. Đơn vị
class DonVi(db.Model):
    __tablename__ = 'DON_VI'
    id_don_vi  = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ten_don_vi = db.Column(db.String(255), nullable=False)
    id_to_chuc = db.Column(db.Integer, db.ForeignKey('TO_CHUC.id_to_chuc'), nullable=False)
 
    can_bos = db.relationship('CanBo', backref='don_vi', lazy=True)
 
    def to_dict(self):
        return {
            'id_don_vi':  self.id_don_vi,
            'ten_don_vi': self.ten_don_vi,
            'id_to_chuc': self.id_to_chuc,
        }
#3. Cán bộ
class CanBo(db.Model):
    __tablename__ = 'CAN_BO'
    id_can_bo = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_don_vi = db.Column(db.Integer, db.ForeignKey('DON_VI.id_don_vi'), nullable=False)
    ten = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)
    sdt = db.Column(db.String(20))
    dia_chi = db.Column(db.Text)
    nam_sinh = db.Column(db.SmallInteger)
    gioi_tinh = db.Column(db.String(5))
    hoc_ham = db.Column(db.String(50))
    hoc_vi = db.Column(db.String(50))
    avatar = db.Column(db.Text)
    slug = db.Column(db.String(255), unique=True)

    tai_khoan = db.relationship('TaiKhoan', backref='can_bo', uselist=False, cascade='all, delete-orphan')
    dao_taos = db.relationship('QuaTrinhDaoTao', backref='can_bo', cascade='all, delete-orphan', lazy=True)
    cong_tacs = db.relationship('QuaTrinhCongTac', backref='can_bo', cascade='all, delete-orphan', lazy=True)
    giang_days = db.relationship('GiangDay', backref='can_bo', cascade='all, delete-orphan', lazy=True)
    linh_vucs = db.relationship('LinhVucNghienCuu', backref='can_bo', cascade='all, delete-orphan', lazy=True)
    cong_trinhs = db.relationship('CongTrinhNghienCuu', backref='can_bo', cascade='all, delete-orphan', lazy=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.slug and self.ten:
            prefix = f"{self.hoc_vi}-{self.ten}" if self.hoc_vi else self.ten
            self.slug = slugify(prefix)
 
    def to_dict(self):
        return {
            'id_can_bo': self.id_can_bo,
            'id_don_vi': self.id_don_vi,
            'ten': self.ten,
            'email': self.email,
            'sdt': self.sdt,
            'dia_chi': self.dia_chi,
            'nam_sinh': self.nam_sinh,
            'gioi_tinh': self.gioi_tinh,
            'hoc_ham': self.hoc_ham,
            'hoc_vi': self.hoc_vi,
            'avatar': self.avatar,
            'slug': self.slug,
        }
#4. Tài khoản
class TaiKhoan(db.Model):
    __tablename__ = 'TAI_KHOAN'
    id_tai_khoan = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_can_bo = db.Column(db.Integer, db.ForeignKey('CAN_BO.id_can_bo', ondelete='CASCADE'), nullable=False, unique=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    mat_khau = db.Column(db.String(255), nullable=False)
    vai_tro = db.Column(db.Enum('admin', 'user'), default='user')
 
    def set_password(self, raw_password: str):
        self.mat_khau = generate_password_hash(raw_password)
 
    def check_password(self, raw_password: str) -> bool:
        return check_password_hash(self.mat_khau, raw_password)
 
    def to_dict(self):
        return {
            'id_tai_khoan': self.id_tai_khoan,
            'id_can_bo': self.id_can_bo,
            'username': self.username,
            'vai_tro': self.vai_tro,
        }
#5. Quá trình đào tạo
class QuaTrinhDaoTao(db.Model):
    __tablename__ = 'QUA_TRINH_DAO_TAO'
    id_dao_tao = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_can_bo = db.Column(db.Integer, db.ForeignKey('CAN_BO.id_can_bo', ondelete='CASCADE'), nullable=False)
    id_to_chuc = db.Column(db.Integer, db.ForeignKey('TO_CHUC.id_to_chuc'), nullable=False)
    bac_dao_tao = db.Column(db.String(50))
    chuyen_nganh = db.Column(db.String(255))
    nam_bat_dau = db.Column(db.SmallInteger)
    nam_ket_thuc = db.Column(db.SmallInteger)
 
    def to_dict(self):
        return {
            'id_dao_tao': self.id_dao_tao,
            'id_can_bo': self.id_can_bo,
            'id_to_chuc': self.id_to_chuc,
            'bac_dao_tao': self.bac_dao_tao,
            'chuyen_nganh': self.chuyen_nganh,
            'nam_bat_dau': self.nam_bat_dau,
            'nam_ket_thuc': self.nam_ket_thuc,
        }
#6. Quá trình công tác
class QuaTrinhCongTac(db.Model):
    __tablename__ = 'QUA_TRINH_CONG_TAC'
    id_cong_tac = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_can_bo = db.Column(db.Integer, db.ForeignKey('CAN_BO.id_can_bo', ondelete='CASCADE'), nullable=False)
    id_to_chuc = db.Column(db.Integer, db.ForeignKey('TO_CHUC.id_to_chuc'), nullable=False)
    chuc_vu = db.Column(db.String(200))
    tu_nam = db.Column(db.SmallInteger)
    den_nam = db.Column(db.SmallInteger)
 
    def to_dict(self):
        return {
            'id_cong_tac': self.id_cong_tac,
            'id_can_bo': self.id_can_bo,
            'id_to_chuc': self.id_to_chuc,
            'chuc_vu': self.chuc_vu,
            'tu_nam': self.tu_nam,
            'den_nam': self.den_nam,
        }
#7. Giảng dạy
class GiangDay(db.Model):
    __tablename__ = 'GIANG_DAY'
    id_giang_day = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_can_bo = db.Column(db.Integer, db.ForeignKey('CAN_BO.id_can_bo', ondelete='CASCADE'), nullable=False)
    ten_mon = db.Column(db.String(255), nullable=False)
    bac_dao_tao = db.Column(db.String(50))
    nam_giang_day = db.Column(db.SmallInteger)
 
    def to_dict(self):
        return {
            'id_giang_day': self.id_giang_day,
            'id_can_bo': self.id_can_bo,
            'ten_mon': self.ten_mon,
            'bac_dao_tao': self.bac_dao_tao,
            'nam_giang_day': self.nam_giang_day,
        }
#8. Lĩnh vực nghiên cứu
class LinhVucNghienCuu(db.Model):
    __tablename__ = 'LINH_VUC_NGHIEN_CUU'
    id_linh_vuc = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_can_bo = db.Column(db.Integer, db.ForeignKey('CAN_BO.id_can_bo', ondelete='CASCADE'), nullable=False)
    ten_linh_vuc = db.Column(db.String(255), nullable=False)
    mo_ta = db.Column(db.Text)
 
    def to_dict(self):
        return {
            'id_linh_vuc': self.id_linh_vuc,
            'id_can_bo': self.id_can_bo,
            'ten_linh_vuc': self.ten_linh_vuc,
            'mo_ta': self.mo_ta,
        }
#9. Công trình nghiên cứu
class CongTrinhNghienCuu(db.Model):
    __tablename__ = 'CONG_TRINH_NGHIEN_CUU'
    id_ctnc = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_can_bo = db.Column(db.Integer, db.ForeignKey('CAN_BO.id_can_bo', ondelete='CASCADE'), nullable=False)
    ten_cong_trinh = db.Column(db.String(500), nullable=False)
    loai_cong_trinh = db.Column(db.String(100))
    nam_cong_bo = db.Column(db.SmallInteger)
    tap_chi = db.Column(db.String(300))
    doi = db.Column(db.String(100))
    link = db.Column(db.String(500))
 
    def to_dict(self):
        return {
            'id_ctnc': self.id_ctnc,
            'id_can_bo': self.id_can_bo,
            'ten_cong_trinh': self.ten_cong_trinh,
            'loai_cong_trinh': self.loai_cong_trinh,
            'nam_cong_bo': self.nam_cong_bo,
            'tap_chi': self.tap_chi,
            'doi': self.doi,
            'link': self.link,
        }

