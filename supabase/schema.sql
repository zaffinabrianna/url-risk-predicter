-- Table to store every analysis event
CREATE TABLE analysis_events (
    id SERIAL PRIMARY KEY,
    url TEXT NOT NULL,
    risk_score FLOAT,
    risk_level TEXT,
    risk_factors TEXT, 
    analyzed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table to store user feedback linked to an analysis event
CREATE TABLE feedback (
    id SERIAL PRIMARY KEY,
    analysis_event_id INTEGER REFERENCES analysis_events(id),
    user_vote TEXT NOT NULL, -- 'Malicious', 'Safe', 'Unsure'
    feedback TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);