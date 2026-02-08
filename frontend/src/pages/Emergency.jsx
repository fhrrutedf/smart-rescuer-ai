import React, { useState } from 'react';
import {
    Container,
    Box,
    Typography,
    Button,
    Paper,
    CircularProgress,
    Alert,
    Chip,
    Grid,
    Card,
    CardContent
} from '@mui/material';
import {
    LocalHospital as EmergencyIcon,
    CameraAlt as CameraIcon,
    Send as SendIcon,
    Videocam as VideoIcon
} from '@mui/icons-material';
import { apiService } from '../services/api';

function Emergency() {
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState(null);
    const [imageFile, setImageFile] = useState(null);
    const [imagePreview, setImagePreview] = useState(null);
    const [error, setError] = useState(null);
    const [downloadLoading, setDownloadLoading] = useState(false);
    const [loadingMessage, setLoadingMessage] = useState('جاري التقييم...');

    // Camera states
    const [isCameraOpen, setIsCameraOpen] = useState(false);
    const [stream, setStream] = useState(null);
    const videoRef = React.useRef(null);
    const canvasRef = React.useRef(null);

    // Live monitoring
    const [isLiveMonitoring, setIsLiveMonitoring] = useState(false);
    const [liveResults, setLiveResults] = useState(null);
    const monitoringIntervalRef = React.useRef(null);

    // Open camera
    const openCamera = async () => {
        try {
            const mediaStream = await navigator.mediaDevices.getUserMedia({
                video: { facingMode: 'environment' }
            });
            setStream(mediaStream);
            setIsCameraOpen(true);

            setTimeout(() => {
                if (videoRef.current) {
                    videoRef.current.srcObject = mediaStream;
                }
            }, 100);
        } catch (err) {
            setError('لا يمكن الوصول للكاميرا. تأكد من السماح بالوصول.');
            console.error('Camera error:', err);
        }
    };

    // Close camera
    const closeCamera = () => {
        stopLiveMonitoring();
        if (stream) {
            stream.getTracks().forEach(track => track.stop());
        }
        setStream(null);
        setIsCameraOpen(false);
    };

    // Capture photo
    const capturePhoto = () => {
        const video = videoRef.current;
        const canvas = canvasRef.current;

        if (video && canvas) {
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
            const ctx = canvas.getContext('2d');
            ctx.drawImage(video, 0, 0);

            canvas.toBlob((blob) => {
                const file = new File([blob], 'camera-capture.jpg', { type: 'image/jpeg' });
                setImageFile(file);

                const reader = new FileReader();
                reader.onloadend = () => {
                    setImagePreview(reader.result);
                };
                reader.readAsDataURL(file);

                closeCamera();
            }, 'image/jpeg', 0.9);
        }
    };

    // Start live monitoring
    const startLiveMonitoring = () => {
        setIsLiveMonitoring(true);
        setLiveResults(null);

        monitoringIntervalRef.current = setInterval(() => {
            analyzeCurrentFrame();
        }, 3000); // كل 3 ثواني
    };

    // Stop live monitoring
    const stopLiveMonitoring = () => {
        setIsLiveMonitoring(false);
        if (monitoringIntervalRef.current) {
            clearInterval(monitoringIntervalRef.current);
            monitoringIntervalRef.current = null;
        }
        setLiveResults(null);
    };

    // Analyze current frame
    const analyzeCurrentFrame = async () => {
        const video = videoRef.current;
        const canvas = canvasRef.current;

        if (!video || !canvas) return;

        try {
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
            const ctx = canvas.getContext('2d');
            ctx.drawImage(video, 0, 0);

            canvas.toBlob(async (blob) => {
                const file = new File([blob], 'live-frame.jpg', { type: 'image/jpeg' });

                try {
                    const response = await apiService.assessEmergency(
                        { patient_conscious: true },
                        file
                    );
                    setLiveResults(response.data);
                } catch (err) {
                    console.error('Live analysis error:', err);
                }
            }, 'image/jpeg', 0.7);
        } catch (err) {
            console.error('Frame capture error:', err);
        }
    };

    // Cleanup
    React.useEffect(() => {
        return () => {
            if (stream) {
                stream.getTracks().forEach(track => track.stop());
            }
            if (monitoringIntervalRef.current) {
                clearInterval(monitoringIntervalRef.current);
            }
        };
    }, [stream]);

    const handleImageSelect = (event) => {
        const file = event.target.files[0];
        if (file) {
            setImageFile(file);
            const reader = new FileReader();
            reader.onloadend = () => {
                setImagePreview(reader.result);
            };
            reader.readAsDataURL(file);
        }
    };

    const handleEmergencyAssess = async () => {
        setLoading(true);
        setError(null);
        setResult(null);

        // Simulate progress messages
        const progressMessages = [
            'جاري رفع الصورة...',
            'تحليل الصورة بواسطة الذكاء الاصطناعي...',
            'جمع البيانات الحيوية...',
            'حساب مستوى الخطورة...',
            'إنشاء التقرير...'
        ];

        let messageIndex = 0;
        const progressInterval = setInterval(() => {
            if (messageIndex < progressMessages.length) {
                setLoadingMessage(progressMessages[messageIndex]);
                messageIndex++;
            }
        }, 3000); // تغيير الرسالة كل 3 ثواني

        try {
            const response = await apiService.assessEmergency(
                { patient_conscious: true },
                imageFile
            );
            clearInterval(progressInterval);
            setResult(response.data);
        } catch (err) {
            clearInterval(progressInterval);
            console.error('Assessment error:', err);
            const errorMsg = err.response?.data?.detail ||
                err.message ||
                'حدث خطأ في التقييم. تأكد من اتصال الخادم.';
            setError(errorMsg);
        } finally {
            clearInterval(progressInterval);
            setLoading(false);
            setLoadingMessage('جاري التقييم...');
        }
    };


    const handleDownloadReport = async () => {
        if (!result) return;

        setDownloadLoading(true);
        setError(null);

        try {
            // Send both assessment and image path
            await apiService.downloadReport({
                assessment: result.assessment,
                patient_image_path: result.patient_image_path
            });
            // Success - file will download automatically
        } catch (err) {
            console.error('Download error:', err);
            const errorMsg = err.response?.data?.detail ||
                err.message ||
                'حدث خطأ في تنزيل التقرير. تأكد من اتصال الخادم.';
            setError(errorMsg);
        } finally {
            setDownloadLoading(false);
        }
    };

    const getSeverityColor = (level) => {
        const colors = {
            critical: '#d32f2f',
            severe: '#f57c00',
            moderate: '#fbc02d',
            mild: '#689f38',
            minimal: '#388e3c'
        };
        return colors[level] || '#757575';
    };

    return (
        <Container maxWidth="md" sx={{ py: 4 }}>
            <style>
                {`
                    @keyframes pulse {
                        0%, 100% { opacity: 1; transform: scale(1); }
                        50% { opacity: 0.7; transform: scale(1.1); }
                    }
                `}
            </style>

            <Box textAlign="center" mb={4}>
                <EmergencyIcon sx={{ fontSize: 60, color: '#f44336', mb: 2 }} />
                <Typography variant="h3" fontWeight="bold" gutterBottom>
                    نظام إنقاذ الحياة
                </Typography>
                <Typography variant="body1" color="text.secondary">
                    {isLiveMonitoring ? '🎥 المراقبة المباشرة نشطة' : 'تقييم فوري للحالات الطارئة'}
                </Typography>
            </Box>

            {/* Camera/Image Section */}
            <Paper sx={{ p: 3, mb: 3 }}>
                <Typography variant="h6" gutterBottom>
                    📸 تصوير الإصابة
                </Typography>

                {!isCameraOpen && !imagePreview && (
                    <Box display="flex" flexDirection="column" gap={2}>
                        <Button
                            variant="contained"
                            startIcon={<VideoIcon />}
                            onClick={() => {
                                openCamera();
                                setTimeout(() => startLiveMonitoring(), 500);
                            }}
                            fullWidth
                            sx={{ bgcolor: '#f44336', py: 1.5 }}
                        >
                            🎥 بدء المراقبة والتحليل المباشر
                        </Button>

                        <Box display="flex" gap={2}>
                            <Button
                                variant="contained"
                                startIcon={<CameraIcon />}
                                onClick={openCamera}
                                fullWidth
                                sx={{ bgcolor: '#2196F3' }}
                            >
                                التقط صورة
                            </Button>

                            <input
                                accept="image/*"
                                style={{ display: 'none' }}
                                id="image-upload"
                                type="file"
                                onChange={handleImageSelect}
                            />
                            <label htmlFor="image-upload" style={{ width: '100%' }}>
                                <Button
                                    variant="outlined"
                                    component="span"
                                    startIcon={<CameraIcon />}
                                    fullWidth
                                >
                                    اختر صورة
                                </Button>
                            </label>
                        </Box>
                    </Box>
                )}

                {/* Live Camera Feed */}
                {isCameraOpen && (
                    <Box mt={2} position="relative">
                        <video
                            ref={videoRef}
                            autoPlay
                            playsInline
                            style={{
                                width: '100%',
                                maxHeight: '400px',
                                borderRadius: '8px',
                                backgroundColor: '#000'
                            }}
                        />

                        {/* Live indicator */}
                        {isLiveMonitoring && (
                            <Box
                                position="absolute"
                                top={12}
                                left={12}
                                bgcolor="rgba(244, 67, 54, 0.95)"
                                color="white"
                                px={2}
                                py={1}
                                borderRadius={2}
                                display="flex"
                                alignItems="center"
                                gap={1}
                            >
                                <Box
                                    width={12}
                                    height={12}
                                    borderRadius="50%"
                                    bgcolor="white"
                                    sx={{ animation: 'pulse 1.5s infinite' }}
                                />
                                <Typography variant="body2" fontWeight="bold">
                                    LIVE  • مباشر
                                </Typography>
                            </Box>
                        )}

                        {/* Live results overlay */}
                        {isLiveMonitoring && liveResults && (
                            <Box
                                position="absolute"
                                bottom={12}
                                left={12}
                                right={12}
                                bgcolor="rgba(0, 0, 0, 0.85)"
                                color="white"
                                p={2}
                                borderRadius={2}
                            >
                                <Typography variant="subtitle2" gutterBottom fontWeight="bold">
                                    📊 التحليل الفوري:
                                </Typography>
                                <Box display="flex" gap={1} flexWrap="wrap" mt={1}>
                                    <Chip
                                        label={`${liveResults.assessment?.severity?.severity_level || 'جاري...'}`}
                                        size="small"
                                        sx={{
                                            bgcolor: getSeverityColor(liveResults.assessment?.severity?.severity_level),
                                            color: 'white',
                                            fontWeight: 'bold'
                                        }}
                                    />
                                    <Chip
                                        label={`نقاط: ${liveResults.assessment?.severity?.total_score || 0}/10`}
                                        size="small"
                                        sx={{ bgcolor: '#fff', fontWeight: 'bold' }}
                                    />
                                    {liveResults.assessment?.injuries?.length > 0 && (
                                        <Chip
                                            label={`🩹 ${liveResults.assessment.injuries.length} إصابة`}
                                            size="small"
                                            color="warning"
                                        />
                                    )}
                                </Box>
                            </Box>
                        )}

                        <Box display="flex" gap={2} mt={2}>
                            {!isLiveMonitoring ? (
                                <>
                                    <Button
                                        variant="contained"
                                        onClick={startLiveMonitoring}
                                        startIcon={<VideoIcon />}
                                        fullWidth
                                        sx={{ bgcolor: '#f44336' }}
                                    >
                                        بدء المراقبة المباشرة
                                    </Button>
                                    <Button
                                        variant="contained"
                                        onClick={capturePhoto}
                                        startIcon={<CameraIcon />}
                                        fullWidth
                                        sx={{ bgcolor: '#4CAF50' }}
                                    >
                                        التقط صورة
                                    </Button>
                                </>
                            ) : (
                                <Button
                                    variant="contained"
                                    onClick={stopLiveMonitoring}
                                    fullWidth
                                    sx={{ bgcolor: '#f44336' }}
                                >
                                    ⏹️ إيقاف المراقبة
                                </Button>
                            )}
                            <Button
                                variant="outlined"
                                onClick={closeCamera}
                                color="error"
                                fullWidth
                            >
                                إغلاق
                            </Button>
                        </Box>
                    </Box>
                )}

                <canvas ref={canvasRef} style={{ display: 'none' }} />

                {/* Image Preview */}
                {imagePreview && (
                    <Box mt={2}>
                        <img
                            src={imagePreview}
                            alt="Preview"
                            style={{
                                width: '100%',
                                maxHeight: '400px',
                                borderRadius: '8px',
                                objectFit: 'contain'
                            }}
                        />
                        <Button
                            variant="outlined"
                            onClick={() => {
                                setImagePreview(null);
                                setImageFile(null);
                            }}
                            fullWidth
                            sx={{ mt: 2 }}
                        >
                            حذف الصورة
                        </Button>
                    </Box>
                )}
            </Paper>

            {/* Emergency Button */}
            {
                !isLiveMonitoring && (
                    <Button
                        variant="contained"
                        size="large"
                        fullWidth
                        startIcon={loading ? <CircularProgress size={24} color="inherit" /> : <SendIcon />}
                        onClick={handleEmergencyAssess}
                        disabled={loading}
                        sx={{
                            py: 2,
                            fontSize: '1.2rem',
                            bgcolor: '#f44336',
                            '&:hover': {
                                bgcolor: '#d32f2f'
                            }
                        }}
                    >
                        {loading ? loadingMessage : 'ابدأ التقييم الطارئ'}
                    </Button>
                )
            }

            {/* Error */}
            {
                error && (
                    <Alert severity="error" sx={{ mt: 3 }}>
                        {typeof error === 'string' ? error : JSON.stringify(error)}
                    </Alert>
                )
            }

            {/* Results */}
            {
                result && (
                    <Box mt={4}>
                        <Alert
                            severity={result.assessment.severity.requires_immediate_attention ? 'error' : 'info'}
                            sx={{ mb: 3 }}
                        >
                            <Typography variant="h6">
                                {result.assessment.severity.requires_immediate_attention
                                    ? '⚠️ حالة طارئة - اتصل بالإسعاف فوراً 997'
                                    : '✓ تم التقييم بنجاح'}
                            </Typography>
                        </Alert>

                        {/* Download PDF Button */}
                        <Button
                            variant="contained"
                            size="large"
                            fullWidth
                            onClick={handleDownloadReport}
                            disabled={downloadLoading}
                            startIcon={downloadLoading ? <CircularProgress size={20} color="inherit" /> : null}
                            sx={{
                                mb: 3,
                                py: 1.5,
                                bgcolor: '#4CAF50',
                                '&:hover': {
                                    bgcolor: '#45a049'
                                }
                            }}
                        >
                            {downloadLoading ? 'جاري إنشاء التقرير...' : '📥 تحميل التقرير الكامل (PDF)'}
                        </Button>

                        {/* Severity */}
                        <Paper sx={{ p: 3, mb: 3 }}>
                            <Typography variant="h6" gutterBottom>
                                مستوى الخطورة
                            </Typography>
                            <Box display="flex" alignItems="center" gap={2} mb={2}>
                                <Chip
                                    label={result.assessment.severity.severity_level.toUpperCase()}
                                    sx={{
                                        bgcolor: getSeverityColor(result.assessment.severity.severity_level),
                                        color: 'white',
                                        fontSize: '1.1rem',
                                        fontWeight: 'bold'
                                    }}
                                />
                                <Typography variant="h4" fontWeight="bold">
                                    {result.assessment.severity.total_score}/10
                                </Typography>
                            </Box>

                            {result.assessment.severity.critical_factors?.length > 0 && (
                                <Box mt={2}>
                                    <Typography variant="subtitle2" color="error" gutterBottom>
                                        عوامل حرجة:
                                    </Typography>
                                    {result.assessment.severity.critical_factors.map((factor, idx) => (
                                        <Alert key={idx} severity="warning" sx={{ mt: 1 }}>
                                            {factor}
                                        </Alert>
                                    ))}
                                </Box>
                            )}
                        </Paper>

                        {/* Vital Signs */}
                        <Paper sx={{ p: 3, mb: 3 }}>
                            <Typography variant="h6" gutterBottom>
                                العلامات الحيوية
                            </Typography>
                            <Grid container spacing={2}>
                                <Grid item xs={6} md={3}>
                                    <Card>
                                        <CardContent>
                                            <Typography variant="caption" color="text.secondary">
                                                معدل القلب
                                            </Typography>
                                            <Typography variant="h5" fontWeight="bold">
                                                {result.assessment.vital_signs.heart_rate || '--'}
                                            </Typography>
                                            <Typography variant="caption">bpm</Typography>
                                        </CardContent>
                                    </Card>
                                </Grid>
                                <Grid item xs={6} md={3}>
                                    <Card>
                                        <CardContent>
                                            <Typography variant="caption" color="text.secondary">
                                                الأكسجين
                                            </Typography>
                                            <Typography variant="h5" fontWeight="bold">
                                                {result.assessment.vital_signs.spo2 || '--'}
                                            </Typography>
                                            <Typography variant="caption">%</Typography>
                                        </CardContent>
                                    </Card>
                                </Grid>
                                <Grid item xs={6} md={3}>
                                    <Card>
                                        <CardContent>
                                            <Typography variant="caption" color="text.secondary">
                                                الحرارة
                                            </Typography>
                                            <Typography variant="h5" fontWeight="bold">
                                                {result.assessment.vital_signs.body_temperature || '--'}
                                            </Typography>
                                            <Typography variant="caption">°C</Typography>
                                        </CardContent>
                                    </Card>
                                </Grid>
                            </Grid>
                        </Paper>

                        {/* Text Summary */}
                        <Paper sx={{ p: 3, bgcolor: '#f5f5f5' }}>
                            <Typography variant="h6" gutterBottom>
                                ملخص التقرير
                            </Typography>
                            <pre style={{ whiteSpace: 'pre-wrap', fontFamily: 'Cairo, sans-serif' }}>
                                {result.text_summary}
                            </pre>
                        </Paper>
                    </Box>
                )
            }
        </Container >
    );
}

export default Emergency;
