// server/routes/auth.js
const express = require('express');
const passport = require('passport');
const jwt = require('jsonwebtoken');
const router = express.Router();

const bcrypt = require('bcrypt');
const User = require('../models/User'); // Adjust path if needed

// Generate JWT Token
const generateToken = (userId) => {
    return jwt.sign(
        { id: userId },
        process.env.JWT_SECRET,
        { expiresIn: '7d' }
    );
};

// @route   POST /api/auth/register
// @desc    Register new user with email/password
// @access  Public
router.post('/register', async (req, res) => {
    try {
        const { email, password, name } = req.body;

        // Check if user exists
        const existingUser = await User.findOne({ email });
        if (existingUser) {
            return res.status(400).json({ error: 'User already exists' });
        }

        // Hash password
        const hashedPassword = await bcrypt.hash(password, 10);

        // Create user
        const user = new User({
            email,
            password: hashedPassword,
            name,
            provider: 'local'
        });

        await user.save();

        // Generate token
        const token = generateToken(user._id);

        res.status(201).json({
            success: true,
            token,
            user: {
                id: user._id,
                email: user.email,
                name: user.name
            }
        });
    } catch (error) {
        console.error('Registration error:', error);
        res.status(500).json({ error: 'Registration failed' });
    }
});

// @route   POST /api/auth/login
// @desc    Login with email/password
// @access  Public
router.post('/login', async (req, res) => {
    try {
        const { email, password } = req.body;

        // Find user
        const user = await User.findOne({ email });
        if (!user) {
            return res.status(401).json({
                success: false,
                message: 'Invalid credentials'
            });
        }

        // Check if user has password (not OAuth-only user)
        if (!user.password) {
            return res.status(401).json({
                success: false,
                message: 'Please login with Google or Facebook'
            });
        }

        // Verify password
        const isMatch = await bcrypt.compare(password, user.password);
        if (!isMatch) {
            return res.status(401).json({
                success: false,
                message: 'Invalid credentials'
            });
        }

        // Generate token
        const token = generateToken(user._id);

        res.json({
            success: true,
            token,
            user: {
                id: user._id,
                email: user.email,
                name: user.name
            }
        });
    } catch (error) {
        console.error('Login error:', error);
        res.status(500).json({
            success: false,
            error: 'Login failed'
        });
    }
});

// @route   GET /api/auth/google
// @desc    Redirect to Google OAuth
// @access  Public
router.get('/google',
    passport.authenticate('google', { scope: ['profile', 'email'] })
);

// @route   GET /api/auth/google/callback
// @desc    Google OAuth callback
// @access  Public
router.get('/google/callback',
    passport.authenticate('google', {
        failureRedirect: `${process.env.CLIENT_URL}/login?error=google_auth_failed`,
        session: false
    }),
    (req, res) => {
        // Generate JWT
        const token = generateToken(req.user._id);

        // Set token in httpOnly cookie
        res.cookie('token', token, {
            httpOnly: true,
            secure: process.env.NODE_ENV === 'production',
            sameSite: 'lax',
            maxAge: 7 * 24 * 60 * 60 * 1000 // 7 days
        });

        // Redirect to frontend
        res.redirect(`${process.env.CLIENT_URL}/dashboard`);
    }
);

// @route   GET /api/auth/facebook
// @desc    Redirect to Facebook OAuth
// @access  Public
router.get('/facebook',
    passport.authenticate('facebook', { scope: ['email'] })
);

// @route   GET /api/auth/facebook/callback
// @desc    Facebook OAuth callback
// @access  Public
router.get('/facebook/callback',
    passport.authenticate('facebook', {
        failureRedirect: `${process.env.CLIENT_URL}/login?error=facebook_auth_failed`,
        session: false
    }),
    (req, res) => {
        const token = generateToken(req.user._id);

        res.cookie('token', token, {
            httpOnly: true,
            secure: process.env.NODE_ENV === 'production',
            sameSite: 'lax',
            maxAge: 7 * 24 * 60 * 60 * 1000
        });

        res.redirect(`${process.env.CLIENT_URL}/dashboard`);
    }
);

// @route   POST /api/auth/logout
// @desc    Logout user
// @access  Private
router.post('/logout', (req, res) => {
    res.clearCookie('token');
    req.logout((err) => {
        if (err) {
            return res.status(500).json({ error: 'Logout failed' });
        }
        res.json({ message: 'Logged out successfully' });
    });
});

// @route   GET /api/auth/status
// @desc    Check if user is authenticated
// @access  Public
router.get('/status', (req, res) => {
    const token = req.cookies.token;

    if (!token) {
        return res.json({ authenticated: false });
    }

    try {
        const decoded = jwt.verify(token, process.env.JWT_SECRET);
        res.json({ authenticated: true, userId: decoded.id });
    } catch (err) {
        res.json({ authenticated: false });
    }
});

module.exports = router;