/**
 * UI Utilities - Toast, Modal, Loading, etc.
 */

// ===== Toast Notifications =====
const toast = {
    container: null,

    init() {
        if (!this.container) {
            this.container = document.createElement('div');
            this.container.className = 'toast-container';
            document.body.appendChild(this.container);
        }
    },

    show(message, type = 'info', duration = 4000) {
        this.init();
        const icons = { success: '✅', error: '❌', warning: '⚠️', info: 'ℹ️' };
        const el = document.createElement('div');
        el.className = `toast ${type}`;
        el.innerHTML = `
            <span class="toast-icon">${icons[type] || '📢'}</span>
            <span class="toast-msg">${message}</span>
            <span class="toast-close" onclick="this.parentElement.remove()">✕</span>
        `;
        this.container.appendChild(el);
        setTimeout(() => {
            el.style.animation = 'slideOutRight 0.3s ease forwards';
            setTimeout(() => el.remove(), 300);
        }, duration);
    },

    success: (msg) => toast.show(msg, 'success'),
    error: (msg) => toast.show(msg, 'error', 6000),
    warning: (msg) => toast.show(msg, 'warning'),
    info: (msg) => toast.show(msg, 'info'),
};

// ===== Modal =====
class Modal {
    constructor(id) {
        this.overlay = document.getElementById(id);
        this.overlay?.querySelector('.modal-close')?.addEventListener('click', () => this.hide());
        this.overlay?.addEventListener('click', (e) => { if (e.target === this.overlay) this.hide(); });
    }

    show() {
        this.overlay?.classList.add('show');
        document.body.style.overflow = 'hidden';
    }

    hide() {
        this.overlay?.classList.remove('show');
        document.body.style.overflow = '';
    }
}

// ===== Loading State =====
function setLoading(el, loading = true, text = 'Đang tải...') {
    if (!el) return;
    if (loading) {
        el._originalHTML = el.innerHTML;
        el.disabled = true;
        el.innerHTML = `<span class="loading-spinner"></span> ${text}`;
    } else {
        el.disabled = false;
        el.innerHTML = el._originalHTML || '';
    }
}

function showTableLoading(tableBody, colSpan = 6) {
    if (!tableBody) return;
    tableBody.innerHTML = `
        <tr>
            <td colspan="${colSpan}">
                <div class="loading-overlay">
                    <div class="loading-spinner" style="width:32px;height:32px;border-width:3px;"></div>
                    <span class="text-muted">Đang tải dữ liệu...</span>
                </div>
            </td>
        </tr>`;
}

function showEmptyState(tableBody, message = 'Không có dữ liệu', colSpan = 6) {
    if (!tableBody) return;
    tableBody.innerHTML = `
        <tr>
            <td colspan="${colSpan}">
                <div class="empty-state">
                    <div class="empty-icon">📭</div>
                    <div class="empty-title">${message}</div>
                </div>
            </td>
        </tr>`;
}

// ===== Format Utilities =====
const fmt = {
    date(d) {
        if (!d) return '—';
        return new Date(d).toLocaleDateString('vi-VN');
    },
    datetime(d) {
        if (!d) return '—';
        return new Date(d).toLocaleString('vi-VN');
    },
    money(n) {
        if (n == null) return '0 ₫';
        return new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(n);
    },
    number(n) {
        if (n == null) return '0';
        return new Intl.NumberFormat('vi-VN').format(n);
    }
};

// ===== Role Labels =====
const ROLE_LABELS = {
    admin: { label: 'Quản trị viên', class: 'badge-purple' },
    librarian: { label: 'Thủ thư', class: 'badge-info' },
    reader: { label: 'Độc giả', class: 'badge-success' },
};

const BORROW_STATUS_LABELS = {
    borrowing: { label: 'Đang mượn', class: 'badge-info' },
    returned: { label: 'Đã trả', class: 'badge-success' },
    overdue: { label: 'Quá hạn', class: 'badge-danger' },
    lost: { label: 'Mất sách', class: 'badge-warning' },
};

const CARD_STATUS_LABELS = {
    active: { label: 'Hoạt động', class: 'badge-success' },
    expired: { label: 'Hết hạn', class: 'badge-warning' },
    suspended: { label: 'Đình chỉ', class: 'badge-danger' },
    cancelled: { label: 'Đã hủy', class: 'badge-muted' },
};

const READER_TYPE_LABELS = {
    student: 'Sinh viên',
    teacher: 'Giảng viên',
    staff: 'Nhân viên',
    external: 'Bên ngoài',
};

const FINE_STATUS_LABELS = {
    pending: { label: 'Chưa thanh toán', class: 'badge-danger' },
    paid: { label: 'Đã thanh toán', class: 'badge-success' },
    waived: { label: 'Được miễn', class: 'badge-muted' },
};

function renderBadge(value, labelMap) {
    const info = labelMap[value] || { label: value, class: 'badge-muted' };
    return `<span class="badge ${info.class}">${info.label}</span>`;
}

// ===== Sidebar active nav =====
function setActiveNav(page) {
    document.querySelectorAll('.nav-item').forEach(el => {
        el.classList.remove('active');
        if (el.dataset.page === page) el.classList.add('active');
    });
}

