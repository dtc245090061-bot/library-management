/**
 * API Client - Giao tiếp với FastAPI backend
 */

const API_BASE = '';  // Same origin

const api = {
    /**
     * Lấy token từ localStorage
     */
    getToken() {
        return localStorage.getItem('access_token');
    },

    /**
     * Headers mặc định
     */
    getHeaders(includeAuth = true) {
        const headers = { 'Content-Type': 'application/json' };
        if (includeAuth) {
            const token = this.getToken();
            if (token) headers['Authorization'] = `Bearer ${token}`;
        }
        return headers;
    },

    /**
     * Thực hiện HTTP request
     */
    async request(method, url, data = null, formData = false) {
        const options = {
            method,
            headers: formData ? { 'Authorization': `Bearer ${this.getToken()}` } : this.getHeaders()
        };

        if (data) {
            options.body = formData ? data : JSON.stringify(data);
        }

        try {
            const res = await fetch(`${API_BASE}${url}`, options);

            // Redirect to login if unauthorized
            if (res.status === 401) {
                localStorage.removeItem('access_token');
                localStorage.removeItem('user_info');
                window.location.href = '/login';
                return null;
            }

            const json = await res.json().catch(() => null);

            if (!res.ok) {
                const msg = json?.detail || `Lỗi ${res.status}`;
                throw new Error(msg);
            }

            return json;
        } catch (err) {
            if (err.name === 'TypeError') {
                throw new Error('Không thể kết nối đến server. Kiểm tra kết nối mạng.');
            }
            throw err;
        }
    },

    get: (url) => api.request('GET', url),
    post: (url, data) => api.request('POST', url, data),
    put: (url, data) => api.request('PUT', url, data),
    delete: (url) => api.request('DELETE', url),

    // Form data (login)
    async postForm(url, formData) {
        const res = await fetch(`${API_BASE}${url}`, {
            method: 'POST',
            body: formData
        });
        const json = await res.json().catch(() => null);
        if (!res.ok) throw new Error(json?.detail || 'Đăng nhập thất bại');
        return json;
    }
};

// ===== Auth API =====
const authAPI = {
    async login(username, password) {
        const formData = new FormData();
        formData.append('username', username);
        formData.append('password', password);
        return api.postForm('/api/auth/login', formData);
    },
    getMe: () => api.get('/api/auth/me'),
};

// ===== Books API =====
const booksAPI = {
    list: (params = {}) => api.get(`/api/books/?${new URLSearchParams(params)}`),
    get: (id) => api.get(`/api/books/${id}`),
    create: (data) => api.post('/api/books/', data),
    update: (id, data) => api.put(`/api/books/${id}`, data),
    delete: (id) => api.delete(`/api/books/${id}`),
    listCategories: () => api.get('/api/categories/'),
    createCategory: (data) => api.post('/api/categories/', data),
    listAuthors: () => api.get('/api/authors/'),
    createAuthor: (data) => api.post('/api/authors/', data),
    exportCSV: (params = {}) => {
        const token = api.getToken();
        const url = `/api/books/export/csv?${new URLSearchParams(params)}`;
        const a = document.createElement('a');
        a.href = url;
        // Thêm token vào header không được với href, dùng fetch
        fetch(url, { headers: { 'Authorization': `Bearer ${token}` } })
            .then(r => r.blob())
            .then(blob => {
                const blobUrl = URL.createObjectURL(blob);
                a.href = blobUrl;
                a.download = 'danh_sach_sach.csv';
                a.click();
                URL.revokeObjectURL(blobUrl);
            });
    },
};

// ===== Readers API =====
const readersAPI = {
    list: (params = {}) => api.get(`/api/readers/?${new URLSearchParams(params)}`),
    get: (id) => api.get(`/api/readers/${id}`),
    getMe: () => api.get('/api/readers/me'),
    getNextCode: () => api.get('/api/readers/next-code'),
    getAvailableUsers: () => api.get('/api/readers/available-users'),
    create: (data) => api.post('/api/readers/', data),
    update: (id, data) => api.put(`/api/readers/${id}`, data),
};

