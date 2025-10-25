const express = require('express');
const jwt = require('jsonwebtoken');
const cookieParser = require('cookie-parser');
const path = require('path');

const app = express();
const PORT = 20001;
const SECRET = 'your_secret_key_here';

app.use(express.urlencoded({ extended: true }));
app.use(express.json());
app.use(cookieParser());
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));
app.use(express.static('public'));

// Valid titans
const VALID_TITANS = [
    'Attack Titan',
    'Colossus Titan',
    'Armored Titan',
    'Female Titan',
    'Beast Titan',
    'Jaw Titan',
    'Cart Titan',
    'War Hammer Titan'
];

// Home page - Titan selection
app.get('/', (req, res) => {
    res.render('index', { titans: VALID_TITANS });
});

// Handle titan selection and set JWT
app.post('/select', (req, res) => {
    const { titan } = req.body;
    
    if (!VALID_TITANS.includes(titan)) {
        return res.status(400).send('Invalid titan selection');
    }

    // Create JWT token with titan selection
    const token = jwt.sign({ titan: titan }, SECRET, { algorithm: 'HS256' });
    
    res.cookie('titanToken', token, { httpOnly: true });
    res.redirect('/fight');
});

// Fight page - Handle both GET and POST for fighting
app.get('/fight', (req, res) => {
    const token = req.cookies.titanToken;
    
    if (!token) {
        return res.redirect('/');
    }

    renderFightPage(res, token, false);
});

// Handle fight button click
app.post('/fight', (req, res) => {
    const token = req.cookies.titanToken;
    
    if (!token) {
        return res.redirect('/');
    }

    renderFightPage(res, token, true);
});

// Function to render fight page with proper win/lose logic
function renderFightPage(res, token, isFightAction) {
    try {
        // Try to verify with secret first (HS256) - normal titans always lose
        const decoded = jwt.verify(token, SECRET);
        if (isFightAction) {
            res.render('fight', { 
                titan: decoded.titan,
                message: `Your ${decoded.titan} was defeated! 💔`,
                won: false
            });
        } else {
            res.render('fight', { 
                titan: decoded.titan,
                message: `Your ${decoded.titan} is ready for battle!`,
                won: false
            });
        }
    } catch (err) {
        // If HS256 verification fails, check for "none" algorithm
        try {
            const decoded = jwt.decode(token, { complete: true });
            
            if (decoded.header.alg === 'none') {
                // For "none" algorithm, we need to verify the signature is empty
                const parts = token.split('.');
                if (parts[2] === '' || parts[2] === 'undefined') {
                    const payload = JSON.parse(Buffer.from(parts[1], 'base64').toString());
                    
                    if (payload.titan === 'Founding Titan' && isFightAction) {
                        // Only Founding Titan wins when fighting
                        res.render('fight', { 
                            titan: payload.titan,
                            message: 'Victory! The Founding Titan dominates all! 🏆',
                            won: true,
                            flag: 'SC2{f0und1ng_t1t4n_c0ntr0ls_4ll}'
                        });
                    } else if (payload.titan === 'Founding Titan' && !isFightAction) {
                        // Founding Titan is ready to fight
                        res.render('fight', { 
                            titan: payload.titan,
                            message: 'The Founding Titan awakens! 👑',
                            won: false
                        });
                    } else if (isFightAction) {
                        // Any other titan with "none" algorithm loses when fighting
                        res.render('fight', { 
                            titan: payload.titan,
                            message: `Your ${payload.titan} was defeated! 💔`,
                            won: false
                        });
                    } else {
                        // Other titans are ready to fight
                        res.render('fight', { 
                            titan: payload.titan,
                            message: `Your ${payload.titan} is ready for battle!`,
                            won: false
                        });
                    }
                } else {
                    throw new Error('Invalid signature for none algorithm');
                }
            } else {
                throw new Error('Invalid algorithm');
            }
        } catch (decodeErr) {
            res.render('fight', { 
                titan: 'unknown',
                message: 'Invalid token!',
                won: false
            });
        }
    }
}

// API endpoint to check token (for debugging)
app.get('/debug', (req, res) => {
    const token = req.cookies.titanToken;
    if (token) {
        try {
            const decoded = jwt.decode(token, { complete: true });
            res.json(decoded);
        } catch (err) {
            res.json({ error: err.message });
        }
    } else {
        res.json({ error: 'No token found' });
    }
});

app.listen(PORT, '0.0.0.0', () => {
    console.log(`Server running on http://localhost:${PORT}`);

});
