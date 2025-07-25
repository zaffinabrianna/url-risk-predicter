-- Table to store every analysis event
CREATE TABLE analyses (
    id SERIAL PRIMARY KEY,
    url TEXT NOT NULL,
    risk_score FLOAT,
    risk_level TEXT,
    risk_factors TEXT, 
    analyzed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table to store user feedback
CREATE TABLE feedback (
    id SERIAL PRIMARY KEY,
    url TEXT NOT NULL,
    user_vote TEXT NOT NULL, -- 'Malicious', 'Safe', 'Unsure'
    feedback TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);