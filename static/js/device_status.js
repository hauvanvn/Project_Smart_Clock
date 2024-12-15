// Kết nối WebSocket
const socket = new WebSocket('ws://127.0.0.1:8000/ws/mqtt/front-end');

// Khi kết nối thành công
socket.onopen = function () {
    console.log("WebSocket connection established.");
};

// Khi nhận được tin nhắn từ server
socket.onmessage = function (event) {
    const data = JSON.parse(event.data);
    console.log("Received data:", data);

    // Hiển thị trạng thái trên giao diện
    const deviceId = data.device_id;
    const status = data.status;

    // Ví dụ: cập nhật trạng thái thiết bị trên HTML
    const statusElement = document.getElementById(`status-${deviceId}`);
    if (statusElement) {
        statusElement.textContent = status;
    }
};

// Khi WebSocket đóng
socket.onclose = function () {
    console.log("WebSocket connection closed.");
};