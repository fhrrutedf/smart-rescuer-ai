import React from 'react';
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import { CssBaseline, AppBar, Toolbar, Typography, Button, Box } from '@mui/material';
import { Home as HomeIcon, LocalHospital as EmergencyIcon, Videocam as LiveIcon, Chat as ChatIcon } from '@mui/icons-material';

import Home from './pages/Home';
import Emergency from './pages/Emergency';
import LiveStream from './pages/LiveStream';
import Chat from './pages/Chat';

const theme = createTheme({
    direction: 'rtl',
    palette: {
        primary: {
            main: '#2196F3',
        },
        secondary: {
            main: '#f44336',
        },
    },
    typography: {
        fontFamily: 'Cairo, Roboto, sans-serif',
    },
});

function App() {
    return (
        <ThemeProvider theme={theme}>
            <CssBaseline />
            <BrowserRouter>
                <AppBar position="static">
                    <Toolbar>
                        <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
                            المنقذ الذكي | Smart Rescuer
                        </Typography>
                        <Button color="inherit" component={Link} to="/" startIcon={<HomeIcon />}>
                            الرئيسية
                        </Button>
                        <Button color="inherit" component={Link} to="/emergency" startIcon={<EmergencyIcon />}>
                            طوارئ
                        </Button>
                        <Button
                            color="inherit"
                            component={Link}
                            to="/live"
                            startIcon={<LiveIcon />}
                            sx={{
                                bgcolor: 'rgba(255,255,255,0.1)',
                                '&:hover': { bgcolor: 'rgba(255,255,255,0.2)' }
                            }}
                        >
                            بث مباشر 🔴
                        </Button>
                        <Button
                            color="inherit"
                            component={Link}
                            to="/chat"
                            startIcon={<ChatIcon />}
                            sx={{
                                bgcolor: 'rgba(255,255,255,0.15)',
                                '&:hover': { bgcolor: 'rgba(255,255,255,0.25)' }
                            }}
                        >
                            الشات الطبي 💬
                        </Button>
                    </Toolbar>
                </AppBar>

                <Box sx={{ minHeight: 'calc(100vh - 64px)', bgcolor: '#fafafa' }}>
                    <Routes>
                        <Route path="/" element={<Home />} />
                        <Route path="/emergency" element={<Emergency />} />
                        <Route path="/live" element={<LiveStream />} />
                        <Route path="/chat" element={<Chat />} />
                    </Routes>
                </Box>
            </BrowserRouter>
        </ThemeProvider>
    );
}

export default App;
