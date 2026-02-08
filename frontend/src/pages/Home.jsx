import React, { useState, useEffect } from 'react';
import {
    Container,
    Box,
    Typography,
    Button,
    Card,
    CardContent,
    Grid,
    Alert,
    CircularProgress,
    Chip
} from '@mui/material';
import {
    LocalHospital as EmergencyIcon,
    Chat as ChatIcon,
    LocalHospital as HospitalIconMain,
    Sensors as SensorsIcon
} from '@mui/icons-material';
import { apiService } from '../services/api';

function Home() {
    const [systemStatus, setSystemStatus] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        loadSystemStatus();
    }, []);

    const loadSystemStatus = async () => {
        try {
            const response = await apiService.getStatus();
            setSystemStatus(response.data);
        } catch (error) {
            console.error('Failed to load system status:', error);
        } finally {
            setLoading(false);
        }
    };

    const features = [
        {
            id: 'emergency',
            title: 'نظام إنقاذ الحياة',
            subtitle: 'Life-Saving System',
            description: 'تقييم فوري للحالات الطارئة بضغطة زر واحدة',
            icon: <EmergencyIcon sx={{ fontSize: 60 }} />,
            color: '#ff4444',
            path: '/emergency'
        },
        {
            id: 'chatbot',
            title: 'الاستشارة الذكية',
            subtitle: 'Smart Consultation',
            description: 'روبوت دردشة طبي للحالات غير الطارئة',
            icon: <ChatIcon sx={{ fontSize: 60 }} />,
            color: '#4CAF50',
            path: '/chat'
        }
    ];

    if (loading) {
        return (
            <Box display="flex" justifyContent="center" alignItems="center" minHeight="100vh">
                <CircularProgress size={60} />
            </Box>
        );
    }

    return (
        <Container maxWidth="lg" sx={{ py: 4 }}>
            {/* Header */}
            <Box textAlign="center" mb={6}>
                <EmergencyIcon sx={{ fontSize: 80, color: '#2196F3', mb: 2 }} />
                <Typography variant="h2" component="h1" fontWeight="bold" gutterBottom>
                    المنقذ الذكي
                </Typography>
                <Typography variant="h4" color="text.secondary" gutterBottom>
                    Smart Rescuer
                </Typography>
                <Typography variant="body1" color="text.secondary" mt={2}>
                    نظام ذكي للاستجابة للطوارئ الطبية بدون إنترنت
                </Typography>
                <Typography variant="body2" color="text.secondary">
                    Offline AI-Powered Emergency Response System
                </Typography>
            </Box>

            {/* System Status */}
            {systemStatus && (
                <Alert
                    severity="info"
                    icon={<SensorsIcon />}
                    sx={{ mb: 4 }}
                >
                    <Box display="flex" alignItems="center" gap={2} flexWrap="wrap">
                        <Typography variant="body2">
                            حالة النظام:
                        </Typography>
                        {Object.entries(systemStatus.sensors).map(([key, sensor]) => (
                            <Chip
                                key={key}
                                label={`${key.toUpperCase()}: ${sensor.ready ? '✓' : '✗'}`}
                                color={sensor.ready ? 'success' : 'default'}
                                size="small"
                                variant={sensor.simulated ? 'outlined' : 'filled'}
                            />
                        ))}
                    </Box>
                </Alert>
            )}

            {/* Main Features */}
            <Grid container spacing={4}>
                {features.map((feature) => (
                    <Grid item xs={12} md={6} key={feature.id}>
                        <Card
                            sx={{
                                height: '100%',
                                transition: 'transform 0.2s, box-shadow 0.2s',
                                '&:hover': {
                                    transform: 'translateY(-8px)',
                                    boxShadow: 6
                                },
                                cursor: 'pointer',
                                borderTop: `4px solid ${feature.color}`
                            }}
                            onClick={() => window.location.href = feature.path}
                        >
                            <CardContent sx={{ textAlign: 'center', py: 4 }}>
                                <Box sx={{ color: feature.color, mb: 2 }}>
                                    {feature.icon}
                                </Box>
                                <Typography variant="h4" component="h2" gutterBottom fontWeight="bold">
                                    {feature.title}
                                </Typography>
                                <Typography variant="subtitle1" color="text.secondary" gutterBottom>
                                    {feature.subtitle}
                                </Typography>
                                <Typography variant="body1" color="text.secondary" mt={2}>
                                    {feature.description}
                                </Typography>
                                <Button
                                    variant="contained"
                                    size="large"
                                    sx={{
                                        mt: 3,
                                        bgcolor: feature.color,
                                        '&:hover': {
                                            bgcolor: feature.color,
                                            opacity: 0.9
                                        }
                                    }}
                                >
                                    ابدأ الآن
                                </Button>
                            </CardContent>
                        </Card>
                    </Grid>
                ))}
            </Grid>

            {/* Information Section */}
            <Box mt={6} p={3} bgcolor="background.paper" borderRadius={2}>
                <Typography variant="h5" gutterBottom fontWeight="bold">
                    📋 كيف يعمل المنقذ الذكي؟
                </Typography>
                <Grid container spacing={2} mt={1}>
                    <Grid item xs={12} md={4}>
                        <Typography variant="subtitle1" fontWeight="bold" color="primary">
                            🩺 قياس العلامات الحيوية
                        </Typography>
                        <Typography variant="body2" color="text.secondary">
                            ECG • SpO2 • معدل النبض • الحرارة
                        </Typography>
                    </Grid>
                    <Grid item xs={12} md={4}>
                        <Typography variant="subtitle1" fontWeight="bold" color="primary">
                            📸 كشف الإصابات
                        </Typography>
                        <Typography variant="body2" color="text.secondary">
                            الرؤية الحاسوبية لتحليل الإصابات الظاهرة
                        </Typography>
                    </Grid>
                    <Grid item xs={12} md={4}>
                        <Typography variant="subtitle1" fontWeight="bold" color="primary">
                            📍 تحديد الموقع
                        </Typography>
                        <Typography variant="body2" color="text.secondary">
                            GPS لإرسال الموقع الدقيق للطوارئ
                        </Typography>
                    </Grid>
                </Grid>
            </Box>

            {/* Footer */}
            <Box mt={4} textAlign="center">
                <Typography variant="caption" color="text.secondary">
                    مشروع تخرج - قسم الهندسة الطبية الحيوية
                </Typography>
            </Box>
        </Container>
    );
}

export default Home;
