from flask import Blueprint, redirect, url_for, request, render_template, session
from . import db
from .models import DonVi, CanBo, QuaTrinhDaoTao, QuaTrinhCongTac, GiangDay, LinhVucNghienCuu, CongTrinhNghienCuu

user_bp = Blueprint('user', __name__)

# 1. Trang chủ
@user_bp.route('/')
def User():
    if 'user_id' not in session:
        return redirect(url_for('auth_bp.login'))
    return render_template('home.html')

# 2. Click vào khoa trên Navbar (chuyển hướng sang trang danh sách)
@user_bp.route('/department/<int:id>')
def department(id):
    if 'user_id' not in session:
        return redirect(url_for('auth_bp.login'))
    # Chuyển thẳng sang trang danh sách và lọc luôn theo ID khoa
    return redirect(url_for('user.lecturer_list', don_vi=id))

# 3. Trang danh sách và tìm kiếm giảng viên (Map với lecturer_list.html)
@user_bp.route('/lecturer')
def lecturer_list():
    if 'user_id' not in session:
        return redirect(url_for('auth_bp.login'))

    # Lấy các từ khóa người dùng nhập vào thanh tìm kiếm
    q = request.args.get('q', '')
    don_vi_id = request.args.get('don_vi', '')
    hoc_vi = request.args.get('hoc_vi', '')
    page = request.args.get('page', 1, type=int)

    # Query cơ bản từ bảng Cán Bộ
    query = CanBo.query

    # Nếu có gõ tìm kiếm thì lọc
    if q:
        query = query.filter(CanBo.ten.ilike(f'%{q}%') | CanBo.email.ilike(f'%{q}%'))
    if don_vi_id:
        query = query.filter(CanBo.id_don_vi == don_vi_id)
    if hoc_vi:
        query = query.filter(CanBo.hoc_vi == hoc_vi)

    # Phân trang (hiển thị 6 người 1 trang)
    pagination = query.paginate(page=page, per_page=6, error_out=False)
    can_bos = pagination.items

    # Lấy danh sách để đổ vào cái Dropdown tìm kiếm
    don_vis = DonVi.query.all()
    # Lấy danh sách các học vị không bị trùng lặp
    hoc_vis = db.session.query(CanBo.hoc_vi).distinct().filter(CanBo.hoc_vi != '').all()
    hoc_vis = [h[0] for h in hoc_vis]

    return render_template('lecturer_list.html',
                           can_bos=can_bos,
                           pagination=pagination,
                           don_vis=don_vis,
                           hoc_vis=hoc_vis,
                           q=q,
                           sel_don_vi=don_vi_id,
                           sel_hoc_vi=hoc_vi)

# 4. Trang xem chi tiết 1 ông giảng viên (Map với lecturer_detail.html)
@user_bp.route('/lecturer/<slug>')
def lecturer_detail(slug):
    if 'user_id' not in session:
        return redirect(url_for('auth_bp.login'))

    # Tìm ông giảng viên đó, không có thì báo lỗi 404
    can_bo = CanBo.query.filter_by(slug=slug).first_or_404()

    # Nhặt tất cả "đồ đạc" của ông ý trong Database ra
    dao_taos = QuaTrinhDaoTao.query.filter_by(id_can_bo=can_bo.id_can_bo).all()
    cong_tacs = QuaTrinhCongTac.query.filter_by(id_can_bo=can_bo.id_can_bo).all()
    giang_days = GiangDay.query.filter_by(id_can_bo=can_bo.id_can_bo).all()
    linh_vucs = LinhVucNghienCuu.query.filter_by(id_can_bo=can_bo.id_can_bo).all()
    cong_trinhs = CongTrinhNghienCuu.query.filter_by(id_can_bo=can_bo.id_can_bo).all()

    return render_template('lecturer_detail.html',
                           can_bo=can_bo,
                           dao_taos=dao_taos,
                           cong_tacs=cong_tacs,
                           giang_days=giang_days,
                           linh_vucs=linh_vucs,
                           cong_trinhs=cong_trinhs)