// ===== Borrows API =====
const borrowsAPI = {
    list: (params = {}) => api.get(`/api/borrows/?${new URLSearchParams(params)}`),
    get: (id) => api.get(`/api/borrows/${id}`),
    create: (data) => api.post('/api/borrows/', data),
    return: (id, data = {}) => api.put(`/api/borrows/${id}/return`, data),
    renew: (id, data = {}) => api.put(`/api/borrows/${id}/renew`, data),
    getOverdue: (params = {}) => api.get(`/api/borrows/overdue?${new URLSearchParams(params)}`),
    exportCSV: (params = {}) => {
        const token = api.getToken();
        const url = `/api/borrows/export/csv?${new URLSearchParams(params)}`;
        fetch(url, { headers: { 'Authorization': `Bearer ${token}` } })
            .then(r => r.blob())
            .then(blob => {
                const blobUrl = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = blobUrl;
                a.download = 'phieu_muon.csv';
                a.click();
                URL.revokeObjectURL(blobUrl);
            });
    },
};

// ===== Fines API =====
const finesAPI = {
    list: (params = {}) => api.get(`/api/fines/?${new URLSearchParams(params)}`),
    update: (id, data) => api.put(`/api/fines/${id}`, data),
};

// ===== Reservations API =====
const reservationsAPI = {
    list: (params = {}) => api.get(`/api/reservations/?${new URLSearchParams(params)}`),
    create: (data) => api.post('/api/reservations/', data),
    cancel: (id) => api.put(`/api/reservations/${id}/cancel`, {}),
};

// ===== Statistics API =====
const statsAPI = {
    dashboard: () => api.get('/api/statistics/dashboard'),
    topBooks: () => api.get('/api/statistics/top-borrowed-books'),
    topReaders: () => api.get('/api/statistics/top-active-readers'),
    monthlyBorrows: () => api.get('/api/statistics/monthly-borrows'),
    categoryDist: () => api.get('/api/statistics/category-distribution'),
    overdueSummary: () => api.get('/api/statistics/overdue-summary'),
    exportCSV: () => {
        const token = api.getToken();
        const url = '/api/statistics/export/csv';
        fetch(url, { headers: { 'Authorization': `Bearer ${token}` } })
            .then(r => r.blob())
            .then(blob => {
                const blobUrl = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = blobUrl;
                a.download = `bao_cao_thu_vien_${new Date().toISOString().slice(0,10)}.csv`;
                a.click();
                URL.revokeObjectURL(blobUrl);
            });
    },
};

// ===== AI API =====
const aiAPI = {
    search: (query) => api.post('/api/ai/search', { query }),
    summarize: (bookId) => api.post(`/api/ai/summarize/${bookId}`, {}),
    suggest: () => api.get('/api/ai/suggest'),
    status: () => api.get('/api/ai/status'),
};

// ===== Users API (Admin) =====
const usersAPI = {
    list: (params = {}) => api.get(`/api/auth/users?${new URLSearchParams(params)}`),
    create: (data) => api.post('/api/auth/users', data),
    update: (id, data) => api.put(`/api/auth/users/${id}`, data),
    toggleActive: (id) => api.post(`/api/auth/users/${id}/toggle-active`, {}),
};

// ===== Utility: User info =====
function getCurrentUser() {
    try {
        return JSON.parse(localStorage.getItem('user_info') || 'null');
    } catch { return null; }
}

function isLoggedIn() {
    return !!localStorage.getItem('access_token');
}

function logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user_info');
    window.location.href = '/login';
}

function requireAuth() {
    if (!isLoggedIn()) {
        window.location.href = '/login';
        return false;
    }
    return true;
}

function hasRole(...roles) {
    const user = getCurrentUser();
    return user && roles.includes(user.role);
}
