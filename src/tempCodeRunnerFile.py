from main import app
from src.models import db, ToChuc, DonVi, CanBo, QuaTrinhDaoTao, QuaTrinhCongTac, GiangDay, LinhVucNghienCuu, CongTrinhNghienCuu, TaiKhoan
from werkzeug.security import generate_password_hash
import unicodedata, re


def slugify(text):
    text = unicodedata.normalize('NFD', text)
    text = ''.join(c for c in text if unicodedata.category(c) != 'Mn')
    text = text.lower().strip()
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    text = re.sub(r'\s+', '-', text)
    return text
# tổ chức
TO_CHUC_DATA = [
    {"ten_to_chuc": "Đại học Kinh tế Quốc dân",
     "loai_to_chuc": "Đại học công lập",
     "dia_chi": "207 Giải Phóng, Hai Bà Trưng, Hà Nội",
     "quoc_gia": "Việt Nam", "website": "https://neu.edu.vn"},

    {"ten_to_chuc": "Đại học Bách Khoa Hà Nội",
     "loai_to_chuc": "Đại học công lập",
     "dia_chi": "1 Đại Cồ Việt, Hai Bà Trưng, Hà Nội",
     "quoc_gia": "Việt Nam", "website": "https://hust.edu.vn"},

    {"ten_to_chuc": "Đại học Quốc lập Trung ương Đài Loan",
     "loai_to_chuc": "Đại học công lập",
     "dia_chi": "Taoyuan, Đài Loan",
     "quoc_gia": "Đài Loan", "website": "https://www.ncu.edu.tw"},

    {"ten_to_chuc": "Đại học Ngoại ngữ - Đại học Quốc gia Hà Nội",
     "loai_to_chuc": "Đại học công lập",
     "dia_chi": "Phạm Văn Đồng, Cầu Giấy, Hà Nội",
     "quoc_gia": "Việt Nam", "website": "https://ulis.vnu.edu.vn"},

    {"ten_to_chuc": "Đại học Sư phạm Hà Nội",
     "loai_to_chuc": "Đại học công lập",
     "dia_chi": "136 Xuân Thủy, Cầu Giấy, Hà Nội",
     "quoc_gia": "Việt Nam", "website": "https://hnue.edu.vn"},

    {"ten_to_chuc": "Trường Cán bộ quản lý giáo dục TP.HCM",
     "loai_to_chuc": "Trường công lập",
     "dia_chi": "Thành phố Hồ Chí Minh",
     "quoc_gia": "Việt Nam", "website": ""},
]
# đơn vị
DON_VI_DATA = [
    {"ten_don_vi": "Khoa Công nghệ Thông tin",
     "ten_to_chuc": "Đại học Kinh tế Quốc dân"},
]
# cán bộ
CAN_BO_DATA = [
    {
        "ten": "Phạm Xuân Lâm", "hoc_vi": "TS", "hoc_ham": "",
        "email": "lampx@neu.edu.vn", "sdt": "0937638683",
        "gioi_tinh": "Nam", "nam_sinh": 1983,
        "don_vi": "Khoa Công nghệ Thông tin", "avatar": "",
        "dao_tao": [
            {"to_chuc": "Đại học Quốc lập Trung ương Đài Loan",
             "bac": "Tiến sĩ", "nganh": "Khoa học máy tính", "tu": 2012, "den": 2017},
            {"to_chuc": "Đại học Bách Khoa Hà Nội",
             "bac": "Thạc sĩ", "nganh": "Công nghệ thông tin", "tu": 2007, "den": 2009},
            {"to_chuc": "Đại học Bách Khoa Hà Nội",
             "bac": "Kỹ sư", "nganh": "Công nghệ thông tin", "tu": 2001, "den": 2006},
        ],
        "cong_tac": [
            {"to_chuc": "Đại học Kinh tế Quốc dân",
             "chuc_vu": "Giảng viên, Khoa Công nghệ Thông tin, Trường Công nghệ",
             "tu": 2006, "den": None},
        ],
        "giang_day": [
            "Lập trình Java", "Thiết kế Web", "Dữ liệu phi cấu trúc",
            "Kiến trúc máy tính", "Hệ điều hành", "Phát triển ứng dụng di động",
        ],
        "linh_vuc": [
            "Công nghệ giáo dục",
            "Công nghệ/ ứng dụng di động",
            "Các hệ thống thông minh",
        ],
        "cong_trinh": [
            {"ten": "Improving the efficiency of Sentiment Analysis System based on integration with RPA and KBS",
             "loai": "Bài báo quốc tế", "nam": 2025,
             "tap_chi": "", "doi": "", "link": ""},
            {"ten": "Đề xuất hệ thống hỗ trợ học tập theo nguyên tắc kiến tạo dựa trên nền tảng Google Codelabs",
             "loai": "Bài báo trong nước", "nam": 2025,
             "tap_chi": "", "doi": "", "link": ""},
            {"ten": "Combining RPA and AI to recognize learners' emotions in Cyberspace: Experiment at some Vietnamese universities",
             "loai": "Bài báo quốc tế", "nam": 2025,
             "tap_chi": "", "doi": "", "link": ""},
            {"ten": "A Constructivist-Based Interactive Learning Management System Leveraging Google Codelabs",
             "loai": "Bài báo quốc tế", "nam": 2025,
             "tap_chi": "", "doi": "", "link": ""},
            {"ten": "Tailored Expert Finding Systems for Vietnamese SMEs: A Five-Step Framework",
             "loai": "Bài báo quốc tế", "nam": 2023,
             "tap_chi": "International Journal of Advanced Computer Science and Applications (IJACSA), Vol.14, No.11",
             "doi": "", "link": ""},
            {"ten": "PACARD: A New Interface to Increase Mobile Learning App Engagement, Distributed Through App Stores",
             "loai": "Bài báo quốc tế", "nam": 2018,
             "tap_chi": "Journal of Educational Computing Research, 57(3), 618-645",
             "doi": "", "link": ""},
            {"ten": "Card-based design combined with spaced repetition: A new interface for displaying learning elements and improving active recall",
             "loai": "Bài báo quốc tế", "nam": 2016,
             "tap_chi": "The Journal of Computer and Education, 98, 142-156",
             "doi": "", "link": ""},
        ],
    },
    {
        "ten": "Lưu Minh Tuấn", "hoc_vi": "TS", "hoc_ham": "",
        "email": "tuanlm@neu.edu.vn", "sdt": "0904143460",
        "gioi_tinh": "Nam", "nam_sinh": 1976,
        "don_vi": "Khoa Công nghệ Thông tin", "avatar": "",
        "dao_tao": [
            {"to_chuc": "Đại học Bách Khoa Hà Nội",
             "bac": "Kỹ sư", "nganh": "Công nghệ thông tin", "tu": None, "den": 1998},
            {"to_chuc": "Đại học Bách Khoa Hà Nội",
             "bac": "Thạc sĩ", "nganh": "Công nghệ thông tin", "tu": None, "den": 2002},
            {"to_chuc": "Đại học Bách Khoa Hà Nội",
             "bac": "Tiến sĩ",
             "nganh": "Hệ thống thông tin - Xử lý ngôn ngữ tự nhiên, Học máy, Học sâu, Gen AI",
             "tu": None, "den": 2022},
            {"to_chuc": "Đại học Ngoại ngữ - Đại học Quốc gia Hà Nội",
             "bac": "Cử nhân", "nganh": "Tiếng Anh (Văn bằng 2)", "tu": None, "den": 2013},
            {"to_chuc": "Trường Cán bộ quản lý giáo dục TP.HCM",
             "bac": "Trung cấp", "nganh": "Lý luận chính trị - hành chính", "tu": None, "den": 2022},
        ],
        "cong_tac": [
            {"to_chuc": "Đại học Kinh tế Quốc dân",
             "chuc_vu": "Giảng viên, Khoa Công nghệ Thông tin",
             "tu": 1998, "den": None},
        ],
        "giang_day": [
            "Cấu trúc dữ liệu và thuật toán", "Cơ sở dữ liệu", "Trí tuệ nhân tạo",
            "Mật mã và bảo mật thông tin", "Xử lý ngôn ngữ tự nhiên",
            "Học máy, học sâu",
            "Ứng dụng trí tuệ nhân tạo (AI) trong kinh doanh và quản lý",
            "Phát hiện tri thức từ cơ sở dữ liệu",
            "Khai phá dữ liệu và học máy", "Xử lý ảnh số",
        ],
        "linh_vuc": [
            "Trí tuệ nhân tạo, Trí tuệ nhân tạo tạo sinh (Gen AI)",
            "Học máy, học sâu",
            "Xử lý ngôn ngữ tự nhiên, các mô hình ngôn ngữ lớn (LLMs)",
            "Phát hiện tri thức và khai phá dữ liệu / dữ liệu lớn (big data)",
            "Xử lý ảnh số và thị giác máy tính",
            "An toàn bảo mật thông tin và Blockchain",
        ],
        "cong_trinh": [
            {"ten": "IDGCN: A Proposed Knowledge Graph Embedding With Graph Convolution Network For Context-Aware Recommendation Systems",
             "loai": "Bài báo quốc tế (SCIE - Q1)", "nam": 2025,
             "tap_chi": "Journal of Organizational Computing and Electronic Commerce, Vol.35, Issue 2",
             "doi": "10.1080/10919392.2024.2435111", "link": ""},
            {"ten": "An Effective Deep Learning Approach for Extractive Text Summarization",
             "loai": "Bài báo quốc tế (Scopus)", "nam": 2021,
             "tap_chi": "Indian Journal of Computer Science and Engineering (IJCSE), Vol.12, No.2",
             "doi": "", "link": ""},
            {"ten": "A hybrid model using the pre-trained BERT and deep neural networks with rich feature for extractive text summarization",
             "loai": "Bài báo quốc tế", "nam": 2021,
             "tap_chi": "Journal of Computer Science and Cybernetics, Vol.37, No.2",
             "doi": "", "link": ""},
            {"ten": "AI4Bank: Một ứng dụng trí tuệ nhân tạo dựa trên tiếp cận học máy phục vụ hoạt động kinh doanh và quản lý cho các ngân hàng",
             "loai": "Bài báo trong nước", "nam": 2023,
             "tap_chi": "Kỷ yếu hội thảo Quốc gia Chuyển đổi số",
             "doi": "", "link": ""},
        ],
    },
    {
        "ten": "Phạm Thảo", "hoc_vi": "TS", "hoc_ham": "",
        "email": "thaop@neu.edu.vn", "sdt": "0966986689",
        "gioi_tinh": "Nam", "nam_sinh": 1982,
        "don_vi": "Khoa Công nghệ Thông tin", "avatar": "",
        "dao_tao": [
            {"to_chuc": "Đại học Quốc lập Trung ương Đài Loan",
             "bac": "Tiến sĩ", "nganh": "Công nghệ học tập mạng", "tu": 2019, "den": 2025},
            {"to_chuc": "Đại học Bách Khoa Hà Nội",
             "bac": "Thạc sĩ",
             "nganh": "Đảm bảo toán học cho máy tính và các hệ thống tính toán",
             "tu": 2006, "den": 2008},
            {"to_chuc": "Đại học Bách Khoa Hà Nội",
             "bac": "Kỹ sư", "nganh": "Tin quản lý", "tu": 2000, "den": 2005},
        ],
        "cong_tac": [
            {"to_chuc": "Đại học Kinh tế Quốc dân",
             "chuc_vu": "Phụ trách phòng thí nghiệm Đổi mới và phát triển Công nghệ giáo dục (Edtech Lab)",
             "tu": 2024, "den": None},
            {"to_chuc": "Đại học Kinh tế Quốc dân",
             "chuc_vu": "Quyền Trưởng bộ môn Công nghệ thông tin, Viện CNTT và Kinh tế",
             "tu": 2014, "den": 2019},
            {"to_chuc": "Đại học Kinh tế Quốc dân",
             "chuc_vu": "Giảng viên, Khoa Công nghệ Thông tin",
             "tu": 2008, "den": None},
        ],
        "giang_day": [
            "Cơ sở lập trình", "Thiết kế và lập trình Web", "Lập trình web",
            "Lập trình ứng dụng .NET",
            "Ứng dụng trí tuệ nhân tạo trong kinh doanh và quản lý",
            "Quản lý dự án công nghệ thông tin",
            "Công nghệ phần mềm", "Phân tích và thiết kế thuật toán",
        ],
        "linh_vuc": [
            "Phân tích học tập", "Công nghệ giáo dục",
            "Công nghệ đeo eye-tracking", "Kỹ nghệ phần mềm",
            "Công nghệ Web", "Phát triển phần mềm ứng dụng",
        ],
        "cong_trinh": [
            {"ten": "Investigation of the influences of instructors and different media on learning attention with a wearable eye-tracking system in the physical classrooms",
             "loai": "Bài báo quốc tế", "nam": 2024,
             "tap_chi": "Journal of Computer Assisted Learning, 1-18",
             "doi": "10.1111/jcal.13023", "link": "https://doi.org/10.1111/jcal.13023"},
            {"ten": "Enhancing educational evaluation through predictive student assessment modeling",
             "loai": "Bài báo quốc tế", "nam": 2024,
             "tap_chi": "Computers and Education: Artificial Intelligence, Volume 6, 100244",
             "doi": "10.1016/j.caeai.2024.100244", "link": ""},
            {"ten": "Self-experienced storytelling in an authentic context to facilitate EFL writing",
             "loai": "Bài báo quốc tế", "nam": 2022,
             "tap_chi": "Computer Assisted Language Learning, 35(4), 666-695",
             "doi": "", "link": ""},
            {"ten": "Chatbot as an intelligent personal assistant for mobile language learning",
             "loai": "Bài báo quốc tế", "nam": 2018,
             "tap_chi": "Proceedings of the 2018 2nd International Conference on Education and E-Learning",
             "doi": "", "link": ""},
        ],
    },
    {
        "ten": "Tống Thị Hảo Tâm", "hoc_vi": "TS", "hoc_ham": "",
        "email": "tamtth@neu.edu.vn", "sdt": "0913520505",
        "gioi_tinh": "Nữ", "nam_sinh": 1975,
        "don_vi": "Khoa Công nghệ Thông tin", "avatar": "",
        "dao_tao": [
            {"to_chuc": "Đại học Sư phạm Hà Nội",
             "bac": "Đại học", "nganh": "Sư phạm", "tu": None, "den": None},
            {"to_chuc": "Đại học Ngoại ngữ - Đại học Quốc gia Hà Nội",
             "bac": "Đại học", "nganh": "Ngoại ngữ", "tu": None, "den": None},
            {"to_chuc": "Đại học Bách Khoa Hà Nội",
             "bac": "Thạc sĩ", "nganh": "Công nghệ thông tin", "tu": None, "den": None},
            {"to_chuc": "Đại học Bách Khoa Hà Nội",
             "bac": "Tiến sĩ", "nganh": "Công nghệ thông tin", "tu": None, "den": None},
        ],
        "cong_tac": [
            {"to_chuc": "Đại học Kinh tế Quốc dân",
             "chuc_vu": "Giảng viên, Khoa Công nghệ Thông tin",
             "tu": 2000, "den": None},
        ],
        "giang_day": [
            "Vật lý đại cương", "Vật lý môi trường", "Quản lý công nghệ",
            "Kỹ thuật số", "Nhập môn Công nghệ thông tin", "Cơ sở lập trình",
        ],
        "linh_vuc": [
            "Khoa học vật liệu",
            "Công nghệ thông tin",
            "Vật liệu quang học, quang điện tử và quang tử",
        ],
        "cong_trinh": [
            {"ten": "Promising deep-red emitting Cr3+-doped SrAl12O19 phosphors for plant growth LEDs",
             "loai": "Bài báo quốc tế (SCIE)", "nam": 2024,
             "tap_chi": "Journal of Luminescence, 39(8)",
             "doi": "", "link": ""},
            {"ten": "Excellent visible light photocatalytic degradation and mechanism insight of Co2+-doped ZnO nanoparticles",
             "loai": "Bài báo quốc tế (SCIE)", "nam": 2022,
             "tap_chi": "Applied Physics A 128, Article number: 24",
             "doi": "", "link": ""},
            {"ten": "Co-precipitation synthesis and optical properties of green-emitting Ba2MgSi2O7:Eu2+ phosphor",
             "loai": "Bài báo quốc tế (SCIE)", "nam": 2014,
             "tap_chi": "Journal of Luminescence, 147, pp.358-362",
             "doi": "", "link": ""},
            {"ten": "Ứng dụng công nghệ thông tin mô phỏng các thí nghiệm áp dụng trong giảng dạy vật lý",
             "loai": "Bài báo trong nước", "nam": 2016,
             "tap_chi": "Kỷ yếu Hội thảo khoa học Quốc gia, ĐH Kinh tế Quốc dân",
             "doi": "", "link": ""},
        ],
    },
    {
        "ten": "Cao Thị Thu Hương", "hoc_vi": "ThS", "hoc_ham": "",
        "email": "huongct@neu.edu.vn", "sdt": "0912916316",
        "gioi_tinh": "Nữ", "nam_sinh": 1981,
        "don_vi": "Khoa Công nghệ Thông tin", "avatar": "",
        "dao_tao": [
            {"to_chuc": "Đại học Ngoại ngữ - Đại học Quốc gia Hà Nội",
             "bac": "Cử nhân", "nganh": "Tiếng Anh (Văn bằng 2)", "tu": 2014, "den": 2017},
            {"to_chuc": "Đại học Bách Khoa Hà Nội",
             "bac": "Thạc sĩ", "nganh": "Công nghệ thông tin", "tu": 2004, "den": 2006},
            {"to_chuc": "Đại học Bách Khoa Hà Nội",
             "bac": "Kỹ sư", "nganh": "Công nghệ thông tin", "tu": 1999, "den": 2004},
        ],
        "cong_tac": [
            {"to_chuc": "Đại học Kinh tế Quốc dân",
             "chuc_vu": "Giảng viên, Khoa Công nghệ Thông tin",
             "tu": 2006, "den": None},
        ],
        "giang_day": [
            "Nhập môn CNTT", "Cơ sở lập trình", "Kỹ thuật số",
            "Mạng máy tính và truyền số liệu", "Quản trị mạng",
            "Thiết kế Web", "Lập trình Python",
        ],
        "linh_vuc": [
            "Học máy",
            "Xử lý ngôn ngữ tự nhiên",
        ],
        "cong_trinh": [
            {"ten": "Ứng dụng Cloud Computing trong giáo dục đại học",
             "loai": "Bài báo trong nước", "nam": 2016,
             "tap_chi": "Hội thảo Khoa học Quốc gia: Đào tạo, nghiên cứu và ứng dụng CNTT",
             "doi": "", "link": ""},
            {"ten": "Ứng dụng các thuật toán phân loại để phân tích và ra quyết định đầu tư trên thị trường chứng khoán",
             "loai": "Bài báo trong nước", "nam": 2016,
             "tap_chi": "Hội thảo Khoa học Quốc gia: Đào tạo, nghiên cứu và ứng dụng CNTT",
             "doi": "", "link": ""},
        ],
    },
]
# seed dữ liệu thực tế
def seed():
    with app.app_context():
        print("Bắt đầu seed dữ liệu thực tế...\n")
        print("Tạo tổ chức...")
        tc_map = {}
        for d in TO_CHUC_DATA:
            obj = ToChuc.query.filter_by(ten_to_chuc=d["ten_to_chuc"]).first()
            if not obj:
                obj = ToChuc(**d)
                db.session.add(obj)
                db.session.flush()
                print(f"  ✅ {obj.ten_to_chuc}")
            tc_map[d["ten_to_chuc"]] = obj
        db.session.commit()

        # Đơn vị
        print("\nTạo đơn vị...")
        dv_map = {}
        for d in DON_VI_DATA:
            obj = DonVi.query.filter_by(ten_don_vi=d["ten_don_vi"]).first()
            if not obj:
                tc = tc_map[d["ten_to_chuc"]]
                obj = DonVi(ten_don_vi=d["ten_don_vi"], id_to_chuc=tc.id_to_chuc)
                db.session.add(obj)
                db.session.flush()
                print(f"  ✅ {obj.ten_don_vi}")
            dv_map[d["ten_don_vi"]] = obj
        db.session.commit()

        # Cán bộ + chi tiết
        print("\nTạo cán bộ giảng viên...")
        for cb_data in CAN_BO_DATA:
            if CanBo.query.filter_by(email=cb_data["email"]).first():
                print(f"  ⏭️  Đã có: {cb_data['ten']}")
                continue

            dv   = dv_map[cb_data["don_vi"]]
            slug = slugify(f"{cb_data['hoc_vi']} {cb_data['ten']}")

            cb = CanBo(
                id_don_vi = dv.id_don_vi,
                ten       = cb_data["ten"],
                email     = cb_data["email"],
                sdt       = cb_data["sdt"],
                hoc_vi    = cb_data["hoc_vi"],
                hoc_ham   = cb_data["hoc_ham"],
                gioi_tinh = cb_data["gioi_tinh"],
                nam_sinh  = cb_data["nam_sinh"],
                avatar    = cb_data.get("avatar", ""),
                slug      = slug,
            )
            db.session.add(cb)
            db.session.flush()

            for dt in cb_data["dao_tao"]:
                tc = tc_map.get(dt["to_chuc"])
                if tc:
                    db.session.add(QuaTrinhDaoTao(
                        id_can_bo    = cb.id_can_bo,
                        id_to_chuc   = tc.id_to_chuc,
                        bac_dao_tao  = dt["bac"],
                        chuyen_nganh = dt["nganh"],
                        nam_bat_dau  = dt["tu"],
                        nam_ket_thuc = dt["den"],
                    ))

            for ct in cb_data["cong_tac"]:
                tc = tc_map.get(ct["to_chuc"])
                if tc:
                    db.session.add(QuaTrinhCongTac(
                        id_can_bo  = cb.id_can_bo,
                        id_to_chuc = tc.id_to_chuc,
                        chuc_vu    = ct["chuc_vu"],
                        tu_nam     = ct["tu"],
                        den_nam    = ct["den"],
                    ))

            for mon in cb_data["giang_day"]:
                db.session.add(GiangDay(id_can_bo=cb.id_can_bo, ten_mon=mon))

            for lv in cb_data["linh_vuc"]:
                db.session.add(LinhVucNghienCuu(
                    id_can_bo=cb.id_can_bo, ten_linh_vuc=lv))

            for ct in cb_data["cong_trinh"]:
                db.session.add(CongTrinhNghienCuu(
                    id_can_bo       = cb.id_can_bo,
                    ten_cong_trinh  = ct["ten"],
                    loai_cong_trinh = ct["loai"],
                    nam_cong_bo     = ct["nam"],
                    tap_chi         = ct.get("tap_chi", ""),
                    doi             = ct.get("doi", ""),
                    link            = ct.get("link", ""),
                ))

            print(f"  ✅ {cb_data['hoc_vi']} {cb_data['ten']} ({cb_data['email']})")

        db.session.commit()

        # Tài khoản admin
        print("\nTạo tài khoản admin...")
        if not TaiKhoan.query.filter_by(username="admin").first():
            admin_cb = CanBo.query.first()
            if admin_cb:
                db.session.add(TaiKhoan(
                    id_can_bo = admin_cb.id_can_bo,
                    username  = "admin",
                    mat_khau  = generate_password_hash("Admin@123"),
                    vai_tro   = "admin",
                ))
                db.session.commit()
                print("Tài khoản: admin / Admin@123")
        else:
            print("  Đã có tài khoản admin")

        print(f"\nSeed hoàn thành!")
        print(f"   - {len(TO_CHUC_DATA)} tổ chức")
        print(f"   - {len(DON_VI_DATA)} đơn vị")
        print(f"   - {len(CAN_BO_DATA)} giảng viên với đầy đủ thông tin")


if __name__ == "__main__":
    seed()