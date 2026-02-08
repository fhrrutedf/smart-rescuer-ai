import axios from 'axios';

// Auto-detect API URL based on environment
const API_BASE_URL = import.meta.env.VITE_API_URL ||
    (window.location.hostname === 'localhost'
        ? 'http://localhost:8000'
        : `${window.location.protocol}//${window.location.host}`);

const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json'
    },
    timeout: 180000 // 3 minutes timeout for AI processing
});

export const apiService = {
    // System status
    getStatus: () => api.get('/api/status'),

    // Emergency assessment
    assessEmergency: (data, imageFile) => {
        const formData = new FormData();
        formData.append('patient_conscious', data.patient_conscious);
        if (imageFile) {
            formData.append('image', imageFile);
        }
        return api.post('/api/emergency/assess', formData, {
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        });
    },

    // Chatbot
    sendChatMessage: (message, resetHistory = false) =>
        api.post('/api/chat', { message, reset_history: resetHistory }),

    // Sensors
    calibrateSensors: () => api.post('/api/sensors/calibrate'),
    getVitalSigns: () => api.get('/api/sensors/vitals'),
    getLocation: () => api.get('/api/location'),

    // Live Stream - Real-time monitoring
    getLiveStream: () => api.get('/api/live/stream'),

    // Download PDF Report
    downloadReport: async (data) => {
        const response = await api.post('/api/emergency/download-report', data, {
            responseType: 'blob'
        });

        // Create blob link to download
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', `medical_report_${new Date().getTime()}.pdf`);
        document.body.appendChild(link);
        link.click();
        link.parentNode.removeChild(link);

        return response;
    }
};

export default api;
