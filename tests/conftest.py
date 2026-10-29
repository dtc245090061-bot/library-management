"""
conftest.py - Shared test fixtures và configuration
Chạy từ thư mục gốc: pytest tests/ -v
"""
import pytest
import os
import sys

# Thêm backend vào Python path để import được
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))


def pytest_configure(config):
    """Cấu hình pytest"""
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )
    config.addinivalue_line(
        "markers", "ai: mark test as AI feature test"
    )
    config.addinivalue_line(
        "markers", "borrow: mark test as borrow/return test"
    )


def pytest_collection_modifyitems(items):
    """Tự động thêm marker dựa trên tên file test"""
    for item in items:
        if "test_ai" in item.nodeid:
            item.add_marker(pytest.mark.ai)
        if "test_borrow" in item.nodeid:
            item.add_marker(pytest.mark.borrow)


@pytest.fixture(autouse=True, scope="session")
def configure_test_ai_environment():
    """Tự động kích hoạt smart local mock AI trong test suite để test chạy siêu tốc (<5s) và không phụ thuộc mạng"""
    from services.ai_service import ai_service
    original_mock = ai_service.is_mock
    ai_service.is_mock = True
    yield
    ai_service.is_mock = original_mock

