-- ════════════════════════════════════════════════════════════════
-- WORDDEE.AI - Database Schema Initialization
-- ════════════════════════════════════════════════════════════════

CREATE TYPE difficulty_enum AS ENUM ('Beginner', 'Intermediate', 'Advanced');

-- Words Table
CREATE TABLE words (
    id SERIAL PRIMARY KEY,
    word VARCHAR(100) UNIQUE NOT NULL,
    definition TEXT NOT NULL,
    part_of_speech VARCHAR(50),
    pronunciation VARCHAR(100),
    difficulty_level difficulty_enum NOT NULL,
    image_url TEXT,
    example_sentence TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT word_lowercase CHECK (word = LOWER(word)),
    CONSTRAINT definition_length CHECK (LENGTH(definition) >= 10)
);

-- Practice Sessions Table
CREATE TABLE practice_sessions (
    id SERIAL PRIMARY KEY,
    word_id INTEGER NOT NULL REFERENCES words(id) ON DELETE CASCADE,
    user_sentence TEXT NOT NULL,
    score DECIMAL(3,1) CHECK (score BETWEEN 0 AND 10),
    cefr_level VARCHAR(10),
    feedback TEXT,
    corrected_sentence TEXT,
    session_duration_ms INTEGER,
    practiced_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT sentence_not_empty CHECK (LENGTH(TRIM(user_sentence)) > 0)
);

-- Indexes
CREATE INDEX idx_words_difficulty ON words(difficulty_level);
CREATE INDEX idx_sessions_word_id ON practice_sessions(word_id);
CREATE INDEX idx_sessions_practiced_at ON practice_sessions(practiced_at DESC);

-- Seed Data (10 Beginner words)
INSERT INTO words (word, definition, part_of_speech, pronunciation, difficulty_level, example_sentence) VALUES
('apple', 'A round fruit with red, green, or yellow skin', 'noun', '/ˈæp.əl/', 'Beginner', 'I eat an apple every morning.'),
('happy', 'Feeling pleasure or contentment', 'adjective', '/ˈhæp.i/', 'Beginner', 'She looks very happy today.'),
('run', 'Move quickly using legs', 'verb', '/rʌn/', 'Beginner', 'I run in the park every day.'),
('book', 'A written work', 'noun', '/bʊk/', 'Beginner', 'This is an interesting book.'),
('water', 'Clear liquid', 'noun', '/ˈwɔː.tər/', 'Beginner', 'Drink water daily.'),
('friend', 'Person you like', 'noun', '/frend/', 'Beginner', 'He is my best friend.'),
('eat', 'Consume food', 'verb', '/iːt/', 'Beginner', 'We eat dinner together.'),
('beautiful', 'Pleasing to senses', 'adjective', '/ˈbjuː.tɪ.fəl/', 'Beginner', 'Beautiful sunset.'),
('help', 'Make easier', 'verb', '/help/', 'Beginner', 'Can you help me?'),
('school', 'Place for education', 'noun', '/skuːl/', 'Beginner', 'Children go to school.');
