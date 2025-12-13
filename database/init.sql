CREATE TYPE difficulty_enum AS ENUM ('Beginner', 'Intermediate', 'Advanced');

CREATE TABLE words (
    id SERIAL PRIMARY KEY,
    word VARCHAR(100) UNIQUE NOT NULL,
    definition TEXT NOT NULL,
    difficulty_level difficulty_enum NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT word_lowercase CHECK (word = LOWER(word))
);


CREATE TABLE practice_sessions (
    id SERIAL PRIMARY KEY,
    word_id INTEGER NOT NULL REFERENCES words(id) ON DELETE CASCADE,
    user_sentence TEXT NOT NULL,
    score DECIMAL(3,1) CHECK (score BETWEEN 0 AND 10),
    cefr_level VARCHAR(10),
    feedback TEXT,
    corrected_sentence TEXT,
    practiced_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_words_difficulty ON words(difficulty_level);
CREATE INDEX idx_sessions_word_id ON practice_sessions(word_id);
CREATE INDEX idx_sessions_practiced_at ON practice_sessions(practiced_at DESC);




INSERT INTO words (word, definition, difficulty_level) VALUES

('apple', 'A round fruit with red, green, or yellow skin', 'Beginner'),
('library', 'A place where books are kept for reading', 'Beginner'),
('garden', 'A piece of ground for growing flowers, fruit, or vegetables', 'Beginner'),
('happy', 'Feeling or showing pleasure', 'Beginner'),
('book', 'A written work consisting of pages', 'Beginner'),
('water', 'A clear liquid without color or taste', 'Beginner'),
('friend', 'A person you know well and like', 'Beginner'),
('school', 'A place where children go to learn', 'Beginner'),
('cat', 'A small furry animal often kept as a pet', 'Beginner'),
('house', 'A building where people live', 'Beginner'),


('ambitious', 'Having a strong desire to succeed', 'Intermediate'),
('collaborate', 'To work together with others', 'Intermediate'),
('innovative', 'Featuring new methods; advanced and original', 'Intermediate'),
('efficient', 'Achieving maximum productivity with minimum effort', 'Intermediate'),
('analyze', 'Examine something in detail', 'Intermediate'),
('responsible', 'Having a duty to deal with something', 'Intermediate'),
('opportunity', 'A chance for advancement or progress', 'Intermediate'),
('communicate', 'Share or exchange information', 'Intermediate'),
('flexible', 'Able to change easily', 'Intermediate'),
('achieve', 'Successfully reach a desired goal', 'Intermediate'),
('significant', 'Important enough to have an effect', 'Intermediate'),
('maintain', 'Keep something in good condition', 'Intermediate'),

('perseverance', 'Continued effort despite difficulties', 'Advanced'),
('ubiquitous', 'Present, appearing, or found everywhere', 'Advanced'),
('meticulous', 'Showing great attention to detail', 'Advanced'),
('paradigm', 'A typical example or pattern of something', 'Advanced'),
('facilitate', 'Make an action or process easier', 'Advanced'),
('comprehensive', 'Complete and including everything necessary', 'Advanced'),
('mitigate', 'Make something less severe or serious', 'Advanced'),
('ephemeral', 'Lasting for a very short time', 'Advanced');