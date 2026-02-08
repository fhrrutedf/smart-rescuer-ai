import { useState, useEffect, useRef } from 'react';
import { apiService } from '../services/api';
import './LiveStream.css';

export default function LiveStream() {
    const [isStreaming, setIsStreaming] = useState(false);
    const [liveData, setLiveData] = useState(null);
    const [alerts, setAlerts] = useState([]);
    const intervalRef = useRef(null);

    const startStream = () => {
        setIsStreaming(true);
        fetchLiveData(); // First fetch

        // Fetch every 2 seconds
        intervalRef.current = setInterval(fetchLiveData, 2000);
    };

    const stopStream = () => {
        setIsStreaming(false);
        if (intervalRef.current) {
            clearInterval(intervalRef.current);
        }
    };

    const fetchLiveData = async () => {
        try {
            const response = await apiService.getLiveStream();
            setLiveData(response.data);

            // Add new alerts to the list
            if (response.data.instant_alerts && response.data.instant_alerts.length > 0) {
                setAlerts(prev => [
                    ...response.data.instant_alerts.map(alert => ({
                        ...alert,
                        timestamp: new Date().toLocaleTimeString()
                    })),
                    ...prev
                ].slice(0, 10)); // Keep last 10 alerts
            }
        } catch (error) {
            console.error('Live stream error:', error);
        }
    };

    useEffect(() => {
        return () => {
            if (intervalRef.current) {
                clearInterval(intervalRef.current);
            }
        };
    }, []);

    const getSeverityColor = (level) => {
        const colors = {
            'critical': '#e74c3c',
            'severe': '#e67e22',
            'moderate': '#f39c12',
            'mild': '#27ae60',
            'minimal': '#2ecc71'
        };
        return colors[level] || '#95a5a6';
    };

    const getAlertColor = (type) => {
        return type === 'critical' ? '#e74c3c' : '#f39c12';
    };

    return (
        <div className="live-stream-container">
            <div className="header">
                <h1>🔴 البث المباشر - Live Monitoring</h1>
                <p>تحليل فوري للعلامات الحيوية</p>
            </div>

            <div className="controls">
                {!isStreaming ? (
                    <button className="btn-start" onClick={startStream}>
                        ▶️ بدء البث المباشر
                    </button>
                ) : (
                    <button className="btn-stop" onClick={stopStream}>
                        ⏸️ إيقاف البث
                    </button>
                )}
            </div>

            {isStreaming && liveData && (
                <div className="stream-content">
                    {/* Status Indicator */}
                    <div className="status-bar">
                        <div className="live-indicator">
                            <span className="pulse"></span>
                            <span>LIVE</span>
                        </div>
                        <div className="timestamp">
                            {new Date(liveData.timestamp).toLocaleTimeString('ar-IQ')}
                        </div>
                    </div>

                    {/* Instant Alerts */}
                    {liveData.instant_alerts && liveData.instant_alerts.length > 0 && (
                        <div className="alerts-section">
                            <h3>⚠️ تنبيهات فورية</h3>
                            <div className="alerts-grid">
                                {liveData.instant_alerts.map((alert, idx) => (
                                    <div
                                        key={idx}
                                        className="alert-card"
                                        style={{ borderLeft: `4px solid ${getAlertColor(alert.type)}` }}
                                    >
                                        <div className="alert-icon">
                                            {alert.type === 'critical' ? '🚨' : '⚠️'}
                                        </div>
                                        <div className="alert-content">
                                            <div className="alert-message">{alert.message}</div>
                                            <div className="alert-value">القيمة: {alert.value}</div>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>
                    )}

                    {/* Vital Signs Cards */}
                    <div className="vitals-grid">
                        {/* Heart Rate */}
                        <div className="vital-card">
                            <div className="vital-icon">❤️</div>
                            <div className="vital-label">معدل القلب</div>
                            <div className="vital-value">
                                {liveData.vital_signs?.heart_rate || '--'}
                            </div>
                            <div className="vital-unit">bpm</div>
                        </div>

                        {/* SpO2 */}
                        <div className="vital-card">
                            <div className="vital-icon">💨</div>
                            <div className="vital-label">نسبة الأكسجين</div>
                            <div className="vital-value">
                                {liveData.vital_signs?.spo2 || '--'}
                            </div>
                            <div className="vital-unit">%</div>
                        </div>

                        {/* Temperature */}
                        <div className="vital-card">
                            <div className="vital-icon">🌡️</div>
                            <div className="vital-label">درجة الحرارة</div>
                            <div className="vital-value">
                                {liveData.vital_signs?.body_temperature || '--'}
                            </div>
                            <div className="vital-unit">°C</div>
                        </div>

                        {/* ECG Rhythm */}
                        <div className="vital-card">
                            <div className="vital-icon">📊</div>
                            <div className="vital-label">نمط القلب</div>
                            <div className="vital-value-text">
                                {liveData.vital_signs?.rhythm || 'Normal'}
                            </div>
                        </div>
                    </div>

                    {/* Severity Score */}
                    <div className="severity-section">
                        <h3>مستوى الخطورة</h3>
                        <div
                            className="severity-bar"
                            style={{
                                background: `linear-gradient(to right, ${getSeverityColor(liveData.severity?.severity_level)} ${(liveData.severity?.total_score || 0) * 10}%, #ecf0f1 ${(liveData.severity?.total_score || 0) * 10}%)`
                            }}
                        >
                            <div className="severity-score">
                                {(liveData.severity?.total_score || 0).toFixed(1)} / 10
                            </div>
                        </div>
                        <div
                            className="severity-label"
                            style={{ color: getSeverityColor(liveData.severity?.severity_level) }}
                        >
                            {liveData.severity?.severity_level?.toUpperCase() || 'NORMAL'}
                        </div>
                    </div>

                    {/* GPS Location */}
                    {liveData.location && (
                        <div className="location-section">
                            <h3>📍 الموقع الجغرافي</h3>
                            <div className="location-info">
                                <div>
                                    خط العرض: {liveData.location.latitude?.toFixed(6) || 'N/A'}
                                </div>
                                <div>
                                    خط الطول: {liveData.location.longitude?.toFixed(6) || 'N/A'}
                                </div>
                                {liveData.location.latitude && liveData.location.longitude && (
                                    <a
                                        href={`https://www.google.com/maps?q=${liveData.location.latitude},${liveData.location.longitude}`}
                                        target="_blank"
                                        rel="noopener noreferrer"
                                        className="maps-link"
                                    >
                                        📍 افتح في خرائط Google
                                    </a>
                                )}
                            </div>
                        </div>
                    )}

                    {/* Alerts History */}
                    {alerts.length > 0 && (
                        <div className="history-section">
                            <h3>📜 سجل التنبيهات</h3>
                            <div className="alerts-history">
                                {alerts.map((alert, idx) => (
                                    <div key={idx} className="history-item">
                                        <span className="history-time">{alert.timestamp}</span>
                                        <span className="history-message">{alert.message}</span>
                                        <span className="history-value">{alert.value}</span>
                                    </div>
                                ))}
                            </div>
                        </div>
                    )}
                </div>
            )}

            {!isStreaming && (
                <div className="placeholder">
                    <div className="placeholder-icon">📡</div>
                    <p>اضغط "بدء البث المباشر" لمراقبة العلامات الحيوية بشكل فوري</p>
                </div>
            )}
        </div>
    );
}
