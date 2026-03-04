CREATE TABLE users (
    id UUID PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE quiz_submissions (
    id UUID PRIMARY KEY,
    student_id UUID NOT NULL,
    quiz_id TEXT NOT NULL,
    payload JSONB NOT NULL,
    submitted_at TIMESTAMP NOT NULL,
    INDEX_quiz_student_time BIGINT GENERATED ALWAYS AS (EXTRACT(EPOCH FROM submitted_at)) STORED
);

CREATE TABLE mastery_scores (
    id UUID PRIMARY KEY,
    student_id UUID NOT NULL,
    concept TEXT NOT NULL,
    score NUMERIC(4,3) NOT NULL,
    measured_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_mastery_student_concept_time ON mastery_scores(student_id, concept, measured_at DESC);

CREATE TABLE learning_paths (
    id UUID PRIMARY KEY,
    student_id UUID NOT NULL,
    path JSONB NOT NULL,
    generated_at TIMESTAMP DEFAULT NOW()
);