// ===== Populate user info in sidebar =====
function populateSidebarUser() {
    const user = getCurrentUser();
    if (!user) return;

    const nameEl = document.getElementById('sidebar-user-name');
    const roleEl = document.getElementById('sidebar-user-role');
    const avatarEl = document.getElementById('sidebar-user-avatar');

    if (nameEl) nameEl.textContent = user.full_name;
    if (roleEl) roleEl.textContent = ROLE_LABELS[user.role]?.label || user.role;
    if (avatarEl) avatarEl.textContent = user.full_name?.charAt(0)?.toUpperCase() || '?';

    // Hide admin-only nav items for readers
    if (user.role === 'reader') {
        document.querySelectorAll('[data-admin-only]').forEach(el => el.style.display = 'none');
        document.querySelectorAll('[data-librarian-only]').forEach(el => el.style.display = 'none');
    } else if (user.role === 'librarian') {
        document.querySelectorAll('[data-admin-only]').forEach(el => el.style.display = 'none');
    }
}

// ===== Pagination =====
function renderPagination(container, current, total, pageSize, onPageChange) {
    if (!container) return;
    const totalPages = Math.ceil(total / pageSize);
    if (totalPages <= 1) { container.innerHTML = ''; return; }

    let html = `<button class="page-btn" ${current <= 1 ? 'disabled' : ''} onclick="(${onPageChange})(${current - 1})">‹</button>`;

    for (let i = 1; i <= totalPages; i++) {
        if (i === current || i === 1 || i === totalPages || Math.abs(i - current) <= 1) {
            html += `<button class="page-btn ${i === current ? 'active' : ''}" onclick="(${onPageChange})(${i})">${i}</button>`;
        } else if (Math.abs(i - current) === 2) {
            html += `<span style="color:var(--text-muted)">…</span>`;
        }
    }

    html += `<button class="page-btn" ${current >= totalPages ? 'disabled' : ''} onclick="(${onPageChange})(${current + 1})">›</button>`;
    container.innerHTML = html;
}

// ===== Confirm Dialog =====
function confirmAction(message) {
    return new Promise(resolve => {
        const overlay = document.createElement('div');
        overlay.className = 'modal-overlay show';
        overlay.innerHTML = `
            <div class="modal" style="max-width:380px">
                <div style="text-align:center;padding:8px 0">
                    <div style="font-size:2.5rem;margin-bottom:12px">⚠️</div>
                    <h3 style="margin-bottom:8px">Xác nhận</h3>
                    <p style="color:var(--text-secondary);font-size:0.9rem">${message}</p>
                </div>
                <div class="modal-footer" style="justify-content:center">
                    <button class="btn btn-outline" id="confirm-no">Hủy</button>
                    <button class="btn btn-danger" id="confirm-yes">Xác nhận</button>
                </div>
            </div>`;
        document.body.appendChild(overlay);
        overlay.querySelector('#confirm-yes').onclick = () => { overlay.remove(); resolve(true); };
        overlay.querySelector('#confirm-no').onclick = () => { overlay.remove(); resolve(false); };
    });
}

// ===== Rich Markdown-like formatter for AI responses =====
function formatAIResponse(text) {
    if (!text) return '';
    
    // Normalize newlines
    let html = text.replace(/\r\n/g, '\n');

    // Headers
    html = html.replace(/^### (.*$)/gim, '<h4 style="color:var(--primary);margin:12px 0 6px 0;font-size:0.92rem;font-weight:700;">$1</h4>');
    html = html.replace(/^## (.*$)/gim, '<h3 style="color:var(--primary);margin:14px 0 8px 0;font-size:1rem;font-weight:700;">$1</h3>');
    html = html.replace(/^# (.*$)/gim, '<h3 style="color:var(--primary);margin:14px 0 8px 0;font-size:1.05rem;font-weight:800;">$1</h3>');

    // Blockquotes (> text)
    html = html.replace(/^\> (.*$)/gim, '<blockquote style="border-left:3px solid var(--primary);background:rgba(79,70,229,0.06);margin:8px 0;padding:8px 12px;border-radius:0 6px 6px 0;font-size:0.84rem;color:var(--text-secondary);">$1</blockquote>');

    // Bold & Italic
    html = html.replace(/\*\*\*(.*?)\*\*\*/g, '<strong><em>$1</em></strong>');
    html = html.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    html = html.replace(/\*(.*?)\*/g, '<em>$1</em>');
    html = html.replace(/`([^`]+)`/g, '<code style="background:rgba(0,0,0,0.06);padding:2px 5px;border-radius:4px;font-family:monospace;font-size:0.85em;color:var(--primary);">$1</code>');

    // Horizontal Rule
    html = html.replace(/^---$/gim, '<hr style="border:none;border-top:1px solid var(--border);margin:12px 0;">');

    // Bullet points (* or -)
    html = html.replace(/^\s*[\-\*]\s+(.*)$/gim, '<li style="margin-bottom:4px;">$1</li>');
    // Wrap adjacent <li> in <ul>
    html = html.replace(/(<li style="margin-bottom:4px;">.*<\/li>\n?)+/g, '<ul style="margin:6px 0 8px 18px;line-height:1.6;">$&</ul>');

    // Numbered lists (1. 2. 3.)
    html = html.replace(/^\s*\d+\.\s+(.*)$/gim, '<li style="margin-bottom:4px;list-style-type:decimal;">$1</li>');

    // Line breaks (convert remaining newlines to <br> if not inside block tags)
    html = html.replace(/\n\n/g, '<div style="height:8px;"></div>');
    html = html.replace(/\n/g, '<br>');

    return html;
}
